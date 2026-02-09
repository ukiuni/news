---
layout: post
title: "Three Cache Layers Between SELECT and disk - SELECT とディスクの間にある 3 つのキャッシュ層"
date: 2026-02-09T14:27:58.219Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://frn.sh/iops/"
source_title: "Three cache layers between SELECT and disk"
source_id: 447248685
excerpt: "Postgresの3層キャッシュでIOPSが急増する原因と即効対処法がわかる"
---

# Three Cache Layers Between SELECT and disk - SELECT とディスクの間にある 3 つのキャッシュ層
クリックしたくなる日本語タイトル: ディスク読み出しはこう動く──Postgresの「3層キャッシュ」と爆発的IOPSの正体

## 要約
Postgresがページを読むときは「shared_buffers（Postgres内）」→「OSページキャッシュ（カーネル）」→「ディスク（例：EBS）」の順に3層をたどる。誤ったインデックスや設定でその全てを突破すると、短時間で大量のI/O（IOPS）を消費してしまう。

## この記事を読むべき理由
クラウドDB（Heroku/RDS/EBS等）を使う日本のサービスでも、プロビジョンドIOPSやコスト上限に簡単に突き当たる。原因の診断と対処を知れば、無駄な課金・タイムアウト・パフォーマンス問題を避けられる。

## 詳細解説
- 3 層の説明  
  1. shared_buffers：Postgresプロセス内の8KBページ単位キャッシュ（プロセス内メモリ）。ここにあれば最も安価。  
  2. OSページキャッシュ：カーネルが管理するブロックキャッシュ。Postgresがread(2)を呼ぶとここでヒットすればディスクは不要。shared_buffers と物理RAMを奪い合う。  
  3. ディスク：キャッシュに無ければデバイス（例：AWS EBS）へI/O。これが IOPS としてカウントされ、最も高コスト・高遅延。

- メモリの競合と設定の落とし穴  
  shared_buffers を増やすとOSページキャッシュが減り、逆に総合性能が落ちることがある。work_mem（ソートやハッシュ用、クエリ単位）を小さくするとディスクへスピルが増え、I/O負荷が上がる。全ては同じ物理RAM上で競合する。

- 実例（問題のクエリ）  
  インデックスで account_id を絞る → その後 JSONB 等でフィルタする、というパターンで大量のヒープ読み出しが発生。元記事の例では:
  - 27,841 ブロック読み出し（1ブロック = 8KB）→ $27{,}841 \times 8\text{KB} \approx 217\text{MB}$ を 14 秒で読み、約 $1{,}989$ IOPS 相当を単一クエリで消費。  
  - インデックス自体の読み（B-tree）→ ヒープページへの参照、という「二段構えのI/O」が発生するためコストが倍になる。  
  - PostgresのMVCCにより更新で行が散らばり、同一account_idの行が多数のランダムページに散るためランダムI/Oが増える。

- なぜインデックスが効かなかったか  
  単純なB-tree index(account_id)は「行の位置」しか示さない。JSONBや追加条件をインデックス内で評価できないため、候補行をヒープから読み出しフィルタして捨てる操作が大量発生する。

## 実践ポイント
- まず観測：shared/heapヒット比やI/Oを確認するSQLや監視を見よう（pg_statio_user_tables, pg_stat_statements, IOPSメトリクス）。  
  例:
  ```sql
  -- PostgreSQL: shared buffer ヒット率確認
  SELECT sum(heap_blks_read) AS heap_read,
         sum(heap_blks_hit) AS heap_hit,
         sum(heap_blks_hit)::float / nullif(sum(heap_blks_hit)+sum(heap_blks_read),0) AS ratio
  FROM pg_statio_user_tables;
  ```
- インデックス設計を見直す：JSONB に対しては GIN インデックス、NULL 条件には部分インデックスを検討し「フィルタ条件をインデックス内で済ます」。  
- work_mem と shared_buffers のバランス：大量同時接続があるなら work_mem を上げすぎない。shared_buffers はOSページキャッシュとトレードオフになるためサーバ全体のRAM設計で検討。  
- テーブルメンテ：VACUUM/REINDEX/pg_repack でテーブル断片化を減らし、行の散らばりを緩和する。  
- 管理クラウド上の対策：EBSのプロビジョンドIOPSを増やす、もしくはNVMeローカルストレージを選ぶ。だが先にインデックス改善でI/Oを削減するのが安上がり。  
- 一時ファイル（temp files）の監視：sortやhashのスピルが増えていないかチェック。  
- クエリ側でやれること：必要な列のみ取得、早めに絞り込みを行う（可能ならサブクエリやマテビューで前処理）。

以上を踏まえれば、「なぜ遅いか」「どこを触れば良いか」が明確になります。まずは観測→インデックス改善→必要ならインフラ拡張の順で対処してください。
