---
layout: post
title: "I Shipped the Solution to Knowledge Collapse in 21 Days - 21日で「知識崩壊」への解決策を出荷した話"
date: 2026-02-09T17:46:45.450Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/the-foundation/i-built-federated-ai-knowledge-commons-heres-how-56oj"
source_title: "I Shipped the Solution to Knowledge Collapse in 21 Days - DEV Community"
source_id: 3243096
excerpt: "21日で分散ナレッジコモンズを構築し、AIチャットに埋もれる知見を安全に保存・検索・共有可能にした。"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fxuuj8wc8c32xy26iq7hi.png"
---

# I Shipped the Solution to Knowledge Collapse in 21 Days - 21日で「知識崩壊」への解決策を出荷した話
「AIチャットに埋もれる知見を救う」──21日で作った分散型ナレッジコモンズの全貌

## 要約
プライベートAIチャットで消える技術的知見を、保存・検索・安全に共有できる分散型プラットフォームとして21日で実装し、本番運用とOSS公開をしたという話です。

## この記事を読むべき理由
Stack Overflow流出やAIチャットの秘匿化で「知識の喪失」が進む中、企業・個人どちらにも関係する「再現可能で安全な知識保存」手法を実践的に示しています。日本の開発現場でも「ナレッジの継承」「情報漏洩対策」「ベンダーロックイン回避」に直結します。

## 詳細解説
- 問題点
  - 有益なデバッグや設計上の知見がClaude等のプライベートチャットに閉じ、発見・帰属・再利用ができない。
  - Stack Overflowのトラフィック低下はナレッジ共有習慣の衰退を示唆。

- 作ったもの（主要機能）
  1. HTMLインポート
     - ClaudeなどのチャットをCtrl+SでHTML保存→専用CLIでインポート。パース→チャンク化→埋め込み生成まで数秒で完了。
  2. セキュリティスキャナ（重要）
     - APIキー、Bearerトークン、localhostや内部ドメインなどを自動検出して公開前にブロック・レビューを要求。実ビルドで複数の重大リークを検出。
  3. セマンティック検索
     - 単なるキーワードではなく埋め込み（Workers AI、768次元）を用いたコサイン類似度検索で意味的に関連する会話を発見。
  4. フェデレーション（ActivityPub）
     - 各自がインスタンスを立て、ActivityPubで接続すれば横断検索や相互公開が可能。Mastodonの仕組みと同様の分散性を目指す。

- 技術スタック
  - 実行基盤: Cloudflare Workers（エッジネイティブ）
  - DB: D1（SQLite edge）
  - ベクトルストア: Vectorize（768-dim）
  - Embeddings: Workers AI (BGE-base-en-v1.5)
  - プロトコル: ActivityPub

- 実装上の課題
  - 非公開チャットのHTMLパース（フォーマットが未文書化）
  - 認証情報判定の文脈把握（コード例か実鍵かの切り分け）
  - ActivityPubのQ&A表現やスパム対策
  - Workersのリソース制約に合わせた設計（短いCPUタイムなど）

## 実践ポイント
- 試す（手早くローカルで）
  - リポジトリ: https://github.com/dannwaneri/chat-knowledge
  - ライブデモ: https://chat-knowledge-api.fpl-test.workers.dev
- 主要コマンド例
```bash
# リポジトリをクローン
git clone https://github.com/dannwaneri/chat-knowledge.git
cd chat-knowledge
npm install

# HTMLをインポート（例）
node dist/cli/import-html.js path/to/chat.html "My First Import"

# 公開前の安全スキャン
node dist/cli/safe-share.js <chat-id>

# 検索（例）
curl -X POST https://your-worker.workers.dev/search \
  -H "Content-Type: application/json" \
  -d '{"query":"debugging tips","maxResults":5}'
```

- 日本の現場での活用案
  - 社内ナレッジの検索可能化とオンプレ／エッジでの運用で情報漏洩リスクを低減
  - チームの過去チャットをインポートしてオンボーディング資料やFAQ代替に
  - フェデレーションでコミュニティ単位の専門ナレッジ共有（例：製造業向け運用ノウハウ共有）

短時間でプロダクト化した実例として、OSSを触って自分のインスタンスを立てれば「失われつつある知見」を取り戻す第一歩になります。興味があればリポジトリをスターして試してみてください。
