---
  layout: post
  title: "PostgreSQL Scripting Tips - PostgreSQL スクリプティングのヒント"
  date: 2026-01-06T19:59:17.769Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://www.pgrs.net/2026/01/06/postgresql-scripting-tips/"
  source_title: "PostgreSQL Scripting Tips - Paul Gross’s Blog"
  source_id: 469412797
  excerpt: "psqlの\gset/\crosstabview/--echo-allで台帳処理を再現・可視化"
---

# PostgreSQL Scripting Tips - PostgreSQL スクリプティングのヒント
psqlで簡潔・再現性の高いSQLスクリプトを書くための実践テクニック3選（pgledgerの実例付き）

## 要約
psqlの便利コマンド（\gset、\crosstabview、--echo-all）を使うと、ランダムIDを扱うスクリプトの再現性、台帳データの可視化、入力＋出力の一括記録が簡潔にできる。

## この記事を読むべき理由
日本でも金融系や決済周りのサービス開発でPostgreSQLを直接操作する機会が増えています。開発・デバッグ・ドキュメント作成の手間を減らし、チームで共有可能な「実行できるサンプル」を簡単に作る方法は即戦力になります。

## 詳細解説
- \gset：クエリ結果をpsqlの変数に格納して、後続のSQLで参照可能にする。pgledgerのように各呼び出しでランダムなIDが返る場合、スクリプト内で変数化すると静的なシーケンスで処理できる。
  - 例：アカウント作成で返るidを保持して利用する
```sql
-- sql
SELECT id FROM pgledger_create_account('user1.external','USD') \gset
-- 以降は :'id' で参照可能
SELECT :'id';
```
  - プレフィックスやASで変数名を整えれば複数の値を扱いやすくなる。

- \crosstabview：行ベースの複数エントリを列に展開して「転置」表示する。台帳のトランスファごとに複数行になる出力を、人間が読みやすい「1転送＝1行、口座ごとに列」形式で確認できる。
```sql
-- sql
SELECT e.transfer_id, a.name, e.amount
FROM pgledger_entries_view e
JOIN pgledger_accounts_view a ON e.account_id = a.id
WHERE e.metadata->>'payment_id' = 'p_123'
ORDER BY e.transfer_id \crosstabview
```

- --echo-all：SQLファイルとその実行結果を同一ファイルに残す。ドキュメントとして配布したり、チュートリアルにする際に有用。
```bash
# bash
psql -f basic-example.sql --echo-all > basic-example.sql.out
```

これらは独立したテクニックなので、必要に応じて組み合わせて使える。pgledgerの例ではこれらを組み合わせることで「再現可能なサンプル」や「人が読めるログ」を簡単に作れている。

## 実践ポイント
- テストデータやCIでランダムIDを扱うなら、\gsetでIDを変数化してスクリプトを決定的にする。
- 台帳や会計データはそのままだと行が重複して読みにくい。調査時は\crosstabviewで転置してアカウント横並びで確認する習慣をつける。
- ドキュメントやサンプル配布にはpsqlの--echo-allで「入力＋出力」を一つの.outファイルにしておくとレビュー／教育で便利。
- チームではpsqlプロファイル（.psqlrc）やjustfile／Makefileでこれらを再利用可能にすると作業効率が上がる。

必要なら、上の例を元に日本向けの具体的なスクリプト（pgledgerを想定）を作成しますか？
