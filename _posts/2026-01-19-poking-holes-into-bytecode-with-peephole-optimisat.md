---
layout: post
title: "Poking holes into bytecode with peephole optimisations - バイトコードに穴を開ける：ピーホール最適化"
date: 2026-01-19T02:30:31.460Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://xnacly.me/posts/2026/purple-garden-first-optimisations/"
source_title: "Poking holes into bytecode with peephole optimisations | xnacly - blog"
source_id: 46624396
excerpt: "即値畳み込みとNOP削除で起動を劇的に速くするピーホール最適化入門"
---

# Poking holes into bytecode with peephole optimisations - バイトコードに穴を開ける：ピーホール最適化
「起動が速いランタイム」はこう作る — 小さな窓で大きな改善をするピーホール最適化入門

## 要約
小さな「窓（window）」で局所的に命令列を書き換えるピーホール最適化で、不要な命令の削除や即値演算の畳み込みを行い、起動時間と実行コストを下げる手法を紹介する。

## この記事を読むべき理由
言語ランタイムやバイトコードVMを作るとき、複雑なIR最適化を入れる前でも効果が出る手軽な最適化が欲しくなる。特に起動速度が重要なCLIツールやサーバーレス、組み込み系で日本のプロダクトにも即応用できる実践的なテクニックだから。

## 詳細解説
元記事は C から Rust にリファクタ中のランタイム「purple-garden」で導入した初期の最適化を解説している。全体パイプラインはざっくり：
Tokenizer → Parser（AST）→ コンパイラ（AST→バイトコード）→ ピーホール最適化 → インタプリタ / JIT

ピーホール最適化の特徴：
- 局所（本文では窓サイズ $3$）での単一パス最適化。大規模な再解析は行わず、IR 側で取りこぼした簡易パターンを拾う役割。
- 起動時間を重視して単パス・軽量にしているため、再帰的（多段階）な畳み込みは行わない。より複雑な定数畳み込みはIR最適化が担当する想定。

主な最適化例
- self_move：Mov 命令で dst == src（自己移動）は NOP に置換して削除。
- const_binary：直前2命令が LoadImm（即値ロード）で、その直後が加減乗除の二項演算なら、事前に計算して単一の LoadImm に置き換える（例: $2+3$ → $5$）。オーバーフローは現状 wrapping（符号なしの巻き付け）で扱っているが将来的にコンパイル時エラーにする余地あり。

簡潔な Rust のイメージ（抜粋）：
```rust
// Rust
const WINDOW_SIZE: usize = 3;
pub fn bc(bc: &mut Vec<Op>) {
    for i in 0..=bc.len().saturating_sub(WINDOW_SIZE) {
        let window = &mut bc[i .. i + WINDOW_SIZE];
        const_binary(window);
        self_move(window);
    }
    bc.retain(|op| !matches!(op, Op::Nop));
}
```

観測性（trace）
- opt_trace! マクロで最適化が起きた箇所をログ出力でき、 --features trace で詳細を得られる。起動時の挙動を把握するのに有効。

統合とフラグ
- 起動時間優先のため、現状は -O1 フラグでのみピーホールを有効化する設計。軽量最適化を必要に応じてオンにできる。

テスト
- パターン単位のユニットテストを用意して、置換の正当性を保証。完全な意味論同値性の検証ではなく、書き換えパターンの検査に集中している。

## 実践ポイント
- 小さく始める：まず窓サイズ $3$ で self_move と const_binary を実装してパフォーマンスと起動時間を確認する。
- 単一パスの利点：起動時間に敏感なアプリ（CLI、サーバーレスのファーストリクエスト、組み込み）では単パスが有利。
- ロギングを用意する：opt_trace のようなトレースをビルドフラグで切れるようにして、最適化が動いた場所を把握する。
- 明確な役割分担：再帰的・複雑な最適化はIR側に任せ、ピーホールは「漏れ取り（fallback）」に限定する方が設計がシンプルになる。
- テストを書く：置換パターン単位でユニットテストを用意し、最適化による副作用（レジスタ割り当てのずれなど）を早期に検出する。
- オーバーフロー方針を決める：現状は wrapping。言語仕様に応じてコンパイル時エラーや警告に変更するか検討する。

短時間で効果が出る最適化手法として、ピーホールは実用的で導入コストも低い。まずは自分のVMで小さな窓を試し、起動時の命令ストリームがどう変わるかを観察してみよう。
