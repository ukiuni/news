---
layout: post
title: The Compiler Is Your Best Friend, Stop Lying to It
date: 2025-12-26 03:55:09.068000+00:00
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: http://blog.daniel-beskin.com/2025-12-22-the-compiler-is-your-best-friend-stop-lying-to-it
source_title: The Compiler Is Your Best Friend, Stop Lying to It - Daniel Beskin's
  Blog
source_id: 438247008
---
# 深夜のPagerを防ぐ技術：コンパイラを味方につけて「嘘」をやめるだけで事故が減る

## 要約
コンパイラはただの変換器ではなく、設計ミスや不整合を早期に示してくれる「味方」。コードでコンパイラに嘘をつく（nullを飼い慣らす、無理なキャスト、例外を隠す、副作用を放置する）とランタイム障害につながる。これをやめ、型やコンパイラの警告を活用する実践を紹介する。

## この記事を読むべき理由
夜中のインシデント対応を減らしたい、レガシーJavaやTypeScript/フロント開発でバグに悩む日本のエンジニアにとって、コンパイラ中心の設計に切り替えるだけで早期検出が増え、運用コストが下がるから。

## 詳細解説
- コンパイラの役割
  - 通常のパイプライン：パース → AST → 型検査 → 最適化 → コード生成。特に型検査(typechecking)が現場で効く。
- 言語ごとの特徴（抜粋）
  - Rust: AOT（事前コンパイル）。マクロ展開・型チェック・borrowチェックで多くのクラスのバグをコンパイル時に消す。ゼロコスト抽象で性能も確保。
  - Java: nullと例外文化が根強い。Optionalや最近の言語機能で「コンパイラに伝える」設計が可能。
  - TypeScript: 型システムは有効だが、anyや緩い設定でコンパイラに嘘をつける。strictモードを有効にすると効果大。
- 「コンパイラに嘘をつく」代表例
  - Null — 値がnullになり得ることを型で表現していない（→ NullPointerException）
  - 例外 — 例外を放置して不整合を起こす設計
  - キャスト — unsafeなキャストで実行時クラッシュを誘発
  - 副作用 — 副作用が分散して状態変化が追えない
- 解決アプローチ（設計の転換）
  - Null: Option/Optional/Nullable型を使い、必ず扱いを明示する。TypeScriptでは strictNullChecks を有効に。
  - 例外: 使い分け（チェック/非チェック）やエラー型を用いた明示的ハンドリング。クロスサービスでは明確なエラー契約を。
  - キャスト: パターンマッチ／ガードで安全に変換。ランタイムでの無効な仮定を排除。
  - 副作用: 不変性を推奨し、副作用は入り口を限定する（pure関数、DI、コマンドとイベントの分離）。

## 実践ポイント
- コンパイラを味方にする設定（すぐやる）
  - TypeScript: tsconfig の strict/strictNullChecks を ON
  - Java: 可能なら Optional を使い、FindBugs/SpotBugs / ErrorProne を CI に組み込む
  - Rust: clippy をルール化し、警告は修正する
- ルール化（チームでやる）
  - 警告をエラー化 (warnings-as-errors)
  - PR テンプレートに「型の扱い」に関するチェック項目を追加
  - 型を使ったドメインモデル（typed wrappers）を導入して意味を型に落とす
- ツールチェーン
  - 静的解析・型チェッカー・linters を CI で必須化
  - 小さな型定義（union types, enum）で仕様を明文化
- レガシー改善の一歩
  - 部分的に型付けを厳しくする（モジュール単位で段階的に導入）
  - 重要パスは型で保証してリファクタしやすくする

