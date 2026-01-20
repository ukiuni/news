---
layout: post
title: "Increasing the performance of WebAssembly Text Format parser by 350% - WebAssembly Text Format（WAT）パーサを350%高速化する方法"
date: 2026-01-20T10:25:51.004Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.gplane.win/posts/improve-wat-parser-perf.html"
source_title: "How did I improve the performance of WAT parser? | Pig Fang"
source_id: 46629399
excerpt: "WATパーサを手書き化と割当削減で350%高速化した具体手法を公開"
---

# Increasing the performance of WebAssembly Text Format parser by 350% - WebAssembly Text Format（WAT）パーサを350%高速化する方法
WATパーサを丸ごと書き換えて性能を3.5倍にした“現場で効く”最適化テクニック集

## 要約
Rust製のWAT（WebAssembly Text Format）パーサを、パーサコンビネータから手書き実装に置き換え、トークンの使い回しやバイト単位の判定、不要な割当て回避などを組み合わせてベンチマークで約350%の高速化を達成した話。

## この記事を読むべき理由
小さな構文解析処理でも繰り返し大量に動くと遅延やコストにつながります。Wasmツールやコンパイラインフラを扱う日本の開発者にとって、低レイテンシ化やリソース削減に直結する実践的テクニックが学べます。

## 詳細解説
元記事は wasm-language-tools の WAT パーサ改善の経緯と実装上のポイントを解説しています。主な技術的施策は次の通りです。

- 手書きパーサへ切替  
  - パーサコンビネータ（例：winnow）は記述しやすいがランタイムオーバーヘッドが出やすい。ホットパスを手書きにすることで余計な抽象化を排し高速化を実現。

- 既知トークン／ノードの使い回し（green token/node のクローン）  
  - WATは括弧やキーワードが頻出するため、rowan::GreenToken/GreenNode の内部が Arc である点を利用して事前生成し LazyLock に置いて必要時にクローンすることで割当てコストを削減。

- キーワード判定を文字列比較ではなくバイトプレフィックスで行う  
  - ソースバッファのバイト列に対して starts_with で早期判定し、続く文字が識別子文字かどうかを別途チェックして誤判定を防止（例："function" が "func" を含む場合の対処）。

- ASCII系トークンでの境界チェック回避（get_unchecked の活用）  
  - 文字列境界や UTF-8 の逐一チェックを避け、ASCII範囲のみのトークンで安全にオプトアウトして速度改善（unsafe 部分はテストでカバーすること）。

- 軽量な Token 型を中間表現に使う  
  - rowan::GreenToken を都度作るのは高コスト。まずは小さな Token<'s> { kind, text } を吐き、必要になった段階で GreenToken に変換する戦略。

- 共有の single Vec を使って割当てを最小化  
  - 各ノードで新しい Vec を作る代わりに一つの Vec を共有し、ノード開始時の長さを start index として保持、ノード終了時に drain で該当範囲を取り出して GreenNode を作る。スタック風の管理で追加の一時配列を減らす。

- ベンチ結果  
  - 改善前: 約59 µs → 改善後: 約13 µs（サンプルモジュールでの測定）。複合的な最適化で大幅な速度向上が確認された。

## 日本市場との関連
- 日本でもWasmはサーバレス、エッジ実行、ブラウザ外ツール（AOT、バイナリ解析）で広まりつつあります。大量のWAT解析やツールチェインを自社で持つ場合、こうした最適化はCI時間削減、低レイテンシ化、クラウドコスト削減に直結します。  
- 組み込み系や省電力環境でも割当てを減らす手法は有効です。安全性を担保しつつ unsafe 最適化を使うノウハウは日本のプロダクト開発でも価値があります。

## 実践ポイント
- 優先順位付け：まずはプロファイラでホットパスを特定し、その箇所を手書きにする。全体を書き換える必要はない。  
- トークン再利用：頻出トークンは事前生成して使い回す。Arc や参照カウント方式との相性を確認する。  
- バイト単位判定：UTF-8全体扱いではなく、ASCII系キーワードはバイト比較で早期判定する（ただし識別子境界を必ずチェック）。  
- 割当て削減：使い捨て Vec を大量に作らない。共有バッファ＋start index＋drain で子要素をまとめて処理する。  
- 安全性対策：unsafe（get_unchecked 等）を使う場合はユニットテストとファズテストで境界ケースを網羅する。  
- 測定を忘れない：小さな変更でも影響があるので、ベンチと統計的差異検定で効果を確認する。

簡単な Token 型の例（Rust）:

```rust
rust
struct Token<'s> {
    kind: SyntaxKind,
    text: &'s str,
}
```

以上を踏まえ、WATに限らず「ホットループの抽象化をほどく」「共通データの再利用」「不要な割当てを減らす」という原則はどのパーサ／コンパイラ実装でも強力に効きます。
