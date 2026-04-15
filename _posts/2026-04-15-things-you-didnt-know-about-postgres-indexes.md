---
layout: post
title: "Things you didn't know about (Postgres) indexes - （Postgres）インデックスの知られざる話"
date: 2026-04-15T14:36:28.181Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://jon.chrt.dev/2026/04/15/things-you-didnt-know-about-indexes.html"
source_title: "Things you didn&#39;t know about indexes"
source_id: 362266923
excerpt: "Postgresのインデックス設計ミスで遅くなる5つの落とし穴と即効対策"
---

# Things you didn't know about (Postgres) indexes - （Postgres）インデックスの知られざる話
魅力的な日本語タイトル: 「速い検索の裏側：Postgresインデックスで知らないと損する5つのポイント」

## 要約
インデックスは検索を劇的に速くするが、使い方次第で効果が出ないどころかコストを生む。Postgres特有の実用的な落とし穴と対策を短くまとめます。

## この記事を読むべき理由
インデックス設計の誤りは、SaaSやECのレスポンス低下・運用コスト増につながります。日本のサービス開発でも遭遇しやすい問題なので、基礎と現場で使える対処法を押さえておくべきです。

## 詳細解説
- インデックスの役割  
  インデックスは教科書の巻末索引のように値をソートして高速検索を可能にします。Postgresは通常B-treeを使い、等価検索や範囲検索を高速化します。

- トレードオフ：読みは速く、書きは遅く  
  インデックスを増やすとSELECTは速くなるが、INSERT/UPDATE/DELETEでその分インデックス更新コストが増え、ディスク容量とキャッシュ利用も増えます。プランナーの検討候補も増え、クエリプランの最適化時間が伸びることもあります。

- 合成（複合）インデックスの順序性  
  CREATE INDEX ON t (a, b); はまず a でソートし、同値グループ内で b を見る構造になるため、a を条件にするクエリに効くが、b のみの検索には使われないことがある。

  ```sql
  CREATE INDEX ON pokemon (type_1, type_2);
  ```

- 関数で包むとインデックスが使えない  
  lower(name) = 'pikachu' のように列を関数で包むと、元の列インデックスは使われません。対策は式インデックス（functional/index on expression）を作ることです。

  ```sql
  CREATE INDEX ON pokemon (lower(name));
  ```

- 部分インデックス（partial index）  
  全行ではなく条件に合致する行だけを索引化すると小さく速いインデックスが作れます（例：is_legendary = true だけ）。ソフトデリートやステータスで頻繁に絞るケースに有効。

  ```sql
  CREATE INDEX ON pokemon (name) WHERE is_legendary = true;
  ```

- カバリングインデックス（Index-only scan）  
  インデックスにクエリで必要な列が全て含まれていれば、テーブル本体にアクセスせずインデックスだけで完結します。Postgresの INCLUDE を活用するとソート対象にせず列を持たせられます。

  ```sql
  CREATE INDEX ON pokemon (name) INCLUDE (base_attack);
  ```

- 測ること（EXPLAIN / EXPLAIN ANALYZE）  
  感覚で作らず、EXPLAINで実行計画を確認。Index Scan / Index Only Scan が出ているか、Seq Scan（全表走査）が出ていないかをチェックする習慣をつける。

  ```sql
  EXPLAIN ANALYZE SELECT * FROM pokemon WHERE name = 'Pikachu';
  ```

## 実践ポイント
- まずはプロファイル：EXPLAIN ANALYZE を用いてボトルネックを特定する。  
- 検索パターンを観察してからインデックス設計（頻出の WHERE 条件順序を優先）。  
- 大きく偏った値（真偽やソフトデリート）には部分インデックスを検討する。  
- ケース変換などで検索するなら式インデックスを作るか、正規化して保存時に揃える。  
- INCLUDE を使い、必要ならカバリングインデックスで読み取りだけ高速化する。  
- インデックスは追加コストも考慮：書き込み負荷やキャッシュ利用をモニタリングする。

短時間で効果を出すには「測る→設計→検証」のループを回すこと。これだけで多くの遅さは解消できます。
