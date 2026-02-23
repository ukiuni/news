---
layout: post
title: "femtolisp: A lightweight, robust, scheme-like lisp implementation - femtolisp: 軽量で堅牢な Scheme系 Lisp 実装"
date: 2026-02-23T16:02:54.323Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/JeffBezanson/femtolisp"
source_title: "GitHub - JeffBezanson/femtolisp: a lightweight, robust, scheme-like lisp implementation"
source_id: 47121539
excerpt: "約150KBで学べる高速Scheme系Lisp実装femtolispの設計と組込み活用法を解説"
image: "https://opengraph.githubassets.com/a7bc8ba8dc00ea2e0436bd92374318abb2000c57c607d666a3db12921d3584fe/JeffBezanson/femtolisp"
---

# femtolisp: A lightweight, robust, scheme-like lisp implementation - femtolisp: 軽量で堅牢な Scheme系 Lisp 実装
小さくて速い！学べる実装で「自分の言語」を触ってみたくなるfemtolisp入門

## 要約
femtolispは約150KBの自己完結型Scheme系Lisp実装で、バイトコードVM、コンパイラ（自身で書かれている）、適切な末尾再帰、コンパクティングGCなどを備えつつソースは非常に簡潔。学習用・組み込みスクリプト・言語実装のプロトタイプに向く。

## この記事を読むべき理由
- 小さくて速い実装は、組み込み環境やツールチェーンのスクリプトに有用。
- 実際のコンパイラとVMの設計が学べるため、初級者が言語実装の全体像を掴むのに最適。
- 日本の小型デバイスや社内ツールで「軽量で可読なスクリプト基盤」が求められる場面にマッチする。

## 詳細解説
- サイズと設計思想: 約150KBの自己完結バイナリ／ライブラリを目指し、機能を少数の場所に集約して可読性と信頼性を重視。コアは12個の特殊形式と33個の組み込み関数というコンパクトさ。
- 言語仕様: Scheme互換度が高いLisp-1（関数と変数が同一名前空間）、レキシカルスコープ、バッククオート、gensym、例外、循環構造の読み書きなど「実用的な機能」をきちんと備える。
- 実装技術:
  - バイトコードコンパイラ＋VMを採用。コンパイラ自体がfemtolispで書かれており、バイトコードは可読なASCII表現として出力・読み込み可能。
  - 多くの高階関数（filter, for-each等）が言語レベルで実装されていても高速。非ネイティブ版Schemeの中で高速クラスに属する。
  - 適切な末尾再帰（proper tail recursion）を効率的に実現する設計を持つ（tinyサブディレクトリに純粋s-exprインタプリタの例あり）。
  - Cデータ型を直接扱う仕組み（Pythonのctypesに似たアプローチ）、UTF-8対応のIO/メモリストリーム、ハッシュテーブル、プリティプリント、コンパクティングGCなど。
- 開発・ライセンス: GitHubで公開（約1.6k stars）、BSD-3-Clauseライセンス。コードベースはCとSchemeで構成され、学習・改変が容易。

## 実践ポイント
- 試す（ビルドとサンプル実行）:
  ```bash
  git clone https://github.com/JeffBezanson/femtolisp.git
  cd femtolisp
  make
  ./flisp        # インタラクティブ実行
  ```
- 学習ルート:
  - tiny/やinterpreterブランチで末尾再帰と簡易インタプリタの実装を読む。
  - コンパイラ部分（compiler.lsp）を追うことでバイトコード生成の流れを把握。
  - flisp.bootやテスト群で標準ライブラリの使い方を確認。
- 応用案:
  - 組み込みスクリプトエンジンとしてCプロジェクトに組み込む（C APIを読む）。
  - 言語実装入門の教材として、機能追加や最適化を試してみる。
  - 小規模プロトタイプや社内ツールの高速スクリプト層に適用検討。

参考: GitHubリポジトリ（BSD-3-Clause） — https://github.com/JeffBezanson/femtolisp
