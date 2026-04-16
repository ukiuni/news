---
layout: post
title: "Adding Persistent Memory to Claude Code with claude-mem — Plus a DIY Lightweight Alternative - Claude Codeに永続メモリを追加する「claude-mem」と手軽な自作代替案"
date: 2026-04-16T13:05:26.475Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/kanta13jp1/adding-persistent-memory-to-claude-code-with-claude-mem-plus-a-diy-lightweight-alternative-4gha"
source_title: "Adding Persistent Memory to Claude Code with claude-mem — Plus a DIY Lightweight Alternative - DEV Community"
source_id: 3493601
excerpt: "claude-memで永続メモ化し、PowerShell自作で依存ゼロ運用。"
image: "https://media2.dev.to/dynamic/image/width=1200,height=627,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F36dcdcycrbn3gdli48ea.png"
---

# Adding Persistent Memory to Claude Code with claude-mem — Plus a DIY Lightweight Alternative - Claude Codeに永続メモリを追加する「claude-mem」と手軽な自作代替案
魅力タイトル: Claude Codeを「一回限りの会話」から「育つ開発パートナー」に変える方法（ゼロ依存の自作案付き）

## 要約
claude-memはClaude Codeにセッションを跨いだ永続メモリを追加するプラグイン。手軽な自作PowerShellフックで同等の「軽量メモリ」も実現でき、用途に応じて使い分けるのが現実的。

## この記事を読むべき理由
日本の開発現場ではGitでの監査性やコスト管理、オンプレ寄りの運用要件が重要。メモリ機能はAI開発効率を劇的に上げる一方で、依存性やトークンコスト、監査可能性のトレードオフがあるため、両方の選択肢を理解する価値が高い。

## 詳細解説
- claude-memの要点
  - 機能: セッション間での自動キャプチャと将来会話へのコンテキスト注入（長期メモリ化）。
  - アーキテクチャ: ライフサイクルフック（SessionStart / UserPromptSubmit / PostToolUse / Stop / SessionEnd）、SQLite + Chromaのハイブリッド検索（キーワード＋ベクトル）、Bun HTTPワーカー（localhost:37777）、MCPツールの3層開示（search → timeline → get_observations）、Web UIでメモリ可視化。
  - インストール: npx claude-mem install / npx claude-mem start（Bun要件あり）。

- 自作（DIY）軽量代替の要点
  - 実装: Claude Codeのhooks APIで2つのPowerShellスクリプトを利用。
    - PostToolUse（auto-capture.ps1）: Bash/Write利用後にgitコミットや新規ファイル作成を日別Markdownに追記。
    - SessionStart（session-resume.ps1）: 直近3日分を読み込みセッション開始時に注入。
  - 設定例（settings.jsonへの登録）:
  ```json
  {
    "hooks": {
      "PostToolUse": [
        {
          "matcher": "Bash|Write",
          "hooks": [
            { "type": "command", "command": "powershell -File auto-capture.ps1" }
          ]
        }
      ],
      "SessionStart": [
        {
          "hooks": [
            { "type": "command", "command": "powershell -File session-resume.ps1" }
          ]
        }
      ]
    }
  }
  ```
  - メリット: 依存無し、トークン費用ゼロ、Markdownはgitで共有/差分監査可能。短所: セマンティック検索や自動圧縮は弱い（単純テキスト検索が中心）。

- 両者の比較（要点）
  - セットアップ: claude-memはワンコマンド、DIYはスクリプト作成。
  - キャプチャ範囲: claude-memは全ツール、DIYはgit/Write等に限定可能。
  - 検索: ベクトル＋キーワード vs grep的テキスト検索。
  - 依存: Bun/SQLite/Chroma vs なし。
  - 監査性: DIYのMarkdownはgitでトレーサブル。

- 運用上の注意
  - 並列インスタンスで同じファイルに書き込むと競合（instance IDでファイル名を分けるのが有効）。
  - 永続メモリは古い情報の蓄積による「見えない技術負債」になり得るので、定期的なクリーニング運用が必要。

- コスト最適化（claude-mem）
  - 既定の圧縮でClaude APIを使うとトークン消費が発生。Gemini（無償）へ切替可能:
  ```json
  {
    "CLAUDE_MEM_PROVIDER": "gemini",
    "CLAUDE_MEM_GEMINI_API_KEY": "your-free-key-from-aistudio.google.com"
  }
  ```

- 3層メモリ戦略（実運用例）
  - L1（短期・セッション内）: claude-mem（SQLite＋セマンティック検索）
  - L2（短中期・チーム共有）: Markdownフック（gitで共有）
  - L3（長期・体系知）: NotebookLM等のナレッジベース

## 実践ポイント
- まずは低コストで始める: 自作フック＋CLAUDE.mdで「80/20」を確保する。
- 並列インスタンス運用時はファイル名にインスタンスIDを付けて競合回避。
- メモリ運用ポリシー（期限・レビュールール）を作り、古い記録が誘導ミスを生まないよう管理する。
- スケールが必要になったらclaude-memを追加し、セマンティック検索と自動圧縮を導入する。

以上。
