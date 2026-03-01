---
layout: post
title: "Supercharge Rust functions with implicit arguments using CGP v0.7.0 - CGP v0.7.0で暗黙引数でRust関数を強化"
date: 2026-03-01T14:15:02.433Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://contextgeneric.dev/blog/v0.7.0-release"
source_title: "Supercharge Rust functions with implicit arguments using CGP v0.7.0 | Context-Generic Programming"
source_id: 1644146116
excerpt: "CGP v0.7.0で暗黙引数を導入、Rustの引数と型ボイラープレートを大幅削減"
image: "https://contextgeneric.dev/img/cgp-logo.png"
---

# Supercharge Rust functions with implicit arguments using CGP v0.7.0 - CGP v0.7.0で暗黙引数でRust関数を強化
「引数が消える」――Rustのボイラープレートを一気に削減するCGP v0.7.0の衝撃

## 要約
CGP v0.7.0は新しい注釈群（#[cgp_fn], #[implicit], #[uses], #[extend], #[use_provider], #[use_type]）を導入し、コンテキストに基づく汎用関数を通常の関数構文で書けるようにして引数の受け渡しと型ボイラープレートを大幅に削減する。

## この記事を読むべき理由
日本のチームやライブラリ開発では、構造体に機能を凝集すると変更耐性が落ちたりコード重複が増えがち。CGPは「コンテキスト（self）のフィールドから自動で値を取り出す」ことで、複数コンテキスト間で同じ関数定義を安全に再利用でき、保守性とAPIの拡張性を高めます。

## 詳細解説
- #[cgp_fn]：通常の関数に付けると「コンテキスト汎用」の能力に変換され、最初の引数は &self を受け取る想定になる。  
- #[implicit]：引数に付けると、その値を呼び出し側が渡すのではなく `&self` のフィールドから名前と型で自動解決する（例：$width \times height$ を計算する関数は呼び出し側で width, height を明示しなくてよい）。  
- #[uses] / #[extend]：ほかのCGP関数を取り込み（uses）・再公開（extend）することで、関数の合成と依存伝搬を簡潔に表現。  
- #[cgp_impl] と #[implicit]：プロバイダ実装の内部でも暗黙引数が使え、以前必要だったゲッタートレイト層が不要に。  
- #[use_provider]：高階プロバイダで内部のプロバイダ型要件を簡潔に宣言する。Self を先頭ジェネリクスに挿入してくれるので where 節が楽。  
- #[use_type]：関連型（例：Scalar）を短縮名で使えるようにする糖衣。内部的には Self::Scalar に展開されゼロコスト。  
- Scalaのimplicitsとの違い：解決は常に `self` のフィールド名＋型に限定され、スコープ探索や曖昧さが発生しないためトラブルが少ない。

簡単な例（要点のみ）:

```rust
rust
#[cgp_fn]
pub fn rectangle_area(&self, #[implicit] width: f64, #[implicit] height: f64) -> f64 {
    width * height
}

#[derive(HasField)]
pub struct PlainRectangle { pub width: f64, pub height: f64 }

let r = PlainRectangle { width: 2.0, height: 3.0 };
let area = r.rectangle_area(); // 6.0
```

## 実践ポイント
- まず公式の Area Calculation チュートリアルを読み、#[derive(HasField)] の使い方を確認する。  
- 小さなユーティリティ関数を #[cgp_fn] + #[implicit] に置き換え、呼び出し-site の引数削減効果を体感する。  
- ライブラリ設計では #[uses]/#[extend] で機能を合成し、コンテキストを肥大化させずに機能追加する。  
- 数値型を抽象化したい場合は #[use_type] を活用して Self::Scalar の冗長を回避する。  
- CIで型エラーのメッセージを確認しつつ導入する（解決範囲が self に限定されるためデバッグは比較的簡単）。

導入は Cargo に cgp を追加して試すだけで効果が実感しやすく、日本のプロダクトでもコードの可読性・拡張性向上に直結します。
