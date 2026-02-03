---
layout: post
title: "LNAI – Define AI coding tool configs once, sync to Claude, Cursor, Codex, etc. - LNAI — AIコーディングツールの設定を一度定義してClaudeやCursor、Codexへ同期"
date: 2026-02-03T10:48:49.579Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/KrystianJonca/lnai"
source_title: "GitHub - KrystianJonca/lnai: Unified AI configuration management CLI"
source_id: 46868318
excerpt: ".ai/で設定を一元化し、ClaudeやCodexに自動同期して管理ミスを撲滅するCLI"
image: "https://opengraph.githubassets.com/496333914ab4fc7bb27b169a372b9c6439d39cb7960ecf6ce3c989868b68041a/KrystianJonca/lnai"
---

# LNAI – Define AI coding tool configs once, sync to Claude, Cursor, Codex, etc. - LNAI — AIコーディングツールの設定を一度定義してClaudeやCursor、Codexへ同期

設定地獄から即解放！`.ai/`でルールを一元管理し、Claude・Codex・Cursor・Copilotなど各ツール向けのネイティブ設定に自動変換するCLIツール

## 要約
LNAIはプロジェクト内のAIツール設定を`.ai/`フォルダで一元管理し、各ツールが読み取るネイティブ形式に自動で出力・同期・クリーンアップするCLIです。

## この記事を読むべき理由
複数のAI支援開発ツールを併用する現場で、個別設定の散逸・齟齬・手作業によるミスが増えています。日本の開発チームでも、統一されたポリシー運用、セキュリティ設定の一元管理、CI連携による自動化が求められているため、本ツールは即戦力になります。

## 詳細解説
- コア概念：1つのソースオブトゥルース（`.ai/`ディレクトリ）にプロジェクトルール、MCPサーバー設定、権限などを定義。lnai CLIが各ツール用のネイティブ設定ファイルを生成します。
- サポートするツール（抜粋）：Claude、Codex、Cursor、Gemini CLI、GitHub Copilot、OpenCode、Windsurf など。各ツールに合わせたディレクトリ／ファイル形式で出力されます（例：`.claude/`、`.codex/`、`.github/copilot-instructions.md`）。
- 同期と検証：`lnai validate`で構成の整合性チェック、`lnai sync`で出力と不要ファイルの自動削除（オートクリーン）を実行。変更は即時反映できます。
- 実装面：TypeScriptで書かれたCLI（MITライセンス）。ローカル開発だけでなく、CI/CDパイプラインに組み込んでリポジトリ単位で設定を配布できます。
- 運用メリット：ツール間でのポリシー差異を防ぎ、オンボーディングを簡素化。監査や内部ルール適用が容易になります。

## 実践ポイント
- まず試す（ローカル）:
```bash
# bash
npm install -g lnai
lnai init        # .ai/ を作成
lnai validate    # エラー確認
lnai sync        # 各ツール向けに出力
```
- チーム運用案：`.ai/` をリポジトリ管理し、CIで`lnai validate`→`lnai sync`を実行してブランチ間で設定差分を防ぐ。
- セキュリティ：APIキーやシークレットは`.ai/`内でも適切に管理（暗号化/環境変数）すること。
- カスタマイズ：社内ポリシー（コードスタイル、生成制限、MCPサーバ指定など）を`.ai/`で規定し、全ツールへ一括反映。
- 参照：公式リポジトリ（GitHub）とドキュメントで設定リファレンスを確認し、必要に応じてコントリビュートを検討。

LNAIは「複数AIツールを使う現場」の設定管理を劇的に簡素化します。まずローカルで試して、社内ワークフローへ組み込んでみてください。
