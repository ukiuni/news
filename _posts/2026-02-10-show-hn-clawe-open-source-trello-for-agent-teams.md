---
layout: post
title: "Show HN: Clawe – open-source Trello for agent teams - Clawe — エージェントチーム向けオープンソースTrello"
date: 2026-02-10T21:15:40.362Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/getclawe/clawe"
source_title: "GitHub - getclawe/clawe: Open-source multi-agent coordination system powered by OpenClaw"
source_id: 46966209
excerpt: "Dockerで即導入、複数AIをカンバンで管理できるオープンソースClawe"
image: "https://opengraph.githubassets.com/731569f3e7c3d7666cd1a2464b7c6a6e2e8d0f443772584e1c4bd025b676d59c/getclawe/clawe"
---

# Show HN: Clawe – open-source Trello for agent teams - Clawe — エージェントチーム向けオープンソースTrello
チームで動くAIエージェントを自前で運用する。Claweで「AI版カンバン＋エージェント管理」を今すぐ試そう

## 要約
ClaweはOpenClawとConvexを組み合わせた、複数AIエージェントを個別ワークスペースで管理するオープンソースのマルチエージェント調整システム。カンバン風タスク管理、定期ハートビート、通知配信、エージェント間の共有ファイルを備える。

## この記事を読むべき理由
日本企業でも、AIを単体ツールではなく「チームの一員」として運用するニーズが高まっている。ClaweはDockerベースでローカル／プライベート環境に入れやすく、データ管理やカスタムエージェント追加がしやすいため、PoCや社内適用に適している。

## 詳細解説
- コア構成  
  - OpenClaw: エージェント用ゲートウェイ。エージェント登録・cronでの起床・通知配信を担う。  
  - Convex: バックエンド（タスク・通知・アクティビティの永続化）。  
  - clawe: Next.js製のWebダッシュボード（カンバン、チャット、スクワッド状況）。  
  - watcher: 通知配信とcronスケジューラ。  
  - 全体は docker-compose で起動可能。

- 主な機能  
  - 複数エージェント（各エージェントにID・役割・性格・ワークスペースを付与）  
  - Cronベースのハートビート（エージェントが定期的に起きてタスクを生成/処理）  
  - Kanban風のタスク、サブタスク、@メンション即時配信  
  - エージェント毎に分離されたワークスペース（SOUL.md, HEARTBEAT.md, MEMORY.md等）  
  - clawe CLI による操作（task:list, task:status, subtask:add, notify 等）

- 導入の流れ（概要）
  1. 前提: Docker/Compose, Convexアカウント, Anthropic APIキー（Claude用）  
  2. クローン & 環境変数設定（.env に ANTHROPIC_API_KEY, OPENCLAW_TOKEN, CONVEX_URL を設定）  
  3. Convex デプロイ → Dockerで openclaw / watcher / clawe を起動  
  4. Webダッシュボードでスクワッド監視 & カンバン確認

- カスタマイズ性  
  - 新エージェントは docker/openclaw/templates にワークスペーステンプレを追加し、watcher の AGENTS 配列に登録してビルド。  
  - ハートビート(cron)や役割はソースで容易に編集可能。

## 実践ポイント
- まずローカルで試す: 必須は Anthropic APIキーのみ。Convexは無料枠で動作する。  
- .env は scripts/start.sh で自動生成できるが、APIキーと OPENCLAW_TOKEN は必ず設定する。  
- 開発サイクル: watcher（cron）と OpenClaw を起動 → claweダッシュボードでタスクの流れを観察 → ワークスペースの HEARTBEAT.md を編集して動作を調整。  
- 日本企業での活用案: 顧客対応のスクリプト自動化、コンテンツ制作チームの役割分担、社内ナレッジの自動更新。オンプレ寄せの運用やログ保全が必要な場合、ソースベースでの改変が可能。  

参考コマンド（最小構成）
```bash
# Clone と環境準備
git clone https://github.com/getclawe/clawe.git
cd clawe
cp .env.example .env
# .env に ANTHROPIC_API_KEY, OPENCLAW_TOKEN, CONVEX_URL を設定
./scripts/start.sh
```

以上を試してみれば、チーム単位で動く“エージェントのワークスペース設計”と運用感を短時間でつかめます。
