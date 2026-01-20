---
layout: post
title: "Unconventional PostgreSQL Optimizations - PostgreSQL の変わり種最適化"
date: 2026-01-20T16:03:14.480Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://hakibenita.com/postgresql-unconventional-optimizations"
source_title: "Unconventional PostgreSQL Optimizations | Haki Benita"
source_id: 1208731180
excerpt: "チェック制約と関数/生成列で誤検索の全表スキャンを回避し小型インデックス化"
image: "https://hakibenita.com/images/00-postgresql-unconventional-optimizations.png"
---

# Unconventional PostgreSQL Optimizations - PostgreSQL の変わり種最適化
間違いを無駄にしない！レポート集計で効く、スキャン回避と小さなインデックスの作り方

## 要約
チェック制約や関数ベースのインデックス、生成列を賢く使えば、意外なクエリの無駄スキャンを防ぎ、インデックス容量と実行時間を両方削減できる。

## この記事を読むべき理由
BI／アナリストによる ad-hoc クエリが多い環境（社内レポーティングやデータウェアハウス）は、日本の多くの企業でも当てはまる。クラウドのストレージ/IOコストや、開発現場での「ちょっとしたミス」が大きな無駄を生む場面で、実務ですぐ役立つテクニックが学べる。

## 詳細解説
- チェック制約で「絶対に真にならない条件」を検出してスキャンを回避する  
  例：plan カラムが 'free'/'pro' のみ許されているとき、アナリストが誤って 'Pro' と検索すると結果は0件。通常の設定だと全表スキャンされるが、constraint_exclusion を利用するとプラン生成時に制約と照合して「常に偽」と判定でき、実行を即終了できる。  
  設定例（セッション単位で切り替え推奨）:
  ```sql
  -- SQL
  SET constraint_exclusion = 'on';
  ```

  注意点：constraint_exclusion を常時オンにするとプラン生成コストが上がることがあるため、主にレポート/分析用の環境で有効化するのが現実的。

- 集計で「日単位」しか使わないなら日時全部をインデックス化しない  
  10M行モデルで sold_at（timestamptz）に普通の B-tree を貼るとインデックスが大きくなる（例：214MB）。一方 date_trunc(... ) の結果をキーにした関数ベースのインデックスは値の種類が少なく、重複排除されて格納効率が良くなるためサイズと検索速度の両方で有利になる。  
  例（関数ベースインデックス）:
  ```sql
  -- SQL
  CREATE INDEX sale_sold_at_date_ix
    ON sale ((date_trunc('day', sold_at AT TIME ZONE 'UTC')::date));
  ```

  この戦略で
  - テーブル全走査 → 600ms
  - 全日時インデックス → 187ms（Index サイズ大）
  - 日付のみインデックス → 145ms（小型インデックス）
  のような改善が期待できる。重要なのは「必要な粒度だけをインデックス化する」こと。

- 弱点：式の厳密一致を求められる（ディシプリン問題）  
  関数ベースのインデックスはクエリ側の式がインデックス作成時と完全一致でないと使われない。たとえば date_trunc(...) と (sold_at AT TIME ZONE 'UTC')::date は見た目似ていても異なる式扱いでインデックスが使われない。  
  対策：
  1) ビューを作って共通の式を提供する（ただしユーザーが直接テーブルを叩くと無効）。  
     ```sql
     -- SQL
     CREATE VIEW v_sale AS
       SELECT *, date_trunc('day', sold_at AT TIME ZONE 'UTC')::date AS sold_at_date
       FROM sale;
     ```
  2) 生成列（generated column）を使う（PostgreSQL の生成列機能で式を列として持たせられる）。生成列にインデックスを貼れば、式の揺らぎに強く、利用者のミスでインデックスが無効になるリスクを下げられる。

## 実践ポイント
- まずは EXPLAIN (ANALYZE, BUFFERS) で実行計画を確認し、何がボトルネックかを把握する。
- constraint_exclusion は全体オンは避け、BI/分析セッションやデータウェアハウスでのみ有効化する。セッション設定や接続プールのプロファイルで切り替えると安全。  
  ```sql
  -- SQL
  SET constraint_exclusion = 'on'; -- 分析セッションだけ
  ```
- 集計の粒度に合わせてインデックス設計をする（日時なら日単位での関数インデックス）。インデックス容量は運用コストに直結するため、サイズを必ず確認する（\di+ など）。
- 関数ベースのインデックスは「式の一致」が必要。利用者ミスを防ぐために、ビューや生成列を使ってクエリ側を統一する運用ルールを作る。
- 変更を加えたら必ずベンチマーク（EXPLAIN/ANALYZE）とモニタリングで効果を確認。特にクラウド環境ではストレージ・IOの削減がコストに直結する。

短いまとめ：単純にインデックスを貼る前に「本当にその粒度が必要か」「クエリの書き方でインデックスが活きるか」を考え、チェック制約と生成列を使ってミスとコストを防ぐのが現場で効くテクニック。
