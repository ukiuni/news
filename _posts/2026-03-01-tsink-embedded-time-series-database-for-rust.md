---
layout: post
title: "tsink - Embedded Time-Series Database for Rust - Rust向け組み込み時系列DB「tsink」"
date: 2026-03-01T21:18:07.760Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://saturnine.cc/tsink"
source_title: "tsink - Embedded Time-Series Database for Rust"
source_id: 689216921
excerpt: "Rust製組み込み時系列DB tsink：23x圧縮でPromQL互換、アプリ内で高速観測を実現"
---

# tsink - Embedded Time-Series Database for Rust - Rust向け組み込み時系列DB「tsink」
組み込みで使える超高速・超圧縮の時系列DBをアプリにそのまま埋め込む――PromQL互換で監視データも扱える「tsink」の魅力

## 要約
tsinkはRust製の組み込み時系列データベースで、LSM-tree＋Gorilla系圧縮で高いスループットと低いストレージ容量を両立。PromQL互換エンジンとPrometheus互換のHTTPサーバを備え、外部サーバなしでアプリ内に時系列エンジンを置けます。

## この記事を読むべき理由
- オペレーションを減らして観測やメトリクス収集をアプリに内蔵したい（IoT、エッジ、サイドカー）。
- Prometheus互換＋PromQLで既存の監視ワークフローと連携できる。
- 高スループット・低容量（例：23x圧縮、0.68 bytes/point）でコストとパフォーマンスを両立できる可能性がある。

## 詳細解説
- アーキテクチャ：LSM-treeベースのストレージ（L0→L1→L2）を採用し、バックグラウンドでコンパクションを行うことで書き込み性能を維持しつつ読み取り増幅を低減。データは時間パーティションとチャンクに分けられます。
- 圧縮アルゴリズム：数値はGorilla XORやdelta-of-deltaビットパッキング、zigzag、定数RLEなどを自動選択。報告されている典型値は約0.68 byte/point（元16 byte→23x圧縮相当）。
- 型システム：f64、i64、u64、bool、bytes、stringの6型をサポート。型ごとに最適なコーデックが適用されます。
- 可用性・耐久性：分割WAL（CRC32チェック）＋fsyncオプションでクラッシュ後の再生が保証。WAL同期モード（PerAppend/Periodic）で耐久性とスループットを調整可能。
- 同時実行とスケーリング：内部で64シャードに分割して書き込み競合を避け、ロックフリー読み取りを実現。非同期ストレージはランタイム非依存（tokio/async-std等で動作）。
- PromQL対応：独自実装のレキサー／パーサー／評価器を持ち、rate/irate/avg_over_timeなど主要関数と集約をサポート。HTTP APIはPrometheusのquery/query_rangeやremote_read/writeを含み、TLSやベアラートークンも利用可能。
- リソース制御：メモリ予算、シリーズカーディナリティ制限、WALサイズ制限といった保護機構でOOMや無限増大を防止。コンテナ環境向けにcgroup検出でスレッドプール最適化。

主な実測指標（ベンチマーク）：単一挿入レイテンシ ~1.7 μs、バッチ挿入(1K)で6.4M pts/s、読み取りピークで数千万pts/sクラス。

## 実践ポイント
- まずはCargoに追加（PromQLやasyncが必要ならfeatureを指定）:
```rust
[dependencies]
tsink = { version = "0.8.0", features = ["promql", "async-storage"] }
```
- 組み込みかサーバモードかを選ぶ：ライブラリとして埋め込むなら StorageBuilder / AsyncStorageBuilder、単独運用するなら tsink-server（Prometheus互換HTTP）を起動。
- 運用設定のチェック項目：retention（保持期間）、memory_limit（メモリ予算）、cardinality_limit（シリーズ上限）、wal_sync_mode（耐久性 vs スループット）。
- カーディナリティに注意：高ラベル多様性はメモリとWALを圧迫するため、ラベル戦略を設計すること。
- コンテナ運用：cgroup自動検出で最適化されるが、メモリ制限とスレッド数は明示設定しておくと安定する。
- 試験運用：まず開発環境で実データを使ったベンチを実行し、圧縮率・レイテンシ・スループットを確認。Prometheus remote_write/readで既存ツールとの相互運用性を検証する。

以上を踏まえ、アプリに直接組み込みたい観測系やエッジでの時系列保存・クエリを検討している日本の開発チームには、tsinkは運用コスト削減と高性能化の良い選択肢になります。
