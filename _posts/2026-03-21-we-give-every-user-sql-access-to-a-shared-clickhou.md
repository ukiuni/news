---
layout: post
title: "We give every user SQL access to a shared ClickHouse cluster - すべてのユーザーに共有ClickHouseクラスタへのSQLアクセスを提供する方法"
date: 2026-03-21T12:18:29.383Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://trigger.dev/blog/how-trql-works"
source_title: "How we give every user SQL access to a shared ClickHouse cluster | Trigger.dev"
source_id: 47414356
excerpt: "言語とコンパイルでTRQLが共有ClickHouseを安全に隔離し高速分析を実現"
image: "https://trigger.dev/blog/how-trql-works/how-trql-works.png"
---

# We give every user SQL access to a shared ClickHouse cluster - すべてのユーザーに共有ClickHouseクラスタへのSQLアクセスを提供する方法
誰でも安全にSQLが叩ける！Trigger.devが作ったTRQLの秘密

## 要約
Trigger.devはTRQLというSQL風DSLを作り、ユーザーが共有ClickHouseクラスターに対して安全かつ隔離された形でクエリを投げられる仕組みを実現した。言語設計とコンパイルパイプラインでセキュリティ、テナント分離、内部実装の抽象化を強制している。

## この記事を読むべき理由
マルチテナントの分析基盤を提供するSaaSや内部ダッシュボードは、ユーザーに自由度を与えつつもデータ漏洩やクラスタ障害を防がねばならない。日本でサービスを運営するエンジニアにとって、TRQLのアプローチは実用的な設計パターンと実装の教科書になる。

## 詳細解説
- なぜDSL（TRQL）か  
  - 文法を自前で定義することで、DELETE/UPDATE/管理コマンドなど危険な操作を「そもそも言語として存在させない」＝セキュリティを構文レベルで担保。  
  - ユーザー側でWHEREに組織フィルタを書かせるのではなく、コンパイラが必ず注入してテナント分離を徹底。  
  - 内部のテーブル名や列名、複雑な計算を隠してユーザー向けの安定APIを提供（例：runs.total_cost → 実際は cost_in_cents + base_cost_in_cents の変換）。

- なぜClickHouseか  
  - 列志向ストレージ、巨大データでの高速集計、豊富な分析関数。分析用途に最適。

- パーサーにANTLRを採用  
  - 文法定義からLexer/Parserを生成し、抽象構文木（AST）で以降の処理を厳密に行う。結果として危険な構文はそもそもパース不可。

- コンパイルパイプライン（ASTベース）  
  1. Parse：ANTLRでAST生成（文法外はエラー）。  
  2. Schema validation：参照テーブル/列/関数／型チェック。  
  3. Tenant isolation：organization_id 等のフィルタをASTに注入（オプトアウト不可）。  
  4. Time restrictions：無制限スキャン防止の時間境界を追加。  
  5. Parameterize values：リテラルはパラメータ化してSQLインジェクション防止。  
  6. Generate ClickHouse SQL：仮想列展開、テーブル名翻訳、TRQL特有関数の変換。  
  7. Execute/Return：読み取り専用レプリカで実行し、結果＋列メタデータを返す。

- 実例（要点のみ）  
  - TRQL: `SELECT task_identifier, SUM(total_cost) AS cost FROM runs GROUP BY task_identifier`  
  - 生成されたClickHouseクエリでは total_cost が `(cost_in_cents + base_cost_in_cents) / 100.0` に展開され、`trigger_dev.task_runs_v2 AS runs FINAL` のように内部名に翻訳、`equals(runs.organization_id, {tsql_val_0})` とタイムフィルタが自動追加される。パラメータ化で値は別送。

- スキーマ層の工夫  
  - 仮想列（virtual columns）：ユーザー向けの列を式で定義し、コンパイラで展開。  
  - 列名マッピング：内部名の変更に対する互換性を維持。  
  - 値変換（whereTransform）：IDプレフィックス剥ぎ取り等、境界での変換を自動化。  
  - 列メタデータ：UI表示（時間表示、通貨、リンクなど）情報を返してレンダリングを簡単に。

## 実践ポイント
- マルチテナント分析を提供するなら、言語レイヤで禁止構文を作る（ANTLRなどを検討）。  
- テナントフィルタはクライアント任せにせずコンパイラ／中間層で必ず注入する（強制ルール）。  
- 仮想列・値変換で内部スキーマを隠し、ユーザーAPIを安定化する。  
- リテラルは必ずパラメータ化し、時間範囲や行数制限で無駄なフルスキャンを防ぐ。  
- ClickHouseを使うなら、読み取り専用レプリカやFINAL等の運用オプションを活用して一貫性と性能を両立する。

（参考：Trigger.dev が TRQL と ClickHouse を組み合わせて、安全にマルチテナント向けSQLアクセスを提供した事例）
