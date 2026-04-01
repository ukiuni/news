---
layout: post
title: "Show HN: Baton – A desktop app for developing with AI agents - Baton — AIエージェントと開発するためのデスクトップアプリ"
date: 2026-04-01T14:05:58.473Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://getbaton.dev/"
source_title: "Baton — A Desktop App for Developing with AI Agents"
source_id: 47599771
excerpt: "衝突ゼロでローカル複数AIを独立ブランチで並行開発、差分確認とPR作成もGUI完結"
image: "https://getbaton.dev/og-image.png?v=2"
---

# Show HN: Baton – A desktop app for developing with AI agents - Baton — AIエージェントと開発するためのデスクトップアプリ
AIエージェントに「独立ブランチで作業させる」新常識—Batonで衝突ゼロのAI開発ワークフローを試す

## 要約
Batonはローカルで動くデスクトップアプリで、複数のAIコーディングエージェントをそれぞれ独立したgit worktree（ブランチ）で並行実行・監視・レビューできるツールです。差分確認→PR作成までGUIで完結します。

## この記事を読むべき理由
日本のチームでも「AIにコードを任せる」運用を安全に試行でき、複数エージェントの衝突やコンテキスト切替を大幅に減らせるからです。オンプレや機密コード運用の懸念がある企業にも受け入れやすい設計です。

## 詳細解説
- アーキテクチャと主張
  - 各エージェントは実際のgit worktree（別ディレクトリ＋別ブランチ）で動作。エージェント同士がファイルを上書きするリスクが無く、stash/checkoutの手間が不要です。
  - エージェントはCLIネイティブで動くものなら基本対応（Claude Code、Codex CLI、Gemini CLI、OpenCodeなどをファーストクラスでサポート）。
  - Baton自体はローカル実行が原則。AIによるブランチ名や説明文の自動生成のみ任意でクラウドAPIを使い、コードは端末外に送られないと明記。

- 主要機能
  - ワークスペース生成：プロンプトで新しいワークスペース（ブランチ）を即作成。Accept Editsで自動編集を許可可能。
  - モニタリング：完了・入力待ち・エラーをラベルで一目表示。ライブでエージェントの変更を追える「Live follow」。
  - 差分とレビュー：Monacoベースのdiffビューアでファイル単位のロールバック・ライブ差分確認。PR作成はGitHub/GitLabにワンクリック。
  - ターミナル重視：本物のターミナル（複数タブ・分割）を内包し、既存CLIツールやスクリプトをそのまま使える。
  - 検索・履歴：fzf／ripgrepベースの高速検索、コミット履歴・ファイル履歴の確認。
  - カスタム化：エージェント起動プリセット、MCPサーバ経由でエージェントが新ワークスペースを作る等の自動化が可能。
  - マルチプラットフォーム：macOS（Intel/Apple Silicon）、Windows（x64/ARM64ベータ）、Linux（x64/ARM64ベータ）を提供。

- 制約と運用上の注意
  - Gitが必須。ワークツリーは標準のgit worktreeなので他ツールとの互換性あり。
  - 無料版は同時ワークスペース4つまで。$49の一度きり課金で無制限解放。
  - LinuxではAppImage実行にFUSE等の追加が必要。ダウンロードチェックのためSHA256公開。

## 実践ポイント
- まずは無料版で試す：ローカルで動くのでプライベートリポジトリで安全に検証可能。
- 前提準備：Gitインストール、Linuxなら fuse/libfuse2 を用意してAppImageを実行。
- エージェントの選定：最初はClaude CodeやCodex CLIなど既にサポートが手厚いエージェントを使うと機能をフル活用しやすい。
- ワークフロー設計：機能ごとにワークスペースを切ってAccept Editsは慎重に。差分を必ずレビューしてからPR。
- 企業導入時：APIキーの管理やクラウド機能のオン/オフ設定をポリシーに合わせて厳格化（BatonはBYO APIキーやクラウド無効化が可能）。
- IDE連携：VS Codeなど既存IDEで編集したければBatonからワークtreeを開くだけでシームレスに併用可能。

短時間で「AIエージェントを複数安全に回す」体験を得られるツールなので、まずは実プロジェクトの小さなタスクで検証してみてください。
