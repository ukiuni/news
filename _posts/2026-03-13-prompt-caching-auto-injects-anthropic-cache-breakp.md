---
layout: post
title: "Prompt-caching – auto-injects Anthropic cache breakpoints (90% token savings) - Anthropicキャッシュブレークポイント自動挿入（90%トークン節約）"
date: 2026-03-13T12:27:36.522Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://prompt-caching.ai/"
source_title: "prompt-caching — 90% Token Savings for Claude Code"
source_id: 47363074
excerpt: "prompt-cachingでClaudeの反復トークン費用を約90%節約"
image: "https://prompt-caching.ai/assets/og.png"
---

# Prompt-caching – auto-injects Anthropic cache breakpoints (90% token savings) - Anthropicキャッシュブレークポイント自動挿入（90%トークン節約）
Claudeの請求を90%削る？「prompt-caching」で繰り返しコストを自動キャッシュ化する方法

## 要約
AnthropicのキャッシュAPIを自動で活用するプラグイン「prompt-caching」は、安定したプロンプト要素を検出してキャッシュブレークポイントを挿入し、反復的なやり取りのトークンコストを平均90%削減します。

## この記事を読むべき理由
Claude（特にClaude Code）やMCP対応クライアントを使う日本の開発者・チームは、繰り返しのコードレビュー・リファクタ・バグ修正で発生するトークン課金を大幅に下げられ、コスト最適化と応答速度改善の両方が期待できます。

## 詳細解説
- 仕組み：Anthropicのサーバー側キャッシュは5分間有効で、キャッシュ作成は通常の1.25×コスト、以降の読み取りは0.1×コストになる。prompt-cachingは安定した要素（システムプロンプト、ツール定義、ファイルの読み取りなど）を自動検出してキャッシュの区切り（breakpoint）を差し込み、以降のターンで低コスト読み取りに切り替える。
- モード：
  - BugFix：スタックトレースを検出して該当ファイル＋エラー文脈をキャッシュし、以降は新規質問のみ課金。
  - Refactor：リファクタ指示とファイル一覧を検出し、変更前のパターンや型定義等をキャッシュ。
  - File Tracking：ファイルの読み取り回数を追跡し、2回目以降をキャッシュ化。
  - Conversation Freeze：Nターン後に過去メッセージをキャッシュ化して最新3ターンのみを新規送信。
- ベンチマーク（一例）：バグ修正セッションで85%削減、リファクタで80%、一般コーディングで92%、繰り返しファイル読みで90%。
- 対応環境：Claude Code推奨だが、Cursor・Windsurf・ChatGPT・Perplexity・Zed・Continue.devなどMCP互換クライアントにも対応。OSS・MITライセンスで導入のハードルが低い。

## 実践ポイント
- Claude Code内での即時導入（設定不要）
  ```bash
  # Claude Code のチャット内コマンド
  /plugin marketplace add https://github.com/flightlesstux/prompt-caching
  /plugin install prompt-caching@ercan-ermis
  ```
- 他MCPクライアントの場合（npmグローバル）
  ```bash
  npm install -g prompt-caching-mcp
  ```
  その後クライアントのMCP設定に追加して有効化する。
- 運用上の注意：
  - キャッシュ作成は初回でやや割高（約1.25×）だが、2ターン目以降は大幅節約。短いやり取りでは効果が薄いが、反復的なワークフロー（バグ調査、リファクタ、ファイルの多読）で効果絶大。
  - インストール後に提供される get_cache_stats 等のツールでヒット率と節約効果をモニタリングする。
- 試すべきワークフロー：大きなレポジトリでの反復レビュー、IDE統合したペアプロ、CI前の自動チェックなどでまず試す。

原文・コードはGitHubで公開（MIT）。まずは小さなセッションで動作と節約率を確認してから本番導入を検討してください。
