---
layout: post
title: "We interfaced single-threaded C++ with multi-threaded Rust - 単一スレッドC++とマルチスレッドRustをつないだ話"
date: 2026-02-13T08:35:31.332Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://antithesis.com/blog/2026/rust_cpp/"
source_title: "How we interfaced single-threaded C++ with multi-threaded Rust | Antithesis Blog"
source_id: 46923825
excerpt: "単一スレッドC++を壊さず非同期Rustへ安全接続する実践パターンと落とし穴"
image: "https://antithesis.com/blog/2026/rust_cpp/images/cover.jpg"
---

# We interfaced single-threaded C++ with multi-threaded Rust - 単一スレッドC++とマルチスレッドRustをつないだ話
古いC++コードを壊さず、非同期で並列なRust側ロジックを安全に呼び出す現場の実践テクニック

## 要約
シングルスレッドで動く既存C++（ref-countがスレッド非安全）に対して、非同期・マルチスレッドなRustコントローラを安全に接続するために採った設計と落とし穴、最終的な実装パターン（Owner/Borrower と SendWrapper）を解説します。

## この記事を読むべき理由
日本の多くの組織で「レガシーC++」と「新しいRust」を混ぜたいというニーズが高まっています。本記事は実戦で遭遇する典型的なスレッド安全性問題と、最小限の変更で安全に統合する具体策を示します。

## 詳細解説
- 背景: Antithesisのfuzzerは決定論的ハイパーバイザ上で動き、コントローラをC++（同期・単一スレッド）からRust（非同期・マルチスレッド）へ拡張したいという要件が出た。FFIはcxxクレートで実現。
- cxxが扱う3つの相互運用形態: extern Rust 型（Rust→C++呼び出し）、extern C++ 型（C++→Rust呼び出し）、shared structures（単純なデータ構造）。
- 問題点: C++側の State が内部でスレッド非安全な ref_ptr（参照カウントがスレッド安全でない）を持っており、Rust側で単純に unsafe impl Send すると参照カウントの競合でセグフォルトが発生した。
- 要点（Send/Sync）: Rustの Send/Sync はコンパイラが安全性を保証する。C++実装に由来するスレッド不安全性を無理に覆すと致命的。
- 初期解法（動いたが非効率）: メインスレッドでのみ所有する CppOwner (内部は Arc<T>) を置き、スレッド間には Arc を渡して借用（CppBorrower）する。ただしメモリ掃除（in_flight の走査）がオブジェクト数に比例して非効率。
- 改良版設計:
  - CppOwner は T を直接所有（Arc<CppOwner<T>> を共有する）。
  - 最後の参照が切れるときに、T をメインスレッドへ戻して破棄する仕組みを作る。
  - ただしこれを実現するには CppOwner が Send である必要があり、T 自体は Send ではない。そこで SendWrapper による「1層の迂回」を使う（Drop 時にメインスレッドへ送り返す）。
- 重要な実装ルール:
  - C++側の型に unsafe impl Send を安易に付けない。
  - C++の参照カウント実装を可能ならスレッドセーフ（shared_ptr/atomic refcount）にするのが根本解決。
  - Rust側では所有権の境界を明確にし、メインスレッドでしか変更できない操作（clone/drop）をそこに限定する。

小さなイメージ（抜粋）:
```rust
// rust
pub struct CppOwner<T> { value: T }          // メインスレッドで所有
pub struct CppBorrower<T> { value: Arc<T> } // 他スレッドへ渡す借用
// SendWrapper: drop時にメインスレッドへ送ることで非-SendなTを安全に渡す
pub struct SendWrapper<T>(Option<T>);
unsafe impl<T> Send for SendWrapper<T> {}
impl<T> Drop for SendWrapper<T> {
  fn drop(&mut self) { if let Some(t) = self.0.take() { send_back_to_main_thread(t) } }
}
```

## 実践ポイント
- cxx を使って Rust/C++ を接続する際、C++型の Send/Sync を安易に付与しない。
- まずは「所有権の境界」を明確に: C++が参照カウント管理するものは可能ならメインスレッドに限定。
- 小規模プロトタイプでは Arc<CppOwner>/CppBorrower パターンで試し、本番でスケール問題が出たら SendWrapper パターンへ移行。
- 長期的には C++ 側をスレッド安全な参照カウント（atomic shared_ptr相当）にするのが最も堅牢。
- テスト: 決定論的シミュレーションやストレステスト（race検出）でdrop/cloneタイミングを重点的に確認する。

以上の設計パターンは「既存C++資産を壊さずRustの非同期利点を得る」現場で有効です。
