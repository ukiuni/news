---
layout: post
title: "Boilerplate Tax - Ranking popular programming languages by density - ボイラープレート税：言語ごとの「冗長度」ランキング"
date: 2026-02-04T22:17:28.917Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://boyter.org/posts/boilerplate-tax-ranking-popular-languages-by-density/"
source_title: "Boilerplate Tax - Ranking popular programming languages by density | Ben E. C. Boyter"
source_id: 410420818
excerpt: "GitHub解析で判明：Lisp系は高密度、C#やGoは冗長多め"
---

# Boilerplate Tax - Ranking popular programming languages by density - ボイラープレート税：言語ごとの「冗長度」ランキング
「どれだけ冗長？主要プログラミング言語の“無駄コード率”を実測してみた」

## 要約
scc の ULOC（Unique Lines of Code）を使って、GitHub上の人気リポジトリ（各言語上位約100件）を解析し、言語ごとの「密度＝冗長の少なさ（Dryness）」を比較した調査。Lisp系が最も密で、C#やCSSなどは冗長が多い傾向。

## この記事を読むべき理由
言語選定やプロダクト設計で「可読性／生産性」といったトレードオフを考えるとき、実データに基づく「行あたりの有用コード割合」は有益。特に日本の企業で多いJava／Kotlin／Go／C#の実務効果が読み取れる。

## 詳細解説
- 測定指標: ULOC（Unique Lines of Code）  
  - ファイル内の重複行を除いた一意な行数を数える。空行は除外され、コメントは維持（コメントも保守コストがあるため）。
- データセット: EvanLi の GitHub-Ranking（各言語の上位100リポジトリ相当）を利用し、各リポジトリを浅いクローンで取得。
- 処理フロー:
  1. リポジトリ一覧を抽出して .git 付きでクローン（/tmp に浅い clone）。
  2. 各プロジェクトのルートで scc を実行: `scc -u -a --format sql | sqlite3 ../code.db`（初回は sql → 次回は sql-insert）。
  3. 出力を SQLite に蓄積し、言語ごとに集計。
- 集計方法:
  - 全行ベースの一意性比率（SUM(nUloc) / SUM(physical_lines)）と、プロジェクト単位での Dryness（プロジェクトごとの ULOC割合の平均）を算出。後者でモノレポや巨大リポジトリの偏りを低減。
- 主な結果（要点）:
  - 上位（高密度）: Clojure (~77.9%)、Haskell (~77.3%)、MATLAB、VimScript。Lisp系／関数型は非常に一行あたりの意味密度が高い。
  - 中位: Python (~67.8%)、Java (~65.7%)、JavaScript (~64.5%)、TypeScript (~63.3%)。
  - 下位（冗長多め）: Rust (~60.5%)、Go (~58.8%)、C# (~58.4%)、CSS 周辺。Go と Rust は思ったより近い冗長度。
- 気づき:
  - Java は昔ほど冗長ではなく、Kotlin の影響で密になっている面がある。  
  - Clojure のようなLispスタイルは最小の記述で高い「人間の思考/行数」比を実現している。  
  - モダン言語やツールチェーンの進化が必ずしも「冗長削減」につながっていない事例も見える。

## 実践ポイント
- 自分のコードベースで同様の指標を取る（scc の ULOC を導入して現状評価する）。  
- 計測例（scc 実行）:
```bash
# bash
scc -u -a --format sql | sqlite3 ../code.db
```
- 言語選定の参考に：新規プロジェクトで「開発速度・思考密度」を重視するなら、言語の表記力や標準ライブラリの充実度を意識する。既存コードの冗長を減らしたければリファクタやテンプレート化、自動生成の見直しを。  
- 再現／拡張: 元調査のスクリプトと scc は公開されているので（gist / scc リポジトリ）、自組織でリポジトリ集合を変えて比較するのが手早い。

（参考: 元調査は Ben E. C. Boyter による「Boilerplate Tax — Ranking popular programming languages by density」。調査用スクリプトと scc を使って誰でも再現可能。）
