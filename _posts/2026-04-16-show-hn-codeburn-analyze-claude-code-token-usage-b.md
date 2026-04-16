---
layout: post
title: "Show HN: CodeBurn – Analyze Claude Code token usage by task - CodeBurn：タスクごとにClaude Codeのトークン消費を解析する"
date: 2026-04-16T17:15:14.981Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/AgentSeal/codeburn"
source_title: "GitHub - AgentSeal/codeburn: See where your AI coding tokens go. Interactive TUI dashboard for Claude Code, Codex, and Cursor cost observability. · GitHub"
source_id: 47759035
excerpt: "CodeBurnでClaudeのタスク別トークン消費とコストをローカル解析し無駄を即発見"
image: "https://opengraph.githubassets.com/fd694d5a239d73b953cb972ef045fc9182377126c9232f5fc220d8660b7af29a/AgentSeal/codeburn"
---

# Show HN: CodeBurn – Analyze Claude Code token usage by task - CodeBurn：タスクごとにClaude Codeのトークン消費を解析する
AI開発で「どこにトークンと時間を無駄にしているか」を瞬時に把握できる可視化ツール

## 要約
CodeBurnはローカルに保存されたセッションデータを読み取り、Claude Code／Codex／CursorなどAIコーディングツールのトークン使用・コスト・タスク別成功率をターミナルTUIで可視化するオープンソースツールです。APIキー不要でプライバシー面も安心です。

## この記事を読むべき理由
日本の開発チームでも複数のAIコーディングツールを併用するケースが増えています。請求や無駄な編集ループを抑えるには「どのタスクでトークンが燃えているか」を見るのが近道。特にClaude CodeやCursorのローカルセッションを使う開発者に即効性のある実用ツールです。

## 詳細解説
- 仕組み
  - 各プロバイダのセッションをファイル/SQLiteから読み込み、メッセージごとのtoken使用を抽出して分類・集計します（JSONLやCursor/OpenCodeのDB）。
  - APIやプロキシを介さずローカル読み取りするため、APIキー不要でプライバシーに配慮。
- 対応プロバイダ
  - Claude Code、Claude Desktop、Codex（OpenAI）、Cursor、OpenCode、Pi（将来的にAmpも）。
- 分類と可視化
  - 13カテゴリ（Coding / Debugging / Feature Dev / Refactoring / Testing …）に自動分類。
  - 「one-shot rate」（AIが一発で成功した割合）を計測し、編集→テスト→修正の無限ループを発見可能。
  - モデル別／プロジェクト別／ツール別ブレイクダウン、日別コストチャート、CSV/JSON出力を提供。
- コスト計算と通貨
  - LiteLLMの価格情報をキャッシュしてコストを算出。通貨はISO 4217指定でJPYなどに切替可（為替はFrankfurterを利用）。
- 導入と実行
  - 要件：Node.js 20+
  - インストール：npm install -g codeburn または npx codeburn
  - 代表コマンド：codeburn（TUI） / codeburn today / codeburn month / codeburn report / codeburn export
  - macOS向けにSwiftBarメニューバーウィジェットも提供（codeburn install-menubar）。
- 開発者向け拡張性
  - プロバイダはプラグイン1ファイルで追加可能。src/providersの構造を参照すれば独自プロバイダを実装できます。

## 実践ポイント
- まずはインストールして「codeburn today」を実行し、今日のトークン消費を確認する（Node.js 20+ が前提）。
- 通貨を日本円に設定：codeburn currency JPY
- 「one-shot rate」が低いカテゴリを優先的に調査。低ければプロンプト設計やキャッシュ設定を見直すと即効でコスト削減できる。
- CursorやOpenCodeを使う場合はbetter-sqlite3のオプション依存に注意。初回解析は大きなDBで時間がかかることがあるがキャッシュされる。
- CIや週次レポート用途には codeburn export でCSV/JSONを出力して可視化ダッシュボードや経費報告に組み込む。
- チームで使うならプロジェクト単位のブレイクダウンとモデル別コストを定期チェックして、過剰な高性能モデル利用を抑制する。

興味があればGitHubリポジトリ（AgentSeal/codeburn）をチェックし、READMEのUsage節からすぐに試せます。
