---
layout: post
title: "Six Simple Sudoku Solvers: Prolog - 6つの簡単な数独ソルバー：Prolog"
date: 2026-01-31T17:02:25.722Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.veitheller.de/Six_Simple_Sudoku_Solvers_III:_Prolog.html"
source_title: "Six Simple Sudoku Solvers III: Prolog | Veit's Blog"
source_id: 890021635
excerpt: "Prolog（clpfd）で約25行の宣言的制約だけで数独を高速に解く方法を解説"
---

# Six Simple Sudoku Solvers: Prolog - 6つの簡単な数独ソルバー：Prolog
25行で驚く、Prologらしい「宣言的」数独ソルバーの作り方

## 要約
Prolog（SWI-Prolog + clpfd）を使えば、数独のルールを制約として書くだけで約25行の短さで解けるソルバーが作れる。バックトラッキングや探索は言語が担うので実装はシンプル。

## この記事を読むべき理由
- 制約プログラミングの威力が分かる：手作業で候補選びをしなくても解ける設計が学べる。  
- 日本の現場でも使える応用例（スケジューリング、割当、テスト自動化）への発想転換になる。

## 詳細解説
ポイントは「盤面を変数と制約に写像する」こと。

主要部分（要約）：
```prolog
% 行・列・ブロックの制約を宣言してラベリングする
length_(L, Xs) :- length(Xs, L).
solve(Rows) :-
  length(Rows, 9), maplist(length_(9), Rows),
  append(Rows, Vars), Vars ins 1..9,
  maplist(all_different, Rows),
  transpose(Rows, Cols), maplist(all_different, Cols),
  blocks(Rows),
  labeling([ff], Vars).
```

- clpfdライブラリを使い、Vars ins 1..9 で変数のドメイン（1〜9）を宣言。  
- all_different/1 で行・列・ブロックの重複禁止を制約化。transpose/2で列を作る。  
- blocks/1 は3x3ブロックの制約を作る補助で、次のように実装する：
```prolog
blocks([]).
blocks([A,B,C|Rs]) :- blocks3(A,B,C), blocks(Rs).

blocks3([], [], []).
blocks3([A,B,C|R1], [D,E,F|R2], [G,H,I|R3]) :-
  all_different([A,B,C,D,E,F,G,H,I]),
  blocks3(R1, R2, R3).
```
- ゼロ（空きセル）を新しい変数に置き換えるユーティリティ：
```prolog
z2v(0, _).
z2v(N, N) :- integer(N), N > 0.
rows_from_zeros(PZero, Rows) :- maplist(maplist(z2v), PZero, Rows).
```
- 最後の labeling([ff], Vars) で探索戦略を指定（ff は fail-first）。ラベリングには ffc, bisect, down などのオプションがある。

要点：ロジック（手順）を書くのではなくルール（制約）を書くと、探索はPrologに任せられるためコードが極端に短くなる。

## 実践ポイント
- SWI-Prolog を入れて、use_module(library(clpfd)). を読み込んで試す。  
- 手持ちの数独を二次元リスト（0=空き）で表し、rows_from_zeros/2 → solve/1 の順で実行。  
- labelingオプションを変えて性能を比較（ff, ffc, bisect, down）。  
- 応用案：スケジューリングや割当問題に同様の制約定義を流用可能（日本の現場での工数割当や試験配置など）。

短くても強力。Prologの「宣言的発想」を一度体験すると、制約問題へのアプローチが変わります。
