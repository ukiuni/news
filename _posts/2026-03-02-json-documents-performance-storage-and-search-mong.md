---
layout: post
title: "JSON Documents Performance, Storage and Search: MongoDB vs PostgreSQL - JSONドキュメントの性能、保存、検索：MongoDB 対 PostgreSQL"
date: 2026-03-02T14:38:47.302Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://binaryigor.com/json-documents-mongodb-vs-postgresql.html"
source_title: "JSON Documents Performance, Storage and Search: MongoDB vs PostgreSQL"
source_id: 930171334
excerpt: "実機ベンチで比較、バルク書込はMongoが優位、トランザクションはPostgresが安心"
image: "https://binaryigor.com/assets/og-image.png"
---

# JSON Documents Performance, Storage and Search: MongoDB vs PostgreSQL - JSONドキュメントの性能、保存、検索：MongoDB 対 PostgreSQL
ドキュメントDBの王者はどっち？実測で分かった「JSON格納」「検索」「大量投入」の現実

## 要約
MongoDB（ドキュメントDB）とPostgreSQL（JSONB対応リレーショナルDB）を同一ハードでベンチし、保存効率・検索・書き込み（単体・バッチ）で実測比較。多くのケースで性能差は小さいが、ワークロード次第で有利不利が分かれる。

## この記事を読むべき理由
日本の開発現場では「既存のSQL資産を活かすか」「柔軟なスキーマで開発速度を取るか」の判断を迫られます。本記事は生データと設定（Docker上・実機スペック・チューニング）に基づく実測結果を要点だけ分かりやすく示し、選定の判断材料を短時間で得られます。

## 詳細解説
- アプローチの違い
  - SQL（テーブル＋厳格スキーマ）：型・制約・参照整合性が強み。Postgresは後からJSON/JSONBを追加。
  - ドキュメント（コレクション＋柔軟スキーマ）：MongoDBは最初からドキュメント指向。配列やネストを自然に扱う。

- ストレージとインデックス
  - Postgres：JSONB（バイナリ形式）、8KBページ、B-treeでテキスト抽出（data->>'id'）、配列等はGINインデックスを使用。
  - MongoDB：フィールド単位の通常インデックス（B-tree相当）。大きいドキュメントは複数ページに渡ると読み書きコストが増える点は類似。

- テストセットとワークロード
  - テスト対象スキーマ：accounts（軽量）、products（数KBの複雑ドキュメント）。
  - 環境：Docker上でMongoDB 7とPostgres 18を同一マシン（16GB制限・8CPU割当）で実行。Postgresは shared_buffers/work_mem/effective_cache_size を増強、Mongoは wiredTigerCacheSizeGB を増強。
  - コネクションプール：Mongoは多め（実験では256）、Postgresは控えめ（64）。Mongoは大量接続で書き込み性能が伸びる傾向。

- 主要な結果（抜粋）
  - 単体INSERT（小ドキュメント）：両者はかなり近い。中央値はPostgresが速い場面あり。だが99/99.9パーセンタイルで遅延スパイクが発生。
  - 単体INSERT（大ドキュメント）：性能差は小さくPostgresがやや有利なケースも。
  - バッチINSERT（大量バルク、バッチ1000）：MongoDBが明確に有利（平均・99パーセンタイルとも優位）。Postgresはバッチ負荷で遅延が増大する傾向。
  - 全体の傾向：ドキュメントサイズが大きくなると両DBとも性能低下。99パーセンタイルの挙動を必ず確認する必要あり。

## 日本市場との関連
- 既存のオンプレ・クラウド（RDS/Aurora/Cloud SQL、MongoDB Atlas）運用を考える日本企業では、Postgresを選ぶとSQLエコシステムや成熟した運用ツールを活かせる。一方、ログ収集・ETLやスキーマ頻繁変更のサービスではMongoの投入スループットが魅力。
- 規制やデータ整合性（金融・官公庁系）が重視される業務では、参照整合性や強い型を持つPostgresが安全側。

## 実践ポイント
- ワークロードで選ぶ：大量バッチ書き込みが主ならMongoを検討。トランザクション性や複雑なSQLが必要ならPostgres。
- インデックス設計：
  - Postgres：JSONBの頻出キーは (data->>'key') に対してB-tree、配列はGINを使う。
  - Mongo：配列やネストフィールドに対するインデックスを適切に作る。
- ドキュメントサイズを抑える：ページ分割はI/O増→2KB〜程度を目安に設計を検討。
- 運用チューニング：DBのメモリパラメータ（wiredTigerCacheSizeGB / shared_buffers / effective_cache_size / work_mem）と接続プールサイズをワークロードに合わせる。
- SLOを見る：平均だけでなく99パーセンタイルを必ず計測し、負荷状況でのスパイクを評価する。
- 最終判断は自前ベンチを：可能なら実データ・実設定でDocker上に再現ベンチを回し、数値で決める。

元記事は実測とテストスクリプトを公開しており、同環境で自分のデータを試すことが推奨されます。
