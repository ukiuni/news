---
layout: post
title: "Not all elementary functions can be expressed with exp-minus-log - exp-minus-logだけで全ての初等関数は表現できない"
date: 2026-04-15T05:44:54.472Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.stylewarning.com/posts/not-all-elementary/"
source_title: "Not all elementary functions can be expressed with exp-minus-log"
source_id: 47773788
excerpt: "exp−logのみでは五次方程式の根（$S_5$）が生成できず主張は誤り"
---

# Not all elementary functions can be expressed with exp-minus-log - exp-minus-logだけで全ての初等関数は表現できない
驚きの主張を冷静に検証する：本当に「1つの演算子で全て表せる」のか？

## 要約
ある論文は $E(x,y):=\exp x-\log y$ と定数・変数だけで「初等関数」を全て表現できると主張したが、標準的な意味での初等関数（多項式根を含む）を考えるとその主張は成り立たない。位相的ガロア理論を使うと、$E$ を基に作る関数のモノドロミー群は可解になり、一般的な五次多項式の根の群 $S_5$ と矛盾する。

## この記事を読むべき理由
- 機械学習やコンパイラ、計算代数系で「表現力の万能性」を議論する際の落とし穴が分かる。  
- 日本の研究者・エンジニアが海外の大げさな主張を正しく評価する助けになる。

## 詳細解説
- 問題の主張：論文は $E(x,y):=\exp x-\log y$ と変数・定数 $1$ を使った再帰的な式（以降 EML term）で多くの定数や関数を構成し、「初等関数をすべて表現できる」と述べる。  
- 定義の違い：筆者（レビュー元）は「初等関数」を厳密に36個の記号など狭い集合で定義する点を指摘する。一方、標準的数学では「有理関数に加えて四則演算・合成・exp/log・多項式根で閉じる」クラスを初等関数とする。特に「多項式根（代数付加）」が重要。  
- キーとなる道具：Khovanskii の位相的ガロア理論を用いると、EML で作れる関数のモノドロミー群（解析接続で枝がどう入れ替わるかを表す群）は常に可解群になる。証明の要点は次の流れ：
  - 定数と座標関数は自明なモノドロミーを持つ。  
  - $A$ が可解なら $\exp A$ のモノドロミーは可解（$\exp$ により群の商が得られる）。  
  - $B$ が可解なら $\log B$ のモノドロミーは可解（分岐による整数シフト分が可換群を与える）。  
  - $f=\exp A-\log B$ の場合は二つの成分の直積の部分群から射が降り、従って可解。  
- 反例（決定打）：一般の五次方程式の根は群が対称群 $S_5$ であり、これは可解でない。したがってある局所枝が EML 項と一致することはあり得ない。結論として、EML で表せる関数族は標準的初等関数族より真に小さい（$\mathcal T_n \subsetneq \mathcal E_n$）。

## 実践ポイント
- 「単一の演算で全て表現できる」という大きな主張は、定義の違い（狭義・広義）をまず確認する。  
- 実用面：数式処理やDSL設計で「どのクラスの関数を対象にするか」を明確にしないと、期待した代数的操作（根の取り扱いなど）ができなくなる。  
- 深堀り課題：位相的ガロア理論（モノドロミー群）と古典的代数ガロア理論の関係を学ぶと、表現可能性の議論が理解しやすくなる。

（原典：Robert Smith, "Not all elementary functions can be expressed with exp-minus-log"）
