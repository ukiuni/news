---
layout: post
title: "Deterministic orchestration vs statistical retries: an architecture for AI agent reliability - 決定論的オーケストレーション vs 統計的リトライ — AIエージェント信頼性の設計"
date: 2026-02-13T19:11:57.302Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/a5c-ai/babysitter"
source_title: "GitHub - a5c-ai/babysitter: Babysitter enables Claude Code to manage sophisticated development workflows through deterministic, resumable orchestration"
source_id: 442445270
excerpt: "Babysitterで中断・再現可能な決定論的オーケストレーションによりAI運用を監査対応で安定化"
image: "https://repository-images.githubusercontent.com/1128400700/26a7534f-da4f-4ad7-9de5-f6ee1ab94ebb"
---

# Deterministic orchestration vs statistical retries: an architecture for AI agent reliability - 決定論的オーケストレーション vs 統計的リトライ — AIエージェント信頼性の設計
AIに任せて安心できる開発ワークフローを作る——Babysitterが示す「再現可能で中断・再開できる」オーケストレーションの実践

## 要約
BabysitterはClaude Code向けのオーケストレーションフレームワークで、イベントソース化された決定論的ワークフローにより、反復・人の承認・品質収束を自動化し、途中中断や再実行でも状態を復元できるようにする。

## この記事を読むべき理由
AIに任せる処理が増えるほど「なぜそうなったか」を追跡できる仕組みが必須になる。特に日本の企業では監査・品質管理が重視されるため、再現性と監査ログを持つオーケストレーションは価値が高い。

## 詳細解説
- コア概念
  - 決定論的オーケストレーション：外部入力とイベント履歴が同じなら同一の実行結果を再現できる設計。
  - イベントソース（event-sourced）：すべての操作・タスク実行結果・状態変化をジャーナルとして記録。
  - 再開可能（resumable）：.a5c/runs/<runId>/配下にジャーナルとタスク状態を保持し、中断から正確に復元できる。

- 実行ループ（Babysitter Loop）
  1. プロセスを進める（Advance）
  2. 保留中の「効果」を取得（Get pending effects）
  3. タスクを実行（Execute）
  4. 結果を記録（Record outcomes）
  5. 品質目標に達するまで反復

- 主要機能
  - 人間による承認ポイント（breakpoints / human-in-the-loop）を組み込み可能
  - 品質収束（quality convergence）：自動反復で品質基準を満たすまで改良
  - エージェントスコアリングと並列実行：複数サブエージェントを同時運用し、採点で選択
  - 完全な監査ログ（audit trail）：誰がどの決定をしたか追跡可能

- 導入要件・実装面
  - Node.js 20+、Claude Codeプラグインとして動作
  - CLI/スキル呼び出し例: /babysitter:call …（Claude側のスキル経由でランを開始）
  - 2,000以上のプロセス定義やREST API、SDKが提供されている点で拡張性あり

- なぜ「統計的リトライ」では不十分なのか
  - 統計的リトライ（ランダムな再試行）は非決定的で再現性が乏しいため、監査やデバッグで原因特定が難しい。決定論的設計は追跡可能性と信頼性を高める。

## 実践ポイント
- まずは小さなワークフローで試す：人手承認があるデプロイ前チェックやコードレビュー自動化から始める。
- ジャーナルをリポジトリで管理して監査証跡を残す（.a5c/runs/をCIに保存）。
- 品質目標（テストの合格基準やレビュー基準）を明確に設定し、収束ループを活用する。
- 並列サブエージェントを使って候補解を生成→スコアリングで最良解を採用するパターンを導入する。
- 日本の規制対応や社内ガバナンスには人間承認のブレークポイントを必ず組み込む。

導入検討時はClaude Codeの利用可否、Node.js環境、既存ツールとの統合性（CI/チケット管理）を確認するとスムーズです。
