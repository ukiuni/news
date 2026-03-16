---
layout: post
title: "How to implement the Outbox pattern in Go and Postgres - GoとPostgresでOutboxパターンを実装する方法"
date: 2026-03-16T11:24:36.275Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://packagemain.tech/p/how-to-implement-the-outbox-pattern-in-golang"
source_title: "How to implement the Outbox pattern in Go and Postgres"
source_id: 382623850
excerpt: "GoとPostgresでトランザクション内にイベントを確実保存し、確実配信するOutbox実践ガイド"
image: "https://substackcdn.com/image/fetch/$s_!oUje!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F09503238-02cd-4d09-9b82-ed02d0f3a853_2912x2096.png"
---

# How to implement the Outbox pattern in Go and Postgres - GoとPostgresでOutboxパターンを実装する方法
クリックせずにはいられない！トランザクションで「確実に通知」を実現するOutboxパターン入門

## 要約
データベースへの変更とイベント送信を同一トランザクションで扱うOutboxパターンを、Go + Postgresの実例と運用上のポイントでわかりやすく解説します。

## この記事を読むべき理由
非同期イベントとDB更新の不整合は分散システムで頻出の致命課題。日本のプロダクト（オンプレ/クラウド問わず）でも高可用性・監査要件を満たすために役立つ実践手法です。

## 詳細解説
- 問題の本質：サービスがDBにコミットしたがメッセージブローカーへ送れないとシステム全体が不整合に陥る。DB更新とメッセージ送信は原子性を持たないため発生する。
- Outboxパターンの核：イベントを直接ブローカーへ送る代わりに、同一トランザクション内で「outbox」テーブルにイベントを記録する。こうすることでビジネスデータとイベントどちらも保存されるかどちらも失われるかの二択になり、メッセージの喪失を防げる。
- 典型的なOutboxスキーマ（例）：

```sql
-- SQL
CREATE TABLE outbox (
  id UUID PRIMARY KEY,
  topic TEXT NOT NULL,
  message JSONB NOT NULL,
  state TEXT NOT NULL DEFAULT 'pending',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  processed_at TIMESTAMPTZ
);
```

- メッセージ中継（Relay）：
  - バックグラウンドワーカーがoutboxから未処理行を取得し、外部ブローカーに送信する。
  - Postgres側で同時実行を安全にするには FOR UPDATE SKIP LOCKED を使い、複数インスタンスが競合しないようにする。
  - 送信確認後にoutbox行を processed に更新する。更新が失敗すると二重送信の可能性があるため、コンシューマ側は必ず冪等にする（at-least-once 配達保証）。
- 実装上のポイント（Go/pgx/GCP Pub/Sub等でよく使われる流れ）：
  1. ビジネス操作とoutboxへのINSERTを同一トランザクションで実行。
  2. Relayは間欠ポーリングまたはプッシュ方式で未処理イベントを取り出し、ブローカーへPublish。
  3. 成功時にoutboxの状態を更新、失敗時はリトライ／エラーハンドリング。
- 代替案：Postgresの論理レプリケーション（WALを読んでpushする）を使えばポーリングを減らせるが、実装はやや複雑。Go向けには pglogrepl 等のライブラリがある。

## 実践ポイント
- まずはシンプルなポーリング型のRelayで運用を始め、負荷やレイテンシ要件に応じて論理レプリケーションへ移行検討する。
- メッセージ処理は必ず冪等設計にする（同一イベントの再処理で副作用が起きない）。
- FOR UPDATE SKIP LOCKED をRelayで使い、スケールアウト時のロック競合を回避する。
- outboxテーブルのライフサイクル（古い行の削除やアーカイブ）を定め、運用監視を入れる。
- 日本のオンプレ環境や主要クラウド（GCP/AWS/Azure）での運用差を把握し、ネットワーク障害やメンテ時のリカバリ手順を明確にしておく。

以上を押さえれば、Go + Postgres環境で堅牢かつ現実的なイベント駆動アーキテクチャを構築できます。
