---
layout: post
title: "CloudSweeper: Cutting Cloud Waste with an AI FinOps Agent - CloudSweeper：AI FinOpsエージェントでクラウドの無駄を削減"
date: 2025-12-31T20:39:12.493Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/qlooptech/cloudsweeper-cutting-cloud-waste-with-an-ai-finops-agent-580l"
source_title: "CloudSweeper: Cutting Cloud Waste with an AI FinOps Agent"
source_id: 3130234
excerpt: "読み取り専用AIが安全に候補提示、クラウド不要資産を可視化してコストを大幅削減"
---

# CloudSweeper: Cutting Cloud Waste with an AI FinOps Agent - CloudSweeper：AI FinOpsエージェントでクラウドの無駄を削減
驚くほど安全に「捨てていい」ものがわかる──迷わずクラウドコストを削るAIエージェント

## 要約
CloudSweeperは、AWS/Azure環境を読み取り専用でスキャンし、利用メトリクスと設定・履歴をAIで解析して「KEEP / DOWNSIZE / DELETE」の3つの明確な提案を出すFinOpsエージェント。自動実行はせず、信頼度・費用影響・説明トレースを付けてエンジニアが安全に判断できるよう支援する。

## この記事を読むべき理由
- 日本のスタートアップ〜中堅エンジニアチームはFinOps専任を置けないことが多く、コスト最適化は「やりたくても怖い」作業になりがち。  
- CloudSweeperの「読み取り専用＋説明可能なAI」という設計は、日本の現場で受け入れやすい安全性と実用性を兼ね備えているため、導入検討のヒントになる。

## 詳細解説
- アーキテクチャと技術スタック  
  - 言語：Python 3.13（完全async設計）  
  - AWS連携：aioboto3／CloudWatchメトリクス  
  - Azure連携：公式Azure SDK（azure-*）／Azure Monitor  
  - 非同期HTTP：aiohttp、データ検証にPydantic v2、状態保存にAzure Cosmos DB  
  - 環境設定：python-dotenv

- スキャン設計と安全性の方針  
  - 完全読み取り専用のIAM/RBACでアクセス（削除権限は与えない）  
  - 非同期・マルチテナントのスキャナで多数アカウントへスケール  
  - メトリクス駆動のアイドル判定。メトリクス不足や曖昧さがある場合は保守的にスキップする（誤判定回避重視）  
  - 各候補に「人が読める理由」を付与（例：実際のCPU%・閾値・観測期間）

- AIリコメンデーションの特徴  
  - 入力はメトリクス、設定、タグ、履歴を「文脈付きで強化」したもの  
  - 出力は構造化：KEEP / DOWNSIZE / DELETE、信頼度、推定コスト影響、説明トレース  
  - 明示的に「エンジニア・イン・ザ・ループ」：自動実行は行わない設計

- 通知と統合  
  - WebhookでSlack/Teamsなどに通知。ペイロードは詳細な理由とコンテキストを含む  
  - 再送・検証ロジックでデリバリ信頼性を担保

- 設計哲学  
  - 安全性優先、説明可能性重視、ブラックボックスではなく人が判断できる形で支援

## 実践ポイント
- まずは読み取り専用の最低権限ロールを用意して数アカウントで短いスキャンを回す。誤検知リスクを確認しつつ運用ポリシーを作る。  
- 「信頼度スコア」と「コスト影響」を基に段階的に運用ルールを作成（例：信頼度80%以上は通知→オーナー承認で削除候補リスト化）。  
- タグ付け・オーナー情報を充実させることでAIの説明力・信頼性が上がる。日本の組織では「サービス毎のオーナー管理」が効果的。  
- Slack/Teamsのワークフローと連携し、ヒューマンレビューを標準化する（削除は必ず人の承認を挟む）。  
- 定期スキャンを自動化し、月次レポートから費用トレンドとリスクの可視化を行う。これで「放置によるムダ」を継続的に抑制できる。

