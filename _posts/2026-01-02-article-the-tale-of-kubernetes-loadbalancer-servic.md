---
  layout: post
  title: "Article: The Tale of Kubernetes Loadbalancer \"Service\" In The Agnostic World of Clouds - クラウド非依存の世界におけるKubernetes LoadBalancer「Service」の物語"
  date: 2026-01-02T11:10:02.667Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://hamzabouissi.github.io/posts/cloud_agnostic_lb_for_kubernetes/"
  source_title: "The Tale of Kubernetes Loadbalancer \"Service\" In The Agnostic World of Clouds | chown u+r mind"
  source_id: 472993502
  excerpt: "クラウド混在環境でLoadBalancerをメタコントローラ＋Webhookで自動化する手法"
  image: "https://hamzabouissi.github.io/%3Clink%20or%20path%20of%20image%20for%20opengraph,%20twitter-cards%3E"
---

# Article: The Tale of Kubernetes Loadbalancer "Service" In The Agnostic World of Clouds - クラウド非依存の世界におけるKubernetes LoadBalancer「Service」の物語
「どのクラウドでも使えるLoadBalancerを作る：CCM／外部IPハックから自作Cloud Controller Managerへ」

## 要約
KubernetesのService type=LoadBalancerはクラウド依存で動作がバラつくため、MetalLBや外部LB、externalIPsといった回避策を経て、最終的にメタコントローラ＋専用Cloud Controller Manager（CCM）で各クラウド・オンプレに横断的に対応する手法に落ち着いた話。

## この記事を読むべき理由
クラウド混在（multi-cloud）や「どのノードにsshできればクラスタ化」するようなプロビジョニングを考える日本のSRE/プラットフォームエンジニアにとって、LoadBalancer問題は必須の設計要素。既存のMetalLBやNodePort運用で陥りやすい落とし穴と、実運用で使える実践解（metacontroller＋WebhookによるCCM）を理解できる。

## 詳細解説
- 問題点の本質  
  KubernetesのLoadBalancer型Serviceは通常Cloud Controller Manager（CCM）経由でクラウドのLBを作る。だがCCMがない環境（多数のプロバイダやオンプレ混在）ではServiceがpendingのままになり、外部IP割当が自動化されない。

- 従来の回避策と欠点  
  LoxiLB/HAProxyのような外部LBやNodePort＋外部DNSは、LBノードがKubernetesのライフサイクル外に置かれるためセルフヒーリングやGitOps的な差分解消が難しい。MetalLBはL2/L3の制御を前提とするため、AWS/GCP/Azureのようなプロバイダや任意ノードには適用できないケースがある。

- externalIPsトリック  
  ノードのパブリックIPをService.spec.externalIPsに渡すとpendingが消えIngressにIPが付くケースがある（nginx-ingressでは有効）が、TraefikのようにService.status.loadBalancer.ingressを参照するコントローラは動かない。またArgoCDなどのヘルスチェックがexternalIPsを「健康」と見なさない問題がある。

- 自作の解：メタコントローラ＋Webhookで疑似CCMを実装  
  メタコントローラ（metacontroller）でServiceを監視し、Webhook（FastAPI等）に状態を送り、Webhook側で条件に合うノードの公開IP一覧を算出してService.status.loadBalancer.ingressに書き戻す。これによりKubernetesが期待する形でLoadBalancer情報を持てるため、Traefikなどのコントローラとも互換性が出る。reconcile周期は30秒程度で可。

- 1:1 NAT（クラウド差分）の罠と対策  
  AWSのようにPublic IPがNATされて内部ではPrivate IPしか見えない環境では、kube-proxyのiptablesルールが期待通り動かない。解決策はWebhook側で、public IPだけでなくprivate IPを使った内部向けClusterIP/Serviceを別途作成し、外部→NAT→内部IPのフローに合わせてルールを生成すること。

- 実装の肝（抜粋）  
  - Nodeにラベル（use-as-loadbalancer=platform/public）を付与して候補ノードを決める  
  - Readyかつラベル一致のノードから node-public-ip と node-private-ip を集める  
  - public_ips を service.status.loadBalancer.ingress にセットする  
  - AWS等では同仕様で内部向け ClusterIP 相当のServiceを作り private IP を externalIPs に入れて補正する

以下はWebhookの同期処理の簡略例（要点のみ）。

```python
# python
from fastapi import FastAPI
from kubernetes import client, config

app = FastAPI()

@app.post("/sync")
def sync(request: dict):
    svc = request['object']
    label = svc['metadata']['labels'].get('use-as-loadbalancer')
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    nodes = v1.list_node().items

    public_ips = []
    private_ips = []
    for n in nodes:
        labels = n.metadata.labels or {}
        if labels.get('use-as-loadbalancer') != label:
            continue
        ready = any(c.type == 'Ready' and c.status == 'True' for c in n.status.conditions)
        if not ready:
            continue
        pub = labels.get('node-public-ip')
        priv = labels.get('node-private-ip') or next((a.address for a in n.status.addresses if a.type=='InternalIP'), None)
        if pub:
            public_ips.append(pub)
        if priv:
            private_ips.append(priv)

    return {
        "status": {
            "loadBalancer": {
                "ingress": [{"ip": ip} for ip in public_ips]
            }
        }
    }
```

メタコントローラの定義例（要点）:

```yaml
# yaml
apiVersion: metacontroller.k8s.io/v1alpha1
kind: DecoratorController
metadata:
  name: lb-service-decorator
spec:
  resources:
    - apiVersion: v1
      resource: services
  labelSelector:
    matchExpressions:
      - { key: "use-as-loadbalancer", operator: In, values: ["platform","public"] }
  resyncPeriodSeconds: 30
  hooks:
    sync:
      webhook:
        url: http://webhook-controller.default.svc.cluster.local/sync
    finalize:
      webhook:
        url: http://webhook-controller.default.svc.cluster.local/finalize
```

## 実践ポイント
- まずは要件を整理：オンプレ混在・多数プロバイダ・Traefik/Ingressの差分を洗い出す。MetalLBは万能ではない。  
- Nodeに公開/内部IPをラベルで管理しておく（node-public-ip / node-private-ip）。自動化パイプラインで登録を忘れない。  
- ArgoCDなどのヘルスチェック対策を用意（externalIPs ≠ LoadBalancerの挙動差に注意）。  
- 小規模ならexternalIPsトリックは早く済むが、Traefik互換性や可観測性が必要なら専用CCM（metacontroller＋Webhook）の導入を検討する。  
- AWSの1:1 NAT問題は見落としがち：publicのみを投げる設計は内部ルーティングで機能しないため、内部向けServiceの自動生成が必須。

## 引用元
- タイトル: Article: The Tale of Kubernetes Loadbalancer "Service" In The Agnostic World of Clouds  
- URL: https://hamzabouissi.github.io/posts/cloud_agnostic_lb_for_kubernetes/
