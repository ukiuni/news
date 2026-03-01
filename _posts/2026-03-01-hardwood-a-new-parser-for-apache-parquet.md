---
layout: post
title: "Hardwood: A New Parser for Apache Parquet - Hardwood: Apache Parquet向け新パーサー"
date: 2026-03-01T07:47:01.347Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.morling.dev/blog/hardwood-new-parser-for-apache-parquet/"
source_title: "Hardwood: A New Parser for Apache Parquet - Gunnar Morling"
source_id: 47167432
excerpt: "Java21対応の軽量マルチスレッドParquetパーサHardwoodで圧倒的高速解析を体験しよう"
---

# Hardwood: A New Parser for Apache Parquet - Hardwood: Apache Parquet向け新パーサー
Parquet解析が激速に—Java 21対応の軽量マルチスレッドパーサ「Hardwood」を今すぐ試すべき理由

## 要約
HardwoodはJava 21+で動くオープンソースのParquetパーサーで、依存を最小化しつつページ単位の並列処理や適応プリフェッチで高い解析性能を実現する。

## この記事を読むべき理由
Parquetはデータレイク／分析パイプラインの事実上の標準。既存のparquet-javaは依存が重く単一スレッド中心なので、軽量かつマルチコアを活かす代替ライブラリが欲しい日本のエンジニアやデータチームに直接関係する。

## 詳細解説
- 背景：Parquetは列指向で圧縮効率／分析性能が高く、IcebergやDelta Lake、Trino/DuckDBなどと相性が良い。  
- Hardwoodの設計：仕様とテストファイルに基づくゼロからの実装で、トランジティブな依存を避ける（圧縮用ライブラリは任意：snappy/zstd/lz4/brotli）。  
- API：  
  - RowReader：ネスト構造や可変長フィールドに便利で可読性重視。  
  - ColumnReader：プリミティブ配列（例 double[]）を返し、ループがJITで自動ベクタ化されやすく高スループットを達成。  
- 高速化手法：  
  - ページレベル並列化：個々のデータページを複数ワーカーでデコード。  
  - 適応的プリフェッチ：遅い列に多くリソースを割り当て、ボトルネックを平準化。  
  - クロスファイルプリフェッチ：複数ファイル処理時の切替遅延を低減。  
  - その他：メモリマップ、割当最小化、オートボクシング回避、JFRでの計測。  
- 実測例（作者環境：M3 Max 16コア）：
  - NYC taxi subset (~9.2GB, 650M行)：RowReaderで約2.7s、ColumnReaderで約1.2s（3列合算）。  
  - Overture Maps (~900MB, 9M行)：RowReader ~2.1s、ColumnReader ~1.3s。  
- 開発スタンス：AI（Claude）を開発補助に多用したが、生成コードは人が精査して最適化・保守している（「AI製だが人の手で完成」）。  
- 今後のロードマップ：predicate push-down（列統計／Bloom filter利用）やparquet-java互換レイヤ、ファイル書き込み・CLIの追加を予定。

## 実践ポイント
- まず試す（Maven例）：
```xml
<dependency>
  <groupId>dev.hardwood</groupId>
  <artifactId>hardwood-core</artifactId>
  <version>1.0.0.Alpha1</version>
</dependency>
```
- 圧縮が必要ならsnappy等を追加。  
- 高スループットを狙うならColumnReaderを優先（フラットスキーマで特に効果大）。  
- ネスト構造の扱いはRowReaderが簡単。  
- プロファイルにはJDK Flight Recorderを使い、プリフェッチやデコードのボトルネックを確認。  
- 注意点：現時点でpredicate push-downは未実装のため、選択的読み取りが必要なワークロードは今後のリリースを待つか工夫が必要。  
- 貢献・移行：parquet-java互換レイヤが進めば既存コードの移行コストが下がるので、実運用前に互換状況をチェック。

興味があれば公式リポジトリを試し、実データでRow/Column両方のAPIを比較してみてください。
