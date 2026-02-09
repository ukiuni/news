---
layout: post
title: "Beta release: Predicated Recursive Descent for Rust - Rust向け「予測付き再帰下降」ベータ公開"
date: 2026-02-09T04:41:36.579Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://wareya.wordpress.com/2026/02/01/beta-release-predicated-recursive-descent-for-rust/"
source_title: "Beta release: Predicated Recursive Descent for Rust &#8211; Abandonculture"
source_id: 1267177347
excerpt: "BNF風DSLで手書き並みの制御ができる高速Rustパーサーのベータ公開"
image: "https://s0.wp.com/i/blank.jpg?m=1383295312i"
---

# Beta release: Predicated Recursive Descent for Rust - Rust向け「予測付き再帰下降」ベータ公開
「BNFで書けて手書きパーサーと同じ自由度。速くて分かりやすい新パーサーライブラリ『pred_recdec』」

## 要約
RustでBNF風のDSLを書くだけで、手作り再帰下降パーサーと同等の表現力と制御が得られるライブラリのベータ公開。CやJSONなど実用的なパーサを短時間で作れるのが特徴。

## この記事を読むべき理由
パーサー実装は敷居が高く時間がかかりがちですが、本ライブラリは「読みやすい文法記述」と「手書きで得られる制御」を両立します。日本のツール開発者や言語好き、リンター／静的解析ツール作成者に即役立ちます。

## 詳細解説
- アプローチ：BNFに近い構文で書くDSL（例：S ::= ...）を用い、各選択肢に対して明示的な「predicates（予測）／ガード」を置いて制御する。つまり一般的なジェネレータが行う曖昧性解消や自動メモ化を行わず、開発者が直線的な制御フローを設計する方式。
- 特徴：
  - 手書き再帰下降の表現力（任意の副作用フックや状態操作）を保持。
  - 文法の形でボイラープレートを自動化し、AST操作やルックアヘッドの大部分を文法表現に委ねられる。
  - tail-call最適化を提供し、左再帰回避やリスト処理の効率化が容易。
  - トークナイザ同梱（別途レキシカル文法を書かなくてもよい）。
- 性能（作者報告）：
  - Cパーサ：GCC/Clangの-fsyntax-onlyモード比で約10–20%遅い程度。
  - JSONパーサ：serde_jsonなどの高度最適化ネイティブ実装より約5倍遅いが、解釈実行＋トークナイズを挟む点を考慮すれば実用域。
- 拡張ポイント：@peek, @guard, !hook といったガードやフックで任意のコードを挿入可能。必要ならその中で高度な解析ロジックやメモ化も実装できる。
- 他ツールとの違い：ANTLR等の曖昧性許容型ジェネレータとは思想が異なり、conflict解決やfirst/followテーブルを気にする代わりに明示的な制御を書く設計。

## 実践ポイント
- まずは小さな言語（JSON、S式）で文法を書いて挙動を確認する。例を見ながらガードの置き方を学ぶと早い。
- あいまいさが許されない文法部分は@peek/@guardで明示的に判定する。これが設計上の肝。
- リストや繰り返しはtail-call最適化を利用してパフォーマンスとメモリ効率を稼ぐ。
- 日本市場では、言語サポート拡張（独自DSLの実装）、静的解析器、フォーマッタ、コード補完のプロトタイプ作成に特に有用。
- ソース・配布：GitHubとcrates.ioで公開中（pred_recdec）。まずはリポジトリのサンプルを動かしてみることを推奨。

元記事の詳細・コードやサンプルは作者のリポジトリやcrates.ioで確認してください。
