---
layout: post
title: "Borrow-checking surprises - 借用チェックの驚き"
date: 2026-04-08T19:22:58.775Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.scattered-thoughts.net/writing/borrow-checking-surprises/"
source_title: "Borrow-checking surprises"
source_id: 1104816765
excerpt: "Rustの借用チェックが裏切る4例と回避法を直観的に解説、今すぐバグを防ぐ具体策付き"
---

# Borrow-checking surprises - 借用チェックの驚き
Rustの借用が裏切る？「評価順」「二段階借用」「再借用」「drop」の微妙な違いでハマる4つの実例

## 要約
Rustの borrow-checker は基本ルールは単純でも、評価順や構文の砂糖づけ（desugar）、再借用、明示的dropなどの例外があり、直感と異なる挙動を取ることがある。この記事は代表的な4つのサンプルを分かりやすく解説する。

## この記事を読むべき理由
Rustは日本でも注目が高く、安全性を武器に採用が増えている。だが現場で初心者や中級者が「なんでコンパイルエラー／通るの？」と迷う借用周りの落とし穴はコストと時間につながる。本記事は実例でその原因と対策を短く示す。

## 詳細解説
1) 左辺と右辺の評価順（思い込みでバグ）
```rust
// rust
fn main() {
    let mut x = 0;
    let y = &mut x;
    *y = *y + 1;
}
```
直感では左辺で可変参照を取った後に右辺がxを読むのは不可と思うが、Rustは右辺（rvalue）を先に評価するため問題なく動く。評価順を意識すること。

2) += とメソッド呼び出しの二相借用（two-phase borrow）
```rust
// rust
fn main() {
    let mut x = 0;
    x += x; // 表面上はOK
    // desugar: AddAssign::add_assign(&mut x, x) はコンパイルエラーになる場合がある
}
```
+= は構文糖で、.add_assign 呼び出し経由では「二相借用」が働き、一時的に不変参照→可変参照へ切り替わる場面がある。desugar すると二相借用が適用されないため差が出る。

3) 関数呼び出しでの再借用（reborrow）
```rust
// rust
fn id(y: &mut usize) -> &mut usize { y }
fn main() {
    let mut x = 0;
    let y = &mut x;
    let z = id(y); // 実際は再借用: id(&mut *y)
    *y = 1; // エラーにならない（zは再借用で、y自体はmoveされない）
}
```
関数引数への直接渡しは再借用に変換される場合があり、元の参照が「move」されず使えることがある。見た目だけで判断しない。

4) 参照の寿命と明示的dropの扱い
```rust
// rust
fn foo(a: &mut usize) -> &mut usize {
    let b = &mut *a;
    let c = &mut *b;
    // drop(b); // これはコンパイルエラーになる
    c
}
```
c のライフタイムは a に紐づくため一見安全だが、drop(b) は b をムーブする必要があり、borrow のルールと衝突してエラーになる。ライフタイムと値のムーブを区別すること。

## 実践ポイント
- 評価順（rhs→lhs）を意識する。デバッグ時はprintln!で確認すると理解が早い。  
- 構文糖（+= やメソッド呼び出し）の desugar を意識し、挙動が違う場面を疑う。  
- 関数呼び出しは再借用されることがある。参照が move されたかは型と文脈で判断する。  
- 明示的な drop は参照の借用ルールと衝突することがあるので注意。  
- 疑問が出たら小さな再現コードを書き、rustc のエラーメッセージ（E0503, E0382, E0505 など）を読む習慣をつける。

必要なら各例の最小再現コードやコマンド（rustcのオプション）を示すサンプルを用意する。
