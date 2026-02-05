---
layout: post
title: "Introducing the GitButler CLI - GitButler CLIの紹介"
date: 2026-02-05T17:07:19.063Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.gitbutler.com/but-cli"
source_title: "Introducing the GitButler CLI | Butler&#x27;s Log"
source_id: 408523784
excerpt: "GitButlerの新CLI「but」でコンフリクトや履歴編集、PR作成が直感的に安全・高速化"
image: "https://gitbutler-docs-images-public.s3.us-east-1.amazonaws.com/introducing-cli.webp"
---

# Introducing the GitButler CLI - GitButler CLIの紹介
もうgitで詰まらない！“but”コマンドでコンフリクト・操作履歴・PRがぐっと楽になる次世代CLI

## 要約
GitButlerの新CLI「but」は、既存のGitワークフローに自然に入るモダンなコマンドラインツールで、スタック/並列ブランチ、無制限のUndo、コミット編集、Forge連携、JSON出力、AIスキルなどを提供します。

## この記事を読むべき理由
国内でもMac＋GitHub/GitLabを使う開発者が増える中、複雑なrebaseやstashに悩む初級〜中級者にとって作業の安全性と効率を一気に上げるツールだからです。CIやPR中心の開発文化にも直結します。

## 詳細解説
- インストール: GitButlerデスクトップから「Install CLI」を押すか、Homebrewで
```bash
brew install gitbutler
```
Mac向けの簡易インストーラも提供中（将来的に他OS対応予定）。

- 基本コマンド: 普通のgitに似た操作が可能（but status, but commit, but push, but branch 等）。ただし内部はより高レベルな概念を扱います。

- 並列ブランチ (Parallel branches): フィーチャー作業中にバグを見つけてもstashせずに
```bash
but branch new bug-fix
```
で並列ブランチを作成し同一作業ディレクトリで分離してコミットできます。

- スタックドブランチ (Stacked branches): 依存関係のある複数のブランチを「積む」ことで、PR作成や差分管理が楽に。下位ブランチを編集しても上位が自動でrebaseされ整合されます。

- コミット編集: rebase -iが苦手でも
  - but reword（メッセージ編集）
  - but uncommit（コミット内容を未コミットに戻す）
  - but amend / but move / but squash / but absorb（未コミット変更を最適なコミットへ吸収）
で柔軟に履歴を整形できます。

- Undoと操作ログ: 変更を行うコマンドは操作ログを残し、任意のセーブポイントへ戻せる（but undoで直前取り消しも可能）。

- Forge連携とPR管理: but prで未作成の適用ブランチに対してPRを作成・管理。CIステータスをバックグラウンドでチェックし、but statusで可視化できます。

- スクリプト化・機械向け出力: すべてのコマンドに--json / -jを付ければ機械可読な出力が得られ、CIや自動化エージェントとの親和性が高い。

- AIスキル: but skill installでエージェント向けスキルを追加し、より高度な自動化や提案を受けられます。

## 実践ポイント
- まずはHomebrewで導入し、手持ちのリポジトリで
```bash
but
but status
```
を試す。視認性とステータスの違いを体感すること。

- バグ対応はstashより並列ブランチで：but branch new bug-fix → 修正 → but prでPR作成。

- 履歴の微調整は but absorb / but reword を活用。rebase -iを避けたい場面で有効。

- 自動化やCI連携には --json を使って出力をパースし、ツールチェーンに組み込む。

- チームで採用する前にローカルでUndo/ログ復元を検証し、運用ルール（stacked branchの使い方等）を共有する。

著者はScott Chacon（GitHub共同創業者）で、今後もCLIは強化予定。試してフィードバックを送ることで日本の現場に合った改善も期待できます。
