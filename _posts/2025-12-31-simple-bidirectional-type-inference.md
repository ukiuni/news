---
layout: post
title: "Simple Bidirectional Type Inference - 単純な双方向型推論"
date: 2025-12-31T09:38:13.403Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://ettolrach.com/blog/bidirectional_inference.html"
source_title: "Simple Bidirectional Type Inference"
source_id: 927165845
excerpt: "双方向型推論でSTLCを簡潔に実装し、エラーが劇的に分かりやすくなる手順をRustで解説"
---

# Simple Bidirectional Type Inference - 単純な双方向型推論
魅力的なタイトル: 型チェックの「推理」と「検証」を両方向で解く──エラーが劇的に分かりやすくなる bidirectional 型推論入門

## 要約
双方向（bidirectional）型推論は、導入（introduction）を「検証(チェック)」に、消去（elimination）を「推論」に分けることで実装が簡単かつエラーを親切にする型推論手法。単純型ラムダ計算（STLC）を例に、ルール設計から簡潔な Rust 実装へ結びつける手順を解説する。

## この記事を読むべき理由
- Rust/Haskell のような言語とは別に、より実装しやすくエラーメッセージが改善される代替手法を実践的に学べる。  
- コンパイラ実装や型システムの教材作成、言語実験（言語機能や型チェックのプロトタイプ）に直結する知見が得られる。  
- Swift も双方向アルゴリズムを採用しているという近年の実例から、日本のライブラリ／社内言語ツールの品質向上にも有効。

## 詳細解説
双方向型推論の中核は「推論 (infer)」と「検証 (check)」という2つの判断。導入則（例えばラムダ抽象の導入）は与えられた型を検証する向きに回し、消去則（関数適用など）は関数側の型を推論してから引数を検証する。設計手順は Pfenning の方法に従う：まず標準的な型付け則を書き、主導となる判断（principal judgement）に応じてコロン $:$ を矢印に置き換える。

言語の最小文法（STLC）例：
$$
\begin{aligned}
L, M &::= \texttt{false} \mid \texttt{true} \mid x \mid \lambda x. L \mid L\,M \mid L : A \\
A &::= \texttt{Bool} \mid A \to B
\end{aligned}
$$

主要ルール（概念）：
- Var: 変数は文脈から型を推論する（推論側）。
- Anno: 注釈は中身を指定された型で検証し、注釈型を推論として返す。
- ->Intro（ラムダ）: 結論の型 $A\to B$ が与えられるなら本体を $B$ として検証する（検証側）。
- ->Elim（適用）: 関数側を推論して $A\to B$ を得たら、引数を $A$ で検証して $B$ を返す（推論側）。
- TyEq: 推論結果を型等価で検証に回すためのルール（等しいかどうかを確かめる）。

実装戦略は infer と check を相互再帰させること。エラー報告を精緻にするためにソース位置（line/column）を持つ AST ノードを使う。

簡略化した Rust のデータ構造（一例）:
```rust
// Rust
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Type {
    Bool,
    Arrow(Box<Type>, Box<Type>),
    Unknown,
}

#[derive(Debug, Clone)]
pub enum Expr {
    True,
    False,
    Fv(String),
    Abs(String, Box<TrackedExpr>),
    App(Box<TrackedExpr>, Box<TrackedExpr>),
    Anno(Box<TrackedExpr>, Type),
}

#[derive(Debug, Clone)]
pub struct TrackedExpr {
    pub expr: Expr,
    pub line: usize,
    pub column: usize,
}
```

エラー表現と判定関数の型署名例:
```rust
// Rust
#[derive(Debug)]
pub enum ErrorKind { AnnotationMismatch{...}, AnnotationRequired, ApplicationNotArrow{actual: Type}, ... }

pub fn infer(tracked_expr: TrackedExpr, context: &mut HashMap<String, Type>) -> Result<Type, TypeError> { ... }
pub fn check(tracked_expr: TrackedExpr, ty: Type, context: &mut HashMap<String, Type>) -> Result<(), TypeError> { ... }
```

代表的な処理の流れ：
- infer(Fv): 文脈から型を取り出す。
- infer(Anno): check を呼び、成功なら注釈型を返す。
- infer(App): 関数側を infer して Arrow を得たら引数を check、結果として戻り型を返す。
- check(Abs, A->B): 文脈に引数型 $A$ を入れて本体を $B$ で check。

双方向は「必要なときに注釈を要求する」性質があるため、ユーザに明示的注釈を促すことでエラーメッセージが格段に良くなる。

## 実践ポイント
- 小さく始める：まず STLC を実装して infer/check の相互再帰を体験する。注釈を入れるテストケースを豊富に用意する。  
- エラーメッセージを先に設計する：どのケースでどんな位置情報を出すかを決めると実装が楽。  
- 拡張は段階的に：Bool → 関数 → if 式 → 多相へ。多相（polymorphism）は別途設計が必要だが、bidirectional は多相型推論にも向いている（実装例多数）。  
- VSCode 連携：言語サーバー（LSP）を作れば、位置情報付きエラーやインライン注釈候補を表示でき、開発者体験が向上する。  
- 日本語ドキュメント化：エラーメッセージのローカライズは採用する国内企業や OSS コミュニティでの導入障壁を下げる。

## 引用元
- タイトル: Simple Bidirectional Type Inference  
- URL: https://ettolrach.com/blog/bidirectional_inference.html
