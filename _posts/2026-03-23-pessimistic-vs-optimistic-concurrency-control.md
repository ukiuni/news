---
layout: post
title: "Pessimistic vs Optimistic Concurrency Control - 悲観的 vs 楽観的 並行制御"
date: 2026-03-23T01:21:17.947Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://pradyumnachippigiri.substack.com/p/concurrency-controls-pessimistic"
source_title: "Concurrency Controls : Pessimistic vs Optimistic"
source_id: 417807851
excerpt: "高負荷ECや決済向け、ロックと再試行の使い分けと実装の判断基準"
image: "https://substackcdn.com/image/fetch/$s_!OpjE!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcd3a6f3e-b28d-4bcd-82fb-c65a775cf4e7_1376x768.png"
---

# Pessimistic vs Optimistic Concurrency Control - 悲観的 vs 楽観的 並行制御
ロックで待つか、検出して再試行するか――現場で使える「並行制御」の選び方と注意点

## 要約
悲観的（Pessimistic）は事前にロックして衝突を防ぎ、楽観的（Optimistic）は衝突を後で検出して再試行する。ワークロード特性（高競合か低競合か）で使い分けるのが基本。

## この記事を読むべき理由
ECやチケット予約、在庫・決済システムなど日本のサービスでは同時更新が頻発する場面が多く、誤った並行制御はデータ不整合や性能劣化につながる。実務で即使える判断基準と実装ヒントを知ると役立ちます。

## 詳細解説
- 並行トランザクションで起きる代表的な異常：Dirty Read、Non-repeatable Read、Phantom Read、Lost Update。
- 基本手法
  - 共有ロック（S-Lock）: 読み取り中は複数許可するが、書き込みは不可。
  - 排他ロック（X-Lock）: 書き込み時に単独で保持。ほかの読書・書込をブロック。
- 悲観的（Pessimistic）
  - 考え方: 衝突は起きる前提で事前にロック。
  - 実装例: SQLのSELECT ... FOR UPDATEなどで行ロック。
  - 長所: 衝突を防ぐので再試行コストが高い業務（銀行等）に適する。
  - 短所: スループット低下、デッドロック、待ち時間増、ロック管理コスト。
- 楽観的（Optimistic）
  - 考え方: 衝突は稀と仮定し、コミット時にバージョン等で検出して失敗したら再試行。
  - 実装例: 行にversion/timestamp列を持ち、更新時にバージョン一致を条件にUPDATE。
  - 長所: 読み取り重視・低競合で高並列を活かせる。
  - 短所: 衝突多発時に無駄な処理とリトライ増、メタデータが必要。
- 実装の実例（参考）
  - 楽観的更新（versionチェック）
```sql
-- 読む
SELECT id, value, version FROM items WHERE id = 42;

-- 更新（バージョン一致を条件に）
UPDATE items
SET value = 'new', version = version + 1
WHERE id = 42 AND version = 3;
```
  - 悲観的ロック（Postgres等）
```sql
BEGIN;
SELECT * FROM items WHERE id = 42 FOR UPDATE;
-- 更新処理
COMMIT;
```

## 実践ポイント
- まず測る：競合率（衝突発生割合）を計測し、楽観的で許容できるか判断する（経験則：衝突が低数％なら楽観的が有利）。
- コストで選ぶ：リトライコストが高い処理（決済など）は悲観的が安全。
- 組み合わせ：読み取り多・書込み少は楽観的、書込み多・高整合性要件は悲観的。必要ならハイブリッド。
- 実装注意：楽観的はバージョン列／ETagを用意、指数バックオフでリトライ、悲観的はトランザクションを短くしてデッドロックを減らす。
- DB機能を活用：PostgresやMySQLのMVCCやトランザクション分離レベルも考慮して最適化する。

以上を踏まえ、まずは自分のサービスの「競合特性」と「リトライの許容度」を明確にして運用ルールを決めると効果的です。
