---
layout: post
title: "Airbnb discloses a billion-series Prometheus metrics pipeline - OpenTelemetry と vmagent で作る大規模メトリクスパイプライン"
date: 2026-04-16T06:21:04.356Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://medium.com/airbnb-engineering/building-a-high-volume-metrics-pipeline-with-opentelemetry-and-vmagent-c714d6910b45"
source_title: "Airbnb discloses a billion-series Prometheus metrics pipeline"
source_id: 47788818
excerpt: "Airbnbが公開、vmagentで10億系列級を低コスト処理するPrometheusメトリクス設計"
---

# Airbnb discloses a billion-series Prometheus metrics pipeline - OpenTelemetry と vmagent で作る大規模メトリクスパイプライン
Airbnbの事例に学ぶ：10K/s級の高カードinalityメトリクスを安定してPrometheus系に移行した設計と実運用の知見

## 要約
AirbnbはStatsDベースのレガシーパイプラインをOTLP（OpenTelemetry）＋otel-collector＋Prometheus系ストレージ（Grafana Mimir）に移行し、vmagentでのストリーム集約とシャーディングを組み合わせて、10億系列級（100M/s以上）の取り込みを低コストで実現した。

## この記事を読むべき理由
日本の大規模サービス運用でも「メトリクスが増えてコスト爆発」「Prometheusに移行したら数値が合わない」といった課題が現実的に発生します。本記事は移行パターン、性能トレードオフ、実装手法（delta/累積、vmagent、ゼロ注入）まで実務で効いた解決策を短く示します。

## 詳細解説
- 背景：元々はStatsD（DogStatsD）＋Veneurで集めていたが、将来性と互換性からOTLP（OpenTelemetry Protocol）を推奨。Prometheus系ストレージをバックエンドに選定。
- マイグレーション戦略（Dual-write）：共通ライブラリを改修してStatsDとOTLPを同時に吐く「デュアルライト」方式で段階移行。利用者のダッシュボードやアラート検証に実データを先に流せる点が利点。
- OTLPの利点：UDPベースのStatsDより信頼性が高く、JVMプロファイルでメトリクス処理のCPUを10%→<1%に削減。Prometheusネイティブ（例：指数ヒストグラム）をフル活用できる。
- スケール課題とdelta選択：高スループット（10K+ samples/sec/インスタンス）サービスではOTLPでメモリ・GC圧が悪化。選択的にAggregationTemporalitySelector.deltaPreferred()（delta temporality）を使い、プロセス内状態を減らして安定化。ただしdeltaは障害時に欠損が出るトレードオフ。
- 集約の必要性と選定：コスト抑制のためインスタンスラベル等を集約する必要があるが、VeneurはPrometheusモデル対応が重く、OTel Collectorは集約未成熟。結果、VictoriaMetricsのvmagentを採用。
  - アーキテクチャ：router（ステートレス、ハッシュでシャード振り）＋aggregator（Stateful、集約・保持）でスケール。routerはaggregation対象外ラベルを除いてハッシュすることで一貫したシャーディングを実現。
  - カスタム点：ネイティブヒストグラム対応やMimir互換のマルチテナンシーなどを内部で追加し、一部をOSSに寄与。
  - 成果：数百台のaggregatorで単クラスター100M/s超を処理、コストを桁単位で削減。
- PromQLの落とし穴（Sparse counters）：Prometheusの累積カウンタ＋rate()の性質上、低頻度でラベル組合せが現れるカウンタの“増分”がリセットで失われるケースが頻発。Airbnbは集約層で「ゼロ注入（初回フラッシュで0を吐く）」を行い、系列を暗黙的に初期化してrate()の欠落を防いだ。副作用は最初の点がゼロになる点だが、ダッシュボード/アラートの正当性が保てる。

## 実践ポイント
- 移行はデュアルライトで始め、ユーザー用ダッシュボードとアラートを実データで検証すること。
- 高ボリュームサービスはOTLPでもdelta temporalityを検討：メモリ削減と可観測性のギャップを理解した上で適用する。
- 大量の系列を安価に集約するにはvmagentのrouter→aggregatorパターンが有効。ラベル除外の一貫したハッシュでシャーディングを安定させる。
- Prometheusで「少ししか増えない高次元カウンタ」がある場合、集約層でゼロ注入する仕組みを導入してrate()/increase()の undercount を回避する。
- 本番スケールでの検証を早期に行い、GC／メモリ／PromQL結果の差分を丹念に比較すること。

（短く言えば）OTLPへ移行して得られる信頼性と機能性を活かしつつ、vmagentによる中央集約＋ゼロ注入といった実務的な工夫で「コストを抑えつつ正しいメトリクス」を維持できる、というケーススタディです。
