---
layout: post
title: "Agent22 - 共通タスク向け opencode ラッパー"
date: 2026-02-23T10:31:41.831Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/cubixle/agent22"
source_title: "GitHub - cubixle/agent22"
source_id: 398713222
excerpt: "OpenCodeでJIRA/GiteaのPR作成とレビューを低コストで自動化するAgent22"
image: "https://opengraph.githubassets.com/06c3f97be69c7e96a2676a608d37f86f095c4fd6afbaa858e8616974a39cd116/cubixle/agent22"
---

# Agent22 - 共通タスク向け opencode ラッパー
定型作業を静かに自動化する──JIRA×Gitea×OpenCodeで「無駄なトークン消費」を減らす実用ツール

## 要約
Agent22はGo製の自動化エージェントで、JIRAのチケットやGiteaのPRに対してOpenCodeを使った実装／レビューを定型的に実行し、無駄なプロンプトやトークン消費を減らすことを目的とします。

## この記事を読むべき理由
日本の開発現場でも「定型的な小さな修正」「レビュー対応」「チケット→ブランチ→PRの流れ」は頻発します。Agent22はこれらをAPI直結で安定実行し、LLM利用コストとノイズを下げつつレビュー文化を残す設計です。

## 詳細解説
- 目的：既に定義された繰り返しワークフロー（例：チケット実装→PR作成→レビュー反映）をOpenCodeに直接渡して実行し、余計な説明やエージェントの“おしゃべり”を省く。直接mainへpushせずPRを作ることで自動化で失われがちな「変化の把握」も担保する。
- 動作モード：
  - チケットモード（デフォルト）: JIRAのJQLで該当チケットをポーリングし、ローカルでベースブランチを同期→ISSUE-KEYブランチを作成→OpenCodeで実装→レビュー適用→コミット・PR作成→JIRAを完了へ遷移。
  - プルリクモード（--pull-request-mode）: GiteaのオープンPRを監視し、レビューコメントごとにOpenCodeで修正を提案・反映。
- フローの特徴：
  - プロンプトは内部ガードレール、チケット要約・説明、ローカルのAGENTS.mdなどから生成。
  - 実行はopencode run <prompt>で行い、進行はコンソールにわかりやすく表示。
  - 重複ノイズやエージェント生成コメントはフィルタリング。
- 前提・必須：
  - Go と git と opencode がPATHにあること、opencodeで認証済みであること、作業ディレクトリに .agent22.yml があること。
- 統合：JIRA、Gitea、OpenCode に対応。設定は .agent22.yml で管理（JQL、ベースブランチ、トークン等）。

## 実践ポイント
- まずはローカルで動かす：.agent22.example.yml をコピーして最小限の設定を入れ、opencode auth を済ませてから試す。
- 設定例（抜粋）：

```yaml
work_provider: "jira"
wait_time_seconds: 30
jira:
  email: "you@example.com"
  api_token: ""
  jql: "project = EXAMPLE AND status = 'ready'"
git_repo: "your-repo"
git_base_branch: "main"
gitea_owner: "your-gitea-owner"
gitea_token: ""
gitea_base_url: "https://gitea.example.com"
```

- 実行コマンド例：

```bash
# チケットモード（デフォルト）
go run .

# プルリクモード
go run . --pull-request-mode
```

- 運用のコツ：
  - AGENTS.md にチームの実装ガイドラインを置くとOpenCodeの出力が安定する。
  - 機密ファイルや自動生成ファイルをコミット対象から除外する設定を確認する。
  - まずは少数のチケットで試験運用し、PRのレビュー頻度と自動修正の品質を監視する。
- 日本市場への示唆：JIRA運用が多い企業や、LLM利用のコストに敏感なチームに特に有用。レビュー文化を残したまま効率化を図りたい現場に導入価値が高い。

以上を踏まえ、まずはテスト環境で安全に動かして「どの程度の修正を自動化できるか」を評価すると良いでしょう。
