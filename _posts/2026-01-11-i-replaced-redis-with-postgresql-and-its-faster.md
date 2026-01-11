---
layout: post
title: "I Replaced Redis with PostgreSQL (And It's Faster) - RedisをPostgreSQLに置き換えた（しかも高速だった）"
date: 2026-01-11T11:17:47.389Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/polliog/i-replaced-redis-with-postgresql-and-its-faster-4942"
source_title: "I Replaced Redis with PostgreSQL (And It&#39;s Faster) - DEV Community"
source_id: 791575009
excerpt: "UNLOGGEDやLISTENなどでRedisをPostgresに置換し高速化、運用簡素化した事例"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fbar9z799eq8gj2v3kot2.jpg"
---

# I Replaced Redis with PostgreSQL (And It's Faster) - RedisをPostgreSQLに置き換えた（しかも高速だった）
クリックしたくなる見出し: 「RedisをやめてPostgres一本にしたらインフラも速さもスッキリした話」

## 要約
PostgreSQLの機能（UNLOGGEDテーブル、LISTEN/NOTIFY、FOR UPDATE SKIP LOCKED、JSONBなど）を使うことで、キャッシュ・Pub/Sub・ジョブキュー・セッション管理・レート制限といったRedisの役割の多くをPostgresだけで代替でき、運用負荷とコストを下げつつ実運用で十分な性能が出せたという事例です。

## この記事を読むべき理由
日本のスタートアップや中小SIでも「運用工数・コスト・データ整合性」に悩むケースは多いはず。Redisを別途管理する代わりに既存のPostgresを賢く使う選択肢を知っておくと、コスト削減・障害耐性・開発の単純化につながります。

## 詳細解説
以下は著者がRedisでやっていた主な用途と、Postgresでの代替手法の概要です。

- キャッシュ（70%程度の利用）
  - PostgresのUNLOGGEDテーブルをキャッシュ領域に使うと、WALを書かない分高速で、クラッシュ時にデータ消失しても問題ない用途に合います。
  - 例（SQL）:
```sql
-- sql
CREATE UNLOGGED TABLE cache (
  key TEXT PRIMARY KEY,
  value JSONB NOT NULL,
  expires_at TIMESTAMPTZ NOT NULL
);
CREATE INDEX idx_cache_expires ON cache (expires_at);

INSERT INTO cache (key, value, expires_at)
VALUES ($1, $2, NOW() + INTERVAL '1 hour')
ON CONFLICT (key) DO UPDATE
  SET value = EXCLUDED.value, expires_at = EXCLUDED.expires_at;

SELECT value FROM cache WHERE key = $1 AND expires_at > NOW();
```

- Pub/Sub（20%程度の利用）
  - PostgresのLISTEN/NOTIFYを利用。遅延はRedisより若干大きいが、同一トランザクション内で発行できる利点があります。トリガーでINSERTと同時に通知することで原子性を確保できます。
  - 例（トリガー＋通知）:
```sql
-- sql
CREATE FUNCTION notify_new_log() RETURNS trigger AS $$
BEGIN
  PERFORM pg_notify('logs_new', row_to_json(NEW)::text);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER log_inserted
AFTER INSERT ON logs
FOR EACH ROW EXECUTE FUNCTION notify_new_log();
```
```javascript
// javascript
const client = new Client({ connectionString: process.env.DATABASE_URL });
await client.connect();
await client.query('LISTEN logs_new');
client.on('notification', msg => {
  const payload = JSON.parse(msg.payload);
  console.log(payload);
});
```

- ジョブキュー（10%程度の利用）
  - FOR UPDATE SKIP LOCKED を使えば複数ワーカーが安全にジョブを取り出せます。Redisのキューに比べ若干遅いが実務上は十分。
  - 例（ジョブ取得）:
```sql
-- sql
WITH next_job AS (
  SELECT id FROM jobs
  WHERE queue = $1 AND attempts < max_attempts AND scheduled_at <= NOW()
  ORDER BY scheduled_at
  LIMIT 1
  FOR UPDATE SKIP LOCKED
)
UPDATE jobs SET attempts = attempts + 1
FROM next_job
WHERE jobs.id = next_job.id
RETURNING *;
```

- レート制限、セッション、JSON検索
  - JSONBでセッションや複雑な条件検索が可能。トランザクション内でビジネスロジックと一緒に扱えるのが強みです。

著者のベンチマーク（小規模RDS環境）では、単発のRedis操作はPostgresより速いが、複数操作を組み合わせると「同じコネクション内で完結するPostgres」が総合的に有利になったと報告しています。具体的には、挿入＋キャッシュ削除＋通知の複合操作でPostgresが速かった、という点が「実務での勝ち筋」です。

いつRedisを残すべきか
- 毫秒未満で大量（数百万ops/s）をさばく必要がある場合はRedis継続
- Redis独自データ構造（sorted sets, HyperLogLog, Streams, geospatial）を活用するケースはRedis向き
- マイクロサービスで明確に独立したキャッシュ層が必要な設計の場合はRedisを残す

## 実践ポイント
- 小〜中規模プロジェクトでの判断基準
  1. 既にPostgresを運用していて、Redisのコスト・運用負荷を減らしたいなら試す価値あり。
  2. Redisをトラブル要因にしている（バックアップやフェイルオーバが複雑）なら段階的移行を推奨。

- 移行の段階的手順（事例）
  1. 並行書き込み（Write to both）で差分を観察する（1週間ほど）。
  2. 読みをPostgres優先にして、問題がなければRedisをフェールバックとして残す（次週）。
  3. 問題なければRedisを縮小・廃止。

- すぐ試せる実装アイデア
  - キャッシュ：UNLOGGEDテーブル＋expires_at索引でTTL管理
  - リアルタイム通知：テーブルトリガー→pg_notify→アプリでLISTEN
  - ジョブキュー：jobsテーブル＋FOR UPDATE SKIP LOCKED
  - セッション：id主キー＋JSONBで内部検索を可能に

短い結論：Redisをゼロにするのが万能解ではないが、多くの現場でPostgresだけで十分代替でき、運用と整合性の面で明確な利点が得られるケースがある。まずは段階的検証から。
