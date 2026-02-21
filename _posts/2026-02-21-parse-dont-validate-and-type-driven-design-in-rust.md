---
layout: post
title: "Parse, Don't Validate and Type-Driven Design in Rust - パースせよ、検証に頼るな：Rustでの型駆動設計"
date: 2026-02-21T20:40:34.274Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.harudagondi.space/blog/parse-dont-validate-and-type-driven-design-in-rust/"
source_title: "Parse, don't Validate and Type-Driven Design in Rust — ramblings of @harudagondi"
source_id: 47103931
excerpt: "境界でパースして型に封じ、Rustでnewtypeで不変条件を保証し運用バグを激減"
image: "https://www.harudagondi.space/uploads/parse-dont-validate/tingey-injury-law-firm-veNb0DDegzE-unsplash.jpg"
---

# Parse, Don't Validate and Type-Driven Design in Rust - パースせよ、検証に頼るな：Rustでの型駆動設計
バグをコンパイル時に葬る：Rustで「検証」から「パース」へ移行する方法

## 要約
関数内部で値を検証するのではなく、入力境界で「パースして型に落とす」ことで、不変条件（invariants）を型レベルに担保し、ランタイムエラーや重複チェックを減らす設計パターンをRustで解説します。

## この記事を読むべき理由
日本のプロダクト開発では信頼性・保守性が重要です。型で不変条件を表現することでレビュー負荷や運用時のバグを減らし、CIやビルド段階で安心を高められます。特に金融系、組み込み、バックエンドSREチームに有用です。

## 詳細解説
- 問題提起：普通の関数でゼロ除算や空の配列をチェックすると、検証ロジックが各所に散らばり、同じチェックを何度も書いたり、リファクタで抜け落ちるリスクがある。
- パース vs 検証：検証(is_nonzero(x) -> bool)は値をチェックするだけで型に変化を与えない。一方でパース(to_nonzero(x) -> Option<NonZeroF32>)は「検証済み」を表す新しい型を返す（newtypeパターン）。
- newtypeパターン（例）
```rust
struct NonZeroF32(f32);

impl NonZeroF32 {
    fn new(n: f32) -> Option<Self> {
        if n == 0.0 { None } else { Some(NonZeroF32(n)) }
    }

    fn get(&self) -> f32 { self.0 }
}
```
- 利点：関数シグネチャで前提条件を明示できる（fn divide(a: f32, b: NonZeroF32) -> f32）。呼び出し側で一度だけ判定してパースすれば、内部に冗長なチェックは不要になる。Vecが非空であることを保証するNonEmptyVecなども同様。
- 実例：標準ライブラリのStringはVec<u8>からのパース（String::from_utf8）でUTF‑8不変条件を担保しており、serdeの型駆動パースも同じ考え方。
- 実践上の注意：過度なnewtypeは煩雑化を招く。既存の標準型（std::num::NonZeroU32 など）やTryFrom/TryInto、FromStr、Result/Optionを活用して境界でのパースを行うのが現実的。

## 実践ポイント
- 入力境界（APIエンドポイント、環境変数、ファイル読み取りなど）でまずパースして意味のある型に変換する。
- パースは Result / Option を返し、エラーは明示的に扱う（ログ・早期リターン）。
- newtypeには必要なトレイト（Deref、Display、演算トレイトなど）を実装し、使いやすさを担保する。
- 標準ライブラリの既存型（NonZero* 系）や TryFrom, FromStr を優先活用する。
- 過剰な型分割を避け、チームで命名規約と「ここでパースする」という境界を決めておく。

短く言えば、「不変条件は型で表現して境界でパースする」ことで安全性と可読性が格段に向上します。
