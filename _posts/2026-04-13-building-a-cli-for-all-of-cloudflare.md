---
layout: post
title: "Building a CLI for all of Cloudflare - Cloudflare全体をカバーするCLIの構築"
date: 2026-04-13T16:45:17.395Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.cloudflare.com/cf-cli-local-explorer/"
source_title: "Building a CLI for all of Cloudflare"
source_id: 47753689
excerpt: "本番APIをローカルで再現、cf CLIとLocal Explorerで高速開発とAI自動化が可能に"
image: "https://cf-assets.www.cloudflare.com/zkvhlag99gkb/368W2qPlsPYe9LtZAcsA3/2143d50e049b8398b0551a262290aab4/BLOG-3224_OG.png"
---

# Building a CLI for all of Cloudflare - Cloudflare全体をカバーするCLIの構築
「ローカルでクラウドを丸ごと触れる—Cloudflareの新しいCLIとLocal Explorerが開発体験を変える」

## 要約
CloudflareがWranglerを再設計し、全製品に対応する新CLI「cf」と、ローカルでAPIと同じ形でリソースを覗けるLocal Explorerの技術プレビューを公開しました。

## この記事を読むべき理由
ローカルで本番と同じAPI形を使えることで、オフラインテストやAIエージェント自動化、CIの高速化が可能になり、日本の開発現場でも開発速度と信頼性が大きく向上します。

## 詳細解説
- 背景：Cloudflareは100以上の製品・約3,000のHTTP APIを持ち、近年はAIエージェントが主要なAPI利用者になっている。CLIやBindings、SDK、Terraformなど、あらゆるインターフェイスを一貫化する必要が出てきた。
- 新設計：OpenAPIだけでは表現しきれない「CLIの対話フロー」「ローカル開発とAPI呼び出しの混在」などに対応するため、TypeScriptベースのスキーマを導入。型・規約・リンティングで一貫性を保ちつつ、CLIやSDK、OpenAPIを生成できるようにした。
- コンシステンシー：コマンドとフラグの命名規則（例：常に get、--force、--json を採用）をスキーマ層で強制し、エージェントや人間の期待を合せる。
- Local Explorer：WranglerとCloudflare Viteプラグインでオープンβ提供。KV、R2、D1、Durable Objects、Workflowsといった「シミュレートされた」ローカルリソースを、実際のAPIと同じ形で閲覧・操作可能にする。Miniflareを用いた完全ローカル挙動（ローカルSQLiteなど）で高速テストが可能。
- ローカルAPIミラー：ローカル上で /cdn-cgi/explorer/api が提供され、エージェントはこのエンドポイントを参照してOpenAPI仕様に基づきローカルリソースを管理できる。これにより --local フラグで同じCLIコマンドがローカル向けに動作する。

## 実践ポイント
- 今すぐ触る：技術プレビューは以下で試せます。
```bash
npx cf
npm install -g cf
```
- Local Explorerを使って、開発中のWorkerがどのバインディングやデータを参照しているかを可視化する（ショートカットは e）。
- CIやテストではローカルAPIミラーを活用してネットワーク不要の高速検証を組み込む。
- エージェント連携を考えている場合は、/cdn-cgi/explorer/api を指すことでローカルでエージェントの挙動を再現・デバッグ可能。
- フィードバックを出す：現状は技術プレビューのため、公式Discordなどで要望を送ると設計に反映されやすい。

（原著：Cloudflare Blog — "Building a CLI for all of Cloudflare"）
