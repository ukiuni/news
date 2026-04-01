---
layout: post
title: "Claude Code Unpacked : A visual guide - Claude Code 分解：ビジュアルガイド"
date: 2026-04-01T06:16:47.720Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://ccunpacked.dev/"
source_title: "Claude Code Unpacked"
source_id: 47597085
excerpt: "ターミナルで動くClaude Codeの内部と40以上のツール、隠し機能を図解で一挙解説"
image: "https://ccunpacked.dev/og-image.png"
---

# Claude Code Unpacked : A visual guide - Claude Code 分解：ビジュアルガイド
ターミナルで動く「Claude Code」の内部を覗く――エージェントループ、40以上のツール、隠し機能まで一気に理解する

## 要約
ソースを読み解き、ユーザー入力がどのように処理されて応答になるかを可視化した非公式ガイド。エージェントループ、ツール群、コマンド群、未公開機能まで網羅している。

## この記事を読むべき理由
Claude Codeはローカル端末でAIエージェントを動かす実践的な実装例で、日本の開発現場でも「自動化」「ローカル実行」「ツール連携」を学ぶ上で参考になるからです。

## 詳細解説
- エージェントループ（重要）
  - 入力 → メッセージ生成 → 履歴管理 → システムプロンプト → API呼び出し → トークン処理 → （ツール呼び出し）→ ループ継続 → レンダリング → フック → 待機、という11段階で動作。たとえばTextInput.tsxがキーボード／stdinを受け取り、ツール呼び出しやトークン制御が中核になっている。
- アーキテクチャ概観
  - 大量のソースツリー（components, tools, commands, services, hooks など多数ファイル）で構成。UI層、コア処理、ツールシステム、インフラ支援が明確に分離されている点が学びやすい。
- ツールシステム（注目）
  - カテゴリ別に多数のビルトインツールを用意。例：
    - ファイル操作（FileRead, FileEdit, FileWrite, Glob, Grep, NotebookEdit）
    - 実行系（Bash, PowerShell, REPL）
    - 検索／取得（WebFetch, WebSearch, ToolSearch）
    - エージェント・タスク（TaskCreate, TaskList, TaskOutput 等）
    - 計画系、MCP（リソース読み取り・認証）など
  - ツール呼び出しで外部プロセスや検索を組み合わせ、エージェントが複雑なワークフローを作る設計。
- コマンドカタログ
  - /init, /login, /review, /commit-push-pr, /session, /files, /tasks, /debug-tool-call 等、日常ワークフローからデバッグ、実験的機能まで幅広いスラッシュコマンドを備える。
- 隠し機能（未公開やフラグ管理）
  - Buddy（ターミナル上のペット）、Kairos（永続モード＋メモリ統合）、UltraPlan（長時間プラン実行）、Coordinator Mode（タスク分散）、Bridge（リモート操作）、Daemonモード、UDS Inbox、Auto‑Dream（セッション間の学習整理）など。実運用での拡張性／運用性の高さを示す。

## 実践ポイント
- 学習用途：エージェントループの各フェーズを小さなデモで再現してみる（入力→トークン→ツール呼び出し→レンダリング）。
- ツール設計：自分のプロジェクト用に「ファイル操作」「実行」「検索」等の小さなツール群を定義し、エージェントから呼べるようにする。
- 既存ワークフロー統合：/review や /commit-push-pr のようなコマンド設計を参考に、CIやコードレビュー自動化をローカルで試す。
- 日本向け注意点：社内コードや顧客データを扱う場合はデータ取り扱いと社内ガバナンスを最優先に。未公開機能は安定性やセキュリティ面で慎重に扱う。

（非公式解析に基づくまとめ。元資料は Claude Code の公開ソースをもとにした第三者の解析です。）
