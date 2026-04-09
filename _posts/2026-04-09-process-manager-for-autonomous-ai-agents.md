---
layout: post
title: "Process Manager for Autonomous AI Agents - 自律AIエージェントのプロセスマネージャ"
date: 2026-04-09T07:50:55.920Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://botctl.dev/"
source_title: "botctl — Process Manager for Autonomous AI Agents"
source_id: 47699814
excerpt: "宣言的設定で常駐AIを起動・監視、ホットリロードやセッション保存で現場運用を自動化するbotctl"
image: "/og-image.png"
---

# Process Manager for Autonomous AI Agents - 自律AIエージェントのプロセスマネージャ
常駐AIボットをターミナルで自在に管理する「botctl」──現場の自動化を手放しで任せられる仕組み

## 要約
botctlは、YAML+Markdownで記述する宣言的設定から自律AIエージェントを常駐プロセスとして起動・監視・操作できるツールです。TUI／Webダッシュボード、セッション保存、ホットリロード、スキル共有など現場で使いやすい機能が揃っています。

## この記事を読むべき理由
日本の開発現場でも「常時動くAIエージェント」による監視・レビュー・通知のニーズが高まっています。botctlはローカルに近い運用感で扱え、ログやセッションを手元で管理できるため、データ保護や運用ルールを重視する日本企業にも導入しやすい設計です。

## 詳細解説
- 宣言的設定：BOT.mdはYAMLのフロントマター（name, interval_seconds, max_turns など）とプロンプト本文を併せ持つ。設定を変えるだけで次回実行に反映されるためデプロイ不要。
- ハーネスとループ：botctlは指定したモデル（例：Claude）を起動し、ツールや作業領域(workspace)と共に「実行→ログ保存→スリープ」を繰り返す常駐ループを管理する。
- セッション永続化：各実行ごとにセッションが保存され、途中から再開したり、稼働中のボットに対してメッセージで動作の軌道修正が可能。
- ホットリロード：BOT.mdを編集すれば次走のみで新設定を取り込むため、再起動やデプロイ無しで運用が続けられる。
- スキル拡張：GitHub上の「スキル」モジュールを検索・追加でき、通知や外部API連携など機能を注入可能。
- UIと運用：TUI（ターミナルダッシュボード）とWeb UI（デフォルト http://localhost:4444）で起動・停止・ログ参照・メッセージ送信が行える。バックグラウンド実行やログ追跡、コスト表示もサポート。
- プラットフォームと導入：macOS/Linux/Windows（amd64/arm64）をサポートし、インストールはシェル／PowerShellワンライナーで可能。
- セキュリティ面：ローカルでプロセスを管理できる利点がある一方、モデルAPIキーや外部API呼び出しの扱いは注意が必要（内部ポリシーや個人情報対策を検討）。

## 実践ポイント
- まずはインストールしてサンプルを起動：  
  ```bash
  # インストール（macOS/Linux）
  curl -fsSL https://botctl.dev/install.sh | sh

  # ボット作成と起動例
  botctl create my-bot
  botctl start my-bot --detach
  botctl logs my-bot -f
  ```
- BOT.mdのフロントマターでスケジュール（interval_seconds）や最大ターン数（max_turns）を調整。変更はホットリロードで次回実行から適用。
- 稼働中のボットへはメッセージで指示を送れる（例：優先タスクの切替）。運用中の介入が容易。
- スキルを追加してSlack通知や社内API連携を組み込むことで、既存ワークフローに溶け込ませやすい。
- 日本の現場向けには、ログの保持方針・APIキーの保護・機密データのフィルタリングを整備してから本番投入すること。

以上を踏まえ、まずはステージング環境で短時間の監視系ボット（例：API監視・PRレビューヘルパー）を試作し、運用フローに合わせてスキルやワークスペースを拡張するのが実践的です。
