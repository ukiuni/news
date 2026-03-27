---
layout: post
title: "Bigoish: Test the empirical computational complexity of Rust algorithms - Bigoish：Rustアルゴリズムの実行計算量を検証する"
date: 2026-03-27T17:00:32.401Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://docs.rs/bigoish/"
source_title: "bigoish - Rust"
source_id: 1591848443
excerpt: "Rustコードが本当に $O(n\log n)$ か CIで自動検証できるテストライブラリ"
---

# Bigoish: Test the empirical computational complexity of Rust algorithms - Bigoish：Rustアルゴリズムの実行計算量を検証する
実行で証明！Rustコードが本当に $O(n\log n)$ か確かめる方法

## 要約
bigoish は、関数の実行時間データから「どの計算量モデルが最も当てはまるか」を統計的に判定するRust向けテストライブラリです。期待するモデルが実際に最良フィットかを自動判定します。

## この記事を読むべき理由
実装したアルゴリズムが理論どおりにスケールしているかはバグ発見やパフォーマンス保証に直結します。特に日本のプロダクトでは、大量データやリアルタイム処理での挙動確認が重要です。本ツールはテストに組み込めるためCIでの防衛線になります。

## 詳細解説
- 目的：与えた関数と複数サイズの入力で実行時間を測定し、複数の複雑度モデル（定数、$n$, $n^2$, $n^3$, $\sqrt{n}$, $\log n$, $n\log n$, $\log\log n$ 等）と比較して「どのモデルが最もよく当てはまるか」を決定します。  
- 主要API：`assert_best_fit(expected_model, func, inputs)`。期待モデルが最良でなければテストはパニックします。`growing_inputs(start, maker, count)` で指数的に増える入力列を作れます。  
- 測定方法：Windows/macOS ではスレッドのCPU時刻、Linux では可能なら命令カウント（不可能な環境はCPU時刻）を使います。環境変数 `BIGOISH_TIME_ONLY=1` で常にCPU時刻に固定できます。  
- リリースとテストプロファイルの差：`cargo test` はデフォルトで test プロファイル（最適化弱め）で動くため、最適化によるスケーリング差がある場合は `--release` でテストを走らせるか、`#[cfg(not(debug_assertions))]` を使ってリリース時のみチェックしてください。  
- 視覚化とアクセシビリティ：失敗時にターミナルでフィットグラフを出力します。画面読み上げ環境では `NO_COLORS` や `TERM=dumb` を設定して無効化可能です。  
- 拡張：既存の `Model` 実装を組み合わせて新モデルを作ることもできます。

例（要旨）：

```rust
// rust
use bigoish::{N, Log, assert_best_fit, growing_inputs};

fn sort(mut v: Vec<i64>) -> Vec<i64> { v.sort(); v }

fn make_vec(n: usize) -> Vec<i64> {
    use fastrand;
    std::iter::repeat_with(|| fastrand::i64(..)).take(n).collect()
}

// n * log(n) が最良フィットかを確認
assert_best_fit(N * Log(N), sort, growing_inputs(10, make_vec, 25));
```

## 実践ポイント
- 入力量は多め（例：20以上）かつサイズは桁数で広げる（10, 100, 1_000…）こと。  
- 最小入力サイズを十分大きくしてノイズを減らす。小さすぎると測定誤差が大きい。  
- 最終検証は `cargo test --release` で行い、コンパイラ最適化後の振る舞いを確認する。  
- Linuxで命令カウントが使えないCI（例：GitHub Actions）の場合は `BIGOISH_TIME_ONLY=1` を検討。  
- テストが視覚出力を行う点に注意し、CIや読み上げ環境では環境変数で制御する。

以上を取り入れれば、実装が本当に期待どおりスケールしているかを自動テストで守れるようになります。
