---
layout: post
title: "Rust Iterators and Closures for Java Programmers - Javaプログラマー向けRustのイテレータとクロージャ"
date: 2026-01-24T13:22:43.303Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://medium.com/gitconnected/rust-adventures-iterators-and-closures-706ab8f1b3c1"
source_title: "Rust Iterators and Closures for Java Programmers"
source_id: 418774576
excerpt: "Java経験者向け：所有権と借用で学ぶ高速安全なRustのイテレータ／クロージャ入門"
---

# Rust Iterators and Closures for Java Programmers - Javaプログラマー向けRustのイテレータとクロージャ

Java経験者が「すぐ使える」視点で学ぶ、Rust流のイテレータとクロージャ入門 — 安全性と性能を両立する実用テクニック。

## 要約
Rustのクロージャは周囲の変数をキャプチャする匿名関数で、イテレータは遅延評価されるチェーン可能な処理単位。Javaのラムダ＋Streamsに似るが、所有権と借用の概念が効いており、より低レイヤで高速なコードが書ける。

## この記事を読むべき理由
JavaからRustへ移る、もしくは両方を業務で扱う開発者は、ラムダ／Streamの感覚をそのまま使いながらも「所有権」「可変性」「ムーブ／借用」の差を理解する必要がある。これを押さえれば、バグを減らしつつ高速なデータ処理が可能になる。

## 詳細解説
- クロージャとは  
  周囲のスコープをキャプチャする匿名関数。Rustでは型推論で定義でき、キャプチャは借用(&T)、可変借用(&mut T)、ムーブ(T)のいずれかになる。クロージャに対するトレイトは主に Fn, FnMut, FnOnce で、呼び出し側の期待（不変／可変／所有権消費）に応じて使い分ける。

  ```rust
  fn main() {
      let multiplier = 2;
      let nums = vec![1, 2, 3];
      // multiplierを不変借用でキャプチャするクロージャ
      let doubled: Vec<_> = nums.iter().map(|n| n * multiplier).collect();
      println!("{:?}", doubled);
  }
  ```

- イテレータの基本と特性  
  Iteratorトレイトは next() を持つ単方向の列挙子。map/filterなどは「アダプタ」で遅延評価され、collect()やforで評価される。Rustのイテレータはゼロコスト抽象（コンパイル時に展開）で、不要なヒープ割当を避けられることが多い。

- iter / into_iter / iter_mut の違い
  - iter(): &T を返す（読み取り）
  - iter_mut(): &mut T を返す（書き換え可）
  - into_iter(): 所有権を消費して T を返す（ムーブ）

  使い分けで所有権エラーや二重借用を防げる。

- collect の使い方
  collect() は収集先の型を推測できないときに明示する必要あり。型注釈やターボフィッシュを使う。

  ```rust
  let v: Vec<i32> = (0..5).map(|x| x * 2).collect();
  // または
  let v = (0..5).map(|x| x * 2).collect::<Vec<i32>>();
  ```

- クロージャを引数に取るAPI設計
  ジェネリックで F: Fn(...) の形にすると高速で柔軟。スレッドに渡すときは move クロージャで所有権を渡す。

  ```rust
  fn apply<F: Fn(i32) -> i32>(f: F, x: i32) -> i32 { f(x) }
  ```

- Java Streamsとの主な違い（簡潔）
  - Rustは所有権と借用で安全性を強制する（GCなし）。  
  - イテレータは単一所有（使い切り）が基本。  
  - 性能面でゼロコスト抽象化に優れるが、型周りの明示やムーブを意識する必要あり。

## 実践ポイント
- 普段のループはまずイテレータで書き直してみる（可読性と安全性向上）。  
- iter/into_iter/iter_mut を意識して所有権ミスを減らす。  
- collect 時は型注釈か <:Vec<T>> を使い、期待するコンテナを明示する。  
- APIでクロージャ受け取りはジェネリック F: Fn* を使う（性能と柔軟性）。  
- スレッドや非同期で変数を渡すときは move クロージャを使う。  
- 小さなベンチを回して、イテレータチェーンが最適化されるか確認する。

以上を押さえれば、Javaの感覚を活かしつつRustらしい安全・高速なコードが書けるようになります。元記事は実例豊富なので、手元で短いサンプルを動かしながら確認するのがおすすめです。
