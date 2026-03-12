---
layout: post
title: "The Cost of Indirection in Rust - Rustにおける間接参照のコスト"
date: 2026-03-12T16:49:01.895Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.sebastiansastre.co/posts/cost-of-indirection-in-rust/"
source_title: "The Cost of Indirection in Rust | Selective Creativity"
source_id: 47312226
excerpt: "Rustの間接参照は大抵無視できる、実測で確かめ方と改善策を解説"
image: "https://blog.sebastiansastre.co/img/cost-of-indirection-rust.jpg"
---

# The Cost of Indirection in Rust - Rustにおける間接参照のコスト
その一行の呼び出しで可読性を捨てるな：Rustで「間接参照＝遅い」は大抵誤解だ

## 要約
Rustのasyncや通常の関数抽出で生じる「追加の関数呼び出しコスト」は、多くの実務ケースで無視できる。まずは最適化済みのビルドとプロファイラで事実を確かめ、読みやすさを優先せよ。

## この記事を読むべき理由
日本の多くの開発現場（Webサービス・業務アプリ）はI/Oやシステムコールが支配的で、ナノ秒単位の関数呼び出し差は実利に結びつきにくい。チームでの設計・コードレビューや保守性を守るための判断基準が得られる。

## 詳細解説
- Rustのasync関数は呼び出しで必ずヒープ割当や動的ディスパッチを生むわけではない。コンパイラはcalleeの状態を親Futureの状態機械にマージして「平坦化」することがあるため、追加のawaitや関数境界がコンパイル後同等になる場合が多い。
- 抽出で増えるコスト（引数受渡し、フレームセットアップ、間接ジャンプ）は、I/Oやロック、syscallと比べれば微小。最適化（releaseビルド）では小さな関数は自動でインラインされることが多い。
- 間接参照が問題になる典型例：極端にホットな内側ループ、dyn Traitによる動的ディスパッチ、コンパイラの可視性を失わせる明示的な境界（最適化不能な箇所）。
- 人間コスト：抽出を拒んで1関数に詰め込むと可読性・テスト性・レビュー時間が悪化し、長期的な総コストはナノ秒のランタイム差を遥かに上回る。

簡単な検証例（比較用）:
```rust
// rust
#[no_mangle]
fn do_the_work_inlined() -> u64 {
    let mut acc = 0u64;
    for i in 1..=10 { acc = acc.wrapping_mul(i).wrapping_add(12345); }
    acc
}

#[no_mangle]
fn do_the_work_extracted() -> u64 {
    do_some_work()
}

#[no_mangle]
fn do_some_work() -> u64 {
    let mut acc = 0u64;
    for i in 1..=10 { acc = acc.wrapping_mul(i).wrapping_add(12345); }
    acc
}
```

アセンブリやベンチで確かめるコマンド例:
```bash
# アセンブリ確認（release）
cargo rustc --release -- --emit asm

# ベンチ（Criterion）
cargo bench
```

プロファイラ例: valgrind --tool=callgrind / perf record → perf report / flamegraph / Instruments (macOS) などで実運用下のホットスポットを確認する。

## 実践ポイント
- まずreleaseビルドとプロファイラでホットスポットを確認する。数ナノ秒の差で設計を犠牲にするな。
- 読みやすさ・テスト性を優先して関数を抽出し、名前で意味を与える。抽出は保守の投資だ。
- 本当にボトルネックが見つかったら、そこで初めてinliningや低レイヤ最適化（dyn回避等）を検討する。#[inline]は計測で裏付けてから使う。
- 日本のチーム文化ではコードレビュー/ドキュメントが価値を生む。微小な実行時間節約より「理解しやすさ」を重視しよう。

この記事の結論：間接参照そのものを恐れてコードの可読性を犠牲にする必要はない。測定してから最適化を。
