---
layout: post
title: "sysp: Systems Lisp compiling to C with homoiconic macros, refcounted memory, Hindley-Milner type inference - sysp：ホモアイコニックマクロ、参照カウント、HM型推論を備えたCへコンパイルするシステム向けLisp"
date: 2026-01-26T06:47:11.477Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/karans4/sysp"
source_title: "GitHub - karans4/sysp: A systems Lisp that compiles to C. Homoiconic macros, refcounted memory, Hindley-Milner type inference."
source_id: 1380366930
excerpt: "ホモアイコニックマクロとHM型推論でC/CUDAカーネルを高性能生成"
image: "https://opengraph.githubassets.com/716fddeb8da653692d440306b6a2bd13c369ce2c7f22c87290d851ccec6c5ca1/karans4/sysp"
---

# sysp: Systems Lisp compiling to C with homoiconic macros, refcounted memory, Hindley-Milner type inference - sysp：ホモアイコニックマクロ、参照カウント、HM型推論を備えたCへコンパイルするシステム向けLisp
魅せるLispでGPU/数値計算用カーネルを「コンパイル時生成」する――小さく始めて大きく最適化する新しい道

## 要約
syspはCommon Lispで書かれた小型コンパイラで、ホモアイコニックなマクロによるコンパイル時コード生成、参照カウントによる簡易メモリ管理、Hindley–Milner風の型推論（モノモルフィゼーション志向）を持ち、読みやすいC（や将来的にCUDA）を生成することを目指しています。

## この記事を読むべき理由
数値計算やGPUカーネル生成で「高性能・専門化されたコード」を自動生成したい日本の研究者・エンジニアにとって、syspは「マクロでカーネルを組み立ててその場でC/CUDAを吐く」試金石。既存のC/CUDAの冗長さと、Pythonの抽象度の落差を埋める実験的なアプローチです。

## 詳細解説
- 目的と設計哲学  
  - 数値／GPUワークロードで、マクロ段階に特化したCコードを生成して性能と可読性の両立を狙う。CarpやZigからの影響を受ける「システム寄りのLisp」。
- 主要機能（抜粋）  
  - ホモアイコニックマクロ：コードとデータが同じ表現（S式）なので、マクロでC/CUDA用の特殊化カーネルを組み立てられる。quasiquote（~, ~@）対応。  
  - コンパイル時評価：defn-ct のような仕組みで本格的なメタプログラミングが可能。  
  - 型推論：Hindley–Milner風のUNIFYを使い、確定した型は専用のC型（例：Vector_int）にモノモルフィ化。未解決はValueというタグ付きユニオンでフォールバック。  
  - メモリ管理：consなどは参照カウント（val_retain/val_release）。ランタイムを極力持たない「直接C生成」が目的。  
  - 最適化系：recur→gotoで末尾再帰を最適化。生成されるCは人間が読める形で出力される。
- コンパイラ構成（単一ファイル約1900行）  
  - Read（カスタムreadtableで[]配列やバッククオート） → Macro-expand（defmacro展開等） → Infer（型推論、未完） → Compile（AST→C） → Emit（ヘッダ/型定義/関数本体）
- 実用例  
  - factorialのLisp実装がそのまま可読なC関数に変換される。  
- 開発状況と将来計画（Roadmap）  
  - 型制約生成とモノモルフィゼーションは進行中。将来的にパターンマッチ、タグ付き和型、借用検査（線型型）、CUDAバックエンドやHPCプリミティブを目指す。

## 実践ポイント
- 試す：SBCLとCコンパイラを用意してリポジトリ内の例をコンパイルしてみる。
  ```bash
  sbcl --script sysp.lisp input.sysp output.c
  cc output.c -o program
  ```
- カーネル生成の感触を掴む：ホモアイコニックマクロで小さな数値カーネルを生成し、吐かれたCを読む。可視化すると最適化ポイントが見える。  
- 型推論の扱い：未解決型はValueに落ちるので、性能重視なら明示的に型を与えてモノモルフィ化を促す。  
- メモリモデルに注意：参照カウント式なので循環参照に注意。必要なら設計段階で回避する。  
- 貢献・検証：まだWIPが多いプロジェクトのため、型推論・CUDAバックエンドなど興味があればIssue/PRで関わる価値あり。

短くまとめると、syspは「Lisp的なメタプログラミングで専門化したC/CUDAカーネルを生成する実験場」。数値計算・GPU開発のワークフローを一段階上げたい開発者は、まず小さな例で吐かれるCを読み、どこまで最適化できるか試してみることを勧める。
