---
layout: post
title: "How to Stop Babysitting Your AI Agents - AIエージェントの「お世話」から卒業する方法"
date: 2026-03-20T06:16:50.953Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/jrswab/how-to-stop-babysitting-your-ai-agents-4376"
source_title: "How to Stop Babysitting Your AI Agents - DEV Community"
source_id: 3367901
excerpt: "チャット画面不要でgitやcronに組込める軽量CLI型AIエージェントAxeの実装と運用術"
image: "https://media2.dev.to/dynamic/image/width=1200,height=627,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fcekyj684wh2vkxtpt3lb.png"
---

# How to Stop Babysitting Your AI Agents - AIエージェントの「お世話」から卒業する方法
チャット画面を開かずにAIを「実行ツール」として使う――面倒なコンテキスト管理から解放されるCLI型エージェントの提案

## 要約
チャット画面で都度プロンプトを書き直す「AIの子守り」をやめ、UNIX哲学に沿った単一責務のCLIエージェント（Axe）で自動化をシンプルにする提案と実装例。

## この記事を読むべき理由
日本の開発現場でも「チャットで実験→運用で手作業」がボトルネックになりがち。軽量CLIで既存のパイプライン（git hook／cron／監視）に差し込めるアプローチは、コストと運用負荷を下げて即戦力になるからです。

## 詳細解説
- 問題点：多くのLLMワークフローは大きなコンテキストと対話セッションに依存し、ユーザーがスケジューラ・コンテキスト管理者・出力パーサーを兼任してしまう。
- 解決方針：UNIXの小さな道具の連携をAIにも持ち込み、1つのエージェントは1つの仕事、stdin→stdoutで入出力を明確にする。
- Axeの特徴（設計の要点）
  - 単一バイナリ（軽量）でデーモン不要。どこでも実行可能。
  - エージェントはファイルで定義（TOML + SKILL.md）。人が読めてバージョン管理可能。
  - 入力は常にstdin、出力はstdout。デバッグはstderrへ流れるためパイプが汚れない。
  - サブエージェントの委譲が可能。各サブエージェントは独立したコンテキストを持ち、親は内部の推論や中間状態を見ない（情報分離）。
  - メモリは単純なタイムスタンプ付きMarkdownファイルに追記。DBや複雑なフォーマット不要。
  - --dry-runで解決済みコンテキストやプロンプトを確認でき、コスト見積りやデバッグに便利。
  - ライセンスはApache 2.0、レポジトリは github.com/jrswab/axe
- 設定例（抜粋）:
```toml
# toml
name = "pr-reviewer"
description = "Reviews git diffs for issues"
model = "anthropic/claude-sonnet-4-20250514"

[params]
temperature = 0.3

[memory]
enabled = true
last_n = 10
```
- 実行例:
```bash
# bash
git diff --cached | axe run pr-reviewer
cat /var/log/app/error.log | axe run log-analyzer
```
- 運用観点：Axeはスケジューラではなく実行器。cron／git hook／fswatchなど既存のツールと組み合わせて使うのが前提。

## 実践ポイント
- まずは小さな単機能エージェントを作る（PRレビュー、ログ集計、コミットメッセージ生成など）。
- git hook や cron にパイプで組み込み、----dry-runで出力を確認してから本番化。
- SKILL.md と config をリポジトリで管理してレビュー可能にする（透明性が運用コストを下げる）。
- サブエージェントで細分化して、各エージェントに必要最小限のコンテキストだけ渡す設計を意識する。
- 興味があれば repo を試して、Dockerや既存エディタのフックから呼び出す運用も検討する（ローカルで完結する点がコスト効率的）。

短時間で「チャット画面を開かない自動化」を試せる手法なので、まずは1〜2個のタスクで置き換えてみることをおすすめします。
