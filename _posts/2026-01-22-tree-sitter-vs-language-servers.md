---
layout: post
title: "Tree-sitter vs. Language Servers - Tree-sitter と言語サーバーの違い"
date: 2026-01-22T16:09:57.416Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lambdaland.org/posts/2026-01-21_tree-sitter_vs_lsp/"
source_title: "Explainer: Tree-sitter vs. LSP | Lambda Land"
source_id: 46719899
excerpt: "編集中の安定色付けはTree-sitter、精密なコード理解はLSPで両者併用が最適"
---

# Tree-sitter vs. Language Servers - Tree-sitter と言語サーバーの違い
編集中でも色が崩れないのはどっち？ 実務で使い分けるためのシンプルガイド

## 要約
Tree-sitterは高速でエラー耐性のあるパーサ生成器で、リアルタイムなシンタックス強調に強い。言語サーバー（LSP）はコンパイラやツールチェーンに接続して意味的な情報（定義移動、補完など）を提供する。

## この記事を読むべき理由
VSCode／Neovim／Emacsなどを使う日本の開発者やツール作成者にとって、編集体験（見た目・操作性）とコード理解（意味解析）は生産性に直結する。どちらを使い分ければ実務で効率が上がるかが一目でわかる。

## 詳細解説
- Tree-sitter  
  - パーサ生成器：言語の文法を与えると解析器を生成する。  
  - 高速かつ入力に文法エラーがあっても部分解析を続けられるため、編集中の色付けが安定する。  
  - クエリ言語で構文木に対する検索ができ、正規表現より堅牢に構文要素を見つけられる。  
- 言語サーバー（LSP）  
  - エディタとサーバー間の標準プロトコル（JSON RPC）を通じ、定義移動・補完・型情報など意味的な機能を提供する。  
  - $N \times M$ 問題（N言語 × Mエディタで実装が膨張する問題）を解決する設計。  
  - コンパイラやランタイム情報にアクセスできるため、例えば同名の関数が複数ある場合でも正しく参照先を特定できる。  
- ハイライトにLSPを使う場合  
  - LSPはセマンティックトークンを返すことでハイライト可能だが、Tree-sitterに比べて重くなる場合がある。EmacsのeglotやVSCodeのsemantic highlightingが例。  
- 実務上の結論（トレードオフ）  
  - 表面的・高速な色付けはTree-sitter、コードナビゲーションやリファクタリングはLSP。多くの環境では両者を組み合わせるのが最適。

## 実践ポイント
- まずはTree-sitterで編集時の安定したシンタックスハイライトを導入する（Neovimなら nvim-treesitter）。  
- プロジェクト規模や言語機能を重視するならLSPを有効化して補完・定義ジャンプを使う（VSCodeは標準でLSPクライアント、Emacsはeglot/lsp-mode）。  
- 両方を併用：Tree-sitterで即時表示、LSPで意味解析を補う。日本の大規模モノレポや複数バージョン依存の環境ではLSPの恩恵が大きい。  
- 設定例（参考）: VSCodeでは "editor.semanticHighlighting.enabled": true を確認、Neovimは nvim-treesitter + lspconfig の組み合わせを検討。
