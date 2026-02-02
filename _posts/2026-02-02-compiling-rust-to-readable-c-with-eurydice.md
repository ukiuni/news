---
layout: post
title: "Compiling Rust to readable C with Eurydice - Rustを読みやすいCに変換するEurydice"
date: 2026-02-02T08:23:48.130Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lwn.net/SubscriberLink/1055211/6f51ebe751ce69a9/"
source_title: "Compiling Rust to readable C with Eurydice [LWN.net]"
source_id: 1267803852
excerpt: "Rustを構造そのまま可読Cへ変換し、既存C検証環境へ橋渡しするEurydiceの可能性と制約"
---

# Compiling Rust to readable C with Eurydice - Rustを読みやすいCに変換するEurydice
Rustコードを“構造そのまま”Cに変換して、安全性検証や既存C環境への橋渡しをする新ツールの全貌

## 要約
EurydiceはRustの中間表現（MIR）を取り込み、元のコード構造を保ったまま読みやすいCを生成するトランスパイラで、特に安全性検証や既存Cベースのツールチェーンへの移行で注目されます。

## この記事を読むべき理由
日本では組み込み、セキュリティ／認証が重要な業界が多く、既存の検証ツールや規格がCを前提にしていることが少なくありません。Rust採用を進めたいが検証インフラを変えられない場面で、Eurydiceは実用的な“自動ブリッジ”になり得ます。

## 詳細解説
- 全体アーキテクチャ: EurydiceはrustcのMIRをCharonでJSON化して取り込み、KaRaMeL由来のIRに変換、複数のパスでRust固有の構造を除去したうえでCコードを出力します。プロジェクトはAeneas群の一部で、InriaやMicrosoftなどが関わりライセンスはMIT/Apache‑2.0混在です。  
- 「構造を保つ」設計: 最終Cは最適化後の機械向けコードではなく、元の評価順序や制御構造を明確に保持します。たとえば一時変数を挿入して評価順をCの制約に合わせるなどの変換を行います。  
- 型・言語差の扱い:
  - ジェネリクスはモノモーフィ化され、型ごとに具体的な関数が生成されます（C的にはコード重複に）。安全クリティカルな現場では静的に分離された実装の方が好まれることもあります。  
  - 可変長型（DynamicallySized）については「柔軟配列型版」と「固定長配列版」の2種の型を出力し、解析上の意味を保つ工夫をしています。ただしこれがCのstrict-aliasing規則と技術的に衝突するため、-fno-strict-aliasingでのコンパイルが推奨されます。  
- 制約と現状: Charonが最新Rust機能（例: const generics）にまだ弱く、大規模なRustコードベース全体を網羅できる段階ではありません。現状は小さく自己完結したモジュール（暗号ライブラリなど）の変換に向いています。  
- 実績例: ポスト量子暗号ルーチンなど、検証や既存C環境での実行を目的とした変換に利用されています。

コード例（イメージ）
```rust
// rust
fn gcd(a: u64, b: u64) -> u64 {
    if b == 0 { a } else { gcd(b, a % b) }
}
fn lcm(a: u64, b: u64) -> u64 {
    (a * b) / gcd(a, b)
}
```

```c
// eurydice生成イメージ
uint64_t example_gcd(uint64_t a, uint64_t b) {
    uint64_t tmp;
    if (b == 0ULL) { tmp = a; }
    else { tmp = example_gcd(b, a % b); }
    return tmp;
}
uint64_t example_lcm(uint64_t a, uint64_t b) {
    uint64_t tmp = a * b;
    return tmp / example_gcd(a, b);
}
```

## 実践ポイント
- 使う場面: 「Rustで開発しつつ、既存のC向け検証ツールや規格を活かしたい」場合に有効。特に暗号や安全クリティカル分野で検討価値あり。  
- ビルド注意点: Eurydice出力は -fno-strict-aliasing でのコンパイルを検討する（strict-aliasing回避のため）。  
- スケール感: 大規模／最新機能を多用するコードにはまだ不向き。最初は小さなモジュールやライブラリ単位で試す。  
- 品質管理: モノモーフィ化によるコード膨張や、変換で挿入される一時変数の意味を理解した上でテストとレビューを行う。  
- 代替／併用: mrustcやgccrs等ほかのRustコンパイラバックエンドや、手動での移植と利害を比較して採用判断する。

短くまとめると、Eurydiceは「Rustの意味を保ったままCに落とす自動ツール」として、日本の既存検証チェーンや組み込み現場にとって魅力的な選択肢を提供しますが、現状は小〜中規模モジュール向けの実験的ツールである点に注意してください。
