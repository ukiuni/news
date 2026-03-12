---
layout: post
title: "AWS in 2025: The Stuff You Think You Know That's Now Wrong - 2025年のAWS：もう通用しない“常識”たち"
date: 2026-03-12T18:55:09.020Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.lastweekinaws.com/blog/aws-in-2025-the-stuff-you-think-you-know-thats-now-wrong/"
source_title: "AWS in 2025: The Stuff You Think You Know That&#039;s Now Wrong - Last Week in AWS Blog"
source_id: 386237312
excerpt: "AWSの常識が激変：EC2/S3/Lambda運用とコスト最適化の最新実務チェック"
image: "https://www.lastweekinaws.com/wp-content/uploads/2025/08/pexels-davidmcelwee-14869523-scaled.jpg"
---

# AWS in 2025: The Stuff You Think You Know That's Now Wrong - 2025年のAWS：もう通用しない“常識”たち
魅力的なタイトル案：AWSの“古い常識”は捨てろ――2025年に知っておくべき実務アップデート

## 要約
AWSの主要サービスはここ数年で挙動やベストプラクティスが大きく変わり、過去の知識で設計・運用すると損をする。この記事は主要サービスごとの「今ではこうなっている」を簡潔に整理する。

## この記事を読むべき理由
日本企業もクラウド移行・コスト最適化・セキュリティ強化の局面にあり、古い情報に頼ると稼働や費用、コンプライアンスでミスを招く。短時間で現行の運用判断に活かせるポイントを押させます。

## 詳細解説
- EC2
  - セキュリティグループやIAMロールを停止せずに差し替え可能。EBSのリサイズ/アタッチ/デタッチも稼働中に可。
  - インスタンスの強制停止/終了やライブマイグレーション機能で、以前ほど突発的な入れ替わりは少ない。
  - スポットの変動は穏やかに。専用インスタンスはほとんど不要に。

- S3
  - 読み書きの整合性が改善され、書き込み直後の読み取りが期待通りに動く（read-after-write）。
  - バケットACLは非推奨で新規は無効、Block Public Accessやサーバーサイド暗号化がデフォルト化。
  - Glacier相当はS3ストレージクラス化され、復元コストや速度の不安は解消済み。

- ネットワーキング
  - EC2-Classicは過去の話。パブリックIPv4は有料（Elastic IP相当）。
  - VPCピアリング以外にTransit Gateway、VPC共有、Cloud WAN、VPC Latticeなど運用を楽にする選択肢が増加。
  - CloudFront更新は大幅に高速化。ALBはクロスAZの追加転送料が発生しない場合が多いが、NLBは依然課金あり。

- Lambda
  - タイムアウトは最大15分、コンテナイメージ対応、EFSマウント、最大10GBメモリ・/tmp 10GBなど実行環境が強化。
  - VPC内起動・コールドスタートの改善でサーバーレス採用の敷居が下がった。

- ストレージ（EFS/EBS）
  - EFSはIO性能と容量の調整が別軸に。EBSは新規ボリュームは即時フル性能、スナップショットからのボリュームは初回読み込みが遅い（プリフェッチ推奨）。

- データベース（DynamoDB）
  - 空フィールド許容など柔軟性向上。ホットキー対策や性能の安定化が進み、料金モデルは大抵On‑Demandが現実的。

- コスト／節約手段
  - Reserved Instancesは縮小傾向、Savings Plansが主流。秒課金の普及で短時間起動の運用が割安に。
  - Cost Anomaly Detectorは実用レベルで無料、Compute Optimizerの推奨は信頼できる。

- 認証・権限
  - 人はIAMユーザーでなくIAM Identity Center（旧AWS SSO）＋IAMロール中心が正解。ルートの多重MFA設定などセキュリティ改善も進む。

- その他
  - リージョン耐久性や運用成熟度が全体的に向上。CloudWatchのメトリクス整合性も改善され、グラフ落ちが即「障害」を示すケースが増えた。

## 実践ポイント
- 既存ドキュメントを見直し：EC2/Lambdaの運用手順や停止再起動要件を最新化する。
- S3バケット戦略：ACL廃止・デフォルト暗号化・Block Public Accessを前提に設計。
- EBSスナップショット運用：スナップショットから復元したボリュームは事前に読み出して性能を確保する。
- コスト最適化：短期負荷は秒課金を活かし、長期需要はSavings Plansを検討。Cost Anomaly DetectorとCompute Optimizerを有効化。
- 認証整備：IAM Identity Center導入とIAMロールへの移行を優先し、ルートやサービスアカウントのMFAを整備する。
- ネットワーク設計：Transit GatewayやVPC Latticeなど新しい選択肢を評価し、古いピアリング設計からの脱却を検討。

以上を踏まえ、古いブログやポリシーに頼らず、まず自分のアカウントで主要サービスの設定を点検することを推奨します。
