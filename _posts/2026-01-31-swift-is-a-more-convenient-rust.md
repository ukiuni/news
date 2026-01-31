---
layout: post
title: "Swift is a more convenient Rust - Swiftは「もっと便利なRust」"
date: 2026-01-31T23:43:45.606Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://nmn.sh/blog/2023-10-02-swift-is-the-more-convenient-rust"
source_title: "Swift is a more convenient Rust"
source_id: 46841374
excerpt: "SwiftはRustの所有権/選択肢を簡潔なC風文法で使い、高生産性と低レイヤ制御を両立する。"
---

# Swift is a more convenient Rust - Swiftは「もっと便利なRust」  
魅力タイトル: Swiftで楽に書ける「所有権」の世界 — Rustの力をCライクな文法で使う方法

## 要約
SwiftはRustと多くの設計思想（所有権、パターンマッチ、Option/Result相当など）を共有しつつ、より高レベルで使いやすく設計されている。性能よりも「簡潔さと生産性」をデフォルトに置きつつ、必要なら低レイヤーへ降りられるのが特徴だ。

## この記事を読むべき理由
日本のモバイル／サーバー／組み込み分野でSwiftを扱うエンジニアや、Rustに興味はあるけれど学習コストを抑えたい人にとって、両者の差と選びどころがはっきりわかるから。

## 詳細解説
- 設計の視点  
  - Rustは「下から積み上げる」低レイヤ寄り。速さをデフォルトにし、所有権／借用を前提に設計。  
  - Swiftは「上から降ろす」高レベル寄り。値型＋コピーオンライトをデフォルトにして、必要なときだけ所有権／ムーブへ切り替えられる。

- メモリモデルと使い勝手  
  - Rust: 明示的にBox/Rc/Arc/Cowなどを使い、借用規則が厳格。  
  - Swift: ほとんどが値型（T? やコピーオンライト）で自動的に扱われ、必要ならunsafeやポインタに降りられる。

- 言語機能の対応  
  - 列挙型とパターンマッチ: Rustのmatchに相当する強力なパターンマッチがSwiftのswitch（式的振る舞い）として馴染みやすい形で提供。  
  - Optional/Error: RustのOption/Resultに対応する機能がSwiftではT?やthrows/do-catchの形で「よりCライクに」隠蔽されている。  
  - 再帰型の扱い: RustはBox等を明示するが、Swiftはindirectでコンパイラが内部処理を吸収する。

- エコシステムと実運用面  
  - Swiftは元々Apple向けだが、近年はWindows/Linux/wasm/組み込みへ拡大。VSCodeのサポートやswift-wasmの統合でクロスプラットフォーム化が進む。  
  - トレードオフとして、コンパイル時間や言語の肥大化、パッケージエコシステムはRustに比べ改善余地あり。

## 実践ポイント
- 目的で選ぶ：UI/アプリ開発やサーバー側で素早く生産性を取りたいならSwift。OSやブラウザエンジン、組み込みの最深部、最大性能が必要ならRust。  
- Swiftを学ぶときの着眼点：Optional（T?）の扱い、switchのパターンマッチ、値型＋コピーオンライトの挙動、throws/do-catch。  
- 環境構築：VSCodeのSwift拡張やswift-wasm、Swift on Windows/Linuxの情報をチェックしてクロスプラットフォーム開発を試す。  
- 日本市場での応用：既存のiOS資産を活かしたサーバーサイドSwiftや、Playdateなど小型デバイスでの組み込み利用は注目に値する。

（元記事: "Swift is a more convenient Rust"）
