---
layout: post
title: "What Is a Database Transaction? - データベーストランザクションとは？"
date: 2026-02-22T13:36:40.191Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://planetscale.com/blog/database-transactions"
source_title: "Database Transactions — PlanetScale"
source_id: 47110473
excerpt: "PostgresとMySQLの違いとリトライ設計を図解で学ぶトランザクション入門"
image: "https://planetscale.com/assets/database-transactions-social-C4_q_qA5.png"
---

# What Is a Database Transaction? - データベーストランザクションとは？
クリックせずにはいられない！「トランザクション」がアプリの信頼性を支える仕組みを図でスッキリ解説

## 要約
トランザクションは「一連の操作を1つの原子処理として扱う仕組み」で、コミットで確定、ロールバックで取り消しを行うことでデータ整合性を守る。PostgresはMVCC（行の多重版）で、MySQLはundoログで一貫した読み取りを実現する。

## この記事を読むべき理由
日本のサービス（決済、EC、業務系SaaSなど）はデータ整合性が命。どのDBを選び、どの分離レベルを使い、アプリ側でどうリトライ設計するかは運用コストと信頼性に直結します。トランザクションの内部動作を知れば、正しい設計判断ができます。

## 詳細解説
- トランザクションの基本
  - begin / commit / rollback によって、複数の読み書き操作を「全体として成功するか失敗するか」の単位にする。
  - commit が成功すると変更が一括適用、rollback は途中の変更を全て無かったことにする。

- 一貫した読み取り（Consistent Reads）
  - トランザクションは自分専用の一貫したデータビューを得る（他のトランザクションの未コミット変更は見えない）。
  - Postgres：MVCC（Multi-Version Concurrency Control）
    - 更新ごとに新しい行バージョンを作成し、各バージョンに xmin/xmax でどのトランザクションが見られるかを管理する。
    - 不要になった古いバージョンは VACUUM（自動/手動）で回収される。
  - MySQL（InnoDB）：undoログ方式
    - 行データを上書きし、過去の値はundoログに残して必要に応じて復元して見せる。

- 分離レベル（Isolation Levels）
  - 強い順に：Serializable > Repeatable Read > Read Committed > Read Uncommitted
  - 許容される問題例
    - Dirty read（未コミットデータの読み取り） — Read Uncommitted が許す
    - Non-repeatable read（同じ行の再読で値が変わる） — Read Committed が許す
    - Phantom read（同じクエリ結果に行の出入りがある） — Repeatable Read では標準的に許されるが、Postgresの実装では防ぐ場合あり
  - トレードオフ：強い分離は安全だがスループット/待ち時間に影響する

- 競合書き込み（Concurrent Writes）
  - MySQL（InnoDB）：行レベルロック（共有ロックS／排他ロックX）で衝突を回避。デッドロックが起きたらDBが一方を殺してロールバックするため、アプリでリトライが必要。
  - Postgres（Serializable Snapshot Isolation）
    - 楽観的制御に近く、predicate lock（範囲や条件に基づくロック）で衝突を検出し、違反があればトランザクションを中止（再試行が必要）。
  - どちらも重要な処理は「失敗したらリトライ」設計が必須。

## 実践ポイント
- トランザクション設計
  - 重要処理（決済・残高更新など）は高い分離レベルで短時間に実行する。長時間トランザクションは避ける。
- エラーハンドリング
  - デッドロックやシリアライザブル違反に備え、明確なリトライ戦略（指数バックオフ＋最大試行回数）を実装する。
- DB選定・運用
  - 読み取り一貫性を重視するなら Postgres（MVCC＋VACUUMの理解が必要）、運用の簡便さや既存互換性重視ならMySQL系を検討。
  - PostgreSQLでは autovacuum を監視、MySQLでは undoログサイズや長期トランザクションに注意。
- 日本市場の留意点
  - 金融・医療など規制分野では強い整合性を優先。ECや分析は性能重視で分離レベルを緩める選択肢も検討可能。
- テスト
  - 並列テストを自動化して、リアルな競合・デッドロック・分離違反を検出する。

以上を押さえれば、トランザクション設計の基本とDBごとの違いを理解し、運用で起きがちな落とし穴を回避できます。
