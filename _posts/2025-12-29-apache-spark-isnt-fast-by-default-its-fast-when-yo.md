---
layout: post
title: Apache Spark Isn’t “Fast” by Default; It’s Fast When You Use It Correctly - Apache Sparkはデフォルトで「速い」わけではない。正しく使えば速いのだ
date: 2025-12-29T20:31:47.026Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.netcomlearning.com/blog/apache-spark"
source_title: "What is Apache Spark?: Complete Guide for 2026"
source_id: 435149815
excerpt: "Sparkはデフォルトで遅く、パーティションやシリアライザ最適化で劇的に高速化できる方法を解説"
---

# Apache Spark Isn’t “Fast” by Default; It’s Fast When You Use It Correctly - Apache Sparkはデフォルトで「速い」わけではない。正しく使えば速いのだ

## 要約
Apache Sparkは高性能をうたうが、デフォルト設定では最適化されておらず、正しいデータ設計・チューニング・実行パターンを適用したときに初めて真価を発揮する。

## この記事を読むべき理由
日本の企業でもログ解析・ETL・機械学習などで扱うデータ量は急増中。Sparkをただ導入するだけではコストと遅延が増えるため、「どこをどう直せば速くなるか」を知ることが即戦力になる。

## 詳細解説
- 基本概念  
  - Sparkは遅延評価とDAG最適化(Catalyst)を行うが、最終的な実行効率はパーティション設計、シャッフル量、シリアライズ方式、GCやメモリ設定に左右される。  
  - DataFrame/Dataset APIは最適化恩恵が大きく、RDDより優先して使うべき（CatalystとTungstenによりネイティブ最適化が行われる）。

- よくあるボトルネック  
  - 過大/過小パーティション（タスク数不適切）→並列性やシャッフル効率の低下。  
  - 不要シャッフル（wide transformationsの多発）→ネットワークとディスクI/O増大。  
  - 遅いシリアライザ（Java序列化）や巨大なオブジェクト→メモリ圧迫とGC停滞。  
  - 小さすぎるファイル群（S3やHDFS）→リスト/オープンコストの肥大化。  
  - UDFの乱用→最適化の抜け地になり性能低下。

- 重要な技術ポイント  
  - shuffleパーティション数はデフォルト(spark.sql.shuffle.partitions=200)を業務負荷に合わせて調整。  
  - Kryoシリアライザでオブジェクト表現を軽量化。  
  - ブロードキャスト結合（小テーブルを broadcast()）で巨大シャッフルを回避。  
  - Parquet/ORCなど列指向フォーマット＋predicate pushdownでI/O を削減。  
  - キャッシュは必要箇所のみ（メモリを食うため無差別に cache() はNG）。  
  - Spark 3系のAdaptive Query Execution (AQE)で動的にパーティションや結合方式を最適化可能。  
  - Structured Streamingはマイクロバッチと状態管理を意識した設計が重要（状態スケーリングやcheckpoint）。

- 運用面の注意  
  - モニタリング（Spark UI、Ganglia、Prometheus等）でタスク/GC/ディスクスピルを監視。  
  - クラウド利用時はS3読み書きの整合性・リスト性能、コミット方式（ハッシュ化・パーティション別出力）を設計。  
  - 日本のオンプレ環境やプライベートクラウドではノードスペックとネットワークのバランスが重要。

## 実践ポイント
1. DataFrame APIを第一選択にし、UDFはPandas UDFやネイティブ関数に置き換える。  
2. Parquetで列指向保存、パーティション設計は読み取りパターンに合わせる（年月日でのクエリが多ければ日付でパーティション）。  
3. シャッフル数を実負荷で調整：小ジョブは少なく、大ジョブは多めに。キーはタスク当たりデータ量を数十〜数百MBにすること。  
4. Kryoを有効化し、必要ならカスタム登録でシリアライズを最適化。  
5. 小テーブルは明示的に broadcast(df) して broadcast join にする。  
6. キャッシュは実行計画を見て局所的に使う（hot pathのみ）。  
7. Spark 3.xならAQEとAdaptive Shuffleを有効にして効果を確認する。  
8. 常にSpark UIでShuffleRead/ShuffleWrite、DiskSpill、GCの割合を確認し、問題箇所を特定する。  
9. ファイルサイズはまとめて128MB〜1GB台を目安に（小ファイル対策）。  
10. 本番導入前に代表データでベンチを回し、設定差分をA/Bで評価する。

短い実例（Pythonでの典型設定）
```python
# python
spark.conf.set("spark.sql.shuffle.partitions", "400")
spark.conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
from pyspark.sql.functions import broadcast
joined = large_df.join(broadcast(small_df), "key")
```

まずは「計測→変更→再計測」のサイクルを回すこと。設定は現場のデータ特性によって変わるため、汎用チューニングよりも実測に基づく最適化が最短で効果を生む。
