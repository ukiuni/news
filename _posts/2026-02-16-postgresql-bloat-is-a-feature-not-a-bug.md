---
layout: post
title: "PostgreSQL Bloat Is a Feature, Not a Bug - PostgreSQLのブロートはバグではなく“仕様”だ"
date: 2026-02-16T16:27:00.077Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://rogerwelin.github.io/2026/02/11/postgresql-bloat-is-a-feature-not-a-bug/"
source_title: "PostgreSQL Bloat Is a Feature, Not a Bug | Roger Welin"
source_id: 440308056
excerpt: "Postgresの見えないbloatが性能とコストを直撃、簡単対策で即効改善"
---

# PostgreSQL Bloat Is a Feature, Not a Bug - PostgreSQLのブロートはバグではなく“仕様”だ
容量だけじゃ済まない！Postgresの「見えないゴミ（bloat）」が性能とコストを蝕む理由と、今すぐできる対策

## 要約
PostgreSQLのテーブルやインデックスが肥大化（bloat）するのは設計（MVCC）による必然で、単なるディスク不足ではなくI/O・CPU・バックアップ性能に直結する問題。理解して適切に監視・運用すれば被害を抑えられる。

## この記事を読むべき理由
日本のSaaS/EC/業務系システムは高頻度更新や長時間トランザクションが多く、気づかないうちにストレージ課金やレスポンス低下を招く。原因と現実的な対策を知ると現場で即効性のある改善ができる。

## 詳細解説
- ページとタプル：Postgresはテーブルを8KBページ単位で管理し、行は「タプル」として格納。ページは一度割り当てられると通常はOSに返らない。
- MVCC（Multi-Version Concurrency Control）：更新は「上書き」せず新しいタプルを作成し、古いタプルは他トランザクションの参照が不要になるまで残る（dead tuple）。これが蓄積してbloatになる。
- I/O影響：Postgresはページ単位で読み込むため、1ページ内に生存タプルが少なくても死んだタプルをスキャンするコストは変わらない。ページ当たりのdead率が高いほど無駄読みが増える。
- インデックスの肥大：削除・更新によるインデックスエントリも残る。インデックスはREINDEXや再構築でしか縮小しない（REINDEX CONCURRENTLYやpg_repackで非ブロッキングな対応が可能）。
- VACUUM：deadタプルを「再利用可能」にするがファイルサイズは縮めない（VACUUMはページ内空き化）。VACUUM FULLはファイルを再書きしてOSへ返すが排他ロックが発生するため本番では注意。
- 自動掃除（autovacuum）：デフォルト閾値は dead > 50 + 0.2 * live。大きなテーブルや高更新率ではデフォルトが遅すぎる場合がある。
- 測定ツール：pg_stat_user_tables、pgstattuple、pageinspect 等で実態が可視化できる。

例（監視・診断に使うSQL例）
```sql
-- 生死タプル確認
SELECT relname, n_live_tup, n_dead_tup FROM pg_stat_user_tables WHERE relname = 'products';

-- pgstattupleで正確な割合
CREATE EXTENSION IF NOT EXISTS pgstattuple;
SELECT * FROM pgstattuple('products');

-- インデックス再構築（アプリ継続）
REINDEX INDEX CONCURRENTLY products_pkey;
```

## 実践ポイント
- まずは可視化：pg_stat_user_tables / pgstattuple でdead比率を確認する。
- インデックス肥大はREINDEX CONCURRENTLYやpg_repackで縮小する（本番影響を考慮）。
- VACUUMは自動化を前提に、autovacuumパラメータ（autovacuum_vacuum_scale_factor / autovacuum_vacuum_threshold）をワークロードに合わせて調整する。
- 更新が多い列を見直す：頻繁に更新するカラムをインデックス化しない、列分割やパーティショニングを検討する。HOT更新を活かす（同ページ内で済む更新を促す）。
- 大きく縮めたい場合はVACUUM FULLを保守時間で実行、もしくはオンラインで使えるpg_repackを検討。
- クラウド利用者はストレージ課金・バックアップ時間・リードレイテンシを意識し、定期メンテナンスとアラートを設定する。

短期：監視→REINDEX/pg_repack。中長期：autovacuum調整、スキーマ見直し、パーティショニングで肥大化を抑える。
