---
layout: post
title: "Emulating Goto in Scheme with Continuations - 続行でSchemeにGOTOをエミュレートする"
date: 2026-02-23T16:03:40.265Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://terezi.pyrope.net/ccgoto/"
source_title: "Emulating GOTO in Scheme with continuations"
source_id: 47076789
excerpt: "Schemeのcall/ccでラベルとgotoを実装し、継続で任意位置へジャンプする仕組みを解説"
image: "/res/pyralspite.webp"
---

# Emulating Goto in Scheme with Continuations - 続行でSchemeにGOTOをエミュレートする
Schemeでcall/ccを使って「GOTO的なジャンプ」を再現してみたら面白かった話

## 要約
Schemeのcall-with-current-continuation（call/cc）を使い、ラベルを定義して任意の位置にジャンプできるミニGOTOマクロを実装する方法と、その仕組みをわかりやすく解説します。

## この記事を読むべき理由
call/ccは関数型言語の強力な制御抽象で、日本でもRacketやChez Schemeを触る人が増えています。本稿は初心者でも理解できるように「GOTOの再現」を題材にしてcontinuationの挙動を直感的に学べます。実務では使わないケースが多くても、制御フローの理解やDSL作りのヒントになります。

## 詳細解説
- GOTOの本質  
  GOTOはプログラムの任意の位置へ制御を飛ばす仕組み。Cのエラー処理でのgotoラベルや、BASICの行ジャンプがイメージしやすいです。繰り返しますが実運用では乱用厳禁。

- call/cc（継続）とは  
  call/ccは「現在の残りの計算（continuation）」を関数に渡す仕組みです。その返された継続を呼ぶと、その時点に戻るのではなく「その継続が表す“残りの計算”をそのまま別の値で再実行」します。これがジャンプ的な制御に使えます。

- アイデア概要  
  1) 構文マクロでラベルごとに引数なしの手続き（thunk）を定義する（ラベル＝手続き）。  
  2) with-gotoのボディをcall/ccで囲み、現在の継続kを取得する。  
  3) goto関数をkを使って実装すると、goto(label)で継続kを呼び、labelの手続きをその場で評価した結果に「置き換える」ことができる。これがジャンプになる。

- マクロの要点（簡易版）  
  - %labels：ボディを走査して「label (body...)」を見つけたら、(define (label) body...) を生成する（尾部共有的に）。  
  - with-goto：goto変数を先に定義し、call/cc内で (set! goto (lambda (label) (k (label)))) とする。こうしてgoto呼び出しは継続kを呼んでラベルの実行結果へ遷移する。

- 簡単な例（無限ループ）  
```scheme
( with-goto goto loop
  (display "Hello, world!\n")
  (goto loop) )
```
このように動き、通常のサブルーチン呼び出しの深さを増やさずにジャンプできる点が特徴です（実装によってはスタック増加しない）。

## 実践ポイント
- 学習用途に最適：continuationの直感を得る実験として試す。RacketやChez SchemeのREPLで小さな例から動かすと理解が早い。  
- 本番用途は推奨しない：可読性・保守性を損なうので、あくまで教育的/DSL的な限定用途に。例：特殊なフロー制御を内包する小さな言語実装のプロトタイプ。  
- 発展トピック：delimited continuations（区切られた継続）や、ambのような非決定選択演算子へ応用できる。興味があればDybvigやRacketの資料を参照すること。

以上。興味があれば簡潔なマクロ実装例や、REPLでの実行手順を添えてお送りします。
