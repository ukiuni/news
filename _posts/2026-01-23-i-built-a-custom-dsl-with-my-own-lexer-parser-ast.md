---
layout: post
title: "I built a custom DSL with my own Lexer, Parser, AST, and Interpreter - カスタムDSLを自作してLexer/Parser/AST/Interpreterを作った話"
date: 2026-01-23T09:34:40.140Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dsavis.com/"
source_title: "DSA Visualizer | Step-by-Step Algorithm Visualization"
source_id: 419793448
excerpt: "Lexer→Parser→AST→Interpreterで学ぶ可視化DSL制作術"
image: "https://dsavis.com/icon.png"
---

# I built a custom DSL with my own Lexer, Parser, AST, and Interpreter - カスタムDSLを自作してLexer/Parser/AST/Interpreterを作った話
学習アルゴリズムを“ステップ実行で見える化”するために生まれた、自作DSLとビジュアライザの舞台裏

## 要約
アルゴリズム可視化のために最小限の文法を定義し、字句解析→構文解析→AST生成→インタプリタで実行まで作り上げた取り組み。視覚化は大画面（タブレット横向き／デスクトップ）での並列表示とリアルタイム実行を重視している。

## この記事を読むべき理由
DSLを一から作る過程は、コンパイラ/インタプリタの基本概念を実践的に学べる最短ルート。日本の学生や面接対策をするエンジニア、教育ツールを作る開発者にとって即戦力になる知見が得られる。

## 詳細解説
- 目的設定：可視化ツール向けDSLは「ステップ実行」「状態のスナップショット」「操作の明示化」が必要。余計な言語機能は省き、観察用フックを設ける。
- Lexer（字句解析）：入力文字列をトークン列に分解。優先度の高い正規表現→識別子／数値／記号／キーワード。位置情報（行・列）を持たせてエラーやハイライトに使う。
  ```javascript
  const tokenSpecs = [
    [/^\s+/, null],
    [/^\/\/.*$/, null],
    [/^\d+/, 'NUMBER'],
    [/^[a-zA-Z_]\w*/, 'IDENT'],
    [/^[\+\-\*\/\(\)\{\};]/, 'SYMBOL'],
  ];
  ```
- Parser（構文解析）：再帰下降やペル式を採用し、優先順位や結合性を管理。文／式の区別、制御構造（if/while）、関数呼び出し等を最低限実装。
- AST（抽象構文木）：ノードは型ごとに定義（Literal, Identifier, BinaryExpr, Call, StatementList）。可視化用に各ノードに実行フック（enter/exit）やメタ情報を付与する。
- Interpreter（実行器）：ASTを歩いて評価。環境（スコープ）管理、ステップ実行のために「1ノード＝1ステップ」でイベントを発行し、ビジュアライザが受け取って状態を描画する。
- ビジュアライゼーション設計：コードと可視化を横並びにし、実行ポイント（現在のノード）をハイライト。小画面だと情報が欠落するため、デスクトップや横向きタブレットでの利用を推奨する（dsavis.comの設計思想）。
- テストと堅牢化：単体テストで字句解析→構文解析→実行結果を検証。エラーメッセージは日本語化や位置情報付きが教育用途で親切。

## 実践ポイント
- まずは簡単な文法（式、代入、if、while）だけでプロトタイプを作る。範囲を狭めるほど完成が早い。  
- Lexerは正規表現リストで実装、Parserは再帰下降が学習に最適。  
- ASTノードで enter/exit イベントを出す設計にすれば可視化との連携が容易。  
- ビジュアライザはデスクトップ／横向きタブレット前提でレイアウト設計する（dsavis.comの推奨）。  
- 学習目的なら最初は自作、実運用ならnearley/pegjs/ANTLR等のツール検討を。
