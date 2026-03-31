---
layout: post
title: "Show HN: How This Graybeard Built the Fastest and Freest Postgres BM25 Search - Graybeardが作った最速かつ自由なPostgres BM25検索"
date: 2026-03-31T20:32:12.703Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/timescale/pg_textsearch"
source_title: "GitHub - timescale/pg_textsearch: PostgreSQL extension for BM25 relevance-ranked full-text search. Postgres OSS licensed. · GitHub"
source_id: 47589856
excerpt: "pg_textsearchでPostgresにBM25高速検索を並列・Block‑Maxで実現。"
image: "https://opengraph.githubassets.com/798d624efd7a9a1563809b457217beb4b878d32f3d4f36b14e362161854e95ad/timescale/pg_textsearch"
---

# Show HN: How This Graybeard Built the Fastest and Freest Postgres BM25 Search - Graybeardが作った最速かつ自由なPostgres BM25検索
Postgres上でBM25ランキングを高速・柔軟に実現する拡張「pg_textsearch」を分かりやすく紹介

## 要約
pg_textsearchはPostgreSQL向けBM25スコアリング拡張で、Block-Max WANDや並列インデックス作成、セグメント圧縮などで「高速な上位k取得（top‑k）」を実現するOSS（Postgres互換）。

## この記事を読むべき理由
日本のサービスで「検索の精度と速度」を両立したいエンジニアにとって、既存のPostgres環境に低コストでBM25ランク付けを追加できる実用的な選択肢だから。既存のPostgres運用・パーティション構成と相性が良く、スケールも効く点が魅力。

## 詳細解説
- コア機能：BM25スコアでの順位付けをPostgresインデックスとして実装。ORDER BY content <@> 'query' LIMIT n の形で高速top‑k検索が可能。  
- BM25式（パラメータ $k_1, b$ を調整可能）:  
  $$\mathrm{score}(q,d)=\sum_{t\in q}\mathrm{IDF}(t)\cdot\frac{tf_{t,d}(k_1+1)}{tf_{t,d}+k_1(1-b+b\cdot|d|/\mathrm{avgdl})}$$
- 最適化：Block‑Max WAND によるブロック単位スキップでLIMIT付きクエリを劇的に高速化。デフォルトでセグメント圧縮やメモリテーブル（memtable）を使い、書込み→クエリのバランスを取る設計。
- 実装上の注意：拡張は shared_preload_libraries にロードして使用。bm25query型や to_bm25query() による明示的インデックス指定（WHEREでの絞り込み時に有効）をサポート。
- 並列ビルド：大きなテーブルは parallel workers でインデックス作成。maintenance_work_mem >= 64MB が必要。パーティションごとに独立して並列構築するので大規模データにも強い。
- 運用GUCやUI：pg_textsearch.default_limit（LIMITが無いときのスコア対象件数）、compress_segments、memtable_spill_threshold などの調整でパフォーマンス制御が可能。
- 日本語対応：拡張自体はPostgresのtext search設定（text_config）を利用するため、形態素解析プラグイン（pg_bigm / mecab連携など）や専用トークナイザーと組み合わせれば日本語コーパスでも有効。ただしトークン化の品質が検索精度に直結する点に注意。

## 実践ポイント
- インストール＆導入（要再起動）:
```sql
-- postgresql.conf に追加してサーバ再起動
shared_preload_libraries = 'pg_textsearch';

-- DBごとに一度だけ
CREATE EXTENSION pg_textsearch;
```
- 基本的なインデックス作成と検索:
```sql
CREATE TABLE documents(id bigserial PRIMARY KEY, content text);
CREATE INDEX docs_idx ON documents USING bm25(content) WITH (text_config = 'english', k1 = 1.2, b = 0.75);

SELECT * FROM documents ORDER BY content <@> 'database system' LIMIT 5;
```
- WHEREで絞る場合：事前に絞り込みが選択的（少数ヒット）ならB-treeで先にフィルタ、そうでなければBM25で上位取得→後段フィルタの戦略を検討。
- 並列インデックス作成の例:
```sql
SET max_parallel_maintenance_workers = 4;
SET maintenance_work_mem = '256MB';
CREATE INDEX docs_idx ON documents USING bm25(content) WITH (text_config = 'english');
```
- 大量ロード後はマージで高速化:
```sql
SELECT bm25_force_merge('docs_idx');
```
- モニタリング:
```sql
SELECT schemaname, tablename, indexname, idx_scan FROM pg_stat_user_indexes WHERE indexrelid::regclass::text ~ 'pg_textsearch';
```

短時間で試せる＝既存Postgresに追加しやすい点が最大の魅力。日本語で使う際はトークナイザー（形態素解析）設計とLIMITを使ったtop‑k戦略を優先的に検証すると効果が出やすい。
