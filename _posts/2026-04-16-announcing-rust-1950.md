---
layout: post
title: "Announcing Rust 1.95.0 - Rust 1.95.0 の発表"
date: 2026-04-16T18:17:35.092Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.rust-lang.org/2026/04/16/Rust-1.95.0/"
source_title: "Announcing Rust 1.95.0 | Rust Blog"
source_id: 984160491
excerpt: "Rust 1.95：cfg_select!で条件分岐が簡潔、if-letガードと多数APIが安定化"
image: "https://www.rust-lang.org/static/images/rust-social-wide.jpg"
---

# Announcing Rust 1.95.0 - Rust 1.95.0 の発表
cfg_select!で条件コンパイルがスッキリ。マッチ式のif-letガードも安定化した最新リリース

## 要約
Rust 1.95.0 が公開され、compile-time の cfg 分岐を簡潔に書ける新マクロ cfg_select! と、match 式内での if-let ガードが安定化。さらに配列周りや原子型の便利メソッドなど多数の API が安定化／const 化されました。

## この記事を読むべき理由
日本のプロジェクト（特にクロスプラットフォームや組込み系、CI で複数ターゲットを扱うケース）で、条件コンパイルの可読性向上やマッチの表現力アップが即効で役立ちます。新 API は安全性とパフォーマンス改善にも寄与します。

## 詳細解説
- cfg_select!  
  compile-time の cfg を列挙して先にマッチした枝の右辺に展開されるマクロ。従来の cfg-if クレートと同目的ですが標準で利用可能になった点が意義。例:
  ```rust
  // rust
  cfg_select! {
      unix => {
          fn foo() { /* unix用 */ }
      }
      target_pointer_width = "32" => {
          fn foo() { /* non-unix 32bit */ }
      }
      _ => {
          fn foo() { /* フォールバック */ }
      }
  }
  let is_windows = cfg_select! { windows => "windows", _ => "not windows", };
  ```
  読みやすく、マクロを使うだけで cfg のネストや #\[cfg(...)\] の分散を避けられます。

- if-let ガード in match  
  match のガードで if-let が使えるようになり、パターンマッチ結果を即座に束縛して条件判定できます。ただし、if-let ガード中で新たにマッチしたパターンは exhaustiveness（網羅性）判定には含まれない点は注意。
  ```rust
  // rust
  match value {
      Some(x) if let Ok(y) = compute(x) => {
          println!("{}, {}", x, y);
      }
      _ => {}
  }
  ```

- API の安定化 / const 化（抜粋）  
  - MaybeUninit<[T; N]> に関する From/AsRef/AsMut など配列向け変換  
  - 原子型の update / try_update（AtomicPtr/AtomicBool 等）  
  - ポインタの as_ref_unchecked / as_mut_unchecked、Vec/VecDeque/LinkedList の push_*_mut 系、Layout のユーティリティ  
  - const コンテキストで使えるようになった API（例: fmt::from_fn, ControlFlow::is_break など）  
  これらにより低レイヤーの安全な初期化やコンパイル時計算がやりやすくなります。

- JSON ターゲット仕様の取り扱い変更  
  stable チャンネルで rustc にカスタムターゲット仕様を渡すサポートが外れました。通常の stable ユーザーに大きな影響は少ないですが、カスタムターゲット（特に組込みでの独自定義）を使う場合は nightly を使う運用が引き続き必要になります。Rust チームはユースケースを収集中です。

- その他  
  Cargo / Clippy の変更や詳細はリリースノートを参照すると良いです。

## 実践ポイント
- まずはアップデート:
  ```bash
  # bash
  rustup update stable
  ```
- 新しい cfg_select! を試して、既存の cfg-if 置換を検討（CI で動作確認を忘れずに）。  
- match + if-let ガードでコードを簡潔にできる箇所を探す（ただし exhaustiveness の挙動に注意）。  
- 組込み・カスタムターゲットを使う場合は nightly/beta を使い、tracking issue をウォッチ。  
- リリースノートを確認して、安定化された API（MaybeUninit 配列系や Atomic::update 等）を活用して安全で効率的な実装に置き換える。

公式リリースノートを読んで、プロジェクトに影響する変更を早めに検証してみてください。
