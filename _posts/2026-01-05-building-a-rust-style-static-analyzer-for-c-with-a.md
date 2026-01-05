---
  layout: post
  title: "Building a Rust-style static analyzer for C++ with AI - C++にRust風静的解析器をAIで作る話"
  date: 2026-01-05T07:11:42.084Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "http://mpaxos.com/blog/rusty-cpp.html"
  source_title: "The Story of Building a Rust-Style Static Analyzer for C++ with AI | Home"
  source_id: 46495539
  excerpt: "AIで短期間に作ったプロトタイプで、既存C++へRust風借用チェックを段階導入してメモリ安全を実現"
  ---

# Building a Rust-style static analyzer for C++ with AI - C++にRust風静的解析器をAIで作る話
AIと実装力で実現した「C++に部分的にRustの安全性を持ち込む」現実的アプローチ

## 要約
15年近くC++でシステム開発を続けた著者が、AIコーディングアシスタントを活用して「Rust風の借用チェック」をC++へ持ち込む静的解析器をプロトタイプとして実装した話。既存コードを壊さずに段階的にメモリ安全性を強化する現実的な方法を提示する。

## この記事を読むべき理由
日本の産業用途（組み込み、ゲーム、金融、通信など）は依然として大量のC++資産に依存しており、セグメンテーションフォルトやメモリ破損は大きなコスト源です。本稿が示す手法は「全部をRustに書き直す」以外の実用的な選択肢であり、既存資産を残したまま安全性を向上させる現実解を提供します。

## 詳細解説
- 基本方針: コードの文法を変えずに互換性を保つため、注釈はコメントベース。関数や名前空間に対して `@safe` / `@unsafe` で境界を宣言し、`@safe` からは直接 `@unsafe` を呼べないルールを採用。これにより監査境界が明確になる。
  ```cpp
  // @safe
  void safe_func() {
    int value = 42;
    // @unsafe {
    //   std::vector<int> v;
    //   v.push_back(value);
    // }
  }
  ```

- ミュータビリティと借用: C++の `const` を「不変」、非 `const` を「可変」と見なすことでRustの mut と同等の概念を導入。複数の不変借用は許可、可変借用は排他、可変と不変の混在はエラーにする借用チェックを実施。
  - 例: 複数の `const int&` はOK、複数の `int&` はNG、`const int&` と `int&` の混在はNG。

- 外部注釈 (External annotations): 標準ライブラリやサードパーティのヘッダを直接変更できないため、外部注釈ファイルで関数の安全性とライフタイム関係を付与。`where`句で返り値と引数の寿命関係を記述し、外部APIから生じるダングリングを検出する。
  ```
// @external:
// strlen: [safe, (const char* str) -> owned]
// strchr: [safe, (const char* str, int c) -> const char* where str: 'a, return: 'a]
  ```

- ツールチェーンと実装上の課題: libclangを使ってASTを取得するが、名前解決や修飾子の取り扱いで不整合が起きやすく、そこは実運用で手を入れる必要がある。解析は単一ファイル中心で実装可能だが、大規模クロスファイル解析は工数が増える。

- Rust標準型の移植: `Box` / `Arc` / `Vec` / `Option` / `Result` などの振る舞いをC++で再現するライブラリを作成。`unique_ptr` と `Box` の違い（null許容の有無など）に注意して実装することでRust的な所有権モデルを模倣。

- スレッド安全 (Send/Sync): C++のConceptsを利用して型にSend/Syncの概念を付与。今は手動マーキングが必要だが、段階的に導入可能。

- AIの役割: 著者はAIコーディングアシスタント（Claude等）を使ってプロトタイプの設計、テスト作成、反復修正を進めた。AIが細かな実装やテストケースの自動生成・修正を支援し、短期間で機能するプロトタイプを得られた点が重要。

- 使い方（概略）:
  ```bash
  $ rusty-cpp-checker myfile.cpp
  Rusty C++ Checker
  Analyzing: myfile.cpp
  ✗ Found 3 violation(s) in myfile.cpp:
    - Cannot create mutable reference to 'value': already mutably borrowed
    - Use after move: variable 'ptr' has been moved
  ```
  大規模プロジェクトは compile_commands.json を使って解析可能（CMakeで `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON`）。

## 実践ポイント
- まずは安全性が重要なモジュール（デバイスドライバ、ネットワーク解析、メモリ管理部）に `@safe` を付け、限定的に解析を導入する。
- 使用している外部ライブラリの注釈ファイルを整備して、APIの寿命（lifetime）を明示する。これがダングリング検出の鍵。
- CMake/CIに統合して、ビルド時に自動チェックを回す習慣を作る。compile_commands.json を生成してツールに渡す。
- libclang周りの名前解決問題やクロスファイル解析の限界は現状の制約。重要箇所は手動レビューや追加テストで補う。
- AIアシスタントは高速プロトタイピングとテスト作成で有用。ただし最終的な設計判断と安全性評価は人間が担うこと（特にクリティカルパス）。

短期的に全てを置き換えるのは無理でも、コメント注釈＋外部アノテーション＋CI導入で段階的に「使えるレベルのメモリ安全」を既存C++資産へ持ち込める点が、このアプローチの最大の利点です。
