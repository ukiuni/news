---
layout: post
title: "Quack-Cluster: A Serverless Distributed SQL Query Engine with DuckDB and Ray - Quack-Cluster：DuckDB と Ray を使ったサーバーレス分散 SQL クエリエンジン"
date: 2026-01-30T16:21:09.799Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/kristianaryanto/Quack-Cluster"
source_title: "GitHub - kristianaryanto/Quack-Cluster"
source_id: 46773793
excerpt: "DuckDB×RayでS3/GCSのParquetをそのまま並列SQL処理、サーバーレスで高速集計"
image: "https://opengraph.githubassets.com/3cad2a42289bbe59425d821dcda892d87c7074bc544224b35daf68951f6b7592/kristianaryanto/Quack-Cluster"
---

# Quack-Cluster: A Serverless Distributed SQL Query Engine with DuckDB and Ray - Quack-Cluster：DuckDB と Ray を使ったサーバーレス分散 SQL クエリエンジン
魅せるタイトル：ファイル群がそのまま“分散データベース”に — 軽量で速いQuack-Cluster入門

## 要約
Quack-ClusterはDuckDBの高速分析とRayの分散実行を組み合わせ、S3やGCS上のParquet/CSVをそのまま並列SQL処理できるサーバーレスな分散クエリエンジンです。軽量でローカルからクラウドまで素早く試せます。

## この記事を読むべき理由
日本のデータエンジニア／分析者は、従来の大掛かりなビッグデータ基盤を導入せずに、既存のオブジェクトストレージ上のデータで高速集計や結合を試せる実運用的な代替を知るべきだからです。PoCや小〜中規模分析に最適です。

## 詳細解説
- アーキテクチャ概要  
  - クライアントがSQLをCoordinator（FastAPI + SQLGlot）へ送信。Coordinatorがファイルワイルドカード等から対象ファイルを特定し、分散実行プランを生成。  
  - Rayクラスタの複数Worker（Ray Actor）へタスクを割り振り、各Workerは埋め込みのDuckDBでデータ断片を処理。部分結果はApache Arrow形式で集約され返却される。  
- キー技術  
  - DuckDB：列指向・ベクトル化された高性能エンジンでローカル分析に強い。  
  - Ray：Pythonネイティブな分散タスク管理。スケールアウトとワーカー管理を担う。  
  - Arrow + Parquet：メモリ効率と高速なシリアライズでネットワーク越しの部分集約を低コスト化。  
- サポートSQL・機能例  
  - 基本句：SELECT / FROM / WHERE / GROUP BY / ORDER BY / LIMIT  
  - 集約: SUM, COUNT, AVG, MIN, MAX  
  - 分散JOIN（異なるファイル集合間）・ウィンドウ関数・CTE・サブクエリ・ファイルグロブ（s3://bucket/**/*.parquet）  
- デプロイと開発体験  
  - Docker + makeベースでローカル起動が簡単（ヘッド + Nワーカー）。FastAPIベースのHTTP APIでcurl/Postmanから利用可能。  
- 向き／向かない用途  
  - 向く：解析重視のバッチ/アドホック分析、データサイエンスの実験、ETL前の探索。  
  - 否：高頻度トランザクションやACID厳密保証が必要なOLTP用途。

## 実践ポイント
- ローカルで試す最短手順（リポジトリをクローン後）：  
```bash
git clone https://github.com/kristianaryanto/Quack-Cluster.git
cd Quack-Cluster
make data
make up scale=2
```
- APIでの簡単な集計例：  
```bash
curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d '{"sql":"SELECT product, SUM(sales) AS total_sales FROM \"data_part_*.parquet\" GROUP BY product"}'
```
- 日本導入での注意点：  
  - S3/GCSアクセスの認証設定（IAM／鍵管理）を整備すること。  
  - コスト：クラウドオブジェクトストレージの読み出しとワーカ数による費用を意識。  
  - データ分割（パーティショニング）を工夫すれば並列効率が向上。  
- 次の一歩：小さなデータセットでPoCを回し、クエリパターンとボトルネック（I/O/ネットワーク/CPU）を測定してから本番スケールを検討する。

この記事を読んでまずはローカルで起動し、手持ちのParquetファイルで簡単な集計を試してみてください。
