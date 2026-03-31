---
layout: post
title: "Good CTE, Bad CTE - CTEの正体（良いCTE、悪いCTE）"
date: 2026-03-31T11:28:35.495Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://boringsql.com/posts/good-cte-bad-cte/"
source_title: "Good CTE, bad CTE | boringSQL"
source_id: 47571330
excerpt: "CTE次第でクエリ性能が激変、MATERIALIZEDで制御する方法"
image: "https://boringsql.com/og-images/good-cte-bad-cte-og.jpg"
---

# Good CTE, Bad CTE - CTEの正体（良いCTE、悪いCTE）
使い方で速さが変わる！PostgreSQLのCTE（WITH句）を味方にする方法

## 要約
PostgreSQLのCTE（WITH句）は書きやすい反面、書き方次第で実行計画に大きく影響します。PostgreSQL 12以降は多くのCTEが「インライン化」されますが、再帰・副作用・複数参照などは「マテリアライズ（固定化）」され、性能に差が出ます。

## この記事を読むべき理由
CTEは可読性向上の魔法箱ですが、誤用するとインデックスやパーティションプルーニングが効かず性能劣化します。日本のアプリでよくある大量データの集計やバッチ処理、トランザクション整合性要件にも直結するため、実務で無駄な遅延を避けたいエンジニアは必読です。

## 詳細解説
- 歴史的背景：PG11以前はCTEは常にマテリアライズされ、オプティマイザは中身を見られませんでした（"optimization fence"）。PG12で非再帰かつ副作用のない単一参照CTEは自動的にインライン化されるようになりました。
- インライン化される条件（代表）：
  - CTEが1回だけ参照される
  - 副作用（INSERT/UPDATE/DELETE）がない
  - VOLATILEな関数（random(), clock_timestamp(), nextval() 等）を含まない
- マテリアライズされる条件（代表）：
  - CTEが複数回参照される（計算を一度だけ実行して再利用）
  - 再帰CTE（WITH RECURSIVE）やデータ変更を伴うCTE
  - VOLATILE関数を含む場合
- 明示的な制御：PG12以降は MATERIALIZED / NOT MATERIALIZED キーワードでオプティマイザの挙動を強制できます。
  
sql
WITH filtered AS MATERIALIZED (
  SELECT * FROM orders WHERE status = 'pending'
)
SELECT * FROM filtered WHERE amount > 400;

sql
WITH recent AS NOT MATERIALIZED (
  SELECT * FROM orders WHERE created_at > now() - interval '7 days'
)
SELECT * FROM recent WHERE status = 'pending';

- 実運用での影響例：インライン化されれば複合インデックスやフィルタの結合（predicate pushdown）が効き高速化。反対に不必要にマテリアライズされると一時的なtuplestoreをスキャンするためI/O/メモリ負荷が増えます。
- 最新の進展：記事はPG12の変更点を中心に扱い、さらに（記事内では）PG17での統計伝播など新機能にも触れています。環境のPostgreSQLバージョンによって挙動が変わる点に注意してください。

## 実践ポイント
- まずEXPLAINでプランを確認する。CTEがCTE Scan/CTE nodeとして残っているかをチェック。
- 単一参照かつ副作用が無ければ素直にWITHを使ってOK。問題があればNOT MATERIALIZEDで強制インライン化して再確認。
- 計算コストが高く複数回参照する場合はMATERIALIZEDで明示的にキャッシュするか、一時テーブルに置いておく。
- random()/clock_timestamp()/nextval()等のVOLATILEを含むCTEは自動的にマテリアライズされると覚える。
- バージョン依存の挙動に注意：本番DBのPostgreSQLバージョンで必ず挙動を確認し、ANALYZEを実行して統計を最新にする。
- 大きなクエリは「可読性」と「性能」を切り分け、必要なら一時テーブルやサブクエリに置き換えてベンチを取る。

短時間で効率的に原因を切り分けたい場合は、EXPLAIN（ANALYZE）→ MATERIALIZED/NOT MATERIALIZED → インデックス/統計の順で試してください。これだけで多くの「CTEで遅い」が解決します。
