---
layout: post
title: "pg-status — a lightweight microservice for checking PostgreSQL host status - pg-status — PostgreSQLホストの状態を軽量に監視するマイクロサービス"
date: 2026-01-08T14:01:49.109Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/krylosov-aa/pg-status"
source_title: "GitHub - krylosov-aa/pg-status: A microservice (sidecar) that helps instantly determine the status of your PostgreSQL hosts including whether they are alive, which one is the master, which ones are replicas, and how far each replica is lagging behind the master."
source_id: 468070731
excerpt: "**サイドカーで動く超軽量Postgres監視ツールで接続先選定と即時フェイルオーバー判定を実現**"
image: "https://opengraph.githubassets.com/5a26c3af32210f89099a5745f4ced2fb42b68b6d702c6633ae9a517a765f6f6b/krylosov-aa/pg-status"
---

# pg-status — a lightweight microservice for checking PostgreSQL host status - pg-status — PostgreSQLホストの状態を軽量に監視するマイクロサービス

一目でわかる！サイドカーで動く超軽量Postgres監視ツール「pg‑status」で接続先選定とフェイルオーバー判断を高速化

## 要約
pg-statusはサイドカーとして動作する超軽量のマイクロサービスで、PostgreSQLホストの生死、マスター/レプリカ判定、レプリカの遅延（時間／バイト）を常時ポーリングして高速なHTTP APIで返します。

## この記事を読むべき理由
日本でもPostgreSQLを使うSaaSやオンプレ運用が増え、アプリ側での接続先選定や簡易フェイルオーバー判断が求められます。pg-statusは低リソースで即応答するため、Kubernetesのサイドカーや軽量VM環境で手早く導入でき、運用コスト削減や可用性向上に役立ちます。

## 詳細解説
- 基本動作
  - バックグラウンドで各Postgresホストをポーリングし、結果をメモリに保持。HTTPで即時応答するためリクエストごとの監視負荷はほぼゼロ。
  - レスポンスはAcceptヘッダでJSON（Accept: application/json）またはプレーンテキストを選択可能。

- 代表的なHTTPエンドポイント
  - GET /master — 現在のマスターを返す（存在しない場合はnull）
  - GET /replica — ラウンドロビンでレプリカを返す（空ならマスター）
  - GET /sync_by_time — 時間差が許容内のレプリカを返す
  - GET /sync_by_bytes — WALのバイト遅延が許容内のレプリカを返す
  - GET /sync_by_time_or_bytes, /sync_by_time_and_bytes — 条件を組み合わせた同期判定
  - GET /hosts — 全ホストの状態一覧（JSON）
  - GET /status?host=ホスト名 — 指定ホストの詳細状態

- 主な環境変数（設定例・デフォルト）
  - pg_status__pg_user, pg_status__pg_password, pg_status__pg_database（デフォルト: postgres）
  - pg_status__hosts — ホスト一覧（区切り文字は pg_status__delimiter、デフォルトは ,）
  - pg_status__port（デフォルト 5432）、pg_status__connect_timeout（秒、デフォルト2）
  - pg_status__max_fails（連続エラーでデッドと判定、デフォルト3）
  - pg_status__sleep（ポーリング間隔秒、デフォルト5）
  - 同期判定: pg_status__sync_max_lag_ms（デフォルト1000ms）、pg_status__sync_max_lag_bytes（デフォルト1,000,000バイト）

- インストール／実行方法（主な選択肢）
  - debパッケージ、静的バイナリ、動的バイナリ、Dockerコンテナ、ソースからCMakeでビルド。
  - 公式Releaseに静的バイナリやdebがあるため、依存関係の少ない環境で即導入可能。

- 依存とライセンス
  - libmicrohttpd（HTTP）、libpq（Postgres接続）、cJSON。ライセンスはMIT（プロジェクト本体）、各コンポーネントはそれぞれのライセンス。

- 性能例
  - 非常に軽量：CPU約0.1、メモリ約9MiB。HTTPレスポンスのスループットは約1.7k req/s（計測例）で、レイテンシもミリ秒〜数十ミリ秒。

- テストサポート
  - テスト用docker-composeが用意されており、マスター／レプリカ切替をプロキシで模擬して振る舞いを検証できる。

## 実践ポイント
- まずはサイドカー配置を試す：アプリと同ノードに配置して /master や /replica を呼べば接続先選定ロジックを外部化できます。
- 具体的なcurl例（JSON取得）
  ```bash
  curl -H "Accept: application/json" http://127.0.0.1:8000/master
  ```
- デプロイ候補
  - Kubernetes: Pod内にサイドカーコンテナとして配置し、アプリは127.0.0.1:ポートで問い合わせるだけで済む。
  - 既存VM/コンテナ環境: systemdやDockerで常駐させると簡単。
- 設定のコツ
  - pg_status__sleep（ポーリング間隔）と pg_status__max_fails を運用のSLAに合わせて調整。短すぎるとDB負荷、長すぎると検知遅延に。
  - 同期判定（ms/bytes）はアプリの整合性要件に合わせて設定（読み取り整合性が厳しいなら低めに）。
- セキュリティと運用
  - 監視専用のPostgres読み取りユーザーを作り、権限を最小化する。
  - サイドカーが返す情報は内部向けに限定し、外部公開しないこと（HTTPを公開する場合は認証やネットワーク制限を検討）。
- 日本市場での活用シナリオ
  - SaaS事業者：複数AZ／オンプレ混在の接続先選定をアプリ側で簡潔に実装可能。
  - レガシー→クラウド移行期：オンプレとクラウドの複合構成で中央の監視を入れずにローカルで判断できる。
  - リソースが限られるスタートアップ：低メモリで動くためコストの少ない監視手段として最適。

導入は簡単、得られる効果は大きい――まずはローカル／ステージングで試して、アプリの接続ロジックをシンプルに保つ運用に組み込んでみてください。
