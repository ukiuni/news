---
layout: post
title: "Rust–: Rust without the borrow checker - Rust--: Borrowチェッカーを無効にしたRust"
date: 2026-01-01T11:34:50.161Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/buyukakyuz/rustmm"
source_title: "Rust–: Rust without the borrow checker"
source_id: 46453062
excerpt: "借用チェッカー無効化RustでFFIや組込みの未定義動作を露呈し設計検証"
---

# Rust–: Rust without the borrow checker - Rust--: Borrowチェッカーを無効にしたRust
危険だけど目が離せない実験場：Borrowチェッカーを切ったRustで見える設計と安全性の境界

## 要約
Rustのコンパイラをフォークし、借用（borrow）チェッカーを無効化したプロジェクト。通常はコンパイルできないコードが通るため、所有権・借用ルールの影響を速やかに観察・検証できるが、同時に未定義動作やメモリ破壊のリスクがある。

## この記事を読むべき理由
借用ルールに由来するバグや設計制約に直面する日本のエンジニアにとって、ルールを一時的に外して挙動を観察できるツールは、問題の切り分け、FFIや組込み用途でのポート検証、教育・研究用途で非常に有用。だが誤用すれば実運用で致命的な問題を招くため、用途と注意点を正しく理解する必要がある。

## 詳細解説
- 何が変わっているか  
  このリポジトリはRustコンパイラ本体を修正し、「borrow checker（借用チェッカー）」の検査をスキップする。結果として、通常ならコンパイルエラーになる「ムーブ後の使用」「複数の可変参照」「可変参照中の値の使用」などがコンパイル・実行可能になる。

- なぜ危険か  
  Rustの借用チェッカーは、エイリアスと可変性、ライフタイムの静的保証によってデータ競合やUse‑After‑Freeなどを防いでいる。チェッカーを切るとこれらの静的保証が消え、未定義動作（UB）やヒープ破壊、データ競合が発生する可能性がある。実行時に即座にクラッシュしないことがしばしばで、バグの発見が難しくなる点も要注意。

- 使い方の概略  
  リポジトリはプリビルドバイナリとインストールスクリプトを提供。ビルドして使うことも可能で、examples/配下にチェッカー違反を示す例が揃っている。典型的なワークフローは、ローカルにインストールして alias を張り（例: rustmm）、実験用のソースをコンパイルして挙動を確認する、という流れ。

- 研究・デバッグでの価値  
  - Borrowチェッカーが拒否するコードが「実際にどう動くか」を素早く観察でき、設計上のトレードオフを実証的に評価できる。  
  - FFI境界や低レイヤ実装の安全性評価、既存Cコードとの統合テストでチェッカーの影響を切り分けられる。  
  - 教育用途で「なぜ借用ルールが必要か」を実例で示すのに有効。

- 制約と留意点  
  - 絶対に本番環境で使用しないこと。  
  - 実行は隔離された環境（コンテナ/VM）で行い、ASan/UBSanやMiri等のツールで追加検査する。  
  - ライセンスはRust本体と同様（Apache‑2.0 / MIT のデュアルライセンス）。

## 実践ポイント
- まずはサンドボックスで試す：コンテナや専用VM上でのみ実行する。  
- 検証手順（最小限）:
  1. インストール（プリビルド）:
     ```bash
     curl -sSL https://raw.githubusercontent.com/buyukakyuz/rustmm/main/install.sh | bash
     alias rustmm="$HOME/.rustmm/bin/rustc"
     ```
  2. 例をコンパイルして挙動を確認（examples/ にサンプルあり）。  
  3. AddressSanitizer/UBSanやMiriで追加チェックを行う。  
- 使ってよい場面:
  - 借用ルールに起因するコンパイル制約が問題の根源かを切り分けたい時。  
  - FFI周りや低レイヤで「実行時にどう振る舞うか」を調べたい研究・検証用途。  
- 絶対に避ける場面:
  - 本番バイナリのビルドや、信頼性が要求されるプロダクトライン。  
- 代替手段:
  - unsafe による限定的な破壊、MiriでのUB検出、より厳密なテストとコードレビュー。

参考となる最小サンプル（rustmmではコンパイル・実行される例）:
```rust
fn main() {
    let a = String::from("hello");
    let b = a;
    // 通常のRustではエラー: borrow of moved value
    println!("{}", a); // rustmmではコンパイル・実行される（ただし危険）
}
```

## 引用元
- タイトル: Rust–: Rust without the borrow checker  
- URL: https://github.com/buyukakyuz/rustmm
