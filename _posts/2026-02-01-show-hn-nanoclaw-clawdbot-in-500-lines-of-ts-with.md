---
layout: post
title: "Show HN: NanoClaw – \"Clawdbot\" in 500 lines of TS with Apple container isolation - Show HN: NanoClaw — 500行のTypeScriptで動くAppleコンテナ隔離の「Clawdbot」"
date: 2026-02-01T23:05:31.749Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/gavrielc/nanoclaw"
source_title: "GitHub - gavrielc/nanoclaw: My personal Claude assistant that runs in Apple containers. Lightweight, secure, and built to be understood and customized for your own needs."
source_id: 46850205
excerpt: "500行TSでMacに隔離展開する安全な個人用Claude—NanoClaw"
image: "https://repository-images.githubusercontent.com/1146738089/6d3089da-11d6-4a31-ae00-8ec33e30c667"
---

# Show HN: NanoClaw – "Clawdbot" in 500 lines of TS with Apple container isolation - Show HN: NanoClaw — 500行のTypeScriptで動くAppleコンテナ隔離の「Clawdbot」

魅力的タイトル: 小さくて安全な個人AIアシスタントを自分で持つ──NanoClawで「自分だけのClaude」をMac上に隔離展開する方法

## 要約
NanoClawは、Claude Agent SDKを使った軽量な個人用AIアシスタントで、ワンプロセス・数ファイル・Appleコンテナ（ファイルシステム隔離）で動作する設計。コードが小さいため理解・改造が容易で、プライバシー重視の日本のユーザーに向いた選択肢です。

## この記事を読むべき理由
- 日本でも増えるMac（特にMac miniや開発用Mac）でローカルに安全にAIを動かしたい人に直球で刺さる。
- 大規模で複雑なOSSに疲れた開発者が「理解できる・改造できる」AIアシスタントを求めている現在のニーズにマッチ。

## 詳細解説
- アーキテクチャ：単一のNode.jsプロセスが中心で、エージェントはAppleのコンテナ（軽量なLinux環境）内で実行される。エージェントは明示的にマウントされたディレクトリしか見られないため、OSレベルでの隔離が効く。
- ハーネス：Claude Agent SDKをネイティブに使っているため、モデルとのやり取りは「正攻法」。ハーネスの品質は結果に直結するという設計思想。
- 構成と拡張：設定ファイルを極力排し、機能追加は「skills」（.claude/skills）として提供。例えば /add-telegram や /add-slack のようなスキルでチャネルを追加する流儀。
- 主要コンポーネント（リポジトリ上の要所）
  - src/index.ts：WhatsApp接続とルーティング
  - src/container-runner.ts：エージェントコンテナの起動
  - src/task-scheduler.ts：定期タスク実行
  - src/db.ts：SQLite操作、グループごとのCLAUDE.mdで文脈保持
- セキュリティ観点：アプリ内の許可（allowlist）よりもファイルシステムマウントによるOS隔離を重視。コードベースが小さいため監査もしやすい。
- 制約：macOS Tahoe（26）以降が想定。Docker化やLinux移植はスキルで対応可能だが、初期設計はAppleコンテナ前提。

## 実践ポイント
- 試す手順（ローカルのMacで）:
```bash
# bash
git clone https://github.com/gavrielc/nanoclaw.git
cd nanoclaw
claude
./setup
```
- 日本向け活用例：社内の限定チャット（Slack/Teams連携をスキルで追加）やローカルObsidianデータにアクセスさせた定期レポート、自分専用の運用自動化に向く。
- セキュリティのチェックリスト：マウントするディレクトリを最小化、CLAUDE.mdの機密情報を分離、setup実行前にコードを読む。
- カスタマイズ方針：大きな変更は「スキル」を作って分離することで、ベースは常に小さく保つのが推奨。

短くまとめると、NanoClawは「自分で理解できて改造できる」「OSレベルで隔離された」個人用Claudeアシスタントを目指すプロジェクトで、Macベースの日本の開発者・プライバシー重視ユーザーに試す価値があります。
