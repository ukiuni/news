---
layout: post
title: "The programming language coding agents perform best in isn’t Python, TypeScript, or Java. It’s the functional programming language Elixir. - コーディングエージェントが最も得意とする言語はPythonでもTypeScriptでもJavaでもない。関数型言語Elixirだ。"
date: 2026-02-19T02:51:30.982Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/Tencent-Hunyuan/AutoCodeBenchmark/"
source_title: "GitHub - Tencent-Hunyuan/AutoCodeBenchmark"
source_id: 438144591
excerpt: "AutoCodeBenchで判明、意外にElixirがLLMコード生成で最良"
image: "https://opengraph.githubassets.com/f3a3bb8a1ce4b5f30961fba81caebe566328571a6d8e13cb4c3f9ad9d3569101/Tencent-Hunyuan/AutoCodeBenchmark"
---

# The programming language coding agents perform best in isn’t Python, TypeScript, or Java. It’s the functional programming language Elixir. - コーディングエージェントが最も得意とする言語はPythonでもTypeScriptでもJavaでもない。関数型言語Elixirだ。

驚きの示唆：LLMにとって「書きやすい」言語は意外にもElixir――AutoCodeBenchが示す評価基盤と手順を短く解説

## 要約
Tencent-HunyuanのAutoCodeBenchは、多言語・高難度なコード生成ベンチマークとサンドボックスを公開し、LLMベースのコーディングエージェントを言語横断で比較可能にした。元記事はその評価からElixirでの成績が突出した点を指摘している。

## この記事を読むべき理由
- 日本でもAIがコード生成を現場導入する流れが加速しており、言語ごとの得手不得手を知ることは導入設計や教育方針に直結するため。  
- AutoCodeBenchは20言語をバランス良く扱うため、日本語環境やマルチ言語プロジェクト評価にも使える。

## 詳細解説
- データ構成：AutoCodeBench-Full（約3,920問）、Lite（1,586問）、Complete（1,000問・3-shot完成形式）を用意。各問題はquestion／canonical_solution／demo_test_func／full_test_funcなどで管理され、難易度は easy/medium/hard。  
- ベンチの特徴：従来のベンチと比べて言語・カテゴリ分布を均衡させ、難易度を高く設定している点が特徴。これによりモデルの「言語横断力」がより厳密に測定できる。  
- 実行環境：MultiLanguageSandboxというコード実行サンドボックス（Dockerイメージ hunyuansandbox/multi-language-sandbox:v1）で、30+言語のコンパイル／実行を安全に自動評価。評価は model_output.jsonl を作り、サンドボックスに投げて pass@1 等を算出する流れ。  
- 評価プロンプトと手順：システムプロンプトで「専門家プログラマ」として一つのMarkdownコードブロックで解答させ、出力を model_output.jsonl に格納。サンドボックス起動→call_sandbox.pyで実行→pass@1を計算、という一連のパイプラインが整備されている。  
- 「Elixir優位」の示唆：元記事はベンチ結果の解析でElixirが相対的に高スコアを示したと伝えている。関数型・並行性の設計がテストケースと相性が良い／LLMが生成しやすいコード構造になっている可能性が考えられる（詳細は元データで言語別スコアを確認すると確かめられる）。

## 実践ポイント
- まずデータを取得：HuggingFaceのAutoCodeBench各種をダウンロードして問題セットを確認。  
- ローカルで評価環境を立てる：Dockerでサンドボックスを起動（イメージをpullして run）、call_sandbox.py で動作確認。  
- 自分のモデルで検証：system_prompt を統一して model_output.jsonl を作成→サンドボックスで実行→言語ごとの pass@1 を比較。  
- Elixirを試す理由：もしElixirで高い再現性が出るなら、並行処理やサーバーサイド処理の自動生成ワークフローや教材設計に活用できる。  
- さらに進める：AutoCodeInstructやAutoCodeGenを使い、RL/SFTデータ作成やモデル改良のための学習素材を自動生成する。

元リポジトリ（AutoCodeBench）には評価チュートリアル、データ、サンドボックス手順が揃っているので、まずは手元で小規模な1言語（例：Elixir）を回して言語別傾向を確認することをおすすめします。
