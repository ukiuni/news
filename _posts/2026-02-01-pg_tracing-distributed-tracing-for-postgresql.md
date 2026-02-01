---
layout: post
title: "pg_tracing: Distributed Tracing for PostgreSQL - pg_tracing：PostgreSQL向け分散トレース"
date: 2026-02-01T05:22:17.733Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/DataDog/pg_tracing"
source_title: "GitHub - DataDog/pg_tracing: Distributed Tracing for PostgreSQL"
source_id: 46804009
excerpt: "pg_tracingでクエリ計画や並列ワーカーまで追跡しPostgres内部を可視化できる。"
image: "https://opengraph.githubassets.com/4ee0f43f929208ff9469e76c267ca7f923a65013d7f3f7a237fbc8b7fc51d257/DataDog/pg_tracing"
---

# pg_tracing: Distributed Tracing for PostgreSQL - pg_tracing：PostgreSQL向け分散トレース
Postgres内部の処理まで追える「サーバーサイド」分散トレーシング拡張、pg_tracingを使いこなす

## 要約
pg_tracingはPostgreSQL拡張で、サーバー側でクエリごとのスパン（Planner/Executor/各実行ノードやトランザクションコミットなど）を生成し、OTLP経由でコレクタへ送信したり、DB内で消費可能な形で参照できます。現在はPostgres 14–16対応の実験的機能です。

## この記事を読むべき理由
DBボトルネックは多くのアプリ障害やSLA違反の根本原因です。アプリ側のトレースだけでなく、Postgresサーバー内部の実行計画ノードや並列ワーカーまで可視化できれば、パフォーマンス解析や障害原因追跡が格段に速くなります。日本のDB中心ワークロード（金融、EC、オンプレ環境）にも直結する知見です。

## 詳細解説
- 何をするか：サーバー側で「サンプリングされたクエリ」に対してスパンを生成。Planner、ExecutorRun/Finish、各実行プランノード（SeqScan/HashJoin等）、トリガー、並列ワーカー、TransactionCommit（fsync時間）まで追跡します。
- スパンの取得方法：
  - pg_tracing_consume_spans / pg_tracing_peek_spans ビュー（レコード群）
  - pg_tracing_json_spans 関数（OTLP互換JSON）
- トレース伝播：
  - SQLCommenterを使ったSQLコメント（traceparent）で親トレースを伝播可能
  - GUC変数 pg_tracing.trace_context をトランザクション内でSET LOCALして伝播
- サンプリング：
  - pg_tracing.sample_rate でランダムサンプリング（1.0で全トレース）
  - SQLCommenterのsampledフラグで強制サンプリングも可
- OTLP送信：
  - pg_tracing.otel_endpoint にOTLP HTTP/JSONエンドポイントを設定するとバックグラウンドで定期送信（pg_tracing.otel_naptime ミリ秒指定）
  - サーバ起動時に設定されていないと、後から非空に変更しても再起動が必要な場合あり
- インストールと設定要点：
  - PGXSでビルド（git clone → make install）
  - postgresql.conf に shared_preload_libraries = 'pg_tracing' を追加（サーバ再起動が必要）
  - pg_tracing.max_span に応じた追加共有メモリが必要（常時消費）
- 注意点：まだ初期段階で不安定な可能性あり。Postgres 14–16のみサポート（執筆時点）。

例：導入に必要な最小設定（postgresql.conf）
```bash
# postgresql.conf
shared_preload_libraries = 'pg_tracing'
compute_query_id = on
pg_tracing.max_span = 10000
pg_tracing.track = all
pg_tracing.otel_endpoint = http://127.0.0.1:4318/v1/traces
pg_tracing.otel_naptime = 2000
```

## 実践ポイント
- まずステージングで試す：sample_rate を低め（例 0.01）から始め、メモリ使用とパフォーマンス影響を観察する。
- アプリ側はSQLCommenterやOpenTelemetryライブラリでtraceparentを付与すると関連付けが容易に。
- OTLPエンドポイント（OpenTelemetry Collector / Jaeger / Datadog）へ送って既存の可観測性ダッシュボードで統合する。
- トラブルシュート時は pg_tracing_consume_spans で内部スパンを確認し、実行計画ノードごとの時間を追う。
- 本番導入前にshared_buffers等の共有メモリ設定を確認し、pg_tracing.max_span に合わせること。

この記事で触れた機能は、DBレイヤでの深い可視化を求める現場に即効性のある武器になります。興味があれば、まずローカルのPostgres 14/15/16で動かしてみてください。
