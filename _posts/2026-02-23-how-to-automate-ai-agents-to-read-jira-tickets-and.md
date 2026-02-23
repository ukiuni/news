---
layout: post
title: "How to automate AI agents to read JIRA tickets and create pull requests - JIRAチケットを読んでプルリクを自動作成するAIエージェント活用法"
date: 2026-02-23T15:07:41.066Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://iain.rocks/blog/how-to-automate-ai-agents-to-read-jira-tickets-and-create-pull-requests"
source_title: "How to automate AI agents to read JIRA tickets and create pull requests | Iain Cambridge"
source_id: 398547656
excerpt: "JIRAチケットからPR作成までAIで自動化する実務向けガイド"
---

# How to automate AI agents to read JIRA tickets and create pull requests - JIRAチケットを読んでプルリクを自動作成するAIエージェント活用法
AIに「チケットを読んでコードを書き、PRを作る」まで任せる——実務で使える自動化ガイド

## 要約
AIエージェントにJIRAチケットの調査〜ブランチ作成〜コミット〜プルリク作成までの一連作業を任せるための実践的なルール集。Junie、Claude、Geminiで検証済みのワークフローとプロジェクト固有ルール（DevHelm/Symfony）を整理している。

## この記事を読むべき理由
AIで単純作業を自動化すれば、レビュープロセスを人間の判断に集中させられる。日本の開発現場でも、チケット→PRの流れを安定化させることでスループットと品質を同時に上げられる。

## 詳細解説
- 基本フロー（AIが従うべき順序）
  1. 指示例: "Please work on ticket DEVHELM-144" を受け取る。  
  2. チケットリサーチ：説明、ラベル、コメント、添付、関連Confluence、履歴、受け入れ基準、Gherkinがあれば機能ファイル化。担当を指示者のリード開発者にアサイン。  
  3. チケット状態を「IN PROGRESS」に移す。  

- Gitワークフロー（AIが自動で行う操作）
  - mainブランチ同期 → featureブランチ作成 → 変更 → ステージ → コミット → push → PR作成
  - 重要ルール：コミットメッセージはJIRAプレフィックス（例：DH-123）を必ず先頭に入れる。PHP変更があればphp-cs-fixerを実行。
  
  例（基本コマンド）:
  ```bash
  # ブランチ準備
  git checkout main
  git pull --rebase origin main
  git checkout -b feature/DH-144-some-fix

  # 変更をステージしてコミット
  git add .
  git commit -m "DH-144: fix foo bar"
  git push origin feature/DH-144-some-fix
  ```
- プルリク作成と更新ルール
  - 新タスクには必ずPRを作る。既存PRには新しいPRを作らず同一ブランチへ追加コミットで更新。
  - PRタイトル・説明にチケット参照、レビュワー割当（例: that-guy-iain）、JIRAリンクを入れる。
  - CIビルドのステータスをポーリングして失敗対応（例：1分間隔でチェック）。

- DevHelm（Symfony/Vue）固有ガイドライン（要点）
  - 環境: Symfony 7.2 + PHP 8.2+ / Vue 3 / Webpack Encore / Tailwind
  - コードスタイル: PHPは属性優先（#[Route(...)]）、php-cs-fixer実行必須
  - テスト: Jest（JS）、PHPUnit（PHP）、Behat（BDD）。テスト配置規約と実行コマンドを徹底。
  - アーキテクチャ: DTO/Repository/Controllerの役割分離、単一クラス／ファイル、DoctrineはApp\Repository内のみ
  - 注意点: webpack.config.js のよくあるタイプミスや、Jest vs Vitestの混在など運用上の落とし穴

- 自動化の実装ポイント
  - エージェント用のガイドラインファイル群を用意し、段階的に実行可能な指示セットを与える（リサーチのみ→実装→PR作成など途中停止対応が容易に）。
  - エージェントが参照するメタ情報（~/agent_info.txt など）にリードやレビュワー情報を置く。

## 実践ポイント
- 小さなチケット（ドキュメント修正や軽微バグ）でまず試す。失敗リスクが低くフィードバックが速い。  
- CIとphp-cs-fixerを必須にして、スタイル・テストで自動ゲートを作る。  
- コミットメッセージとPRテンプレを厳格化して、JIRAとのリンクを自動付与するスクリプトを用意する。  
- エージェントに「必ず人間が最終レビューする」チェックポイントを残す（自動マージは当面NG）。  
- 使用モデルはJunie/Claude/Geminiで検証済みだが、プロンプトとルール整備で挙動は大きく変わるためログを取りつつチューニングする。

短期的には工数削減、中長期ではレビュー品質向上が見込める。まずはガイドラインファイルを用意して小さなタスクで試してみてください。
