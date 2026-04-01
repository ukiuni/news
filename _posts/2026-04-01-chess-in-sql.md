---
layout: post
title: "Chess in SQL - 純粋なSQLでチェスを描く"
date: 2026-04-01T06:17:32.939Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.dbpro.app/blog/chess-in-pure-sql"
source_title: "Chess in Pure SQL - DB Pro Blog"
source_id: 47562961
excerpt: "SQLだけでチェス盤を描き駒を動かす実例—ピボットとCTEで8×8を可視化"
image: "https://www.dbpro.app/blog/chess-in-pure-sql/opengraph-image"
---

# Chess in SQL - 純粋なSQLでチェスを描く
ブラウザで動くチェスを「SELECT / UPDATE」だけで作ったら、DBがゲームボードになった話

## 要約
SQLだけでチェス盤を「描画」して駒を動かすデモ。行列をピボットする条件付き集約で8×8のグリッド表示を作り、DELETE/INSERT（またはUPDATE）で駒を移動するアイデアを示す。

## この記事を読むべき理由
SQLを単なるデータ保存言語としてではなく「視覚化／操作の表現手段」として使う発想が学べる。BIやデータ系ツールを使う日本のエンジニアにとって、ピボット技法やCTEの応用は実務でも役立つ。

## 詳細解説
- ボード表現：rank（1–8）とfile（1–8）とpieceカラムを持つテーブルで駒を管理。空マスはNULLや記号で表す。
- 64マス生成：rankとfileのクロスジョイン（または数列生成）で全マスを用意し、駒テーブルをLEFT JOINして全体を埋める。
- 行→列の変換（ピボット）：SQLは行を返すため、条件付き集約で列を作る。各ファイルに対して CASE WHEN file = N THEN piece END を MAX() で取り出す。
- 見た目調整：COALESCEで空マスを '·' にし、ORDER BY rank DESC で通常のチェス表示に揃える。
- 駒の移動：DELETE + INSERT（出発マスの駒を削除して到着マスに挿入）か、単純な UPDATE で位置を更新。取った駒は先に削除する必要あり。
- 応用性：同じピボット技法はカレンダー表示、座席表、ヒートマップなど任意のグリッド可視化に使える。

例：ピボット表示（簡略）
```sql
WITH full_board AS (
  SELECT r AS rank, f AS file
  FROM generate_series(1,8) AS r
  CROSS JOIN generate_series(1,8) AS f
)
SELECT rank,
  COALESCE(MAX(CASE WHEN file=1 THEN piece END),'·') AS a,
  COALESCE(MAX(CASE WHEN file=2 THEN piece END),'·') AS b,
  ...,
  COALESCE(MAX(CASE WHEN file=8 THEN piece END),'·') AS h
FROM full_board
LEFT JOIN pieces USING (rank,file)
GROUP BY rank
ORDER BY rank DESC;
```

駒を移動（DELETE/INSERT の例）
```sql
BEGIN;
DELETE FROM pieces WHERE rank=2 AND file=5; -- e2 の白ポーンを削除
INSERT INTO pieces (rank,file,piece) VALUES (4,5,'P'); -- e4 に挿入
COMMIT;
```

## 実践ポイント
- 自分のDBクライアント（Visual Studio Code の DB拡張など）で上のクエリを試し、結果をテキストで「盤」に見立てると理解が早い。
- ファイル a–h を 1–8 にマップする仕組みを用意すると入力が楽になる。
- 同じ手法でカレンダーや座席表の可視化に転用可能。大量更新がある場合はトランザクションで整合性を確保すること。
- まずは「1手だけ動かす」簡単なUPDATE/DELETEで試し、徐々に操作系（キャプチャ、成り、キャスリング）を追加してみる。
