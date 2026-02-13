---
layout: post
title: "PlanDrop: a Chrome extension to control Claude Code on remote servers with plan-review-execute workflow - PlanDrop：Claude Codeをリモートで「計画→確認→実行」するChrome拡張"
date: 2026-02-13T02:02:20.148Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/genecell/PlanDrop"
source_title: "GitHub - genecell/PlanDrop: Chrome extension for plan-review-execute workflows with Claude Code on remote servers. Type a task in your browser, review the plan, authorize execution over SSH."
source_id: 443133143
excerpt: "リモートGPU/HPCでClaude Codeを計画確認し手動承認で安全実行、監査ログ付き"
image: "https://opengraph.githubassets.com/b9449c0510976749c9e45b26fc3c3cd8c219ca57088e3e01c919b218dd7466d3/genecell/PlanDrop"
---

# PlanDrop: a Chrome extension to control Claude Code on remote servers with plan-review-execute workflow - PlanDrop：Claude Codeをリモートで「計画→確認→実行」するChrome拡張

魅力的な日本語タイトル：リモートGPU/HPCでAIに勝手に触らせない — 「計画確認」が必須のPlanDropで安全に自動化する方法

## 要約
ブラウザからタスクを送ってAI（Claude Code）にリモートサーバ上でコードを実行させるが、実行前に必ず「計画（read-only）」をレビューしてから手動で承認する仕組みを提供するChrome拡張。SSHとファイルキューだけで動き、第三者のサーバを介さない点が特徴。

## この記事を読むべき理由
日本の研究室や企業のGPUサーバ、HPC環境ではデータ漏洩や誤操作が致命的。PlanDropは「AIに自動で任せっぱなし」にしない設計で、監査ログや再現性も残せるため、セキュリティやコンプライアンスを重視する現場に有用です。

## 詳細解説
- 全体像：Chrome拡張（サイドパネル）⇔ネイティブメッセージング（ローカルPython）⇔既存のSSH設定を使ってリモートの .plandrop/ ディレクトリにJSON/MDファイルを往復。サーバ側の watch.sh がファイルを監視し、Claude Code CLI を実行する。
- 強み
  - 強制的な人間による承認：AIは「計画」を提示するだけで、ファイル編集やコマンド実行はブラウザでのExecuteクリックがないと走らない（アーキテクチャで実現）。
  - インフラ不要：専用サーバやWebSocketは不要。SSHアクセスだけで始められる。
  - 再現性と監査：全プロンプト・応答をファイルで保存しgit管理可能。誰が何を承認したか追跡できる。
- モード
  - Interactive（計画→レビュー→実行）: 計画を読んで承認、ブロックされたコマンドは個別承認、実行中は進捗・コストをフィードバック。
  - Quick Drop：選択テキストやMarkdownをそのままプロジェクトにscpで送る簡易モード。
- 技術スタックと要件（概略）
  - ローカル：Chrome/Edge/Brave、Python 3、SSH鍵
  - サーバ：Node.js 18+（Claude Code CLI）、SSHアクセス、plandrop-watchスクリプト
  - インストール要点：Claude Codeのnpmインストール、サーバで plandrop-watch --init と watcher 起動、拡張はデベロッパーモードで読み込み、native-host を登録。
- セキュリティ面
  - データは第三者経由しない（SSH直結）。ただしサーバ側での権限管理、SSH鍵の保護、AN­THROPIC_API_KEY等の取り扱いは必須管理項目。

## 実践ポイント
- まず試す：ローカルでChrome + Python3、サーバにNode.js入れて claude install → plandrop-watch --init → plandrop-watch（tmux推奨）。
- 拡張導入：リポジトリをクローンして chrome://extensions から Load unpacked、native-host の install.sh に拡張IDを渡す。
- 設定：拡張のSettingsでサーバ名（~/.ssh/configのHost名を一致させる）とプロジェクトパスを登録、Interactive Modeを有効化して権限プロファイルを設定。
- 運用ルール案：本番データはRead-onlyプロファイルでテスト、重要操作は複数承認ルール（人間の確認を複数段階）を運用に組み込む。
- 日本環境での活用例：大学の計算機センター、製薬/バイオ系のクローズドGPU環境、社内プライベートクラウドでの安全なAI支援ワークフロー。

興味があるなら、まずリポジトリのREADMEのQuick Startでサーバ側セットアップ（claude CLI、plandrop-watch）を試してみてください。
