---
layout: post
title: "Clawdbot - open source personal AI assistant - Clawdbot — オープンソースのパーソナルAIアシスタント"
date: 2026-01-26T01:16:00.519Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/clawdbot/clawdbot"
source_title: "GitHub - clawdbot/clawdbot: Your own personal AI assistant. Any OS. Any Platform. The lobster way. 🦞"
source_id: 46760237
excerpt: "ローカル常駐でSlackやiMessageと連携する多機能AI、Clawdbotを試す"
image: "https://opengraph.githubassets.com/8d935ed4095a69d868fe2b200ac1ebd9fdac3a58d7f595c36108530f518925d5/clawdbot/clawdbot"
---

# Clawdbot - open source personal AI assistant - Clawdbot — オープンソースのパーソナルAIアシスタント
あなた専用の「常時オン」AI秘書を手元で動かす——ロブスター流のローカルファーストAI

## 要約
Clawdbotは自分のデバイスや小さなサーバ上で動くオープンソースのパーソナルAIアシスタントで、WhatsAppやSlack、Discord、iMessageなど既存のチャネルと連携し、音声・キャンバス・ブラウザ操作など豊富なツールを持つのが特徴です。

## この記事を読むべき理由
データを外部サービスに預けたくない個人や企業、オンプレ寄りの運用を考える日本のエンジニア／プロダクト担当にとって、Clawdbotは「ローカルで常時稼働」「多チャネル対応」「ツール連携」が揃った実用的な選択肢になるため。

## 詳細解説
- アーキテクチャ
  - Gateway（制御面）を中心に、CLI・デバイスノード（macOS/iOS/Android）・WebChatやmacOSアプリがWebSocketで接続。Gatewayはセッション管理・チャネル接続・ツール実行のコントロールプレーンです。
- 対応チャネル
  - WhatsApp、Telegram、Slack、Discord、Google Chat、Signal、iMessage、Microsoft Teams、WebChat、Matrix、Zaloなど。日本でよく使うSlackやTeams、iMessage（mac/iOS）経由の利用が実用的。
- マルチエージェント／ルーティング
  - チャネルや会話ごとに分離されたエージェント（セッション）を作り、履歴やツールを独立して管理。グループルールや返信ポリシー細かく設定可能。
- ツール群
  - ブラウザ操作（専用clawd Chrome）、Canvas（A2UI）、ノード経由のカメラ/画面録画、cron/webhook、ブラウザスナップショットなどをエージェントから直接操作できます。
- 音声・モバイル
  - macOS/iOS/AndroidでVoice WakeやTalk Mode対応、常時音声インプットが可能。ElevenLabsなどで出力音声も連携。
- モデルと運用
  - どのモデルでも動くが、開発元はAnthropic Pro/Max（長コンテキスト）を推奨。モデル認証はOAuthやAPIキー、フォールバック/フェイルオーバー設定あり。
- セキュリティ
  - デフォルトでDMは「ペアリング」方式（未承認ユーザにワンタイムコードを送る）となり、安全性を重視。Gatewayはローカルバインド＋Tailscale Serve/Funnel経由でリモートアクセス可能。
- インストール/開発
  - Node≥22が必要。CLIウィザード（clawdbot onboard）が導入・ペアリング・チャネル設定を案内。DockerやNix導入もサポート。ソースはpnpm推奨でビルドループやホットリロードが可能。

## 実践ポイント
- まず触る：Node≥22 を用意してウィザードを起動
```bash
npm install -g clawdbot@latest
clawdbot onboard --install-daemon
```
- モデル選定：長い履歴やプロンプト注入耐性が欲しいならAnthropic Pro/Maxを検討する
- セキュリティ：初期は dmPolicy="pairing" のまま使い、clawdbot doctor で設定を確認する
- 日本での活用例：社内Slack連携＋ローカルGatewayで社内ドキュメント検索や自動化、macOSメニューアプリで開発者の常設アシスタントに
- リモート運用：小さなLinux VPSでGatewayを動かし、Tailscale Serveでセキュアに外部接続するのが現実的
- 開発/拡張：pnpmでソースからビルドし、skillsやCanvasなどを試して自分のワークフローに合わせたスキルを作る

Clawdbotは「自分専用」「ローカル優先」「多チャネル・多ツール連携」を求める日本の個人や小中規模チームに魅力的な実用OSSです。興味があれば公式リポジトリ（GitHub）とドキュメントのGetting startedをまず試してみてください。
