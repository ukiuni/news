---
layout: post
title: "Work_mem: It's a Trap - work_mem: 罠だ！"
date: 2026-03-20T22:24:51.725Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://mydbanotebook.org/posts/work_mem-its-a-trap/"
source_title: "work_mem: it&#39;s a trap! | My DBA Notebook"
source_id: 47431304
excerpt: "work_memの誤解で数百GB消費、PostgresがOOMする原因と対策"
---

# Work_mem: It's a Trap - work_mem: 罠だ！
Postgresのwork_memが「小さくても」クラスタ全滅を招いた話 — 見落としがちなメモリ管理の罠

## 要約
work_memは「1回のハッシュ／ソート操作あたり」の上限だが、Postgresのメモリコンテキスト設計により割当てが一括で解放されるため、意図せず巨大メモリ消費を招くことがある。pg_log_backend_memory_contextsで原因追跡が可能。

## この記事を読むべき理由
日本のミッションクリティカルなDB環境でも、短時間で大量メモリを消費してOOMに至るパターンは現実的なリスク。原因追跡手順と対策を知っておけば、夜中の障害対応やチーム説得が格段に楽になる。

## 詳細解説
- 問題の症状：開発者がwork_mem=2MBに設定していたにも関わらず、単一クエリで数百GB〜TB級のメモリを消費し、OOMでクラスタが落ちた。
- キーとなる観察：pg_log_backend_memory_contexts(PID)を使うと、ExecutorStateやHashTableContextのサイズ・チャンク数が出る。今回の再現ではExecutorStateに524,059個のチャンクが積み上がっていた。
- なぜ起きるか：work_memは「ハッシュ／ソートごとの上限」。だがPostgresはメモリコンテキスト（ExecutorState → 子コンテキスト）単位で管理し、コンテキスト内の個々の割当てはクエリ終了まで解放されない。結果として多数の操作が同一ExecutorStateにたまり、それぞれが最大値まで割り当てられると合算で巨大になる。
- 実例の流れ：関数をFROM句で扱うなど「関数の結果を中間状態として長く保持する」クエリ構造があり、1つの巨大なExecutorStateに膨れ上がった。これがOOMに直結した。
- 設計上の注意：Postgresはバックエンド単位のハードメモリ上限を持たない（OS依存）。work_memの単純な値変更だけでは防げないケースがある。

SQLでメモリコンテキストを確認する例：
```sql
-- SQL
SELECT pg_log_backend_memory_contexts(<PID>);
```

統計作成の例（相関のある列がある場合）：
```sql
-- SQL
CREATE STATISTICS corr_stats ON (col1, col2) FROM my_table;
ANALYZE my_table;
```

## 実践ポイント
- 問題発生時はまず pg_log_backend_memory_contexts(PID) を呼んで、どのコンテキストが膨れているかを見る。
- クエリ修正：関数をそのままJOINで流用するなど「大きな中間結果を1つの実行コンテキストにためる」構造を避け、必要なら一時テーブルや明示的なマテリアライズで分割する。
- 統計を整備：ANALYZE、CREATE STATISTICS、必要に応じて ALTER TABLE ... SET STATISTICS でプランナーの精度を上げ、ディスクスピルを適切に誘導する。
- 運用防衛：statement_timeoutで長時間実行クエリを自動打ち切り、pg_stat_activityや監視でメモリ増大を早期検知する。
- 教訓：ハードウェア増強で「解決」できるわけではない。設計と観測で根本を潰すこと。

以上。問題を再現できる環境があるならまず pg_log_backend_memory_contexts を使ってログを取ってください。
