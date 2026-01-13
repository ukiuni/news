---
layout: post
title: "Visualizing Recursive Language Models - 再帰型言語モデルの可視化"
date: 2026-01-13T10:05:16.016Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/code-rabi/rllm"
source_title: "GitHub - code-rabi/rllm"
source_id: 428027237
excerpt: "TSでV8アイソレート上のRLLMが巨大データを分割並列で高速・安全に可視化"
image: "https://opengraph.githubassets.com/42abe3e2462260230c9b0ea23b0da28443d889bef1aa7f6f26c31990d2a72af1/code-rabi/rllm"
---

# Visualizing Recursive Language Models - 再帰型言語モデルの可視化
巨大コンテキストを「分割して処理」するTypeScript版RLLM — 高速・安全に大規模データをLLMで解析する新潮流

## 要約
TypeScriptで書かれたRLLM（Recursive Large Language Models）は、V8アイソレート上でLLMが生成したJavaScriptを実行し、巨大なコンテキストを小さなタスクに分割して並列処理・集約する実装。クラウドやオンプレのOpenAI互換APIにも接続可能で、高速かつ安全に大規模データ解析ができる。

## この記事を読むべき理由
日本のプロダクトや企業データは巨大なコードベースやログ、ドキュメントを抱えがちで、従来の単一プロンプトでは扱いにくい。RLLMは「LLMが自らコードを書いて分割・再帰処理→集約」を行うため、現場での大規模解析・可視化やオンプレ環境での利用にフィットする実践的な選択肢を提供する。

## 詳細解説
- コアアイデア
  - RLLMは「入力（巨大コンテキスト）をLLMが小さなチャンクに分け、サブLLM呼び出しで並列処理し、最終結果を合成する」という再帰的ワークフローを実装する手法。
  - TypeScript実装では、LLMが出力するJavaScriptをV8アイソレートで実行。Python実装のサブプロセス＋TCPよりも高速で安全に動くのが特徴。

- なぜV8アイソレートか
  - TCP／サブプロセス不要：同プロセス内で直接バインディングを呼び出すためオーバーヘッドが小さい。
  - 起動高速化：アイソレートはミリ秒単位で立ち上がる。
  - メモリ分離：V8のサンドボックスで実行されるためホスト側の安全性が高い。

- TypeScriptに適した点
  - Zodスキーマを与えるとLLMは型情報を参照してより正確なコードを生成できる（context.users のように型付きでアクセス可能）。
  - TypeScriptネイティブなので、生成コードの検証やIDE体験が扱いやすい。

- APIとバインディング（主なもの）
  - createRLLM(options) でインスタンス作成（provider：openai/anthropic/gemini/custom 等）。
  - rlm.completion(prompt, { context, contextSchema, onEvent }) — コード実行を伴うフルRLM完了処理。
  - サンドボックスに注入されるバインディング例：context、llm_query、llm_query_batched、print、giveFinalAnswer。
  - 実行イベント（iteration_start / llm_query_start / code_execution_start / final_answer）を受け取ってUIへストリーミング可能。

- カスタムプロバイダ対応
  - vLLM、Ollama、LM Studio、Azure OpenAI などOpenAI互換APIを baseUrl で指定して利用可能。日本でのオンプレ運用や企業のセキュリティ方針にも対応しやすい。

## 実践ポイント
- すぐ試す
  - インストール: pnpm add rllm （npm でも可）
  - 公式の examples/node-modules-viz/ は、node_modules を解析して依存関係を可視化する実例で参考になる。

- 最低限の利用例（TypeScript）
  ```typescript
  import { createRLLM } from 'rllm';

  const rlm = createRLLM({ model: 'gpt-4o-mini', verbose: true });
  const result = await rlm.completion("この資料の要点は？", { context: hugeDocument });
  console.log(result.answer);
  ```

- 型情報を渡す（Zod）
  - データ構造が決まっている場合は Zod スキーマを渡すと生成コードの精度が向上する。

- 可視化・デバッグ
  - onEvent ハンドラでイベントを受け取り、UIの進捗表示や部分的なログ表示に使うとユーザビリティが上がる。

- 運用上の注意
  - カスタムプロバイダ利用時は baseUrl と APIキー設定を忘れずに（オンプレ環境での認証・監査要件を確認）。
  - サンドボックス実行だが、生成コードの出力内容はレビューするのが安全。

ライセンスはMIT。大規模データ解析や企業内でのLLM活用を考えている日本の開発チームには、まずローカルでexamplesを動かして挙動を確かめることをおすすめする。
