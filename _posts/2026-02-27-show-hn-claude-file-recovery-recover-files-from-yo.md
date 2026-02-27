---
layout: post
title: "Show HN: Claude-File-Recovery, recover files from your ~/.claude sessions - Claude セッションからファイルを復元するツール"
date: 2026-02-27T21:53:57.858Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/hjtenklooster/claude-file-recovery"
source_title: "GitHub - hjtenklooster/claude-file-recovery: Recover files created and modified by Claude Code from JSONL session transcripts"
source_id: 47182387
excerpt: "ClaudeセッションのJSONLから消えたコードを時点復元するCLI/TUI"
image: "https://opengraph.githubassets.com/e0e29ef26268fcc1338b4f67e7f9b2ba981400972a7d068684f1fd34315d0e77/hjtenklooster/claude-file-recovery"
---

# Show HN: Claude-File-Recovery, recover files from your ~/.claude sessions - Claude セッションからファイルを復元するツール
クリックせずにはいられないタイトル: 「AIとの会話で“消えた”コードを丸ごと復元する – Claude のセッションログからファイルを取り出す方法」

## 要約
Claude（Claude Code）が生成・編集したファイルを、~/.claude/projects のJSONLセッション記録から時系列で再構築して復元できるCLI/TUIツール。ポイントインタイム復元や差分表示、バッチ抽出に対応する。

## この記事を読むべき理由
- Claudeを使ってコード生成・編集していると、ファイルが散逸しがち。日本でもAIアシスタントを業務や学習で多用するエンジニアが増えており、セッション履歴から確実にデータを取り出せるのは実務上の価値が高い。
- ローカルに残るJSONLログを解析するため、外部サービスに送らないで復元できる点はプライバシーや社内ポリシーに敏感な日本企業にも有用。

## 詳細解説
- 収集対象：Claude Codeが保存する ~/.claude/projects 配下のJSONLセッションファイル。各行はツール呼び出しや会話の記録。
- 仕組み（簡潔）
  - Scan：並列処理でセッションを走査。高速化のための「fast-reject」バイトチェックで不要行の約77%をパスしてからJSON解析を行う。
  - Correlate：assistantのtool_useリクエストと、結果を含むuserメッセージを tool_use_id で突合。これによりファイル内容（結果側にある）を操作履歴に紐付ける。
  - Reconstruct：ファイルごとに時系列でWrite（新規／上書き）、Edit（差分適用）、Read（スナップショット）を順に再生して任意時点の状態を再現。--before フラグで任意の時点に切り落として復元可能。
- 機能ハイライト
  - TUI（テキストUI）：ファジー検索、vim風のキー操作（j/k/g/G、/で検索）、選択して抽出。
  - 差分表示：カラー化された統一差分／フルコンテキスト／生データ表示。
  - バッチ抽出：複数ファイルをまとめて取り出せる。
  - 高速処理：orjsonなどで高速パース、並列化。
  - シンボリックリンクの重複検出（パスを正規化して統合）。
  - スマートケース検索（大文字を含めると大文字小文字区別する）。
- ライセンス：MIT。OSSとして改造やIssue提出が可能。

## 実践ポイント
- インストール（推奨 uv ツール、pipx、pip のいずれか）:
```bash
# uvツール推奨
uv tool install claude-file-recovery

# pipx
pipx install claude-file-recovery

# pip
pip install claude-file-recovery
```
- 必要環境：Python 3.10+
- 基本コマンド例：
```bash
# TUI起動
claude-file-recovery

# 復元可能ファイル一覧
claude-file-recovery list-files

# フィルタ
claude-file-recovery list-files --filter '*.py'

# CSV出力
claude-file-recovery list-files --filter '*.ts' --csv

# ファイルを指定フォルダへ抽出
claude-file-recovery extract-files --output ./recovered --filter '*.py'

# 過去時点での状態に復元
claude-file-recovery list-files --before '2025-02-20 14:00'

# Claudeデータディレクトリを指定
claude-file-recovery --claude-dir /path/to/claude-backup
```
- TUIの主なキー操作：j/k（上下）、g/G（先頭/末尾）、/（検索）、Ctrl+R（検索モード切替）、x/Space（選択）、Enter（詳細）、d（差分切替）、Ctrl+E（抽出）、q（戻る/終了）。
- 運用上の注意：企業のログポリシーや個人情報保護の観点で、復元したデータの取り扱いルールを確認すること。

このツールは「AIとの対話で生まれたコード資産を取り戻す」ための実用的なツールチェーンを提供する。試してみて、社内ワークフローに組み込む価値があるか判断してみよう。
