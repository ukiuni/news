---
layout: post
title: "If AI writes code, should the session be part of the commit? - AIがコードを書いたら、そのセッションをコミットに含めるべきか？"
date: 2026-03-02T04:44:44.448Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/mandel-macaque/memento"
source_title: "GitHub - mandel-macaque/memento: Keep track of you codex sessions per commit"
source_id: 47212355
excerpt: "AIとの対話をコミットに紐付け、監査やガバナンスを実現するgit-mementoの実践導入法"
image: "https://opengraph.githubassets.com/c6e304ca6735ea5f9f597b9cd08636bb3ecbb5b8a781eeebad294aae26e8acf5/mandel-macaque/memento"
---

# If AI writes code, should the session be part of the commit? - AIがコードを書いたら、そのセッションをコミットに含めるべきか？
コミットに「AIとの会話」を残す――透明性と追跡性を手に入れるgit-memento入門

## 要約
git-mementoは、AI（CodexやClaudeなど）で行ったコーディングセッションをコミットに紐づけ、会話をMarkdown形式のgit noteとして保存・共有・監査できるツールです。

## この記事を読むべき理由
日本の開発現場でもAI補助開発が急速に普及する中、誰がどんな指示を出したか、どのAIセッションがあるかを確実に残す仕組みは法務・セキュリティ・コードレビューで重要になります。git-mementoはその実務的解決策を提供します。

## 詳細解説
- 基本概念：git-mementoはコミット実行後にAIとの会話を整形したMarkdownをgit notesに書き込み、コミット履歴に「プロンプトと応答の痕跡」を紐付けます。ノートはrefs/notes/*として扱われるため既存のGit運用と併存可能です。  
- サポートプロバイダ：デフォルトはCodex。環境変数（例：MEMENTO_AI_PROVIDER）やローカルgit設定でCodex/Claudeを切替可能。セッション取得コマンドも設定可能で拡張設計。  
- 主なコマンド：`git memento init`（リポジトリ設定）、`git memento commit <session-id> [-m ...]`（セッションを添えてコミット）、`git memento amend <session-id>`、`git memento audit --range <base>..HEAD`（ノート漏れの検出）、`git memento notes-sync`（リモートと同期）、`git memento notes-rewrite-setup` / `notes-carry`（rebase/amendでのノート継承）など。  
- ノート構造：マルチセッション対応で明確なデリミタ（例: <!-- git-memento-session:start -->）を持ち、ユーザ発言はgit user.name、AI発言はプロバイダ名でラベル付け。古い単一セッション形式も互換性維持で扱えます。  
- CI連携：Marketplace向けのActionがあり「comment」モードでプルリクに会話ノートを投稿、「gate」モードでaudit結果をCIゲートにできます。インストール用actionや例示ワークフローが用意済み。  
- ビルド／導入：.NET 10 + NativeAOTでビルドされ、リリースは単一バイナリ。curlワンライナーのinstall.shでインストール可能。ローカルではgit-<name>命名規則でgitコマンドとして動作。  
- 運用上の注意：ノートはリポジトリの一部として共有可能だが、機密情報や個人データを含めないポリシー設計が必要。rebaseやsquashを使うワークフローではnotes-rewrite-setupやnotes-carryで履歴保持を整備する。

## 実践ポイント
- まず実験用リポジトリで導入：`curl -fsSL https://raw.githubusercontent.com/mandel-macaque/memento/main/install.sh | sh` を試してから `git memento init`。  
- PRパイプラインにActionを追加して、`mode: gate` でノート未付与コミットをCIで拒否する仕組みを作る。  
- rebaseやsquashを多用するチームは `git memento notes-rewrite-setup` と `notes-carry` を採用して会話の継承を確保。  
- 社内ルールを決める：AIプロンプトのログ保存方針、機密情報除外ルール、レビュー時の確認項目（プロンプトの有無・プロバイダ名・セッションIDなど）。  
- 日本企業向けには、監査証跡・IP帰属・セキュリティ要件を満たすために、まずは部分導入（CI gate + audit）から始めるのが現実的です。
