---
layout: post
title: "Introduction to PostgreSQL Indexes - PostgreSQLのインデックス入門"
date: 2026-01-25T11:20:20.107Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dlt.github.io/blog/posts/introduction-to-postgresql-indexes/"
source_title: "Introduction to PostgreSQL Indexes ::"
source_id: 46751826
excerpt: "Postgresのインデックスで検索を数msに短縮する実践指針"
---

# Introduction to PostgreSQL Indexes - PostgreSQLのインデックス入門
Postgresのインデックスで検索を劇的に速くする — 初心者向けやさしい実践ガイド

## 要約
インデックスはディスク読み取りを減らしてクエリを高速化する仕組みで、種類（B-tree/BRIN/GIN/GiST/Hash/SP‑GiST）ごとに得意・不得意がある。使いどころとコスト（ディスク・書込み負荷・メモリ・プランニング時間）を理解すると効果的に運用できる。

## この記事を読むべき理由
Postgresは日本でもクラウドDBやオンプレで幅広く使われており、誤ったインデックス運用は性能劣化やコスト増に直結します。初心者にも分かる実測と実践的な指針を押さえれば、検索改善・運用コスト削減に直結します。

## 詳細解説
- データ配置の基礎  
  Postgresのテーブルはヒープ（8KBページの集合）にランダムに行（tuple）を置く。各行には内部識別子としてctid（(block, offset)）が付き、インデックスは「検索キー → ctid」のマップを持つ。

- インデックスが速い理由  
  インデックス（典型はB-tree）は値から該当行の位置(ctid)を短時間で特定でき、全ページを走査する「シーケンシャルスキャン」を避けられる。B-treeの探索は$O(\log n)$（1百万件でも約20比較）という性質を持つ。

- 実測例（概念）  
  大きなテーブルで全件走査すると数千ページを読み取り数百msかかるが、適切なインデックスがあれば数ページ読み取りで数ms以下に短縮される。インデックス自体もディスクを消費し、場合によってはテーブルより大きくなることもある。

- インデックスの種類（代表）  
  - B-tree：デフォルト。一般用途、レンジ／ORDER BYに強い。主キー・一意制約で必須。  
  - BRIN：超大規模で主に物理的に近い値（タイムスタンプ連続追加など）に有利、非常に小さい。  
  - GIN：全文検索や配列検索など多値インデックス向け。  
  - GiST/SP‑GiST：空間データや特殊データ構造向け。  
  - Hash：等価検索専用（用途限定）。  

- コスト（運用上の注意）  
  - ディスク容量とバックアップ増加。  
  - INSERT/UPDATE/DELETEでインデックス更新が発生し書込みコスト増。  
  - インデックスが増えるとクエリプランナーの選択肢が増え、プラン時間が増える場合がある。  
  - shared_buffersやワークメモリを圧迫する可能性。

## 実践ポイント
- まず測る：`EXPLAIN (ANALYZE, BUFFERS) <query>`で実行プランとI/Oを確認。  
- ロックを避ける：本番で作るときは `CREATE INDEX CONCURRENTLY ...` を検討。  
- 適用基準：目安として返る行数がテーブルの15–20%未満で効果が出やすいが、必ずEXPLAINで検証する。  
- マルチカラムは左端ルールを意識：`CREATE INDEX ON t(a,b)` は a の検索に優先。複数条件で頻繁に使うならマルチカラムか複数インデックスの使い分けを検討。  
- 大規模時はBRINを検討：時間順追加のログやセンサーデータ等でコスト効率が高い。  
- 運用監視：`pg_stat_user_indexes` や `pg_stat_all_tables`、定期的な `VACUUM` / `REINDEX` を忘れず。  
- 不要なインデックスを削除して書込み負荷とバックアップ容量を削減。

参考アクション（すぐ試せる）
```sql
-- 実行計画とバッファを確認
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM foo WHERE name = 'Ronaldo';

-- 本番でロックを避けて作る
CREATE INDEX CONCURRENTLY ON foo(name);

-- BRINの例（連続時刻列に有効）
CREATE INDEX CONCURRENTLY ON logs USING BRIN (created_at);
```

以上を踏まえ、まずは疑わしいクエリをEXPLAINで測り、必要なインデックスを最小限に追加して効果を確認することをおすすめします。
