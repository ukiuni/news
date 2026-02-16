---
layout: post
title: "picol: A Tcl interpreter in 500 lines of code - picol: 500行で書かれたTclインタプリタ"
date: 2026-02-16T08:42:49.002Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/antirez/picol"
source_title: "GitHub - antirez/picol: A Tcl interpreter in 500 lines of code"
source_id: 47032235
excerpt: "500行のCで動くTcl風インタプリタで言語実装を短時間で学ぶ"
image: "https://opengraph.githubassets.com/a4e86eb26072f4976d19aca8a5a6fee923e79bf6ca32842be5d78f4cd68df22b/antirez/picol"
---

# picol: A Tcl interpreter in 500 lines of code - picol: 500行で書かれたTclインタプリタ
たった500行のCで「動く」インタプリタを学ぶ — 実践で分かる小さな言語実装入門

## 要約
antirez（Salvatore Sanfilippo）が公開した「picol」は、手書きのパーサと評価器を約500行のCで実装したTcl風インタプリタで、学習用として分かりやすく実用的な機能を備えています。

## この記事を読むべき理由
インタプリタ設計の基本（トークン化、代入・評価、スコープ、コマンド実装）を実際に動くコードで短時間に理解できるため、Cで組み込みスクリプトを作りたい人や言語処理を学びたい初学者に最適です。日本の組込み開発やツール作成にも応用しやすい軽量さが魅力です。

## 詳細解説
- 全体像: ソースは主に手書きパーサ（約250行）と評価器(picolEval)で構成。picolGetTokenがソースを走査し、トークンの種類と位置を返す。picolEvalがそのトークン列を解釈して実行します。
- トークン処理: トークンは区切りで新しい引数にするか、連結して補間（$変数や[コマンド]）を実現。変数参照はコールフレームから検索し、コマンド置換は再帰的にpicolEvalを呼んで結果を使います。
- コマンド実装: 各コマンドは名前とC関数ポインタで表され、void*のprivateデータを持てるため一つのC関数で複数コマンドやユーザ定義プロシージャを実装可能。ユーザ手続きは引数リストと本文をprivateデータとして扱い、呼び出し時に新しいコールフレームを作成してスコープを維持します。
- 機能一覧: 文字列・数式補間、proc（return含む）、if/else、while（break/continue）、再帰、算術演算・比較・putsなど。対話シェルも付属。
- 使いどころ: 小さな言語を設計したい場合や、Cに埋め込む軽量スクリプト機構、教育用サンプルとして有用。パーサ部分は冗長だが手書きパーサの学習教材としての価値が高い。

簡単な利用例:
```bash
# コンパイル
gcc -O2 -Wall -o picol picol.c

# 対話シェル起動
./picol

# ファイル実行
./picol sample.tcl
```

Tcl風サンプル（picolで実行可能）:
```tcl
proc fib {x} {
  if {== $x 0} { return 0 }
  if {== $x 1} { return 1 }
  return [+ [fib [- $x 1]] [fib [- $x 2]]]
}
puts [fib 20]
```

## 実践ポイント
- リポジトリをクローンしてまず対話シェルを触る（picol.cを読む前に動かすと理解が深まる）。
- 注目関数: picolGetToken（パーサロジック）、picolEval（評価・補間）、コマンド登録部分。これらを順に追うと内部動作が把握しやすい。
- 機能拡張の練習: 既存のCコマンドを1つ追加してみる（void* privateデータの使い方を理解する良い題材）。
- 応用例: 組込み機器の簡易スクリプト、テスト用の小さなDSL、教育用サンプルとして転用可能。

元リポジトリ: https://github.com/antirez/picol
