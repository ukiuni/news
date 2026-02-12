---
layout: post
title: "Allocators from C to Zig - CからZigまでのアロケータ"
date: 2026-02-12T20:43:59.654Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://antonz.org/allocators/"
source_title: "Allocators from C to Zig"
source_id: 1106469186
excerpt: "RustのグローバルとZigの明示的アロケータを比較し、実務で使える選択肢と導入方針が一読で分かる"
image: "https://antonz.org/allocators/cover.png"
---

# Allocators from C to Zig - CからZigまでのアロケータ
Cの伝統を超えて学ぶ「選べる」メモリ管理：現代言語のアロケータ設計がわかる

## 要約
本記事は、Cの慣習的なヒープ割当てからRust/Zig/Odinのようなモダン言語が採る「アロケータを第一級に扱う」設計までを整理し、実務で役立つ考え方と具体的な使い方を短く解説します。

## この記事を読むべき理由
メモリ割当ての挙動はパフォーマンスや信頼性に直結します。日本でも組込み、ゲーム、サーバー（WebAssembly含む）開発で「どのアロケータを使うか／どう扱うか」を判断できる知識は差別化になります。

## 詳細解説
- 基本概念：アロケータはヒープ上に領域を確保・解放する仕組み。重要なのは「サイズ」と「アライメント（整列）」：
  - アライメントはアドレスが2のべき乗で割り切れる必要があり、CPU読み出し効率／SIMDに影響します（例：u8=1, i32=4, f64=8）。
  - 言語ごとにアロケータAPIの扱い方が異なる。

- Rust（グローバル中心）
  - 現行の安定APIは「グローバルアロケータ」。`GlobalAlloc`トレイトで `alloc` / `dealloc` を実装。
  - 型レベルでサイズ・アライメントを扱う`Layout`構造体があり、Box/Vecなどが内部で使う。
  - デフォルトは実行環境のシステムアロケータ（malloc等）だが、`#[global_allocator]`で切替可能。
  - 低レイヤー関数は失敗時にnullを返すが、標準コレクションは失敗時に `handle_alloc_error` でプロセスを終了する傾向がある。

```rust
// Rust: グローバルアロケータの指定例
use std::alloc::System;
#[global_allocator]
static GLOBAL: System = System;
fn main() { /* ... */ }
```

- Zig（明示的なアロケータパラメータ）
  - デフォルトのグローバルアロケータは無く、割当てが必要な関数はアロケータを引数で受け取る設計。
  - `std.mem.Allocator` は vtable（alloc/resize/remap/free）を持ち、`ret_addr` を渡して呼び出し元情報を得られるデバッグ支援が可能。
  - 高水準ラッパ（`allocator.alloc` / `allocator.create`）はエラーを返すので、明示的なエラーハンドリングが奨励される（panicしない）。

```zig
// Zig: アロケータを明示的に使う例
const allocator = std.heap.page_allocator;
const slice = try allocator.alloc(u8, 100);
defer allocator.free(slice);
```

- Odin（コンテキスト経由の暗黙的アロケータ）
  - スコープに「コンテキスト」があり、明示しなければそのコンテキストのデフォルトアロケータを使う。APIは単一プロシージャで操作モードを指定するスタイル。

- 設計思想の違い（要点）
  - グローバル型（Rustの現状）：簡潔だが全体へ影響を与えやすい。
  - 明示引数型（Zig）：透明性と切替の自由度が高く、テスト・組込みで有利。
  - コンテキスト型（Odin）：明示性と簡便性の折衷。

## 実践ポイント
- 開発フェーズではデバッグ用アロケータを使う（ダブルフリーやリーク検出が楽）。
- 一時的な多数割当てにはArena（アリーナ）を使い、まとめて解放して高速化。
- Rustでグローバルを差し替えるなら`#[global_allocator]`を理解する。低レイヤーでnull戻りを扱う場合は`handle_alloc_error`の挙動に注意。
- Zigを学ぶなら「 allocator を関数の引数にする習慣 」を早めに採り入れるとポータブルで安全な設計になる。
- 日本の現場では、組込みやWebAssembly（メモリ制約）での採用を見据え、明示的アロケータ設計が特に有効。まずは小さなライブラリでArenaやDebugAllocatorを試してみることを推奨。

以上を踏まえ、元記事は「言語設計がメモリ管理APIにどう反映されるか」を理解するのに最適です。興味があれば、実際に小さな実験プロジェクト（Rustでカスタムグローバル、Zigで明示アロケータ）を作って違いを体感してみてください。
