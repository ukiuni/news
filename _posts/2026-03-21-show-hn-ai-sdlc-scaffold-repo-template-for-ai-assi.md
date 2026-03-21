---
layout: post
title: "Show HN: AI SDLC Scaffold, repo template for AI-assisted software development - AI優先のソフト開発向けSDLCスキャフォールド（リポジトリテンプレート）"
date: 2026-03-21T17:26:24.055Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/pangon/ai-sdlc-scaffold/"
source_title: "GitHub - pangon/ai-sdlc-scaffold: Template scaffolding for AI-first software development focused on the pre-coding phases · GitHub"
source_id: 47466513
excerpt: "AIエージェントが4フェーズで設計・実装・決定履歴をリポジトリで自動管理するテンプレ"
image: "https://opengraph.githubassets.com/378c35b5aae5da8a95ca9aec3f45a06371c62e9ec908a25daf892555a5752be7/pangon/ai-sdlc-scaffold"
---

# Show HN: AI SDLC Scaffold, repo template for AI-assisted software development - AI優先のソフト開発向けSDLCスキャフォールド（リポジトリテンプレート）
AIエージェントに「考えさせて記録する」開発フローをリポジトリに埋め込む――日本の現場で使えるAIファーストなプロジェクト立ち上げテンプレ

## 要約
リポジトリは「Objectives → Design → Code → Deploy」の4フェーズをファイル構造と指示書で定義し、AI（主にClaude Code）に作業を任せつつ人間が上位監督するためのテンプレートスキャフォールドを提供する。

## この記事を読むべき理由
AIがコード生成だけでなく要件・設計・決定記録まで担う流れは、日本のスタートアップや規制対応が必要な企業（トレーサビリティや監査が重要）で即戦力になる可能性が高い。

## 詳細解説
- 目的：AIエージェントが各段階で何を確認し、いつ意思決定を記録するかをリポジトリ内に明文化することで、プロジェクト知識をすべてバージョン管理下に置く。
- フェーズと構成：ルートのCLAUDE.mdを起点に、1-objectives/、2-design/、3-code/、4-deploy/ の各ディレクトリとCLAUDE.<phase>.mdで指示やインデックスを持つ。
- キー設計
  - Everything-in-repo：目標、要求、設計、決定、タスクがコードと同居する。
  - Two-file decisions：実行中の決定（DEC-xxx.md）と履歴（DEC-xxx.history.md）に分け、監査性を確保。
  - Context-window効率化：階層化された指示とフェーズ単位のインデックスでLLMが扱うトークンを最小化。
  - フェーズゲート：各フェーズに進むための最低条件を定義。
- 自動化スキル：.claude/skills に /SDLC-init、/SDLC-elicit、/SDLC-design、/SDLC-decompose、/SDLC-implementation-plan、/SDLC-execute-next-task、/SDLC-status などがあり、Claude Codeからコマンド（/skill-name）で実行可能。  
- ワークフロー：初期化→要件抽出→設計→コンポーネント分解→実装計画→逐次実行→状態確認、という順で進める。手作業よりも「エージェントが生成→リポジトリへ記録→人が承認」というループを推奨。

## 実践ポイント
- クイック開始（推奨）：degitでテンプレートをコピーして新規リポジトリを作る。
```bash
# bash
npx degit pangon/ai-sdlc-scaffold my-project
cd my-project
git init && git add -A && git commit -m "Initial scaffold"
```
- 初期化：Claude Code上で /SDLC-init を実行し、CLAUDE.md にプロジェクト説明を入れる。これがエージェントのコンテキストになる。
- 運用ルール：すべての成果物やコード変更はエージェント経由で生成・記録し、人がドラフト→承認へと遷移させる。決定は必ず DEC-*.md と履歴ファイルに残す。
- 日本向け注意点：監査要件や個人情報保護に関する証跡は特に厳格に扱う。フェーズゲートと履歴ファイルを使って説明責任を担保すると現場で受け入れられやすい。
- 適用先：PoCや新規プロダクト、ガバナンスが必要な業務システムの前段（要件・設計）を効率化するのに有用。

元リポジトリはツールではなく「テンプレート」です。実プロジェクトでは方針（人の承認プロセス、LLMの出力ポリシー、ログ保存）を定めてから導入してください。
