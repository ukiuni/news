---
layout: post
title: "Deterministic codebase reasoning for LLMs using AST graphs instead of pure embeddings - LLM向け：純粋な埋め込みではなくASTグラフで決定論的にコードベースを推論する方法"
date: 2026-02-20T13:42:52.057Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/bekirdag/docdex"
source_title: "GitHub - bekirdag/docdex: A document index with MCP, http and client support. https://docdex.org/"
source_id: 436975927
excerpt: "Docdex：ASTとインパクトグラフでローカル完結にコード影響を決定論的に可視化しLLM連携を実現"
image: "https://opengraph.githubassets.com/3997a86be87605f7dfe4a86f8422125b553b44e6a36722b63fb820731a1cb072/bekirdag/docdex"
---

# Deterministic codebase reasoning for LLMs using AST graphs instead of pure embeddings - LLM向け：純粋な埋め込みではなくASTグラフで決定論的にコードベースを推論する方法
LLMに“信頼できる記憶”を与えるローカルインデクサ — Docdexがベクトル依存を減らしコードの因果関係を理解する

## 要約
Docdexはローカルで動くドキュメント／コードインデクサ兼デーモンで、ASTとインパクトグラフを使いLLMに対して決定論的でプライバシー重視のコンテキスト提供を実現するツールです。

## この記事を読むべき理由
クラウドへのコードアップロードに抵抗がある日本の企業・開発者にとって、ローカル完結で「何がどこに影響するか」を正確に渡せる仕組みは即戦力です。コードリファクタやセキュリティ対応、LLMアシスタント統合での信頼性向上に直結します。

## 詳細解説
- コア概念：Docdexは単なる全文検索や埋め込みによるRAGではなく、パース結果（AST）と依存関係を表すインパクトグラフを内部に持つ。これにより「文字列マッチ」では見落としがちな定義場所／呼び出しチェーン／変更時の影響範囲を決定論的に追える。
- ローカル優先設計：インデクシング、検索、メモリ保存（リポジトリ事実やユーザープロファイル）は全てローカルで完結。企業のコードガバナンスや情報漏洩リスクを低減します。
- MCP（Model Context Protocol）対応：Claude DesktopやCursorなど複数のエージェントとMCPで連携可能。エディタやAIクライアントはDocdexのデーモンに接続して共有コンテキストを利用できます。
- 機能ハイライト：ドキュメントランキング・サマリ、AST/インパクト解析（Rust, Python, JS/TS, Go, Java, C++等対応）、リポジトリ／エージェントメモリ、MCP/HTTP API、ローカルLLM（Ollama）連携。
- 運用：一度インデックスを作ればデーモン常駐でCLI・HTTP・MCP経由の照会が可能。マルチリポジトリも単一デーモンで管理できます。
- セキュリティ：ループバックはTLS不要でローカル運用しやすく、公開する場合はTLS／認証トークンで保護可能。

## 実践ポイント
- インストール（npm推奨）とインデックス作成例：
```bash
npm i -g docdex
docdexd index --repo /path/to/my-project
```
- デーモン起動とチャット例：
```bash
docdex start
docdexd chat --repo /path/to/my-project --query "how does auth work?"
```
- AST定義検索 & インパクト解析（HTTP API）：
```bash
curl "http://127.0.0.1:28491/v1/ast?name=addressGenerator&pathPrefix=src"
curl "http://127.0.0.1:28491/v1/graph/impact?file=src/app.ts&maxDepth=3"
```
- リポジトリメモやエージェントスタイル保存：
```bash
docdexd memory-store --repo . --text "Payments retry up to 3 times with backoff."
docdexd profile add --agent-id default --category style --content "Use concise bullet points."
```
- ローカルLLM連携：Ollamaを使うと埋め込みやチャットをローカルで補完可能。企業ポリシーでクラウド不可なら試す価値あり。
- 日本向け注意点：Windowsで動かす場合はMSVCランタイム（Visual C++ Redistributable）が必要。社内ポリシーやSAML/ネットワーク設定に合わせてTLS／認証を有効にすること。

短時間でコードの因果関係を把握しつつ、データを社外へ出さずにLLMと連携したい現場には即導入を検討できるツールです。
