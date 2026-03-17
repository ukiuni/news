---
layout: post
title: "OTel-Native by Design - OTelネイティブ設計"
date: 2026-03-17T09:08:12.302Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://signoz.io/blog/otel-native-by-design/"
source_title: "OTel-Native by Design - Building Backends That Export to Any Observability Stack | SigNoz"
source_id: 381782954
excerpt: "OTelネイティブでOTLPプッシュを採用し、ベンダーロックインなしで観測データを即送信"
image: "https://signoz.io/img/blog/2026/03/otel-native-by-design.webp"
---

# OTel-Native by Design - OTelネイティブ設計
ユーザーに「どこへでも送れる」観測データを渡す——OTelネイティブで作る、ベンダーロックインゼロのバックエンド設計

## 要約
OTel（OpenTelemetry）でログ・トレース・メトリクスを標準化してOTLPでエクスポートできるように設計すると、ユーザーは任意の観測基盤へほぼリアルタイムにデータを送れる。プッシュ（OTLP）モデルが新設計のゴールドスタンダード。

## この記事を読むべき理由
SaaSやプラットフォームを作る日本の開発者は、顧客から「自社の観測基盤にデータを送れるようにしてほしい」と求められる場面が増えています。コンプライアンスやコスト管理、ツール選択の自由を提供するための実務的な設計指針が学べます。

## 詳細解説
- 三つの観測シグナル：ログ（イベント・アクセス等）、トレース（分散トレース）、メトリクス（カウンタ／ゲージ／ヒストグラム）。OTLPはこれらを同一プロトコルで扱う。  
- デプロイ形態の違い：
  - Self-hosted（ユーザーがプロセスを持つソフトウェア）→ アプリにOTel組み込み、起動設定でOTLPエンドポイントを受け取る。例：Keycloak、Kuma。
  - Platform（プロバイダがインフラを運用）→ プラットフォーム側で収集・転送する「Telemetry Drains / Observability Destinations」を用意。例：Heroku、Cloudflare。
- プッシュ vs プル：
  - プル（APIをポーリング）→ 実装負荷と遅延が大きく、特にトレース/メトリクスに不向き。レガシーAPI向けに限定的に採用。
  - プッシュ（OTLP）→ ベンダ中立、コンテキスト（traceID や属性）保持、ほぼリアルタイム。推奨。
- 実装パターン：
  - アプリにOTel SDKを埋め込むか、内部でCollectorを動かして再エクスポートするかを選択。  
  - エンドポイント・ヘッダ・プロトコル（gRPC/HTTP）・送信するシグナルの選択をユーザーが設定可能にする。  
  - ログ⇄トレースの関連付けや属性名のスキーマをドキュメント化しておくことが重要。

## 日本市場との関連性
- 金融や医療系顧客のデータ滞在先要件、SIerや大企業の既存監視基盤（オンプレ/クラウドのGrafana/Grafana Cloud、Splunkなど）への接続要求に強く刺さる。  
- クラウドネイティブ（Kubernetes）採用が進む日本の現場では、アプリ内OTelやCollector経由のエクスポートが運用負荷低減に寄与する。

## 実践ポイント
- ユーザーにOTLPエンドポイントと認証ヘッダを設定させるUI/CLIを用意する。  
- シグナルごとのON/OFF（例：traces, metrics, logs）をユーザーが選べるようにする（データ量とコスト制御のため）。  
- OTEL標準環境変数を使って設定を統一する（例：OTEL_EXPORTER_OTLP_ENDPOINT）。  

bash example:
```bash
# 簡易例：環境変数でOTLPエンドポイントを指定
export OTEL_EXPORTER_OTLP_ENDPOINT="https://my-otel-collector:4317"
export OTEL_EXPORTER_OTLP_PROTOCOL="grpc"
```

yaml example:
```yaml
# プラットフォーム向け：ユーザーが指定するシグナル切替の例
telemetry:
  otlp_endpoint: "https://collector.example:4317"
  signals: ["traces","logs"]  # metricsはオフにする例
  headers:
    Authorization: "Bearer <ingestion-key>"
```

短期実行：まずは「OTLPエンドポイント指定」「シグナル選択」「traceIDをログに含める」を実装し、次フェーズでCollector導入やサンプリング設定を追加するのが現実的です。
