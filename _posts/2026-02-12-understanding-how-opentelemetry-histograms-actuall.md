---
layout: post
title: "Understanding How OpenTelemetry Histograms (Actually) Work - OpenTelemetry ヒストグラムの正体を理解する"
date: 2026-02-12T18:37:17.005Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://signoz.io/blog/opentelemetry-histogram/"
source_title: "Understanding How OpenTelemetry Histograms (Actually) Work | SigNoz"
source_id: 444592351
excerpt: "OTelヒストグラムの動作原理とバケツ設計・属性爆発対策を実例で解説"
image: "https://signoz.io/img/blog/2026/01/opentelemetry-histogram.webp"
---

# Understanding How OpenTelemetry Histograms (Actually) Work - OpenTelemetry ヒストグラムの正体を理解する
p95の謎がスッキリ！OpenTelemetryヒストグラムを正しく使ってレイテンシの“形”を掴む

## 要約
OpenTelemetryのヒストグラムは値の分布を「バケツ（bucket）」で表現し、バックエンド側でパーセンタイル（例：$p_{95}$）などを算出するための基本データを出力します。実装には固定境界の「explicit」と、動的スケールの「exponential」の2種類があり、それぞれトレードオフがあります。

## この記事を読むべき理由
ヒストグラムはSLO監視やレイテンシ解析で不可欠ですが、バケツ設計や属性（label）によるカードinality爆発で誤った運用コストを招きがちです。日本のプロダクション運用でも実践できる設定・注意点が押さえられます。

## 詳細解説
- 基本概念  
  ヒストグラムは観測値をバケツに分類して分布を表現する。OTelでは各バケツは「上限を含み、下限を含まない」(例：境界 [0,5,10,...] なら 0<=x<=0 が最初、0<x<=5 が次) と扱われる。最終バケツはオーバーフロー用。

- SDKがエクスポートするデータ  
  - Count：観測件数  
  - Sum：観測値合計（例えば累積レイテンシ）  
  - Buckets：各境界ごとのカウント（+オーバーフローバケツ）  
  - （オプション）Min/Max  
  バックエンドはこれらからパーセンタイルを推定するため、バケツ解像度が精度に直結する。

- ヒストグラムの種類  
  1. Explicit bucket（固定境界）  
     - SDKやユーザが境界配列を指定。低レンジに高解像度を置くのが一般的。だが将来の分布変化に合わせて境界見直しが必要。  
  2. Exponential histogram（指数スケール）  
     - スケールパラメータで動的にバケツを生成し、長い裾（p99など）もコンパクトに表現可能。メモリ管理のためにSDK側でスケールをダウンすることがある。現時点でプラットフォーム依存の対応状況がある（SigNoz等で段階的対応）。

- 属性（labels）とメトリクスの分離  
  同じメトリクスでも属性の組合せごとに別ストリームを作るため、高カードinality属性（user_idなど）を付けるとバケツ数が爆発、アプリ側のメモリ・ネットワーク・バックエンドストレージを圧迫する。

- Temporal aggregation と一貫性  
  SDKは記録された観測を時間単位で集約してエクスポートする（DeltaやCumulativeの概念）。Exponentialを使う場合、Deltaを推奨するケースがある（バックエンド依存）。

- SigNozでの注意点（実例）  
  Exponentialヒストグラムを有効化するには自己ホスト版で設定をオンにし、エクスポート時のtemporalityをDeltaにする必要がある（プラットフォームごとに手順が異なるため公式ドキュメントを参照）。

- 実用的な理解例  
  100リクエストのうち90件が100ms以下、残りがスパイクを生む場合、$p_{95}$ や $p_{99}$ を見ることでSLO違反を検出できる。パーセンタイルの正確さはバケツ設計に依存する。

サンプル（Python）は最小構成のヒストグラム登録例：
```python
from opentelemetry.metrics import set_meter_provider, get_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader

reader = PeriodicExportingMetricReader(ConsoleMetricExporter(), export_interval_millis=1000)
meter_provider = MeterProvider(metric_readers=[reader])
set_meter_provider(meter_provider)
meter = get_meter_provider().get_meter("otel-histogram-demo", "0.1.0")

hist = meter.create_histogram("demo_latencies", unit="ms", description="demo HTTP latencies")
hist.record(99.9)
hist.record(50, attributes={"http.route":"/v1/users","http.method":"GET"})
```

## 実践ポイント
- まず目的を決める：SLOがあるなら対象パーセンタイル（例：$p_{95}$）に合わせて設計する。  
- 境界設計 or 指数ヒストグラムを選ぶ：分布が予測困難なら exponential を検討。  
- 属性は厳選する：高カードinalityは避け、必要なタグのみ付与する。  
- Viewsを活用してメトリクス変換やtemporality調整を行う。  
- アラートはパーセンタイルで設定し、問題発生時はトレース/ログと必ず紐付ける。  

短く言えば：ヒストグラムは「何が遅いか」ではなく「どのくらいの割合で遅いか」を示すツール。設計とラベリング次第で観測精度もコストも大きく変わるため、まずは小さく試して監視・アラート・相関（trace/log）を整備すること。
