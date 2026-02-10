---
layout: post
title: "Show HN: Rowboat – AI coworker that turns your work into a knowledge graph - Rowboat：作業をナレッジグラフ化して動くAI同僚（OSS）"
date: 2026-02-10T18:52:50.267Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/rowboatlabs/rowboat"
source_title: "GitHub - rowboatlabs/rowboat: Open-source AI coworker, with memory"
source_id: 46962641
excerpt: "Rowboat：ローカルでMarkdownナレッジを構築しメールや会議から文脈を自動蓄積するOSS"
image: "https://opengraph.githubassets.com/4bf3fd784b96f338de823082c36c3d61b347b8c0baa51554fd30016530ce8930/rowboatlabs/rowboat"
---

# Show HN: Rowboat – AI coworker that turns your work into a knowledge graph - Rowboat：作業をナレッジグラフ化して動くAI同僚（OSS）

あなたの作業履歴を「ローカルで溜める・編集できる記憶」に変える、次世代のAI同僚

## 要約
RowboatはローカルにMarkdownベースのナレッジグラフ（Obsidian互換）を構築し、過去のメールや議事録から文脈を継続的に蓄積して、会議準備やメール作成、資料生成などを自動化するオープンソースのAIアシスタントです。

## この記事を読むべき理由
日本企業・個人で「機密性を保ちつつ生産性を上げたい」需要は高く、Rowboatはデータをローカルに保持してモデルを差し替えられる設計で、プライバシー重視の導入候補として実務で即役立ちます。

## 詳細解説
- アーキテクチャ概略  
  - ローカルファースト：すべてのデータはプレーンなMarkdown（Obsidian互換）で保存。埋もれない「編集可能な記憶」を保持。  
  - モデル柔軟性：Ollama/LM Studioなどのローカルモデルも、APIキー差し替えでクラウドモデルも利用可能。  
  - 拡張性：Model Context Protocol（MCP）で検索、CRM、Slack、GitHubなど外部ツールを接続可能。  
  - バックグラウンドエージェント：定期的なメール下書き作成や毎朝の要点生成など自動化を実行。ユーザーが何を実行するか明示的に管理。  
- 入出力と機能  
  - Gmail/Calendar/Driveや会議録（Granola、Fireflies）から自動で文脈を抽出。  
  - 会議準備（過去の決定・未解決課題を要約）、メール草稿、ドキュメント／PDFスライド生成、音声メモ（Deepgram連携）などを出力。  
  - Markdownノートとバックリンクで関係性を明示、手作業で編集可能。  
- セキュリティ・運用観点  
  - データはローカル保存でホスティングロックインなし（Apache-2.0、GitHubスター約4.4k）。  
  - 組織導入時はモデル配置（オンプレ/クラウド）とアクセス制御を社内ポリシーに合わせて設計する必要あり。

## 実践ポイント
- まずは公式リリースをダウンロードしてローカルで試す（Mac/Windows/Linux対応）。  
- Google連携は README の google-setup.md を参照して設定。音声メモは Deepgram API を ~/.rowboat/config/deepgram.json に設定。  
- プライバシー重視ならローカルモデル（Ollama/LM Studio）を選び、APIキーを外部に渡さない構成にする。  
- ナレッジはMarkdownで直接確認・編集可能：運用ルール（命名規則・バックアップ）を決めておく。  
- MCPで既存の業務ツール（Jira/Linear/GitHub/Slack等）を繋ぎ、まずは1つの自動化（例：会議要約の自動生成）から運用を始める。  
- 導入前に社内の機密データポリシーと法務チェックを忘れずに。

Rowboatは「記憶を育てる」アプローチで、特に機密性と継続的な文脈が重要な日本の現場にフィットする可能性が高いツールです。興味があれば公式リポジトリで README とセットアップ手順を確認してください。
