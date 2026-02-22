---
layout: post
title: "Postgres Is Your Friend. ORM Is Not - Postgresは頼れる相棒、ORMは必ずしも正解ではない"
date: 2026-02-22T13:35:53.289Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://hypha.pub/postgres-is-your-friend-orm-is-not"
source_title: "Postgres Is Your Friend. ORM Is Not"
source_id: 47110310
excerpt: "ORM依存を減らしPostgres(JSONB/pg_trgm)で運用負荷を激減"
---

# Postgres Is Your Friend. ORM Is Not - Postgresは頼れる相棒、ORMは必ずしも正解ではない
ORMに頼らずPostgresをフル活用する現場の実践ガイド

## 要約
Postgresは単なるRDBMS以上の強力なエコシステムで、JSONBや全文検索、パーティショニング、LISTEN/NOTIFY＋FOR UPDATE SKIP LOCKEDといった機能を使えば、Elasticsearchやメッセージキューなしで多くの要件を満たせる。ORMは便利だが隠れた副作用（N+1、意図しないflush、キャッシュ問題）があり、リポジトリ層で素直なSQLを書く方が安全で効率的という主張。

## この記事を読むべき理由
日本のスタートアップや中小チームは「運用コストを抑えつつ安定を得たい」ケースが多い。Postgresを正しく使えばサービスの複雑度とインフラ負荷を劇的に下げられるため、実務で役立つテクニックを短時間で学べる。

## 詳細解説
- JSONBとインデックス：PostgresはJSONBをネイティブに扱い、GIN等で効率的に検索できる。スキーマレスな属性をDB内に保ちつつ高速検索を実現可能。
```sql
CREATE TABLE videos (
  id UUID PRIMARY KEY,
  metadata JSONB
);
CREATE INDEX idx_videos_tags_gin ON videos USING GIN ((metadata->'tags') jsonb_path_ops);
SELECT * FROM videos WHERE metadata->'tags' @> '["personal"]';
```

- 簡易全文検索：pg_trgm拡張で中くらいの規模ならElasticsearch不要。タイトル類似検索やLIKEより高速な類似度検索が可能。
```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_videos_title_trgm ON videos USING GIN (lower(title) gin_trgm_ops);
SELECT * FROM videos WHERE title ILIKE '%' || $1 || '%' OR similarity(title, $1) > 0.12;
```

- パーティショニングと運用自動化：pg_partman等で定期的なパーティション作成や保持期間管理を自動化できる。

- 軽量なワークキュー：LISTEN/NOTIFY + FOR UPDATE SKIP LOCKEDの組合せで、外部キュー不要の堅牢な分散ワーカーが作れる。通知でワーカーを起動し、短命なトランザクションで行ロックして安全に処理する設計が可能。
```sql
-- シンプルなロック付き取得
SELECT * FROM tasks WHERE id = $1 AND state = 'PENDING' FOR UPDATE SKIP LOCKED;
```
Python側は長期接続で通知を受け、短期接続でロックして処理する流れにするだけでスケールする。

- ORMの落とし穴：ORMは双方向マッピング、オブジェクト同一性、フラッシュや内部キャッシュなどを提供するが、その分、予期せぬSQLやN+1、覆い隠された副作用を生む。複雑なクエリや複数テーブルにまたがる集約を扱うとき、ORMの抽象が邪魔になることがある。

- リポジトリ＋生SQLの勧め：集約の永続化・復元はリポジトリに任せ、プレーンなSQL（ドライバのプレースホルダを使った安全な実行）で書く方が可読性・パフォーマンス・デバッグ性で有利。複数テーブルにまたがる保存や「traits」的なスキーマレス保存も素直に表現できる。

## 実践ポイント
- まずはSQLを学ぶ：複雑なクエリやインデックス設計はSQLで最短。ORMに頼る前にSQLを書けるようになる。
- JSONB＋GINでスキーマレスデータを高速化：属性検索が必要ならjsonb_path_opsや適切な式インデックスを作る。
- pg_trgmで中規模の全文検索を代替：まずは運用コストの低いPostgresで試す。
- LISTEN/NOTIFY + FOR UPDATE SKIP LOCKEDで軽量キューを構築：小〜中規模なら外部メッセージシステム不要。
- ORMは全面否定しないが、リポジトリ境界では「生SQLで明示的にやる」方針を採る。テストしやすくバグの発見も早い。
- 必要になったら専用ツールを追加：スループットや配信保証の要件が高くなったらKafka等を検討する。

短く言えば、まずはPostgresを深く知り、試してみること。多くのケースで「余計なミドルウェア」を減らし、運用性と開発体験を改善できる。
