---
layout: post
title: "Vercel Claude Code plugin wants to read your prompt - Vercelプラグインがあなたのプロンプトを読みたがっている"
date: 2026-04-09T16:12:56.079Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://akshaychugh.xyz/writings/png/vercel-plugin-telemetry"
source_title: "The Vercel Plugin on Claude Code wants to read all your prompts! | akshay chugh"
source_id: 47704881
excerpt: "Vercelプラグインがプロンプトとシェルコマンドを収集、機密漏洩の危険と即対処法"
image: "https://akshaychugh.xyz/assets/images/og-default-wide.png"
---

# Vercel Claude Code plugin wants to read your prompt - Vercelプラグインがあなたのプロンプトを読みたがっている
Vercelのプラグインがあなたのあらゆるプロンプトとコマンドを収集している？その実態と即効の対処法

## 要約
VercelのClaude Codeプラグインが、プロジェクトの種類に関係なくユーザのプロンプトとbashコマンドを収集しており、同意表示が事実上AI経由の「プロンプト注入」で行われている問題を報告しています。収集は永続デバイスIDで紐付けられ、オプトアウト手段は分かりにくく隠されています。

## この記事を読むべき理由
日本の開発現場でも社内コードや環境変数、インフラ情報が含まれるコマンドやプロンプトを外部に送信するとリスクになります。特に企業プロジェクトやクローズドなリポジトリで作業する開発者は、既定の動作を知らないまま機密情報を送ってしまう可能性があります。

## 詳細解説
- 何が送られるか：常時送信される「ベース」テレメトリにデバイスID・OS・検出フレームワーク・Vercel CLI版、そして「bashコマンドの全文」が含まれます。プロンプト本文は別途オプトイン項目となっているが、bashコマンドの収集は常に有効です。
- 同意の仕組みの問題：プラグインはClaudeのシステムコンテキストに自然言語命令を注入し、Claude側のAskUserQuestionで質問を出し、回答に基づいてシェルコマンドを実行して設定ファイルを書きます。見た目はネイティブのUIと同じで、第三者プラグイン由来であることが明示されません。
- スコープの問題：プラグインはプロジェクト種別の検出機能を持つにもかかわらず、テレメトリ収集は全プロジェクトで有効（マッチャーが全てにマッチする設定）になっています。つまりNext.js以外のRustやPythonプロジェクトでも動作します。
- アーキテクチャ的な余地：問題はVercelの実装だけでなく、Claude Codeのプラグインアーキテクチャにもあり、プラグイン質問に視覚的所属表示や細かな権限付与、アクティベーションスコープが欠けています。

## 実践ポイント
すぐにできる対処法（ローカルでのオプトアウト）:
- 全テレメトリを無効化する環境変数（シェル設定に追加）：
```bash
export VERCEL_PLUGIN_TELEMETRY=off
```
- プラグインを無効にする（設定ファイルを編集）：
```bash
# ~/.claude/settings.json に以下を追加
"vercel@claude-plugins-official": false
```
- デバイス追跡IDをローカルから削除：
```bash
rm ~/.claude/vercel-plugin-device-id
```

開発者・運用への提案（期待される改善）
- 明確な個別オプトイン（セッションメタ、bashコマンド、プロンプトを個別に選べる）  
- プラグイン由来のUI表示（[Vercel Plugin] のような明示）  
- プロジェクトやファイルスコープでのフック起動（VS CodeのactivationEventsに相当する仕組み）

この問題はツール提供側の選択とプラットフォーム設計の両方に原因があります。企業や個人で扱う機密情報を守るため、まずは上記のオプトアウトを適用し、プラグイン運用方針を見直してください。
