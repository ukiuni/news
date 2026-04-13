---
layout: post
title: "GitHub Stacked PRs - 積み上げ式プルリクエスト"
date: 2026-04-13T21:38:39.120Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.github.com/gh-stack/"
source_title: "GitHub Stacked PRs | GitHub Stacked PRs"
source_id: 47757495
excerpt: "Stacked PRsで段階的に差分を分割、gh stackで即時安全マージ"
---

# GitHub Stacked PRs - 積み上げ式プルリクエスト
大きな変更を「小さな層」に分けてレビュー・マージを一気に実現する、新しいGitHubネイティブワークフロー

## 要約
Stacked PRsは、大きな差分を順序付けられた小さなPRの積み重ね（スタック）に分割し、各層を独立してレビューしつつ一括で安全にマージできるGitHubの機能と、それを補うgh stack CLIの組合せです。

## この記事を読むべき理由
レビュー負荷やコンフリクトで開発が滞りがちな日本のチームにとって、レビュー効率向上とマージの信頼性を同時に担保する現実的な手段だからです。

## 詳細解説
- スタックの構造：各PRは直下のPRのブランチをベースにした連鎖（最終的にはmainへ到達）。GitHub側でスタックマップを表示し、レイヤー間の移動や差分確認が容易。
- CI・保護ルール：各PRは最終ターゲットに向けた動作を模擬する形でCIが走り、ブランチ保護ルールも最終ターゲットに対して適用されるため安全性が高い。
- マージとリベース：スタックは一括（または一部）マージ可能。マージ後、残るPRは自動でカスケードリベースされ、次にマージすべきPRが常に最下部で最終ターゲットを指す状態になる。
- gh stack CLI：ローカルでのブランチ作成、カスケードリベース、push、PR作成を簡単にするコマンド群。UIとCLIが連携してワークフローを完結させる。
- AI連携：npx skills add github/gh-stack でCODINGエージェントにスタック操作を学習させ、自動化を進められる（現状はプライベートプレビュー・ウェイトリストあり）。

## 実践ポイント
- まず試すコマンド（ghが必須）:

```bash
# bash
gh extension install github/gh-stack
gh stack alias
gs init auth-layer
# コミットを作業
gs add api-routes
# コミット
gs add frontend
gs push
gs submit
```

- レイヤー設計のコツ：API/契約、ビジネスロジック、UIの順で分けるとレビューしやすい。
- CIとブランチ保護は必須：各PRが最終ターゲット相当でCIを通す前提なので、保護ルールとテストを整備する。
- マージ戦略：小さく頻繁にマージする方が衝突が減る。マージキューと自動リベースを活用する。
- チーム導入案：最初は1つのリポジトリでトライアルを行い、レビュー時間・コンフリクト発生率をKPIで比較する。

（注）Stacked PRsは現時点でプライベートプレビューのため、利用にはウェイトリスト登録が必要な場合があります。
