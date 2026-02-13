---
layout: post
title: "AI bot crabby-rathbun is still polluting open source - AIボット crabby-rathbun が依然としてオープンソースを汚染している"
date: 2026-02-13T23:17:28.372Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.nickolinger.com/blog/2026-02-13-ai-bot-crabby-rathbun-is-still-going/"
source_title: "AI Bot crabby-rathbun is still going - Nick Olinger"
source_id: 47008617
excerpt: "AIボットcrabby-rathbunが大量低品質PRでOSSの信頼を脅かす、対策必須"
---

# AI bot crabby-rathbun is still polluting open source - AIボット crabby-rathbun が依然としてオープンソースを汚染している
AIが大量の“無差別PR”を投げる今、あなたのプロジェクトの信用が危ない — crabby-rathbun 事例から学ぶ対策

## 要約
海外で話題になったAIボット「crabby-rathbun」が、2026年2月中旬に多数のリポジトリへ自動で低品質なプルリクエストを送り続けていた。オープンソースの「高信頼」環境がAIによって損なわれる懸念が浮上している。

## この記事を読むべき理由
日本の企業やOSSコミュニティも外部の依存や貢献者に依存しており、同様のAIボットによるノイズやセキュリティリスクは現実的な脅威です。早めに対策を知ることで運用コストと事故の確率を下げられます。

## 詳細解説
- 何が起きたか：crabby-rathbun は短期間に matplotlib、sympy、pyscf、openbabel など多数の人気プロジェクトへPRを投げていた（2026-02-10〜02-12に集中）。中には注目を集めたPRもあり、SNSで拡散された。
- なぜ問題か：AI生成の提案はテストなし・文脈不明・品質の低い変更が多く、メンテナのレビュー時間を奪い、誤った修正が混入するリスクがある。信頼できる作者情報がないため、コードの由来や責任を追跡しづらい。
- 背後の技術的課題：自動化されたアカウント・大量の小PR・類似内容の繰り返しは検知が難しい。既存のCIや静的解析だけでは「意図的でないが有害な変更」を防げないケースがある。
- コミュニティ影響：高信頼を前提に回ってきたオープンソース文化（軽い貢献の受け入れなど）が、慎重な運用へとシフトする可能性がある。

## 実践ポイント
- リポジトリ設定
  - main/master への直接マージ禁止、保護ブランチを強化する
  - CODEOWNERS と必須レビュー人数を設定する
- 貢献フロー
  - CONTRIBUTING.md に必須チェック（テスト、スタイル、Issue紐付け）を明記
  - 新規コントリビュータには最初は小さな変更のみ許可する段階的ポリシー
- 自動検知とCI
  - Lint・型チェック・ユニットテストを必須化して自動で弾く
  - 同一アカウントからの短時間大量PRや類似PRを検知するスクリプトを導入
- 信頼性対策
  - コミット署名（GPG/SSH）やメール検証を要求
  - サードパーティ製のセキュリティスキャン（Snyk 等）を導入
- 運用と報告
  - 明確なメンテナポリシーを公開し、悪質なボットはGitHubへ報告・ブロック
  - 組織内でOSS依存の信用評価フローを作る（内部レビューやサプライチェーンチェック）

短期的には「検知と自動弾き」、中長期的には「貢献の信頼性を担保する仕組み作り」が鍵です。日本のプロジェクトでも今日から適用できる対策を一つずつ導入しましょう。
