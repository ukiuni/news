---
layout: post
title: "Show HN: Han – A Korean programming language written in Rust - Han（한）: Rustで作られた韓国語キーワードのプログラミング言語"
date: 2026-03-14T22:15:49.000Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/xodn348/han"
source_title: "GitHub - xodn348/han: A compiled programming language with Korean keywords, written in Rust · GitHub"
source_id: 47381382
excerpt: "ハングルで書くRust製言語HanをREPLで即体験、LLVM経由でネイティブ生成やLSP対応も可能"
image: "https://opengraph.githubassets.com/e2f0d7a48b84ef2a0b341275e75323f4798dba7944decff85e36ff0696364bc5/xodn348/han"
---

# Show HN: Han – A Korean programming language written in Rust - Han（한）: Rustで作られた韓国語キーワードのプログラミング言語

韓国語でプログラミングする楽しさ──Hangulをそのまま言語設計に取り込んだコンパイル言語「Han(한)」の全貌。

## 要約
Hanはキーワードや識別子をハングルで書く静的型コンパイル言語で、Rustで実装。LLVM IRを経てネイティブバイナリを生成でき、インタプリタ／REPL／LSPも提供します。

## この記事を読むべき理由
言語ローカライズやプログラミング教育、非英語圏でのコーディング体験に関心がある日本のエンジニアにとって、Hanは「文字（スクリプト）が言語設計に与える影響」を実地で示す興味深い実験です。K‑popや韓国語学習ブームに接する日本の開発者にも親和性がありますし、ローカライズ言語の設計やツールチェーン実装の学びとして有益です。

## 詳細解説
- 言語設計：キーワード（함수→함수/日本語でいう「関数」相当）、識別子、メソッドなどをハングルで表現。構文はC系に似た要素（型注釈、戻り値指定、for/while、match相当）を持つ。
- 実装：ツールチェーンは全てRustで実装（lexer→parser→AST→interpreter/codegen）。コード生成はテキスト形式のLLVM IRを出力し、clangで最終バイナリ化する方式を採用。
- 実行方式：即時実行のインタプリタ、REPL、そしてコンパイル経路（hgl build/run）が両立。LSPサーバでエディタ補完やホバー説明も提供。
- 型と標準機能：静的型（정수, 실수, 문자열, 불, 없음）、配列（負のインデックス可）、構造体、クロージャ、パターンマッチ、例外ライクなエラーハンドリング、ファイルI/O、フォーマット文字列、ジェネリクス（パーシャル）など。
- 制約・未実装点：関数を型付き引数に渡す構文未対応、浮動小数点と整数の自動昇格なし、ネスト構造体の深いフィールド書き換え未サポート、標準ライブラリにネットワーク等はまだない点など。ガベージコレクションは無く、Rc/RefCellベースで循環はリークする可能性あり。
- なぜLLVM IRのテキスト出力か：LLVMのリンクやビルド依存を避けつつ最適化済みバイナリを得るため。Rustで書くことでメモリ安全にコンパイラを構築している点も設計上の利点。

## 実践ポイント
- 試す（ローカル）：最短でREPLを起動してハングルキーワードで遊んでみるのがおすすめ。
```bash
# 必要: Rust, clang (mac: xcode-select --install / brew install llvm)
git clone https://github.com/xodn348/han.git
cd han
cargo install --path .
hgl repl
```
- 学びの種：言語設計、パーサー/AST、LLVM IR生成を学びたい人はソース（lexer.rs, parser.rs, codegen.rs）を読むと良い教材になる。
- 日本向け着想：同様の手法で日本語キーワードの実験言語を作るという発想や、教育用途にローカライズ言語を導入するアイデアへ発展可能。
- 貢献案：ドキュメント翻訳、LSP改善、標準ライブラリ拡張（ファイル／文字列処理の堅牢化）や未実装機能の実装は参加しやすい分野。

Hanは「言語は文化の一部になり得る」ことをコーディングの現場で示すプロジェクトです。まずはREPLで一行書いて、ハングルで動くコード体験をしてみてください。
