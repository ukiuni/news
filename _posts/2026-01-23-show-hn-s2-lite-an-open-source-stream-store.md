---
layout: post
title: "Show HN: S2-lite, an open source Stream Store - Show HN: S2-lite（オープンソースのストリームストア）"
date: 2026-01-23T13:48:48.935Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/s2-streamstore/s2"
source_title: "GitHub - s2-streamstore/s2: Durable Streams API"
source_id: 46708055
excerpt: "ローカルやCIでクラウド並の永続ストリームを手軽に構築できる自己ホスト型S3対応ストア"
image: "https://opengraph.githubassets.com/bdedae08e43c92f165adab516c605300ddf162eb014c60cf7bda1d2ba42fc1c8/s2-streamstore/s2"
---

# Show HN: S2-lite, an open source Stream Store - Show HN: S2-lite（オープンソースのストリームストア）
S3やローカルで「永続的なストリーム」を手軽に試せる—小規模運用・開発環境向けの軽量実装

## 要約
S2-liteはS2のAPI互換で自己ホスト可能な単一バイナリのストリームストア。SlateDBを使い、オブジェクトストレージ（例：S3/Tigris）上にデータを永続化することで、ACK前に確実に耐久化する設計を提供します。

## この記事を読むべき理由
オンプレやデータ国内保持、CIでの統合テスト、ローカル開発環境で“クラウド相当の永続ストリーム”を手軽に再現したい日本のエンジニア／スタートアップにとって実用度が高いからです。

## 詳細解説
- アーキテクチャ概要  
  - 単一ノードの自己完結バイナリ（外部依存なしでin-memoryモードも可能）。  
  - ストレージはSlateDB（オブジェクトストレージ前提）：書き込みはオブジェクトストレージに確実に置いてからACKするため耐久性が高い。  
  - HTTPはaxum、非同期実行はTokio。各ストリームは"streamer"タスクがテイル位置を保持して直列化したappendを管理し、フォロワーへ配信する。  
  - アペンドのパイプライン化で高遅延ストレージ向けの性能改善を図る（ただし安全化が要改善）。  
- 運用面・互換性  
  - CLI/TypeScript/Go等のSDKと互換（各SDKの対応バージョンに注意）。  
  - API定義はOpenAPI／Protobuf／S2S（ストリーミングセッション）。クラウド版と異なりHTTPリクエストで明示的にS2-Basinヘッダが必要。  
- 注意点（Caveats）  
  - 削除機能は未完、パイプラインはデフォルト無効で安全化中。SDKやAPIバージョン差分に注意。

（実際の運用ではバケット設定・認証やメトリクス監視、パイプラインの有効化可否の確認が必要）

## 実践ポイント
- ローカルでまずはin-memoryで試す（Docker一発）:
```bash
# in-memory 起動（外部依存なし）
docker run -p 8080:80 ghcr.io/s2-streamstore/s2-lite
```
- S3や互換オブジェクトストレージに接続する例:
```bash
# S3バケットを使う例（~/.awsをマウント）
docker run -p 8080:80 \
  -e AWS_PROFILE=${AWS_PROFILE} \
  -v ~/.aws:/root/.aws:ro \
  ghcr.io/s2-streamstore/s2-lite \
  --bucket ${S3_BUCKET} --path s2lite
```
- CLI/SDKから接続する環境変数例:
```bash
export S2_ACCOUNT_ENDPOINT="http://localhost:8080"
export S2_BASIN_ENDPOINT="http://localhost:8080"
export S2_ACCESS_TOKEN="redundant"
```
- 確認・検証コマンド例: /pingで準備確認、/metricsはPrometheus形式。ベンチやストリーム作成はCLIで可能（s2 create-basin / s2 bench）。  
- 推奨ユースケース: CIの統合テスト・ローカル開発環境・オンプレでの小〜中規模耐久ストリーム。運用投入前に削除/パイプラインの挙動、SDK互換性を確認すること。

短時間で「クラウド相当の永続ストリーム」をローカルや自社クラウドに持ち込みたい場合、S2-liteは試す価値があります。
