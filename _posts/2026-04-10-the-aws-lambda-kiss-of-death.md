---
layout: post
title: "The AWS Lambda 'Kiss of Death' - AWS Lambda の「キス・オブ・デス」"
date: 2026-04-10T04:49:04.590Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://shatteredsilicon.net/the-aws-lambda-kiss-of-death/"
source_title: "The AWS Lambda &#039;Kiss of Death&#039; - Shattered Silicon"
source_id: 365732745
excerpt: "Lambdaの接続再利用がInnoDBのundo肥大でDBを凍結させる仕組みと即効対策"
image: "https://shatteredsilicon.net/wp-content/uploads/2026/04/image-1030x438.png"
---

# The AWS Lambda 'Kiss of Death' - AWS Lambda の「キス・オブ・デス」

魅力的なタイトル: Lambdaの接続再利用が招く「見えないトランザクション」問題 — 知らないとDBが止まる

## 要約
AWS Lambdaの接続再利用（プール）でトランザクションの「読み取りビュー」が長時間残り、InnoDBの履歴(undo)が増大してDBがフfreezeする問題の原因と対策を解説する。

## この記事を読むべき理由
日本でもLambda＋RDS/AuroraやMariaDB/Galeraを使う案件は増加中。サーバレス環境で突発的なDBフリーズに悩む開発・運用者は、原因特定と回避策を知っておくべきだ。

## 詳細解説
- 根本問題：InnoDBはMVCCで過去バージョン（undo）を保持する。古いバージョンは「パージ」されるが、あるトランザクションの読取ビュー(read view)が存在する間は削除できない。
- Lambdaの特徴：実行コンテナが再利用され、同じDB接続が複数リクエストで共有されると、「短いSELECTしかしていない」ように見えても接続上に読取ビューが残ったままアイドル化することがある。結果、undo履歴が肥大化（innodb_history_list_length上昇）し、書き込みが停滞する。
- Galera環境ではさらに悪化：InnoDB依存＋マルチマスターの差分解決で影響が大きくなる。
- 有効な対策（記事の発見点）：
  - セッション単位で transaction_isolation を READ-COMMITTED に設定すると、読取ビューが「ステートメント単位」になり長期に残らず、パージが追いつきやすくなる。
  - innodb_undo_log_truncate を ON にし、 innodb_max_undo_log_size を適切に制限することでディスク肥大と復旧負荷を抑えられる。
- 問題の確認方法：情報スキーマのトランザクション一覧や innodb_history_list_length を監視し、長時間のread viewや巨大なundoログを検出する。

## 実践ポイント
- まず監視：
  - innodb_history_list_length を監視アラートに追加する。
  - 長時間アイドルのトランザクションを確認 :
```sql
-- sql
SELECT * FROM information_schema.INNODB_TRX ORDER BY trx_started;
```
- Lambda側で接続確立直後にセッション変数を設定（接続プール毎に一度）：
```sql
-- sql
SET SESSION transaction_isolation='READ-COMMITTED';
```
- サーバ側設定検討：
  - innodb_undo_log_truncate=ON
  - innodb_max_undo_log_size=<適切な値>
- 運用ルール：Lambdaでトランザクションを開いたまま放置しない、短い処理は明示的にコミット/ロールバックする。
- 検証：変更はステージングで負荷をかけて履歴の増減とアプリ挙動を確認する。

短くまとめると、Lambda等での接続再利用は「見えない長期トランザクション」を作ることがあり、session isolation を READ-COMMITTED にすることが即効性の高い対策になる。
