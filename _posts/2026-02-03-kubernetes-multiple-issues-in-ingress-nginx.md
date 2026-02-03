---
layout: post
title: "[kubernetes] Multiple issues in ingress-nginx - ingress-nginxに複数の脆弱性が公開されました"
date: 2026-02-03T11:58:23.073Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://seclists.org/oss-sec/2026/q1/140"
source_title: "oss-sec: [kubernetes] Multiple issues in ingress-nginx"
source_id: 412159331
excerpt: "ingress-nginxにCVSS8.8含む重大脆弱性、即v1.13.7/v1.14.3へ更新を"
image: "https://seclists.org/images/oss-sec-img.png"
---

# [kubernetes] Multiple issues in ingress-nginx - ingress-nginxに複数の脆弱性が公開されました
深刻度「高」：今すぐ確認・アップデートすべきingress-nginxの脆弱性まとめ

## 要約
ingress-nginxに複数の脆弱性が公開され、うちいくつかはCVSSスコア8.8（High）です。該当バージョン未満を使っているクラスタは速やかにv1.13.7またはv1.14.3以上へアップグレードしてください（CVE-2026-1580、CVE-2026-24512、CVE-2026-24513、CVE-2026-24514）。

## この記事を読むべき理由
ingress-nginxは多くのKubernetes環境で外部トラフィックを受ける入り口コンポーネントの代表です。脆弱性が悪用されるとサービス停止や情報漏洩に直結するため、日本のクラウド／オンプレ環境を運用するエンジニアは即確認が必要です。

## 詳細解説
- 公開されたCVE: CVE-2026-1580、CVE-2026-24512、CVE-2026-24513、CVE-2026-24514。最も深刻なものはCVSS 8.8（ネットワーク経由で低権限で影響、完全な機密性・完全性・可用性の喪失を招く可能性）。
- 影響範囲: ingress-nginxの古いリリース（v1.13.7未満、v1.14.3未満）が対象。該当しなければ影響なし。
- 検出方法: クラスタにingress-nginxがいるかをまず確認（下記コマンド）。各CVEの詳細な検出手順はGitHubの各Issueにまとめられています。
- 緩和と対処: 根本対処はIngress-nginxをv1.13.7またはv1.14.3以降にアップグレードすること。一部の脆弱性はパッチ適用前に限定的な緩和策が可能で、個別Issueを参照してください。もし実害（侵害痕跡）を見つけたら security@kubernetes.io に連絡することが推奨されています。

コード（インストール確認）:
```bash
# クラスタに ingress-nginx が存在するか確認
kubectl get pods --all-namespaces --selector app.kubernetes.io/name=ingress-nginx
```

アップグレード手順や公式ドキュメント:
- Upgrading Ingress-nginx: https://kubernetes.github.io/ingress-nginx/deploy/upgrade/
- 各CVEの詳細（検出・緩和情報）: GitHub Issue（CVEごとのリンクを参照）

## 実践ポイント
- まず上記kubectlコマンドで存在確認。見つかったらバージョンを確認して該当範囲か判断。
- 影響を受ける場合は「ステージングで動作確認→本番でロールアウト」の手順でv1.13.7またはv1.14.3へ早急に更新する。
- マネージドKubernetes（GKE/AKS/EKS）やクラウドロードバランサを使っている場合は、使っているコントローラがingress-nginxか管理サービスの独自実装かを確認する（プロバイダの案内に従う）。
- ログや異常なトラフィック、未認可の設定変更が無いか監査して、攻撃痕跡があれば速やかに対応・報告する。

元情報（参照元）: oss-sec告知および各GitHub Issue（上記CVEリンク）
