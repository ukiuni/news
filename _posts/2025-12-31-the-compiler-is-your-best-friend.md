---
layout: post
title: "The compiler is your best friend - コンパイラは最高の味方だ（コンパイラに嘘をつくのをやめよう）"
date: 2025-12-31T17:38:26.655Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.daniel-beskin.com/2025-12-22-the-compiler-is-your-best-friend-stop-lying-to-it"
source_title: "The compiler is your best friend"
source_id: 46445131
excerpt: "コンパイラを味方にして深夜の障害を防ぐ、現場で使える実践テクニック集"
---

# The compiler is your best friend - コンパイラは最高の味方だ（コンパイラに嘘をつくのをやめよう）
思わずクリックしたくなるタイトル: 「夜中の障害を防ぐ“コンパイラとの対話術” — 今すぐチームで取り入れたい実践テクニック」

## 要約
コンパイラは単なる「変換ツール」ではなく、バグを未然に防ぐ強力な検査官。型やコンパイル時チェックを正しく使えば、深夜の障害対応を大幅に減らせる。

## この記事を読むべき理由
日本の多くの現場では、レガシーなJava/スクリプト混在や短納期で型が緩いコードが増えがち。コンパイラを味方につける設計とツール運用を学べば、運用コストと障害リスクを同時に下げられる。

## 詳細解説
- コンパイラの役割（簡潔）
  - パース → 抽象構文木（AST） → 型チェック → 最適化 → コード生成。多くの価値は「型チェック」にある。
- AOT と JIT の違い
  - Rust のような AOT はコンパイル時に厳密なチェック（借用検査など）を行い、実行時バグを防ぐ。
  - Java はバイトコード＋JVMで JIT を使い、実行時にホットスポットを最適化する。JIT により「ウォームアップ」が必要になる点は運用で考慮が必要。
- Rust の強み
  - 所有権・借用チェッカーでダングリングやデータ競合をコンパイル時に排除。ゼロコスト抽象で高性能と安全性を両立。
- Java の現実
  - バイトコード経由でプラットフォーム互換性を得る一方、型キャストや unchecked null によるランタイム例外が現場で多い。
- TypeScript のアプローチ
  - JavaScript に対するトランスパイラで「段階的型付け（gradual typing）」を導入。大規模 JS コードベースの保守性を向上させる目的で設計されている。
- 「コンパイラに嘘をつく」とは
  - null を放置、例外制御を乱用、頻繁な型キャスト、副作用を隠す設計……これらは型システム／コンパイラの前提を破り、ランタイムクラッシュや難解なバグを招く。

## 実践ポイント
- コンパイル時チェックを最大化する設定を有効化する
  - TypeScript: "strict": true / strictNullChecks をオン
  - Java: @Nullable/@NotNull 注釈＋静的解析（SpotBugs, Error Prone）を CI に組込み
  - Rust: 警告をゼロにする、unsafe を限定的に
- 「消極的なキャスト」をやめる
  - キャストで回避する代わりに、型変換を明示的な関数/ラッパーに置き換える
- Null と例外の扱い方を明確にする
  - Optional/Result 型や明示的なエラー伝播（戻り値で扱う）を採用し、例外は最小限に
- 副作用を隠さない
  - 副作用は明示的な境界（サービス層、ファサード）にまとめ、純粋関数を単体テスト可能にする
- CI で「コンパイルに通ること」を品質ゲートにする
  - ビルドと静的解析を PR 却下条件に設定。夜間の出動を減らすためにコンパイル段階で失敗させる
- 技術選定の視点
  - 高信頼性を求めるインフラや低レイテンシ処理には Rust、エコシステムと移行コスト重視なら Kotlin/Java（Kotlin の null 安全）、フロントエンドは TypeScript の厳格化を検討

## 引用元
- タイトル: The compiler is your best friend
- URL: https://blog.daniel-beskin.com/2025-12-22-the-compiler-is-your-best-friend-stop-lying-to-it
