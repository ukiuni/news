---
layout: post
title: "Cord: Coordinating Trees of AI Agents - Cord：AIエージェントの協調ツリー"
date: 2026-02-21T02:36:57.417Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.june.kim/cord"
source_title: "Cord: Coordinating Trees of AI Agents | June Kim"
source_id: 47096466
excerpt: "目標を投げるだけでAIがspawn/forkで並列タスク木を自律生成・管理する実践手法"
image: "https://www.june.kim/assets/default-icon.png"
---

# Cord: Coordinating Trees of AI Agents - Cord：AIエージェントの協調ツリー
AIがプロジェクトを「自分で分解」して並列処理まで指揮する—現場で使える新しいマルチエージェント設計

## 要約
Cordは「目標を投げるだけ」でエージェントが実行時にタスクツリーを自律生成・管理するプロトコル／実装。spawn と fork という「伝達される文脈の違い」を軸に、並列性・依存管理・人間の問いかけを自然に扱う点が特徴。

## この記事を読むべき理由
従来は開発者がワークフローを全て設計していたが、現在の大規模言語モデルは自律的にタスク分解・依存判断ができる。日本のプロダクト開発やレガシー改修（例：APIマイグレーション）で「設計しきれない仕事」を効率化できる実践的アプローチだから。

## 詳細解説
- 問題意識：既存のマルチエージェントフレームワーク（静的なグラフ、役割ベース、雑談型調整、線形ハンドオフ）はいずれも「協調構造を事前定義」する必要があり、動的な分解や並列処理に弱い。
- Cordの核心：ルートに「ゴール」を与えると、エージェントが実行時にツリー（ノード＝サブタスク、依存関係、ブロック）を作る。ワークフローは事前固定されない。
- spawn vs fork（キー概念）：
  - spawn：子は指定された依存だけを受け取る。外部委託（コントラクター）的でコンテキストは限定的。再実行が安く、独立タスク向け。
  - fork：兄弟ノードの完了結果を全部注入して起動する。チーム要約（ブリーフィング）的で、既存成果を踏まえた総合分析向け。
- 実装要素：Claude Code CLIプロセスを使うエージェント、MCP（小さなサーバ）で依存解決と権限スコープを管理、SQLiteで状態保存。提供される原始ツールは spawn, fork, ask, complete, read_tree の5つ。
- 人間の関与：askノードでインタラクティブに質問し、回答を結果として注入。人はオブザーバーではなくツリー参加者になる。
- 検証：小さなプロトタイプでClaudeがツールの意味を学び、正しくspawn/fork/askを使い分けた（著者のテストでは高い成功率）。
- 拡張性：実装はProof-of-Concept。プロトコル自体は別のDBや複数LLM、あるいは人手混在で再実装可能。

## 実践ポイント
- 試す手順（簡潔）：
  - 必要条件：Claude Code CLIと該当サブスクリプション
  - リポジトリ：git clone https://github.com/kimjune01/cord.git
  - 起動例：cord run "Should we migrate our API from REST to GraphQL?" --budget 2.0
- 運用上の勧め：
  - まずは「調査タスク＋まとめタスク」のような小さなゴールで挙動を観察する。
  - 分析系ノードは fork、独立調査は spawn を意識してプロンプトを書いてみる。spawn=fixed spec、fork=知識継承。
  - 人に聞くべき不明点（スケール、SLA、既存制約）は ask ノードで明示的に切り出す。
  - 実運用時はSQLite→Postgres、単一LLM→ハイブリッドLLM、人の承認ワークフローを組み合わせる設計を検討する。
- 日本の現場での応用例：APIマイグレーション評価、レガシー解析、監査タスクの並列化、営業・企画リサーチの分解など。

短く言えば、Cordは「モデルに分解ルールを委ねて、実行時に最適な協調ツリーを作らせる」考え方の実証。権限やコンテキストの流れを明確にすることで、現実的な並列作業と人の判断を組み合わせられる点が実務的に有用。
