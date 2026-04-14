---
layout: post
title: "Show HN: Kontext CLI – Credential broker for AI coding agents in Go - AIコーディングエージェント向けクレデンシャルブローカー（Go）"
date: 2026-04-14T16:00:47.000Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/kontext-dev/kontext-cli"
source_title: "GitHub - kontext-security/kontext-cli: Open-source CLI for AI coding agents. Give your coding agents access to services without exposing keys. · GitHub"
source_id: 47765374
excerpt: "短命トークンで長期APIキーを渡さずAIエージェントの権限・ツール利用を監査管理するKontext"
image: "https://opengraph.githubassets.com/251eaed7073670a5a40efef1d75fc8d1196970e413176400e5080cc09318b776/kontext-security/kontext-cli"
---

# Show HN: Kontext CLI – Credential broker for AI coding agents in Go - AIコーディングエージェント向けクレデンシャルブローカー（Go）
エージェントに「鍵を渡さない」運用へ：短命トークンでAIコードエージェントの権限を安全に管理するKontext CLI

## 要約
Kontext CLIはローカルで実行するAIコーディングエージェントに対し、長期APIキーを渡さずに短命・スコープ付きの認証情報を注入し、ツール呼び出しを監査するオープンソースのCLIツール。

## この記事を読むべき理由
- .envに長期間のAPIキーを置く運用を安全に改善したい日本の開発チームやスタートアップに即効の代替手段を提供するため。  
- ガバナンス（監査ログ、セッション単位のトークン）やSaaS連携（GitHub/Stripe/DB等）でのリスク低減に直結する。

## 詳細解説
- ワークフロー：プロジェクトに宣言ファイル `.env.kontext` を置き、`kontext start --agent <agent>` でセッション開始。CLIはブラウザでOIDCログインを行い、システムキーリングにリフレッシュトークンを保存、RFC 8693（トークン交換）でプレースホルダーを短命トークンに交換してエージェントに環境変数として注入する。セッション終了でトークンは失効する。  
- セキュリティ面：OIDC認証、システムキーリング保存、RFC 8693トークン交換、保存時は AES-256-GCM による暗号化を採用。エージェント側の会話履歴やLLM推論は取得せず、ツール呼び出し（PreToolUse/PostToolUse/UserPromptSubmit）だけがガバナンス用に送られる設計。  
- 実装とアーキテクチャ：Go製のネイティブCLIで軽量サイドカー（Unixソケット経由）を起動。CLI↔バックエンドは ConnectRPC を使用。Claude Code が現時点でアクティブサポート、他エージェントは順次対応予定。リポジトリはMITライセンスのOSS。  
- 運用注意：テンプレート（`.env.kontext`）はリポジトリにコミット可能だが、実際のシークレットはKontext側で管理される。バックエンドにセッション/ツールコールのテレメトリが送られる点は組織ポリシーで確認しておく。

## 実践ポイント
- まず試す（macOS Homebrew例）：
```bash
brew install kontext-dev/tap/kontext
kontext start --agent claude
kontext logout
```
- `.env.kontext` の例：
```env
GITHUB_TOKEN={{kontext:github}}
STRIPE_KEY={{kontext:stripe}}
DATABASE_URL={{kontext:postgres/prod-readonly}}
```
- 運用提案：
  - リポジトリにはテンプレートのみをコミットし、実働キーはKontextで短命トークン化する。
  - 監査ログ（ツール呼び出し）をSOC/セキュリティチームと連携してレビュー導線を作る。
  - ステージングでまず試験運用し、バックエンドへ送られるメタデータの範囲を確認する。
  - 自動更新チェックを無効化する場合は `KONTEXT_NO_UPDATE_CHECK=1` を設定。

参考：OSS・Go実装、RFC 8693トークン交換、OIDCを組み合わせた「セッション単位での権限付与」と監査の実装がポイント。
