---
layout: post
title: "Index: a crucial data structure for search performance - インデックス：検索性能を左右する重要なデータ構造"
date: 2026-03-30T12:09:12.540Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://binaryigor.com/index-a-crucial-data-structure-for-search-performance.html"
source_title: "Index: a crucial data structure for search performance"
source_id: 410427560
excerpt: "B-tree/GIN/GIST/BRINなど使い分けで検索が劇的に高速化する方法を解説"
image: "https://binaryigor.com/assets/og-image.png"
---

# Index: a crucial data structure for search performance - インデックス：検索性能を左右する重要なデータ構造

遅い検索にサヨナラ！DBインデックスでクエリが劇的に速くなる仕組み

## 要約
インデックスは「検索を速くするための追加データ構造」で、用途に応じてB-tree、Hash、GIN、GIST、BRINなど複数の実装があり、適切に選べばクエリ性能を大幅に改善できる。

## この記事を読むべき理由
日本のサービスやログ集計、ECや業務系システムでもデータ量は増加中。インデックスを正しく理解すると検索応答・コスト・運用性すべてに直結するため、初級〜中級エンジニアは必読。

## 詳細解説
- B-tree  
  - 最も一般的。等価・範囲検索・ソートに強く、検索は $O(\log n)$。葉ノードが双方向リストでつながれており、行参照はRID（row id）で取得。大規模データでも深さが小さいため高速。
- Hash  
  - 等価検索専用。理論上は $O(1)$。Postgresでは用途が限定されるが、KV系（Redis等）では主要手法。
- GIN（Generalized Inverted Index）  
  - 逆インデックス。文書中の単語や配列／jsonbのキー＋値をインデックス化し、1行が複数のエントリを持つ。全文検索やjsonbフィルタに有効。  
  - 例:
    ```sql
    CREATE TABLE account (id UUID PRIMARY KEY, attributes JSONB);
    CREATE INDEX account_attributes ON account USING GIN (attributes);
    ```
- GIST（Generalized Search Tree）  
  - 多次元データ向けのテンプレート。R-tree（地理座標など）実装でPostGISと相性が良い。独自比較演算子を定義可能。
- BRIN（Block Range INdex）  
  - ディスク上のページ範囲をまとめて索引化。タイムスタンプなど挿入順がほぼ増加する列に強く、時系列／大規模ログに最適。ランダム挿入では効果が落ちる。
- クラスタ化（Clustered） vs ヒープ＋セカンダリ  
  - MySQL/InnoDBのように主キーでテーブル自体をソートするモデル（クラスタ化）は主キー検索が超高速だが、セカンダリ検索は主キー経由で二重参照が必要。Postgresはヒープ＋独立インデックスでバランス型。
- 複合・カバリング・Index-only scan・選択性  
  - 複合インデックスで複数列を同時にカバーでき、インデックスだけで答えが得られれば index-only scan が成立する（テーブルアクセス不要）。重要なのは選択性（絞り込みの効き）で、高選択性列を先頭に持つと有利。

## 実践ポイント
- クエリに合わせて種類を選ぶ：  
  - 範囲やソート → B-tree、json/配列/全文 → GIN、地理 → GIST、時系列の大量データ → BRIN。  
- 過剰インデックスは書き込みコストとディスク増を招く。使用頻度の低いクエリは慎重に。  
- EXPLAIN/EXPLAIN ANALYZEでプランを確認してから作成。index-only scanが使えているか要チェック。  
- 選択性が低い列（性別など）には索引効果が出にくい。部分インデックスや式インデックスを検討する。  
- 運用面：VACUUM/REINDEX/統計情報の更新は忘れずに。BRINはテーブルの挿入順が維持されていることが前提。  

短いまとめ：インデックスは「何を」「どのように検索したいか」を起点に選ぶと性能効果が最大化する。
