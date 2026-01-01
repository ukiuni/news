---
  layout: post
  title: "OpenWorkers: Self-Hosted Cloudflare Workers in Rust - OpenWorkers：Rustで作るセルフホスト型Cloudflare Workers"
  date: 2026-01-01T16:54:25.606Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://openworkers.com/introducing-openworkers"
  source_title: "Introducing OpenWorkers – Self-hosted Cloudflare Workers in Rust"
  source_id: 46454693
  excerpt: "自社でWorkers互換を動かし、Rust製OpenWorkersで安全にエッジ処理を内製化"
  ---

# OpenWorkers: Self-Hosted Cloudflare Workers in Rust - OpenWorkers：Rustで作るセルフホスト型Cloudflare Workers
自社サーバで“Cloudflare Workers”の使い勝手を実現する――OpenWorkersが示すエッジの内製化パス

## 要約
OpenWorkersは、Rust上で動くオープンソースのランタイムで、V8アイソレートを使って安全に未検証のJavaScriptを実行し、Cloudflare Workers互換の開発体験を自社インフラで提供します。

## この記事を読むべき理由
- ベンダーロックインを避けたい企業や、データを社内に留める必要のある日本のプロダクト開発者にとって実用的な選択肢になるため。  
- Cloudflare Workers互換なので既存のWorkersコードやナレッジを活かせ、オンプレ／クラウド混在環境で「エッジ的」アーキテクチャを構築できるから。

## 詳細解説
- ランタイム設計  
  OpenWorkersはRustで実装されたランタイム上で直接 rusty_v8（V8のRustバインディング）を使い、各ワーカーをV8アイソレートでサンドボックス化します。各ワーカーにはCPU時間（デフォルト100ms）とメモリ（128MB）などの実行制限が設定され、安全性と予測可能なリソース消費を担保します。

- 互換性とAPI  
  Cloudflare Workersの文法互換を目指しており、fetch/Request/Response、ReadableStream、crypto.subtle、TextEncoder/Decoder、Blob、setTimeout、AbortControllerといったWeb系APIをサポート。既存のWorkersコードの移行コストが低い点が魅力です。

- バインディング（外部連携）  
  - KV風のキー・バリューストレージ（get/put/delete/list）  
  - PostgreSQL（SQLクエリ）  
  - S3 / R2互換ストレージ  
  - サービスバインディング（他サービスへの接続）、環境変数・シークレット管理  
  これにより、既存のDBやストレージをそのまま使って“エッジ関数”からアクセスできます。

- ランタイム構成と運用  
  アーキテクチャは nginx（プロキシ）を前置し、dashboard、api、logs、複数のrunner、scheduler、Postgresなどのコンポーネントを組み合わせる構成。メッセージングにNATSやPostgresを利用する設計が見られ、スケールはrunner数で水平に対応します。Cron（5/6フィールド）対応のスケジューラも組み込み済み。

- デプロイのしやすさ  
  単一のPostgreSQLとDocker Composeで立ち上がることを目標にしており、リポジトリをクローンして.envを用意し、docker composeでPostgres→マイグレーション→サービス起動といった流れで簡単に試せます。

- 生い立ちと今後  
  7年にわたる進化の結果で、vm2→deno-core→rusty_v8と移行してきた背景があります。今後は実行記録と再生（deterministic debugging）などデバッグ機能の強化が予定されています。

## 実践ポイント
- 即試せる手順（ローカル検証用）:
```bash
# bash
git clone https://github.com/openworkers/openworkers-infra
cd openworkers-infra
cp .env.example .env
docker compose up -d postgres
# 必要ならマイグレーションやトークン生成を実行
docker compose up -d
```
- 移行戦略案  
  1. 既存のCloudflare Workers（小さめのエンドポイント）をOpenWorkers上で動かして互換性テスト。  
  2. 外部依存（DB/オブジェクトストレージ）を社内サービスに差し替え、通信経路と認証を確認。  
  3. リソース制限（タイムアウト/メモリ）をアプリごとに見直し、監視とアラートを整備。  
- 日本市場での活用例  
  - 個人情報や機微なログを外部に出せない金融・医療系システムのエッジ処理。  
  - CDN/エッジサービスに頼らず国内データセンターで低レイテンシ処理を完結させたいメディア・ゲーム分野。  
  - SIerやホスティング事業者がマネージド版を提供して差別化する余地。

- 注意点  
  - サンドボックスは強いが完全無謬ではないため、定期的なセキュリティレビューとアップデート運用が必要。  
  - 大量リクエストや重いCPU処理はランナー数/リソース設計でコストが変わるため事前検証を推奨。

## 引用元
- タイトル: OpenWorkers: Self-Hosted Cloudflare Workers in Rust  
- URL: https://openworkers.com/introducing-openworkers
