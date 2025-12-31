---
layout: post
title: "End-to-End Static Type Checking: PostgreSQL to TypeScript | NpgsqlRest - PostgreSQLからTypeScriptまで：エンドツーエンド静的型検査（NpgsqlRest）"
date: 2025-12-31T15:40:49.547Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://npgsqlrest.github.io/blog/end-to-end-static-type-checking-postgresql-typescript.html"
source_title: "End-to-End Static Type Checking: PostgreSQL to TypeScript | NpgsqlRest"
source_id: 474421490
excerpt: "PostgreSQL関数を型の単一原典にしてTypeScriptを自動生成、DB変化をビルドで即検出"
---

# End-to-End Static Type Checking: PostgreSQL to TypeScript | NpgsqlRest - PostgreSQLからTypeScriptまで：エンドツーエンド静的型検査（NpgsqlRest）
魅力的なタイトル: データベースの変更でフロントが壊れる前にビルドを止める――PostgreSQL関数を「真の型の単一原典」にする実践ガイド

## 要約
PostgreSQLの関数定義を「型の単一原典」にして、NpgsqlRestで自動的にTypeScriptクライアントを生成すれば、DBスキーマ変更はTypeScriptのビルドエラーとして即座に検出できる。マイグレーション時に関数を再生成し、SQLレベルの型チェック＋組み込みアサーションで安全性を高めるワークフローを紹介する。

## この記事を読むべき理由
日本の開発現場では複数チームやレガシーAPIが混在しがちで、DBスキーマの変更がフロントエンドのランタイム障害につながるケースが多い。CIで早期に検出できればリリース品質が上がり、障害対応コストと顧客影響を大幅に削減できる。特に金融・決済・SaaSなど型の正確性が重要な分野で有益だ。

## 詳細解説
- 問題点の整理  
  伝統的なREST開発では型定義がデータベース → API層 → クライアントの複数箇所に散らばり、同期が取れないとランタイム障害を招く。

- なぜPostgreSQL関数か  
  PostgreSQL関数は明示的な戻り型を持ち、関数作成時にDB自身が返却型を検証する。業務ロジックをDBに寄せると「中央集権的なロジック」「パフォーマンス」「トランザクションの原子性」と並んで「静的型保証」を得られる。

- ワークフローの核心（Single Source of Truth）  
  PostgreSQL Function → NpgsqlRest → 生成されたTypeScript API Client → アプリケーション  
  関数シグネチャが変わればNpgsqlRestがTypeScriptインターフェースを再生成し、アプリ側のビルドが落ちる。

- 実装のポイント
  - マイグレーションファイル命名規約
    - R__...: スキーマ/テーブルを再作成する「繰り返し実行」マイグレーション
    - A__...: 関数を毎回再生成する「常に実行」マイグレーション（これが型検査を徹底する鍵）
  - 関数の戻り型
    - returns setof users → usersテーブル全列を返す契約
    - returns table(username text, ...) → 指定された列・型のみを返す契約
  - エンドポイント指定はコメントで（例: comment on function ... is 'HTTP GET'）でNpgsqlRestに公開指示
  - SQLレベルの検証：関数作成時に戻り型が一致しないとエラーで失敗する（マイグレーション段階で検出）
  - 組み込みアサーションとテスト：関数ファイル内に do $$ begin assert(...) end $$; を入れ、期待データや振る舞いをマイグレーション時に検証
  - テストの独立性：テストブロックで rollback; を使えば挿入データを巻き戻し、他テストに影響を与えない

- 変更伝播の流れ（例）
  1. DBでカラム名/型を変更
  2. A__マイグレーションが走り関数を再作成 → PostgreSQLで型ミスマッチがあれば失敗
  3. 関数更新が成功すればNpgsqlRestがTypeScript型を再生成
  4. TypeScriptコンパイルで不整合があればビルドエラー（即発見）
  5. アプリ側を修正して再ビルド

## 実践ポイント
- マイグレーション規約をルール化する：A__を関数定義に、R__をスキーマに割り当てる。
- すべての公開関数に戻り型を明示し、コメントでHTTPメソッドを付与してNpgsqlRestに接続。
- 各関数ファイルに最低1つのassertブロックを入れて「動作のガード」を作る。変更時に即座に失敗するため安心。
- rollbackを活用してテストの副作用を消す。CIでマイグレーションを実行し、失敗したら即止める設定にすること。
- NpgsqlRestで生成したTypeScriptクライアントはコミットせず、CIで毎回生成してコンパイルを通す運用にすると古い型の残存を防げる。
- 日本のチームでは、DB管理者とフロント/バックエンドの責任分担を明確化し、関数定義の変更はレビュープロセス（DBとAPI契約のレビュー）を必須にする。

## 引用元
- タイトル: End-to-End Static Type Checking: PostgreSQL to TypeScript | NpgsqlRest
- URL: https://npgsqlrest.github.io/blog/end-to-end-static-type-checking-postgresql-typescript.html
