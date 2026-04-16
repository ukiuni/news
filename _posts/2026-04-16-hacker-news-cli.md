---
layout: post
title: "Hacker News CLI - Hacker News CLI（ハッカーニュース CLI）"
date: 2026-04-16T00:01:04.048Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://pythonhosted.org/hackernews-cli/commands.html"
source_title: "Commands &mdash; HackerNews CLI  documentation"
source_id: 47785582
excerpt: "ターミナルでHNを即チェック、記事閲覧・コメント投稿まで高速化する軽量CLI"
---

# Hacker News CLI - Hacker News CLI（ハッカーニュース CLI）
ターミナルから一瞬でHNをチェック！開発者向けシンプルCLIで情報収集を高速化

## 要約
hnコマンドはターミナルでHacker Newsを操作する軽量CLI。ストーリー一覧取得、ブラウザで開く、コメント表示・投稿が可能で、キーオプションでソートや件数指定ができます。

## この記事を読むべき理由
日本の開発者も英語圏の技術トレンドを素早く追う必要があります。GUIを開かずに端末でHNを扱えれば、作業フローを崩さずに重要記事をキャッチできます。

## 詳細解説
- 基本コマンド構成: `hn [OPTIONS] COMMAND [ARGS]...`
  - 全体オプション: `--version`（バージョン表示）、`--help`（ヘルプ）
- 主要コマンド:
  - `stories` — ストーリー一覧を表示  
    - オプション: `-s, --sort_by [newest|best]`（並べ替え）  
    - `-l, --limit INTEGER`（表示件数）
  - `go STORY_ID` — 指定ストーリーをHacker Newsで開く（ブラウザへ遷移）
  - `comments STORY_ID` — 指定ストーリーのコメントをターミナルで表示
  - `comment STORY_ID` — ストーリーにコメントを投稿
- 使い勝手: シンプルなサブコマンド設計で、スクリプトやシェルワークフローへ組み込みやすい。

使用例:
```bash
# トップ10の最新ストーリーを表示
hn stories -s newest -l 10

# ストーリーID 12345 をブラウザで開く
hn go 12345

# ストーリーのコメントを表示
hn comments 12345

# ストーリーにコメントを投稿
hn comment 12345
```

## 実践ポイント
- 日常的なニュースチェックは `hn stories -s newest -l 20` をエイリアス化して短縮。
- 気になる記事は `hn go <ID>` を使って即ブラウズ、議論は `hn comments` でローカル確認。
- CIや定期タスクに組み込んで、時間帯ごとの人気トピックを自動収集する運用が可能。
