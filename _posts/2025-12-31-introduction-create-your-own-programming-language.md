---
layout: post
title: "Introduction - Create Your Own Programming Language with Rust - Rustで自分のプログラミング言語を作る入門"
date: 2025-12-31T20:39:52.945Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://createlang.rs"
source_title: "Introduction - Create Your Own Programming Language with Rust"
source_id: 474201602
excerpt: "Rustで電卓からJITやオブジェクト指向まで段階的に自作言語を作る実践ロードマップ"
---

# Introduction - Create Your Own Programming Language with Rust - Rustで自分のプログラミング言語を作る入門
Rustで「自分だけの言語」を4段階で実装する実践書を要約し、今すぐ試せるロードマップを提示します。

## 要約
Rustを使って電卓レベルの言語から型付き・JIT対応・オブジェクト指向まで段階的に作る方法を解説するチュートリアルシリーズ。パーサ（pest）、AST、インタプリタ、VM、LLVM/JITまで実装例付きで学べます。

## この記事を読むべき理由
コンパイラや実行系の仕組みを理解すると、システム設計力やパフォーマンス最適化能力が飛躍的に向上します。日本でもRust採用や低レイヤー開発の需要が高まる中、実践的に手を動かして学べる教材は希少です。本シリーズは最小限の例から着実に拡張していくため、初心者〜中級者に最適です。

## 詳細解説
- 動機と方針  
  教材は「最も小さな例（電卓）」から始めてコア概念を共に作りながら学ぶ設計。既存の成熟ライブラリ（pest, LLVM/inkwellなど）を活用して再発明を避け、理解を深めます。

- 学習の流れ（4言語の段階）  
  1. Calculator（18行の文法）: PEG（pest）でパーサを生成し、ASTを作成。インタプリタ、バイトコードVM、JITの3つの実行バックエンドを比較。  
  2. Firstlang（70行）: 変数、関数、制御構造、再帰を追加。木を歩くインタプリタでスコープと呼び出しスタックを学ぶ。  
  3. Secondlang（77行）: 静的型、型推論、最適化パスを導入してLLVMでネイティブコードを生成。文法の変更は小さいがコンパイラフェーズが増える点が学びどころ。  
  4. Thirdlang（140行）: クラス・メソッド・コンストラクタ・メモリ管理を追加。ヒープ割当てやLLVMの構造体表現が登場。

- 実装上のポイント  
  - 文法は短く、意味解析や型付けで複雑さが増す設計。  
  - 同じASTから複数の実行戦略（インタプリタ、VM、JIT）へ分岐させることで性能と実装のトレードオフを学べる。  
  - JITはnightly Rustと適切なLLVMバージョン（inkwellのfeatures）を必要とする点に注意。

- 必要環境（抜粋）  
  - Calculator/Firstlang: stable Rust 1.70+（外部依存なし）  
  - Secondlang/Thirdlang: nightly Rust + LLVM（inkwellのfeatureをLLVM版に合わせる）

- 実例コマンド（ローカルで試す）  
```bash
# リポジトリを取得
git clone https://github.com/ehsanmok/create-your-own-lang-with-rust
cd create-your-own-lang-with-rust

# Calculator（インタプリタ）
cd calculator
cargo run --bin main examples/simple.calc

# Firstlang（インタプリタ）
cd ../firstlang
cargo run -- examples/fibonacci.fl

# Secondlang（nightly + LLVMが必要）
rustup toolchain install nightly
cd ../secondlang
rustup run nightly cargo run -- examples/fibonacci.sl
```

- inkwellの例（Cargo.tomlの機能指定）
```toml
[dependencies]
inkwell = { version = "0.7", features = ["llvm20-1"] } # LLVMのバージョンに合わせる
```

## 実践ポイント
- まずはCalculatorを丸ごと動かし、ASTの構造と評価の流れを手で追う。変更（例: 新しい二項演算子）を入れて差分を確認する。  
- 次にFirstlangでスコープ／スタックの振る舞いを理解し、簡単な関数を追加してみる。  
- 型チェックや型推論に興味がある場合はSecondlangで型推論フェーズのコードを読み、単純な最適化パス（定数畳み込みなど）を実装して効果を測る。  
- JITを試す際はローカルのLLVMバージョンとinkwellのfeatureを揃えること。DockerやHomebrewでLLVMを管理すると環境差が減る。  
- 学びの単位を小さく保ち、各段階で「小さく動く」変更を加えることで理解が定着する。

## 引用元
- タイトル: Introduction - Create Your Own Programming Language with Rust  
- URL: https://createlang.rs
