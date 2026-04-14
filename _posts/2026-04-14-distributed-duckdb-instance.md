---
layout: post
title: "Distributed DuckDB Instance - 分散化された DuckDB インスタンス"
date: 2026-04-14T07:06:46.194Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/citguru/openduck"
source_title: "GitHub - CITGuru/openduck: Distributed DuckDB - dual execution and differential storage · GitHub"
source_id: 47761997
excerpt: "差分ストレージとハイブリッド実行で手元とクラウドを一体化するOpenDuck"
image: "https://opengraph.githubassets.com/6f7b81ed9c253afc6da589e827f286861cb2a083225b205ea55fbcbb1df19c07/CITGuru/openduck"
---

# Distributed DuckDB Instance - 分散化された DuckDB インスタンス
DuckDBをクラウド級に拡張するOpenDuck：差分ストレージとローカル×リモートのハイブリッド実行で「手元」と「クラウド」を自然に融合

## 要約
OpenDuckは、MotherDuckのアイデア（差分ストレージ、デュアル実行、ATTACHベースのUX）をオープン化したプロジェクトで、DuckDBに対して透明なリモート表・分散実行・スナップショット付きの差分ストレージを提供します。

## この記事を読むべき理由
日本の開発現場ではデータの国内配置、コスト最適化、ローカルでの軽快な分析体験が重要です。OpenDuckは「ローカル端末の軽さ」と「クラウドのスケール」を同時に活かせるため、オンプレ＋クラウド混在やデータ主権を気にするプロジェクトに有用です。

## 詳細解説
- 差分ストレージ  
  OpenDuckはデータを「追記のみの層（immutable layers）」としてオブジェクトストレージに保存し、Postgresのメタデータで管理します。DuckDBは通常のファイルとして扱い、スナップショットによる一貫読み取りを提供。書き込みはシリアライズ経路、読み取りは多数の並行リーダーを許容します。

- ハイブリッド（デュアル）実行  
  単一のSQLクエリをクライアント側とリモート側で分割して実行します。ゲートウェイがプランを分割し、各演算子に LOCAL/REMOTE を割当て、境界に橋渡し演算子（bridge）を挿入。ネットワーク越しに送るのは中間結果のみで、無駄な転送を抑えます。

- DuckDBネイティブ統合  
  OpenDuckの拡張はDuckDBのStorageExtensionとCatalogを実装し、リモート表がローカル表と同じように最適化やJOINに参加します。ユーザー体験はATTACHでリモートをローカルに「くっつける」感覚です。

- オープンプロトコル  
  実行プロトコルは非常に小さく、gRPCとArrow IPCで結果をやり取りする2つのRPCで構成。バックエンドは任意のgRPC＋Arrow対応サービスで置換可能なので、独自の実行エンジンやクラウドを組み合わせやすい設計です。

- アーキテクチャ（概略）  
  クライアント（DuckDB拡張） ←→ gRPC/Arrow ←→ Gateway（プラン分割・認証） ←→ Worker群（各Workerは埋め込みDuckDB）  
  メタはPostgres、データはオブジェクトストレージのシール済みレイヤーとして保持。

- 商用サービスとの違い  
  MotherDuckは管理型サービス、OpenDuckはセルフホスト向けのオープン実装。プロトコルが開放されているためロックインが小さい点が利点です。

## 実践ポイント
- すぐ試す（ローカルPoC）  
  - Pythonクライアントを使った簡易接続例：
  ```python
  import openduck
  con = openduck.connect("mydb")
  con.sql("SELECT 1 AS x").show()
  ```
  - Gateway/Workerはリポジトリ内のRust実装で起動可能（cargoベース）。拡張はDuckDB側にロードしてATTACHすればリモート表が使えます。

- 日本の導入での着目点  
  - データ主権：オブジェクトストレージとメタDBを国内環境に置けるため法規対応に有利。  
  - コスト：頻繁に叩く集計はローカルで、重い集計はクラウドWorkerへ、でネットワーク・コストの最適化が可能。  
  - 開発：プロトコルがシンプルなので、自社の実行エンジンや既存分析基盤との統合がしやすい。

- 採用前チェックリスト  
  - S3互換オブジェクトストレージとPostgresを用意する。  
  - セキュリティ（認証・TLS）とネットワーク帯域を評価する。  
  - ワークロード特性（ローカルで高速化できるか、リモート集約が効率的か）をベンチする。

ライセンスはMIT。興味があればリポジトリ（CITGuru/openduck）をクローンして、GatewayとWorkerを立てるところからPoCを始めるのがおすすめです。
