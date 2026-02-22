---
layout: post
title: "Google restricting Google AI Pro/Ultra subscribers for using OpenClaw - OpenClaw利用でGoogle AI Pro/Ultra加入者が制限される"
date: 2026-02-22T23:55:22.304Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://discuss.ai.google.dev/t/account-restricted-without-warning-google-ai-ultra-oauth-via-openclaw/122778"
source_title: "Account Restricted Without WARNING– Google AI Ultra / OAuth via OpenClaw - Google Antigravity - Google AI Developers Forum"
source_id: 47115805
excerpt: "OpenClaw連携でGoogleの有料加入者が警告なく403凍結、原因と回避法"
image: "https://d3qe71uytubmmx.cloudfront.net/original/2X/8/8bfe64fc593eb7baba8df149ebba4457c16ca1f9.png"
---

# Google restricting Google AI Pro/Ultra subscribers for using OpenClaw - OpenClaw利用でGoogle AI Pro/Ultra加入者が制限される
有料サブスクが警告なしに凍結？OpenClaw連携で発生した「403大量凍結」事件の全貌

## 要約
GoogleのAntigravity（いわゆるIDE/サービス）で、OpenClaw経由でGeminiを使った利用者の有料アカウントが警告なしに403で利用停止される事例が多数報告されている。サポート対応が遅く、恒久的な禁止（zero-tolerance）を通告された例もある。

## この記事を読むべき理由
有料でAI機能を使う日本の開発者や企業にも起こり得る問題で、サブスク課金中に開発ワークフローが突然止まるリスクとその回避策を知る必要があるため。

## 詳細解説
- 何が起きたか：複数ユーザーが、OpenClawなどのサードパーティツールをOAuthで接続してGeminiモデルを利用した直後に「This service has been disabled…（403）」でアクセス不能に。通告や段階的なブロックがなく、突然の全停止が多発。
- 技術的要因：報告では「Antigravity（GoogleのIDE/Cloud Code Private API）サーバを、非Antigravity製品のバックエンドとして使った」ことが利用規約違反とされ、OAuthトークンの利用パターンやWAF（Web Application Firewall）の判定で自動的に停止された可能性が示唆されている。一部利用者は「既知のWAFバグ」を指摘。
- サポート/運用の問題：ユーザーはGoogle OneやGCP経路でエスカレーションを試みるも、担当のたらい回し、連絡無視、フォーラム投稿の削除やさらなるアカウント制限が報告されている。企業向けGCC（有償サポート）への誘導や追加料金要求のケースも散見。
- 結末の一例：調査の結果「第三者ツールでAntigravityのサーバを使う行為がToS違反」と結論づけられ、取り消し不能（zero-tolerance）で復旧不可と通知された事例がある。

## 実践ポイント
- すぐやること：
  - OpenClaw等のサードパーティ連携を一時停止・切断してログを保存する。
  - 画面キャプチャ、Trajectory ID、エラーメッセージを保存しておく。
  - Antigravityのアプリ内フィードバック（Feedback → Report Issue）でバグ報告を送る。
  - 指定の問い合わせ先（例：gemini-code-assist-user-feedback@google.com、antigravity-support）へ事実と証拠を送付。
- 中期的対策：
  - 本番ワークフローではサードパーティ連携をまずはテスト用アカウントで検証する（本アカウントの直結は避ける）。
  - サブスクや重要データは定期的にバックアップし、ベンダー依存を減らす（マルチプロバイダ戦略）。
  - 企業ならば有償のエンタープライズサポート契約で対応窓口を整備する。
- 代替案の検討：
  - Gemini以外（Anthropic/Claude、OpenAI等）の選定、あるいはローカル実行モデルの検討。
  - 利用規約（ToS）を読み、サードパーティツール利用時のポリシーリスクを事前に確認。

この事件は「有料でも運用リスクはある」ことを示しています。まずは連携ツールの利用管理と証拠保存を徹底し、必要ならプロバイダ変更の準備を進めてください。
