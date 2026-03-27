---
layout: post
title: "Anatomy of the .claude/ Folder - .claude/ フォルダの構造"
date: 2026-03-27T15:49:20.685Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.dailydoseofds.com/p/anatomy-of-the-claude-folder"
source_title: "Anatomy of the .claude/ Folder - by Avi Chawla"
source_id: 47543139
excerpt: "CLAUDE.mdやrulesでチームAI挙動を安全に標準化する方法"
image: "https://substackcdn.com/image/fetch/$s_!ITpM!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3b81cc25-df87-4ea8-a11b-9a719d5836b1_1166x1176.png"
---

# Anatomy of the .claude/ Folder - .claude/ フォルダの構造
魅せるチームAI設定術：Claudeを「勝手に賢く」するプロジェクト設定ガイド

## 要約
プロジェクト内の .claude/ はClaude Codeの動作を制御する「司令塔」。CLAUDE.md、commands、rules、skills、agents、settings.json を使えばチーム向けの一貫したAIワークフローを作れる。

## この記事を読むべき理由
日本の開発チームでもAIアシスタントをただ使うだけでなく、安全・再現可能・運用しやすい形で導入するには設定の設計が鍵。特に複数人開発や社内規程がある現場で役立つ具体策が得られます。

## 詳細解説
- 二種類の .claude フォルダ
  - プロジェクト内の .claude/：チーム共有設定（git管理）。
  - グローバル ~/.claude/：個人設定・セッション履歴（マシン単位）。
- CLAUDE.md（最重要）
  - セッション開始時に読み込まれる「システム指示」。ルールやコマンド、コーディング慣習を短く明確に書く（目安200行未満）。
  - 例（簡潔なCLAUDE.md）:
```markdown
# Project: Acme API
## Commands
npm run dev
npm run test
## Architecture
- Node 20, Express, Prisma
## Conventions
- Use zod for request validation
- Return shape: { data, error }
## Watch out for
- Strict TS: no unused imports
```
- CLAUDE.local.md / settings.local.json
  - 個人用の上書き設定。自動でgitignoreされるためチーム設定を汚さない。
- rules/（モジュール化された規約）
  - 関心毎に分割。YAMLフロントマターでパススコープ可能（特定フォルダにのみ適用）。
  - パス指定例:
```text
---
paths:
- "src/api/**/*.ts"
- "src/handlers/**/*.ts"
---
# API Design Rules
- Use zod...
```
- commands/（スラッシュコマンド）
  - .claude/commands/*.md が /project:コマンド を作る。ファイル内で !`cmd` を使うとシェル出力を埋め込み可能。
  - 例: git diff を埋める review コマンド。
- skills/（自動トリガーワークフロー）
  - 会話内容に応じてClaudeが自発的に起動するパッケージ型のワークフロー（SKILL.md +補助ファイル）。
- agents/（専門サブエージェント）
  - 専門家ペルソナを定義し、ツールアクセスやモデルを制限して分離実行。中間トークンをメイン会話に流さないメリット。
- settings.json（権限制御）
  - 許可/禁止コマンドを明示。$schema を入れるとVS Codeで補完が効く。
  - 推奨allow/deny例:
```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": ["Bash(npm run *)", "Bash(git status)", "Read", "Write", "Grep", "Glob"],
    "deny": ["Bash(rm -rf *)", "Bash(curl *)", "Read(./.env)", "Read(./secrets/**)"]
  }
}
```
- グローバルメモリとプライバシー
  - ~/.claude/projects/ に自動メモ。プロジェクト単位で消去や編集が可能。機密データ取り扱いは settings.json で厳格に制御。

## 実践ポイント
- CLAUDE.md は短く具体的に（~20–200行）。ビルド/テスト/命名規則と「NG行為」を明記。
- チームルールは rules/ に分割して所有者を割り当てる（変更の責任を明確に）。
- 繰り返し使う作業は commands/ または skills/ に移して自動化する。!`...` で実データを注入。
- permissions は allow と deny を必ず両方設定し、敏感ファイルは deny に入れる（例: .env）。
- 個人設定は必ず CLAUDE.local.md / settings.local.json にして git に上げない。
- VS Code では settings.json の $schema による補完を有効活用してミスを減らす。

元記事の知見を踏まえれば、チーム単位で安全かつ再現性の高いClaude導入が可能です。
