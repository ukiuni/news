---
layout: post
title: "Java gives a status update about new language features -- Constant Patterns and Pattern Assignment! - Javaが語る新言語機能の進捗 ― 定数パターンとパターン代入！"
date: 2026-01-10T00:27:32.823Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://mail.openjdk.org/pipermail/amber-spec-experts/2026-January/004306.html"
source_title: "Amber features 2026"
source_id: 466787169
excerpt: "Javaがパターン代入と定数パターンで冗長なinstanceofやwhenを削減し可読性を大幅向上へ"
---

# Java gives a status update about new language features -- Constant Patterns and Pattern Assignment! - Javaが語る新言語機能の進捗 ― 定数パターンとパターン代入！
Javaがついに「パターンで代入できる」時代へ：冗長な instanceof ガードと when を減らし、可読性と表現力を高める新機能の予告

## 要約
Javaチームは2026年のAmber機能として「パターン代入（Pattern Assignment）」と「定数パターン（Constant Patterns）」を優先して進めると発表しました。これにより、パターンマッチングがより直感的で簡潔になります（既にプレビュー中のプリミティブパターンも継続）。

## この記事を読むべき理由
これらは日常的なボイラープレート（instanceof → キャスト／when ガード）を減らし、レコードやパターンマッチングを多用するコードベースで生産性と可読性を大幅に改善します。日本の企業でもレコードやパターンを使った設計が増えており、導入影響は大きいです。

## 詳細解説
- パターン代入（Pattern Assignment）
  - 問題点：現在はレコード分解に instanceof を使うと、条件式内でないとパターン変数が有効にならずインデントやスコープの問題が発生する。
  - 提案されている書き方：左辺にパターンを置く代入文で「常に一致する」ことを明示できる。例：

  ```java
  // 従来の冗長な書き方
  void somethingImportant(ColorPoint cp) {
      if (cp instanceof ColorPoint(var x, var y, var c)) {
          // important code
      }
  }

  // パターン代入（提案）
  void somethingImportant(ColorPoint cp) {
      ColorPoint(var x, var y, var c) = cp; // Pattern Assignment
      // important code
  }
  ```

  - 型システム上の扱い：JLS にある「無条件に一致する（unconditional）」なパターンの定義を利用し、無条件でない場合はコンパイルエラーとする設計。つまり代入先パターンが必ずマッチすることをコンパイラが保証します。

  - 影響：スコープや可視性が簡潔になり、ネストを浅くできる。既存のパターンマッチングの概念と自然に統合される想定。

- 定数パターン（Constant Patterns）
  - 問題点：特定の要素（例：座標が原点）の場合分けを when ガードで書くと冗長で数学的でない。
  - 提案されている書き方：定数や null をパターンの位置に直接書けるようにすることで、より直感的にケースを表現できる。例：

  ```java
  void code(Shape s) {
      switch (s) {
          case Point(0, 0) -> {
              // 原点用の特別処理
          }
          case Point(var x, var y) -> {
              // 原点以外の点
          }
      }
  }
  ```

  - 利点：when による追加条件を書かずに済み、switch のパターンと定数が一貫した扱いになる。null や単純な定数式のサブセットを許可する方向。

- 現状と今後
  - プリミティブパターンは既にプレビュー中。今回の2機能は優先してDraft JEPが用意される予定で、草案公開後の議論が期待されている。

## 実践ポイント
- まず試すには：Amber のドラフトJEPや JDK の early-access ビルドを待ち、プレビュー機能を有効にしてコンパイル／実行してみる（JDK のプレビュー機能フラグを使用）。
- IDE対応：導入直後はコンパイラは先行していても IDE の解析やリファクタリング対応が追いつかない可能性があるので、IntelliJ や VS Code の Java 拡張の更新を確認すること。
- 使い分けの目安：
  - 「マッチが必ず成立する」分解にはパターン代入を使ってネストとガードを減らす。
  - 特定の値に対する分岐は定数パターンで直接表現して可読性を高める。
- 注意点：
  - パターン代入は「無条件一致」でなければならないため、実際に不確実な型の値に対して使うとコンパイルエラーになる。
  - 過度に分解・ネストしすぎると逆に読みづらくなるため、可読性を優先して利用する。
- 日本の現場での意義：API レスポンスのデータモデル（レコード）やドメインモデルの分解が頻繁なプロジェクトで、テストやメンテナンスの工数削減につながる可能性が高い。

草案JEPの公開と実装追跡が始まれば具体的なサンプルと移行ガイドが出るはずです。関心のある方はドラフト公開時に実際に手を動かして互換性とIDEサポートを確認すると良いでしょう。
