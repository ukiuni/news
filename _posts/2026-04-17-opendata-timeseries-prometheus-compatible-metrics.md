---
layout: post
title: "OpenData Timeseries: Prometheus-compatible metrics on object storage - OpenData Timeseries：オブジェクトストレージ上のPrometheus互換タイムシリーズ"
date: 2026-04-17T01:29:01.051Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.opendata.dev/blog/introducing-timeseries"
source_title: "OpenData Timeseries: Prometheus-compatible metrics on object storage | OpenData"
source_id: 359924805
excerpt: "SlateDBでS3を唯一の永続層にし、Prometheus互換を低コストで実現する手法"
image: "https://www.opendata.dev/blog/introducing-timeseries/og.png"
---

# OpenData Timeseries: Prometheus-compatible metrics on object storage - OpenData Timeseries：オブジェクトストレージ上のPrometheus互換タイムシリーズ
魅力的なタイトル: オブジェクトストレージでPrometheusを劇的に安く・シンプルに運用する方法

## 要約
OpenData Timeseriesは、SlateDB（オブジェクトストアネイティブなLSMツリー）上に構築されたMITライセンスのPrometheus互換TSDBで、オブジェクトストレージを唯一の永続層にすることで運用コストと複雑さを大幅に削減します。

## この記事を読むべき理由
大規模な自前の監視基盤を運用している日本のチームにとって、マネージド観測サービスの高コストを避けつつPromQL/Grafana互換を維持できる現実的な選択肢が提示されているため。

## 詳細解説
- 背景：従来のPrometheus互換スタック（Cortex等）はシャーディングやレプリケーション、複数サービスの管理が必要で運用負荷とコストが高い。一方でWarpStreamやturbopufferが示したように、オブジェクトストアを唯一の永続層にする設計は運用簡素化とコスト低減に強く有利。  
- アーキテクチャ：OpenData Timeseriesは書き手（writer/indexer）と読み手（reader/querier）を分け、永続化はS3/GCS/Azure等のオブジェクトストレージに一任。ノードはステートレスに近く、追加・削除が容易で再レプリケーション作業が不要。OTLP、Prometheus remote_write、Prometheus scraping、PromQLをサポート。  
- SlateDBの役割：SlateDBはオブジェクトストレージ上で動くLSMツリー実装で、書き込みを大きな不変ファイル（SST風）にまとめてフラッシュ・コンパクションする設計。タイムシリーズのインデックス化とサンプル読み出しがLSMのput/get/scanに自然にマップするため相性が良い。  
- トレードオフ：オブジェクトストアはコールドリードで10–100msのラウンドトリップ遅延があるため、キャッシュ（SlateDBの4KBブロックキャッシュ＋ローカルNVMe）でホットデータを温める運用が重要。書き込みはバッチ化されるので新鮮データのクエリ可視化に数秒の遅延が生じるが、監視用途では許容範囲。  
- 実測値（著者ベンチマーク）：単一 m5.xlarge（4vCPU,16GB）でSlateDB+S3に対し約55k samples/sec（= 約4.7B samples/日）を維持。推定で writer＋2 reader ノード＋S3 の計算コストは約$560/月で、同等規模をマネージドサービスで運用すると数千〜数万ドル/月に相当する差が出ると示唆。

## 実践ポイント
- 検証開始：まず quickstart で試し、p8s-bench等で自分の負荷プロファイルを測る。  
- デプロイ方針：writer（インデクサ）とreader（クエリ）を分離し、ローカルNVMeを用意してSlateDBのブロックキャッシュを確保することで暖かいクエリ性能を確保。  
- リソース目安：数百万アクティブ系列を扱うなら数十GBの総メモリ＋数百GBのNVMeキャッシュを検討（ベンチは約3.3M系列で140GB NVMeを想定）。  
- 運用監視：キャッシュヒット率とコンパクション状況を監視して、コールドリード頻度を下げる。古いデータはコンパクションでバケットを統合してスキャン量を減らす設計を検討。  
- 適用先：クラウドコスト削減が重要なSaaS/スタートアップ、オンプレや規制対応でクラウド完全委託が難しい組織に特に有効。

興味があれば公式リポジトリと quickstart を試して、手持ちのPrometheus/OTelパイプラインと接続してみてください。
