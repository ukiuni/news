---
layout: post
title: "Show HN: PgDog – Scale Postgres without changing the app - PgDog を紹介 — アプリを変えずに Postgres をスケールする"
date: 2026-02-23T18:12:06.861Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/pgdogdev/pgdog"
source_title: "GitHub - pgdogdev/pgdog: PostgreSQL connection pooler, load balancer and database sharder."
source_id: 47123631
excerpt: "アプリ改修不要でPostgresを接続プーリング・読み書き分離・シャーディングでスケールするPgDog"
image: "https://opengraph.githubassets.com/62ef35cedc4adede0d527ab140b9eb16d0b815e557dfc85fcbfd97bf8b2ded32/pgdogdev/pgdog"
---

# Show HN: PgDog – Scale Postgres without changing the app - PgDog を紹介 — アプリを変えずに Postgres をスケールする

アプリ側の変更ゼロで、接続プーリング・読み書き分離・シャーディングを提供するPostgresプロキシ「PgDog」をわかりやすく紹介します。

## 要約
PgDog は Rust 製の Postgres プロキシで、接続プール、アプリ層のロードバランサ、シャーディング、フェイルオーバ管理を提供し、既存アプリを変えずにデータベースを大規模化できます。

## この記事を読むべき理由
日本でも RDS/Aurora や Kubernetes 上の Postgres を使う現場が増えています。アプリ改修なしでスケール戦略（読み/書き分離・シャード追加・高可用性）を導入したいエンジニアやSREにとって即戦力になるツールです。

## 詳細解説
- 実装と用途  
  - Rust 実装で高速かつ軽量。数千接続を低コストで捌けることを謳っています。  
  - 用途は「接続プール」「ロードバランス（アプリ層/L7）」「シャーディング」「フェイルオーバ監視」「単一エンドポイントによる讀寫振り分け」。

- 接続プーリング  
  - トランザクションプーリング／セッションプーリング対応。PgBouncer と同様に接続数を削減しつつ、SET 文や起動オプションを解析してセッション状態を正しく維持します。自動的なトランザクションロールバックや接続再同期機能も備えます。

- ロードバランサ（L7）  
  - Postgres プロトコルを理解してレプリカへトラフィックを振り分け（round-robin / random / least-active）。ヘルスチェックで不調ノードを除外します。

- 単一エンドポイントとクエリ解析  
  - pg_query を用いたネイティブパーサでクエリを解析し、書き込みは primary、読み取りは replica に振り分け可能。アプリは常に PgDog の一つのエンドポイントに接続できます。

- フェイルオーバ連携  
  - レプリカ昇格を検知して書き込み先を切替。Patroni やマネージド RDS と併用可能（PgDog はオーケストレーションは行わない点に注意）。

- シャーディング  
  - パーティション関数（HASH / LIST / RANGE）をそのまま採用し、スキーマ単位のシャーディングもサポート。シャードキーがあれば単一シャードへルーティング、キーがない/複数のシャードを跨ぐクエリは各シャードで実行して結果をアセンブルします。クロスシャードでは一部 SQL 機能に制約あり（CTE・サブクエリ非対応など。集計の一部は部分サポート）。

- トランザクション整合性と COPY  
  - 2PC を利用したクロスシャードの原子性サポート。COPY コマンドは行を分割して各シャードに振り分け可能。

- 運用と導入経路  
  - Docker / docker-compose、Kubernetes Helm chart、AWS（EKS / ECS + Terraform）向けモジュールあり。設定は pgdog.toml と users.toml を使います。

- 便利機能  
  - pgdog.unique_id() による時刻ベースの BIGINT 一意 ID 生成（シーケンス不要でシャード横断で重複なし）。

短い設定例:
```toml
# toml
[general]
port = 6432
default_pool_size = 10

[[databases]]
name = "pgdog"
host = "127.0.0.1"
```

```sql
-- sql
PGPASSWORD=postgres psql -h 127.0.0.1 -p 6432 -U postgres
CREATE DATABASE pgdog;
CREATE USER pgdog PASSWORD 'pgdog' LOGIN;
```

## 実践ポイント
- まずはローカルで docker-compose up して psql で接続し、読み書き分離や接続プーリングの挙動を確認する。  
- Kubernetes 環境なら Helm chart（helm repo add / helm install）で試す。  
- RDS/Aurora の環境では read replica と組み合わせて読み負荷を外に出すのが現実的。  
- シャーディング導入はまずテスト環境で「直接シャードに行くクエリ」と「クロスシャードの制約」を確認してから本番へ。2PC を有効にしてクロスシャードの整合性要件を満たすか検証する。  
- UUID ではなく pgdog.unique_id() を使えばシャード横断でのユニークIDを軽く扱える。

参考: GitHub リポジトリ https://github.com/pgdogdev/pgdog（導入前にドキュメントとライセンス（AGPL-3.0）を確認してください）。
