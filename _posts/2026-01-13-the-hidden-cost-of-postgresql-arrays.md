---
layout: post
title: "The hidden cost of PostgreSQL arrays - PostgreSQL配列の隠れたコスト"
date: 2026-01-13T13:12:14.344Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://boringsql.com/posts/good-bad-arrays/"
source_title: "The hidden cost of PostgreSQL arrays | boringSQL"
source_id: 699761893
excerpt: "PostgreSQL配列の便利さが、本番での性能低下や更新コスト増を招く理由を解説"
image: "https://boringsql.com/og-images/good-bad-arrays-og.jpg"
---

# The hidden cost of PostgreSQL arrays - PostgreSQL配列の隠れたコスト
PostgreSQL配列で“ラク”をすると、気づかないうちに性能や保守性の踏み穴にはまる。

## 要約
PostgreSQLの配列型は手軽だが、設計・更新・インデックス・ストレージ面で意外なトレードオフがあり、本番でパフォーマンス問題やデータ不整合を招くことがある。

## この記事を読むべき理由
日本のプロダクトでも「タグやIDのリストをそのまま列に入れる」設計はよく見られます。短期的な開発効率を優先すると、運用中に大規模リライトや検索遅延、整合性問題で手戻りが発生します。本稿は初心者にも分かるように、避けるべき落とし穴と実務で使える回避策を示します。

## 詳細解説
- 配列はドキュメント型の誘惑  
  配列(integer[] / jsonbなど)は「行に関連データを埋め込む」設計で、ローカリティ（同一行にまとめる）を優先するため結合が不要になる利点がある。一方、参照整合性（外部キーやON DELETEの保証）は配列内要素には効かない。タグIDや参照する別テーブルのIDを配列で持つと、関連テーブル削除で配列内に孤立IDが残る。参照整合性が必要ならリンクテーブル（中間テーブル）を選ぶべき。

- 型と次元の「見かけ」  
  宣言が integer[][] のようでも、PostgreSQLはスキーマで次元数を厳密に保証しない。多次元の均一性（各ネストが同じ長さ）だけは保証されるが、正確な次元制約が必要なら CHECK で array_ndims()/array_length() を使う必要がある。

  例（次元チェックの簡易例）:
  ```sql
  -- SQL
  CREATE TABLE strict_matrix (
    board integer[] CHECK (array_ndims(board) = 2 AND array_length(board, 1) = 3)
  );
  ```

- インデックスと検索の注意点  
  B-tree は配列の部分検索には役立たない（全配列比較か順序付きソートのみ）。要素の存在検索には GIN インデックスを使うのが基本。主要な演算子は次のとおり：
  - 包含: @> （列が指定要素をすべて含む）
  - 重複: && （列がいずれかの要素を持つ）

  ANY の落とし穴：引数として配列を渡す用途（外部からリストを渡す）には id = ANY($1::int[]) が有効だが、テーブル列（tags など）の中身をスカラー値と比較して存在を調べると、= ANY(tags) は配列専用演算子に頼らないためインデックス（GIN）を使えずシーケンシャルスキャンになる。代わりに tags @> ARRAY['feature'] のように書く。

  悪い例（遅くなる）:
  ```sql
  -- SQL
  SELECT * FROM tickets WHERE 'feature' = ANY(tags);
  ```
  良い例（GINを使える）:
  ```sql
  -- SQL
  SELECT * FROM tickets WHERE tags @> ARRAY['feature'];
  ```

- GIN の書き込みコストと fastupdate  
  GIN は1行が要素数分の索引エントリを持つため、書き込み負荷が増える。PostgreSQL は「fastupdate」で一時バッファに入れてマージによる負荷緩和をするが、pending リストが大きくなるとクエリが遅くなる可能性がある。読み取り重視なら fastupdate を無効化する選択肢がある：
  ```sql
  -- SQL
  CREATE INDEX posts_by_tags ON posts USING GIN (tags) WITH (fastupdate = off);
  ```

- 配列更新の本質的なコスト（MVCC と TOAST）  
  PostgreSQL は行をインプレース更新せず MVCCで新しい行を書き換えるため、配列要素を1つ変更しても行全体が再書き込みされる。さらに配列が大きくなると TOAST によって外部ストレージに退避され、更新時は外部チャンクを全部読み出してデコンプレス→修正→再圧縮して書き戻す必要が出る。TOAST の閾値はおおよそ:
  $$\text{threshold} \approx \frac{\text{page\_size}}{\text{tuples\_per\_page}} = \frac{8192}{4} = 2048\ \text{bytes}$$
  つまり ~2KB を超えると外部化されやすい。Postgres 14 以降は LZ4 を指定でき、pglz より高速なので TOAST のCPUコストが下がる：
  ```sql
  -- SQL
  ALTER TABLE articles ALTER COLUMN tags SET COMPRESSION lz4;
  ```

- 多次元配列・スライスの罠  
  添字 [1] とスライス [1:1] は振る舞いが違い、スライスは常に配列を返す。多次元配列は「配列の配列」ではなく一つの行列として扱われるため、配列の部分を期待どおりに取り出すには unnest と再集約が必要になる場合がある。

- 使ってよいケース／避けるべきケース  
  - 良いケース：生成後ほぼ変更しない大きな配列（参照専用）／プリミティブ型でメモリ効率が重要な場合  
  - 悪いケース：高頻度で要素を追加・削除する小〜中サイズ配列（毎リクエストで更新されるログやイベントIDなど）

- 代替手段
  - リレーショナルな一貫性が必要なら中間テーブル（正規化）
  - 可変で複雑な構造なら jsonb（柔軟だがメタデータが増える）
  - 数値集合や高速集合演算が必要なら intarray 拡張、埋め込みベクトルには pgvector など拡張を検討

## 実践ポイント
1. 設計判断のチェックリスト
   - そのリストは「行のライフサイクルと一致」しているか？ 参照整合性が必要なら配列ではなく中間テーブルを選ぶ。
   - その配列は頻繁に更新されるか？ 更新が多ければ配列は避ける。  

2. クエリの書き方
   - 外部からリストを渡すとき：id = ANY($1::int[]) を使う（プレースホルダ1つで済む）。
   - 配列列内検索は @> / && を使って GIN を活かす（'x' = ANY(tags) は避ける）。

3. スキーマと制約
   - 次元や長さを保証したければ CHECK で array_ndims()/array_length() を使う。
   - 多次元配列を意味的に使うなら jsonb の方が扱いやすいことが多い。

4. インデックスと運用
   - 要素検索には GIN を使う。読み取り一辺倒なら fastupdate = off を検討。
   - 大きな配列は TOAST に入りやすいので圧縮方式を lz4 に変えることで更新コストを下げられる。

5. モニタリング
   - 更新負荷が高いテーブルは VACUUM/ANALYZE、GIN pending リストのサイズ、TOAST テーブルのI/Oを監視する。

まとめ：配列は便利だが万能ではない。用途（読み取り専用か更新多発か）、整合性要件、検索パターンを踏まえて、配列か正規化か、あるいは jsonb/拡張かを選ぶことが重要。短期的な楽を取ると中長期でコストが増える点を意識して設計を行ってほしい。
