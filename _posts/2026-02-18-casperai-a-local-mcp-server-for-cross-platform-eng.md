---
layout: post
title: "CasperAI – A local MCP server for cross-platform engineering context - CasperAI：クロスプラットフォームのエンジニアリングコンテキスト向けローカルMCPサーバー"
date: 2026-02-18T15:49:22.354Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/chose166/CasperAI"
source_title: "GitHub - chose166/CasperAI: Tribal Knowledge Super-Brain"
source_id: 439811131
excerpt: "散らばった社内チャットや設計書とコードをローカルで結び即時検索するCasperAI"
image: "https://opengraph.githubassets.com/b940d992691f4b32056e2c7dc8464d9cad983cdca5265973adb0426c882ae43a/chose166/CasperAI"
---

# CasperAI – A local MCP server for cross-platform engineering context - CasperAI：クロスプラットフォームのエンジニアリングコンテキスト向けローカルMCPサーバー
社内Slackの会話とソースコードを「つなげて検索」するローカルAI——CasperAIで散らばった知見を一箇所に

## 要約
CasperAIはSlack、GitHub、Jira、Notionなど複数ツールの会話・履歴をローカルSQLiteに取り込み、関数名やファイル参照をコードと双方向で紐付けるMCPサーバーです。検索は全文検索＋意味埋め込みで行い、データはローカルに留まります。

## この記事を読むべき理由
日本の開発チームでも「会話はSlack、設計はNotion、実装はリポジトリ」に分断されがち。CasperAIはその断片をつなぎ、バグ発生時やオンボーディングでの情報探索を圧倒的に速くします。社内情報を外部クラウドに出したくない企業にも適します。

## 詳細解説
- 基本アーキテクチャ
  - MCP（Model Context Protocol）サーバーとして動作。Slack/GitHub/Jira/Notion等をインデックスしてローカルSQLite（FTS5）に保存。
  - 意味検索はローカルの小型モデル（Transformers.js）で埋め込みを作成、全文検索はSQLite FTS5で高速化。
- コード参照の紐付け
  - 自然文から関数名やファイルパスを抽出するために正規表現ベースのマッパーを使用（例：authenticateUser(), src/auth/handler.ts）。
  - 抽出後はファイルシステムを横断して該当ファイル／定義を探索し、confidenceスコアで信頼度を付与。
- なぜ正規表現？
  - 利点：複数言語で軽量に動く、速度が速い、Slackのような非構造的表現に強い。
  - 欠点：偽陽性や定義と呼び出しの区別が付かない等。将来的にはtree-sitter等のASTベース解析を検討。
- セキュリティ／プライバシー
  - 全データをローカルDBに保持。PIIは取り込み時に正規表現でマスク。GDPR/HIPAA等の対応を意識した設計。
- 開発者向け体験
  - CLI中心（例：npx casperai init）、MCP互換クライアントやClaude Desktopと連携が可能。
- 対応プラットフォーム（代表）
  - Slack, GitHub, GitLab, Jira, Linear, Notion, Sentry, Datadog 等（必要なものだけ設定可能）。

## 実践ポイント
- まずは1コマンドで試す（ターミナルで実行）:
```bash
npx casperai init
```
- 最小構成で試す手順
  1. リポジトリをクローンして依存を入れる：npm install
  2. .env.example をコピーしてSLACK_API_TOKEN等を設定
  3. チャンネルをインデックス（例）:
```json
{
  "tool":"index_slack_channel",
  "arguments":{"channel":"C12345678","maxMessages":1000,"generateEmbeddings":true}
}
```
- 運用のコツ
  - generateEmbeddingsを有効にすると意味検索できるが初回はモデルをダウンロードするため時間がかかる。
  - 正規表現由来の誤検出に注意。重要なマッピングはチームでレビューする運用ルールを作る。
  - コンプライアンスが厳しい環境では「ローカル保存」「PIIマスク」を必ずオンに。
- 次の一歩
  - 小さなチャンネル（エンジニアリング）から試験導入して効果を測る。成果が出れば他ツールも順次追加する。

以上を踏まえ、社内知識を素早く結びつけたいチームは一度ローカルで動かしてみる価値があります。
