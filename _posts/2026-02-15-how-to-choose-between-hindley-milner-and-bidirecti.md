---
layout: post
title: "How to Choose Between Hindley-Milner and Bidirectional Typing - Hindley-Milner と双方向型付けの選び方"
date: 2026-02-15T19:16:36.143Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://thunderseethe.dev/posts/how-to-choose-between-hm-and-bidir/"
source_title: "How to Choose Between Hindley-Milner and Bidirectional Typing · Thunderseethe's Devlog"
source_id: 440971865
excerpt: "ジェネリクス要否で決める型システム選択術—軽量双方向からHMへ拡張可能"
---

# How to Choose Between Hindley-Milner and Bidirectional Typing - Hindley-Milner と双方向型付けの選び方
言語設計で迷ったら「HMか双方向か？」ではなく、まず「ジェネリクスが要るか？」と問い直そう — 型推論の本質をシンプルに導く選択基準

## 要約
Hindley-Milner（HM）は型変数と結合（unification）を中心に据えた自動推論を提供する。一方で双方向型付け（bidirectional）は注釈を活用して推論の必要性を減らせるが、結合を組み込めばHMの能力を包含できる。実際の判断軸は「ジェネリクス（汎用型）をサポートしたいかどうか」である。

## この記事を読むべき理由
言語実装や学習目的で小さな言語を作るとき、型システム選びは開発コストに直結する。日本の開発者が「何を削ぎ落とし、何を残すべきか」を最短で判断できる実践的指針を示すため。

## 詳細解説
- HM（Hindley-Milner）
  - 型変数と結合（unification）を使い、プログラマが型を書かなくても多くを推論する。
  - ジェネリクスや型変数の導入が自然で、一般目的言語向き。
- 双方向型付け（Bidirectional）
  - 「infer（推論）」と「check（検査）」の二つのモードで型付けを行う。注釈を要所で与えることで、推論を最小化できる。
  - 文献には結合無しの実装例も多いが、結合を組み合わせることでHMができることは全て行える（スーパーセット的関係）。
- 結合（unification）の役割
  - 型変数に値を割り当て、式同士を一致させる処理。ジェネリクス実装ではほぼ必須。
  - 双方向のcheckで「厳密な等価」ではなく「結合可能か」を判定するようにすれば、双方向＋結合で強力な型推論が可能になる。
- 実装上の簡単なイメージ（Rust風）
```rust
// 推論と検査の分離（概念イメージ）
fn infer(env: &Env, ast: &Ast) -> Result<Type, TypeError> { /* 推論 */ }
fn check(env: &Env, ast: &Ast, ty: &Type) -> Result<(), TypeError> {
    let inferred = infer(env, ast)?;
    unify(&inferred, ty) // 等価ではなく結合を使う
}
```
- 双方向の利点
  - 初期段階や教育目的では、注釈を多めにして結合を省くことで実装を簡潔にできる。
  - 将来的に結合を追加する余地を残せる：最初はcheck-heavyで始め、後からinfer/unifyを拡張する設計が現実的。

## 実践ポイント
- まず答えるべき問い：あなたの言語は「ジェネリクス（汎用型）を必要とするか？」  
  - 必要なら結合を組み込む設計（HMか双方向＋unify）が適切。
  - 不要なら双方向＋注釈中心で実装コストを下げる。
- 開発戦略：最初は双方向（check重視）で軽く作り、要件が出たらunifyを追加する。
- DSL（ドメイン固有言語）はジェネリクスを省いて単純化するのが有効。ただし将来拡張の可能性は念頭に。
- 実装のテスト：型推論のケース（タプル、関数、ジェネリック型）を単位テストで網羅しておく。
- 学びたいなら結合の実装は良い教材。学習目的でなければ必要最小限で始めるのが早道。

以上。必要なら実装サンプル（unifyアルゴリズムやcheck/inferの具体例）を短いコードで示しますか？
