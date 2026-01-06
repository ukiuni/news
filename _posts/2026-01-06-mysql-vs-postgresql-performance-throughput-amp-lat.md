---
  layout: post
  title: "MySQL vs PostgreSQL Performance: throughput & latency, reads & writes - MySQL vs PostgreSQL 性能比較：スループットとレイテンシ（読み書き別）"
  date: 2026-01-06T11:24:28.469Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://binaryigor.com/mysql-vs-postgresql-performance.html"
  source_title: "MySQL vs PostgreSQL Performance: throughput & latency, reads & writes"
  source_id: 469768786
  excerpt: "実測でPostgresが書込で最大約4.9倍高速、MySQLとの設定差も解説"
  image: "https://binaryigor.com/assets/og-image.png"
---

# MySQL vs PostgreSQL Performance: throughput & latency, reads & writes - MySQL vs PostgreSQL 性能比較：スループットとレイテンシ（読み書き別）

魅力的なタイトル: 「Dolphin vs Elephant — 実測でわかった“本番で速い”データベースはどっちか？」

## 要約
大規模な実測ベンチマークでは、チューニングした環境下でPostgreSQLが多くの挿入・読み取りワークロードでMySQLを上回った。MySQLが勝るケースもあるが、総合的にはPostgresが低レイテンシ・高スループットを示す場面が多い。

## この記事を読むべき理由
クラウド移行や新規アプリ設計でDB選定に迷う日本のエンジニアにとって、実機（Docker上・同一ハードウェア）での詳細な比較は即戦力になる。単なる“どちらが速い”論ではなく、設定・ワークロード別の挙動と実務での示唆が得られる。

## 詳細解説
- テスト概要  
  - ソース記事はローカル環境（AMD Ryzen 7 PRO 7840U、32GB、NVMe）でMySQLとPostgresをDockerで起動し、17種類のテストケース（単一挿入・バッチ挿入・複合SELECT/JOIN・更新・削除など）を実行。テスト実行はJavaベースのテストランナーで行い、QPS目標を与えてスループットとレイテンシ（p50/p90/p99/p99.9）を収集している。  
  - DB設定（抜粋）: MySQL 9.5（innodb_buffer_pool_size=12G、innodb_redo_log_capacity=2G、transaction-isolation=READ-COMMITTED）、Postgres 18.1（shared_buffers=4GB、work_mem=64MB、effective_cache_size=12GB）。Dockerで各DBは16Gメモリ、8CPUに制限。接続プールは経験的に MySQL=128、Postgres=64。

- 主要結果のポイント（代表例）  
  - 単一行挿入（500k users）: MySQL 実効 ~4,383 qps, 平均 ~26.8 ms / Postgres 実効 ~9,663 qps, 平均 ~2.19 ms。Postgresをさらに高負荷で再実行すると ~21,338 qps を達成（MySQL比で約4.87x）。  
  - バッチ挿入（orders 100件/クエリ）: Postgres がスループット・レイテンシとも優位（例: Postgres 実効 ~2,959 qps vs MySQL ~1,883 qps）。  
  - 一部バッチ（order_item 1,000件/クエリ）では MySQL がスループットで勝るケースあり（MySQL ~543 qps vs Postgres ~389 qps）が、レイテンシはPostgresが良好で総合では互角に近い。  
  - 読み取り（SELECT by id / email）: Postgres が高QPSで低レイテンシを維持（例: SELECT by id 実効 Postgres ~44k–55k qps vs MySQL ~33k qps、p99 5ms 対 12ms 程度）。

- なぜ差が出たか（技術的要因）  
  - バッファ設計とOSキャッシュの使い方（InnoDB vs Postgresのページキャッシュ／shared_buffers）やトランザクション処理の内部実装差が効いている。  
  - 接続プールや同時接続数の扱いでMySQLは高接続数で有利になる場面があり、書き込み集中時の最適接続数はDBごとに異なる。  
  - redo/log系の設定（MySQLのredo log容量やPostgresのワークメモ等）によって書き込みバースト時のI/O特性が変わる。

- 注意点（実験の制約）  
  - 単一ホスト・Docker環境での評価。ネットワーク分散、レプリケーション、クラウド運用（マネージドDB）では振る舞いが変わる。  
  - 設定は「良い線を目指したチューニング」だが、ワークロードに応じた最適化はさらに可能。  
  - アプリのクエリパターンやインデックス設計次第で結果は大きく変わるため、自社負荷での検証が不可欠。

## 実践ポイント
- まず自分のワークロードでベンチを回す：公開されたテスト手順は再現可能。Dockerで環境を作り、実アプリのクエリで p50/p99 を測る。  
- 設定の優先調整候補：バッファ（innodb_buffer_pool_size / shared_buffers）、work_mem、effective_cache_size、redo/logサイズ、トランザクション分離レベル。  
- 接続プールはDBごとに最適値を探索する：MySQLは高接続数で恩恵を受けることがあるが、無制限は逆効果。  
- バッチやトランザクション化で書き込み効率を上げる：大量挿入はバッチ化・トランザクションでI/Oを削減。  
- 本番導入前に「p99」を重視して確認する：平均だけでなく極端遅延（p99, p99.9）がユーザ体験に直結する。  
- 選定は性能だけでなく運用性で判断：レプリケーション、障害復旧、クラウド／マネージドサービスの選択肢も考慮する。

元記事の詳細とスクリプトは記事のGitHubリポジトリに公開されているので、実環境で再現して比較することを推奨する。
