---
layout: post
title: "The tricky parts of building a reliable job scheduler: leases, idempotency, and timezone-aware cron"
date: 2025-12-28T23:18:31.313Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/Spooled-Cloud/spooled-backend"
source_title: "The tricky parts of building a reliable job scheduler: leases, idempotency, and timezone-aware cron"
source_id: 437103901
excerpt: "リース・冪等性・タイムゾーンCronで分散ジョブの落とし穴と実装指針を具体解説"
---

# 分散ジョブを“確実に”回すための地雷回避ガイド — リース、冪等性、タイムゾーンCronを徹底解説

## 要約
Spooled の設計から、分散ジョブスケジューラで実運用するときに必ず直面する「リース（lease）」「冪等性（idempotency）」「タイムゾーン対応Cron」の課題と、その現実的な回避策を技術的に整理する。

## この記事を読むべき理由
分散システム運用ではジョブの重複実行・ロスト・時間ズレで障害になりやすい。日本市場でのサービス提供（JSTや業務時間の要件、多テナントSaaS）では特に重要となるため、実装パターンと運用上の落とし穴を知っておくと問題発生を未然に防げる。

## 詳細解説
- リース（Lease）パターン  
  - ワーカーはジョブを「取得（claim）」して一定期間のリースを持つ。リース期限内に処理結果を返すか、heartbeatで延長する。失敗やタイムアウト時はリース失効後に別ワーカーが再取得する。  
  - 実装上の注意：リース期間は明確なSLAに合わせる（短すぎると重複、長すぎると遅延復旧）。heartbeatの頻度は処理の長さとネットワーク変動を踏まえて設計する。Spooled は POST /api/v1/jobs/claim、/heartbeat、/complete を提供。  
  - DB側は FOR UPDATE SKIP LOCKED を使い、同時取得競合を効率的に回避する（Postgresでの一般的実装）。

- 冪等性（Idempotency）  
  - At-least-once 処理はリトライとリースで実現するが、「副作用（外部API呼び出し、課金、メール送信等）」を一意に管理するために idempotency key を使うと「正確に一度（exactly-once）」に近づけられる。  
  - 実装例：ジョブペイロードに idempotency_key を含め、処理側でそのキーの成功履歴をDBに保存して二重実行を検出する。外部呼び出しはトランザクション境界外なので、記録と確認の仕組みが必須。

- タイムゾーン対応Cron  
  - 単純なUTCスケジューラだと「現地の9時」に実行したい要件を満たせない。スケジュールに IANA タイムゾーン（例: Asia/Tokyo）を持たせ、cron評価はそのローカル時間で行う必要がある。  
  - 注意点：夏時間（DST）や歴史的なTZ変更がある地域では、同一カレンダー時刻が存在しない／重複することがあるため、ライブラリ選定とテストが重要。Spooled は timezone をスケジュールに持たせ、cron_expression と組合せてトリガーする設計を採用している。

- 運用周り（観測性・多テナント・耐障害）  
  - Prometheus/Grafana、OpenTelemetry でメトリクスとトレースを収集。DLQ（Dead Letter Queue）で繰り返し失敗するジョブを隔離し、手動リトライやアラートをルール化する。  
  - 多テナント対策には PostgreSQL の RLS（Row-Level Security）を使ったデータ分離が有効。Spooled は RLS を採用し、API層はステートレスで水平スケール可能な設計。

- パフォーマンス考慮点  
  - gRPC（HTTP/2）＋Protobuf、Redis キャッシュ、Rust＋Tokio による非同期実装で高スループットを確保。日本のクラウド環境でも同様の構成は低レイテンシで有効。

## 実践ポイント
- idempotency_key をジョブAPIの必須オプションにして外部副作用を保護する。  
- リース期間は平均処理時間の3倍程度を目安に設定し、heartbeat で延長可能にする。  
- DBロックは FOR UPDATE SKIP LOCKED を使い、ワーカーは短時間で再試行する設計にする。  
- Cronスケジュールは必ず IANA タイムゾーンを保存し、DST シナリオを含むテストを作る。  
- DLQ を必須機能として運用し、失敗原因の可視化・自動通知を整備する。  
- ローカル検証は Docker Compose で再現（Postgres + Redis）して、運用時のレイテンシやロック競合を負荷テストする。  
- 日本向け運用では JST や営業時間帯（09:00 JST 等）のトリガー要件を明示し、SLA とアラート閾値を合わせる。

短いcurl例（スケジュール作成）：

```bash
# bash
curl -X POST http://localhost:8080/api/v1/schedules \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"daily-sales-report",
    "cron_expression":"0 0 9 * * *",
    "timezone":"Asia/Tokyo",
    "queue_name":"reports",
    "payload_template":{"report_type":"daily_sales"}
  }'
```

## 引用元
- タイトル: The tricky parts of building a reliable job scheduler: leases, idempotency, and timezone-aware cron  
- URL: https://github.com/Spooled-Cloud/spooled-backend
