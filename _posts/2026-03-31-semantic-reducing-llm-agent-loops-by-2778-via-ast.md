---
layout: post
title: "Semantic – Reducing LLM \"Agent Loops\" by 27.78% via AST Logic Graphs - Semantic — AST論理グラフでLLMの「エージェントループ」を27.78%削減"
date: 2026-03-31T04:56:58.041Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/concensure/Semantic"
source_title: "GitHub - concensure/Semantic: Semantic analysis · GitHub"
source_id: 47582545
excerpt: "AST論理グラフでLLMのループを27.78%削減、ローカルで安全な自動編集を実現"
image: "https://opengraph.githubassets.com/4b8221413fc98d9499925ba817db725832dc14063e7e4a7f603b38a90b583f5d/concensure/Semantic"
---

# Semantic – Reducing LLM "Agent Loops" by 27.78% via AST Logic Graphs - Semantic — AST論理グラフでLLMの「エージェントループ」を27.78%削減
LLMエージェントの迷走を止める――ローカルグラフとASTで「開発ステップ」を27.78%削減した実装の中身

## 要約
GitHubのSemanticは、ASTベースの論理ノードと依存グラフを使った「セマンティック第一」のローカルサービスで、LLMによる無駄な反復（Agent Loops）を減らし、開発者の手順を約27.78%削減することを目指すプロジェクトです。

## この記事を読むべき理由
日本の開発現場でも、LLM支援開発はコストと誤誘導（misdirection）が課題です。Semanticはローカルでの決定論的検索・文脈構築や安全な編集パイプラインを備え、企業方針やプライバシーを守りつつLLMの有用性を高められるため、実運用に直結する示唆が得られます。

## 詳細解説
- アーキテクチャ概要：Rust製のローカルAPI（Axum）＋Tree‑sitterでAST抽出、SQLite＋Tantivyでインデックスを保持。ローカルで決定論的にコードのシンボル／論理ノードを取得する設計。
- グラフセマンティクス：論理ノード（logic nodes）に制御フロー/データフローのエッジと意味ラベルを持たせ、クラスタリングとハイブリッドランキングで関連文脈を選別。get_control_flow_slice / get_data_flow_slice 等の取得APIがある。
- 推論向け取り出し（Reasoning Retrieval）：依存グラフ幅優先探索や論理近傍取得を組み合わせ、deterministicなコンテキスト（get_reasoning_context / get_planned_context）を構成。バジェッターでトークン予算を管理し過剰取得を防止。
- MCPブリッジ：外部ツール向けに retrieve（多様な取得操作）と ide_autoroute（タスクの意図ルーティング・アクション実行）の2ツールを公開。既存の旧ツール群も互換性維持。
- セーフ編集パイプライン：impact_analysis → safe_edit_planner → llm_router → patch_engine → validation といった流れで、AST変換（ASTTransform）やUnifiedDiffプレビューを使い安全に自動編集を行う仕組みを持つ。
- 計測とABテスト：従来のトークン節約指標から「step savings（開発ステップ削減）」へ評価軸を移行。最新のA/Bでは27.78%のステップ削減を報告（詳細はAB_TEST_DEV_RESULTS.md）。
- プライバシーと運用：ローカルでのトークン追跡やNDJSON形式のテレメトリ、厳格〜デバッグのプライバシーモードが用意され、企業での採用に配慮。

## 実践ポイント
- ローカルで試す：リポジトリを取得し `cargo run -p api -- ./test_repo` で動作確認。環境変数 $SEMANTIC_API_BASE_URL を設定。
- まず使うAPI：POST /retrieve の get_reasoning_context / get_function / get_logic_nodes を触って、どの程度意味的コンテキストが返るか確認する。
- IDE統合：VS Code等のIDEに組み込み、single_file_fast_path と reference_only を活かして単一ファイル編集の過剰取得を防ぐ設定を試す。
- セーフ編集の導入：patch_engine と safe_edit_planner を使い、自動修正のプレビュー→検証→適用ワークフローを組み込む。
- 評価指標の変更：トークン節約だけでなく「ステップ削減」をKPIに設定し、A/Bでautoroute_first等のフラグを比較検証する。
- 運用上の注意：.semantic 配下の設定（retrieval_policy, edit_config, llm_routing 等）をプロジェクト方針に合わせてカスタマイズし、トークン追跡のプライバシーモードを選ぶ。

このプロジェクトは、LLM支援開発を「実用的で安全なツールチェーン」に近づけるための具体的な実装例を示しており、日本の現場でのコスト管理・プライバシー要件・CI統合に直結する知見が得られます。
