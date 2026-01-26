---
layout: post
title: "Kubernetes Remote Code Execution Via Nodes/Proxy GET Permission - nodes/proxy GET による Kubernetes リモートコード実行"
date: 2026-01-26T21:33:34.447Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://grahamhelton.com/blog/nodes-proxy-rce"
source_title: "Kubernetes Remote Code Execution Via Nodes/Proxy GET Permission"
source_id: 416804820
excerpt: "nodes/proxyGET権限でKubelet経由、任意Podでのコマンド実行が可能に"
image: "https://grahamhelton.com/assets/images/og-nodes-proxy-rce.png"
---

# Kubernetes Remote Code Execution Via Nodes/Proxy GET Permission - nodes/proxy GET による Kubernetes リモートコード実行
nodes/proxy GET 権限で「読み取り」つもりがクラスタ内のあらゆる Pod にコマンド実行できる可能性――Kubernetes の認可の盲点をわかりやすく解説

## 要約
Kubernetes の RBAC で nodes/proxy の GET 権限を持つサービスアカウントが、Kubelet の直接接続（例：WebSocket ハンドシェイク経由）を通じて本来は CREATE で保護される /exec や /run を実行できるケースが報告されました。該当バージョンとして v1.34 / v1.35 が検証されています（公開は Won't fix / 意図的挙動）。

## この記事を読むべき理由
多くの監視・ログ収集ツール（Prometheus/Grafana/Datadog/Cilium などの Helm チャート）で nodes/proxy GET を要求する例があり、日本でも広く利用されているため、意図せず「読み取り権限」が持つリスクに晒されている可能性があります。管理者は早急に影響範囲と対策を確認すべきです。

## 詳細解説
- RBAC と nodes/proxy の位置づけ：通常、pod のコマンド実行は pods/exec に対して CREATE 権限が必要。nodes/proxy は API Server 経由のプロキシや Kubelet 直接 API へのアクセスを許す特殊なリソースで、メトリクスやコンテナログ取得に多用される。
- 問題の本質：Kubelet の /exec や /run といった実行系エンドポイントは、本来 POST→CREATE に対応すべき操作だが、WebSocket の初期ハンドシェイクは HTTP GET を使うため、Kubelet が「最初の HTTP メソッド（GET）」に基づいて認可判断をする実装だと、nodes/proxy GET が実行を通してしまう場合がある。
- 影響：ノードの Kubelet（通常 10250）に到達可能な service account が nodes/proxy GET を持つと、任意の Pod（特権 Pod 含む）でコマンドが実行でき、最悪クラスタ全体の侵害につながる。直接 Kubelet に接続すると API Server を経由しないため、AuditPolicy によるコマンドの完全な記録が残らない点も問題を悪化させる。
- 検証環境／範囲：公開記事では v1.34 / v1.35 で確認、69 の Helm チャートで nodes/proxy が言及されていると報告。

## 実践ポイント
- まず検出：nodes/proxy GET を許可する ClusterRole と、それをバインドしている ServiceAccount を列挙する。
```bash
# bash
kubectl get clusterrole -o json | jq -r '.items[] | select(.rules[]? | .resources[]? == "nodes/proxy" and (.verbs[]?=="get")) | .metadata.name'
kubectl get rolebinding,clusterrolebinding --all-namespaces -o yaml | grep -B2 -n "nodes/proxy"
```
- ネットワーク制御：Kubelet（10250）への直接アクセスをクラスタ内外から制限する。管理プレーン以外からノードに到達できないようファイアウォール／セグメンテーションを設定する。
- 最小権限化：監視ツールには可能な限り限定的な権限を与える。ベンダーへ代替手段（API Server 経由の安全なアクセスなど）の確認を依頼する。
- Audit と検出：API Server 経由のプロキシアクセスはログに残るが、Kubelet 直接接続は実行コマンドが残らない点を踏まえ、ノードレベルのネットワーク／プロセス監視や異常な subjectaccessreview の増加検知を導入する。
- Helm とサードパーティ点検：自社で使う Helm チャートやサードパーティのデフォルト RBAC を確認し、nodes/proxy GET を要求しているかどうかを洗い出す。
- ベンダー連携：該当権限が必要というツールは多く存在するため、ベンダーと連携してセキュアな設定や代替案を検討する。

以上を踏まえ、まずはクラスタ内の nodes/proxy GET を持つエントリを特定し、ネットワーク制御と最小権限ポリシーを優先して適用してください。
