---
layout: post
title: "Test your PostgreSQL database like a sorcerer - PostgreSQLを魔術師のようにテストする"
date: 2026-02-17T02:54:01.969Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://docs.spawn.dev/blog/regression-tests/"
source_title: "Test your PostgreSQL database like a sorcerer | Spawn"
source_id: 439855326
excerpt: "Spawnでgolden fileとテンプレDBでPostgres回帰テストを簡単自動化"
---

# Test your PostgreSQL database like a sorcerer - PostgreSQLを魔術師のようにテストする
PostgreSQLのテストが劇的にラクになる！Spawnで「golden file」方式＋テンプレDBコピーを使った再現性の高いDBテスト入門

## 要約
Spawnを使えば、psql経由で実行したSQLのstdout/stderrを「golden file」と比較することで、PostgreSQLの回帰テストを簡単に自動化できます。テンプレートDB（WITH TEMPLATE）やminijinjaマクロ／JSONフィクスチャで使い回し可能な、再現性の高いテストを作れます。

## この記事を読むべき理由
DBのスキーマ変更やマイグレーションでの破壊的なバグは致命的です。日本でもPostgres採用は多く、Spawnのような軽量・拡張不要でpsqlベースのテスト手法はCI導入やデータ互換性確認に即役立ちます。

## 詳細解説
- 基本概念  
  - Spawnはpsqlに接続してSQLを実行し、その標準出力を「期待値ファイル（golden）」と比較するテストフレームワーク。拡張不要でCLIだけで動きます。  
  - ワークフロー：spawn test new → spawn test run／build → spawn test expect（期待値記録）→ spawn test compare（差分検出）。

- 主要コマンド（例）  
  ```bash
  # テスト作成／実行／期待値登録／比較
  spawn test new check-order-creation
  spawn test run check-order-creation
  spawn test expect check-order-creation
  spawn test compare check-order-creation
  ```

- 再現性を作る方法  
  - WITH TEMPLATEを使い、あらかじめ用意したベースDB（例: regression）を複製して各テストごとにクリーンなDBを作る。トランザクションでのロールバックでは不可能な操作（CREATE DATABASE 等）やコミット含む振る舞いの検証に強い。  
  - 利用例（要約）：
    ```sql
    DROP DATABASE IF EXISTS check_order_creation_test;
    CREATE DATABASE check_order_creation_test WITH TEMPLATE regression;
    \c check_order_creation_test;
    -- テスト用SQL実行...
    \c postgres;
    DROP DATABASE IF EXISTS check_order_creation_test;
    ```

- テンプレート／フィクスチャで再利用性アップ  
  - Spawnはminijinjaテンプレートを使える。マクロでINSERT文を生成したり、JSONフィクスチャを読み込んで一括投入することで、複数テスト間で同一データセットを共有可能。  
  - 重要な書き方例（抜粋）：
    ```sql
    {% macro create_item(name, item_id="default"|safe, quantity_on_hand=1, price=1.23) %}
    INSERT INTO item (item_id, name, quantity_on_hand, price)
    VALUES ({{item_id}}, {{name}}, {{quantity_on_hand}}, {{price}});
    {% endmacro %}
    ```
    safeフィルタでSQLキーワード（defaultなど）をそのまま出力。

- 実践的注意点  
  - WITH TEMPLATEはコピー元DBに接続が残っていると失敗する（\c postgres などで切り替え要）。  
  - 非決定的出力（タイムスタンプや順序の変動）はgoldenテストで差分を生むので、テストでは正規化（ORDER BY／形式固定）や差分除外の工夫が必要。

- 追加の機能例（記事が扱う応用）  
  - 複合型や関数（create_order）・トリガで在庫を更新する実用的なロジックをベースDBに入れ、関数の動作やトリガの副作用まで検証できる。

## 実践ポイント
- まずはローカルでspawn init --dockerして、spawn test run → expect → compareの流れを体験する。  
- ベースDB（regression）を用意して、WITH TEMPLATEでクリーンコピーを使うテストから始める。  
- 共通データはJSONフィクスチャ＋minijinjaマクロで管理すると、複数テストの整合性が保ちやすい。  
- CIにはspawn test compareを組み込み、goldenファイルの差分をPRでレビューする運用にすると安全。  
- 非決定要素（日時や順序）はSQL側で整形しておくこと。

短時間で導入でき、Postgresのマイグレーションや関数・トリガの回帰検証に強いアプローチです。まずは小さなテストを一つ作って、goldenファイルワークフローを試してみてください。
