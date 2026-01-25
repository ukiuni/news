---
layout: post
title: "Using PostgreSQL as a Dead Letter Queue for Event-Driven Systems - イベント駆動システムでの Dead Letter Queue に PostgreSQL を使う"
date: 2026-01-25T16:44:39.953Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.diljitpr.net/blog-post-postgresql-dlq"
source_title: "Using PostgreSQL as a Dead Letter Queue for Event-Driven Systems — Blog"
source_id: 46755115
excerpt: "PostgreSQLをDLQ化して失敗イベントを可視化・安全に再試行"
---

# Using PostgreSQL as a Dead Letter Queue for Event-Driven Systems - イベント駆動システムでの Dead Letter Queue に PostgreSQL を使う
障害を“見える化”する実務テク：PostgreSQLをDLQにして日次レポートパイプラインを安定化させる方法

## 要約
イベント処理で失敗したメッセージをKafka上の別トピックに投げる代わりに、PostgreSQLのテーブルに保存して可視化・再試行を行う手法を紹介する。可観測性と運用性が大幅に向上する。

## この記事を読むべき理由
日本のエンタープライズ環境でも、Kafka＋ダウンストリーム呼び出しで日次レポート等を作る構成は一般的。失敗時の扱いで運用負荷が増える課題を、既存のCloud SQL（Postgres）で低コストに解決できる実践的手法だから必読。

## 詳細解説
- 問題点：KafkaをDLQにすると「なぜ・どれが失敗したか」を調べにくく、特定イベントの再処理や障害傾向分析が面倒。  
- 解決策：失敗イベントをPostgreSQLのDLQテーブルに格納し、失敗理由・ペイロード・状態を明示的に保持することでクエリや再処理を容易にする。  
- 状態管理：status（PENDING / SUCCEEDED）、retry_count、retry_after を持たせることで再試行ロジックをDB内で追えるようにする。payload は JSONB にしてスキーマ固定を強制しない。  
- 再試行設計：スケジューラは定期実行で PENDING かつ retry_after <= now() の行をバッチで取得し再処理。複数インスタンス環境では ShedLock（あるいは DB のロック機構）を使い単一実行を保証。行選択には FOR UPDATE SKIP LOCKED を利用して重複処理を防ぐ。  
- 運用効果：SQLで直接検索・集計・フィルタができ、問題パターンの把握や限定的再処理が容易になる。ダウンストリームが長期停止しても再試行ポリシーで安全に待機可能。

代表的なDLQテーブル例（要点を抽出）
```sql
CREATE TABLE dlq_events (
  id BIGSERIAL PRIMARY KEY,
  event_type VARCHAR(255) NOT NULL,
  payload JSONB NOT NULL,
  error_reason TEXT NOT NULL,
  error_stacktrace TEXT,
  status VARCHAR(20) NOT NULL, -- 'PENDING' / 'SUCCEEDED'
  retry_count INT NOT NULL DEFAULT 0,
  retry_after TIMESTAMPTZ NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_dlq_status ON dlq_events (status);
CREATE INDEX idx_dlq_status_retry_after ON dlq_events (status, retry_after);
CREATE INDEX idx_dlq_event_type ON dlq_events (event_type);
CREATE INDEX idx_dlq_created_at ON dlq_events (created_at);
```

再試行時の安全な行選択例（概念）
```sql
SELECT * FROM dlq_events
WHERE status = 'PENDING' AND retry_after <= now()
ORDER BY created_at
LIMIT 50
FOR UPDATE SKIP LOCKED;
```

## 実践ポイント
- payload は JSONB にして元データを丸ごと保存。スキーマ変化に強い。  
- status / retry_count / retry_after を必須にして再試行ライフサイクルをDBで追跡。  
- インデックスは (status), (status, retry_after), (created_at) を最低限用意してスケジューラの性能を確保。  
- 再試行はバッチ／固定間隔（例：6時間）で、max-retries を設ける。  
- マルチインスタンスでは FOR UPDATE SKIP LOCKED と ShedLock 相当で重複処理を防止。  
- 運用用SQLビューや簡易管理UIを用意して、データサイエンスやSREが原因分析・選択再処理できるようにする。  

このアプローチはKafkaを置き換えるものではなく、「移動はKafka、失敗の可視化と再試行はPostgres」という役割分担でシステム全体の堅牢性と運用効率を高める実務向けパターンである。
