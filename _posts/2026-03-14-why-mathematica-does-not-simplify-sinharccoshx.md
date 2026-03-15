---
layout: post
title: "Why Mathematica does not simplify Sinh[ArcCosh[x]] - なぜ Mathematica は Sinh[ArcCosh[x]] を簡略化しないのか"
date: 2026-03-14T20:56:19.772Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.johndcook.com/blog/2026/03/10/sinh-arccosh/"
source_title: "Why Mathematica does not simplify Sinh[ArcCosh[x]]"
source_id: 1115673848
excerpt: '分岐と符号の定義ゆえに、Mathematicaは$\sinh(\operatorname{arccosh}x)$を$\sqrt{x^2-1}$に簡略化しない'
image: "https://www.johndcook.com/blog/wp-content/uploads/2022/05/twittercard.png"
---

# Why Mathematica does not simplify Sinh[ArcCosh[x]] - なぜ Mathematica は Sinh[ArcCosh[x]] を簡略化しないのか
意外な落とし穴：Mathematicaが sinh(arccosh(x)) を自動簡約しない「符号と分岐」の理由

## 要約
Mathematica が $\sinh(\operatorname{arccosh} x)$ を単純に $\sqrt{x^{2}-1}$ に置き換えないのは、逆双曲線関数と平方根の「分岐（branch cut）」定義により値域・符号が変わるためで、全複素平面で一貫した結果を返すための設計による。

## この記事を読むべき理由
記号計算ソフトを使う日本のエンジニアや学生は、CAS の自動簡約が必ずしも数学的直感通りではないことを知っておくべきです。数式の定義域や分岐を誤解すると、バグや誤った数値解に繋がります。

## 詳細解説
- 背景：通常の実数範囲で $\cosh$ は偶関数で、$\operatorname{arccosh}(x)$ は $x\ge1$ で正の実数を返すよう定義されます。しかし複素解析的に逆関数を一貫して定義するには分岐を作る必要があります。Mathematica は ArcCosh の分岐切断を $(-\infty,1]$ に置き、切断上は上側からの連続性を選びます。
- 平方根の分岐：$\sqrt{z}$ も通常は切断 $(-\infty,0]$ を持ち、切断上は上側からの値を取るように定義されます。これにより式変形で暗黙に使う等号（たとえば $\sqrt{(x+1)^2}=x+1$）は常に成り立ちません。
- 結果：以上のため、Mathematica が返す $\sinh(\operatorname{arccosh} x)$ の式は複素全体で正しく連続になるように符号やルートの取り方を調整した形です。実数の特定範囲（例：$x\ge-1$ や $x\ge1$）に限定すれば、期待される簡約 $\sqrt{x^{2}-1}$ が成立します。
- 数値例（直感の落とし穴）：分岐の取り方により、ある点で符号が逆になる場合がある（元記事では具体例として Mathematica の返す値と単純な平方根の符号が異なる例を示しています）。

## 実践ポイント
- 前提を明示する：簡約を期待するなら Mathematica に明示的な仮定を与える（例：Simplify[Sinh[ArcCosh[x]], Assumptions -> {x >= -1}] は $\sqrt{x^{2}-1}$ を返す）。
- 数値チェック：シンボリック変形後は代表点で数値評価して符号や分岐の整合性を確かめる。
- 分岐意識：複素関数や逆関数を扱うときは分岐位置と連続性（上側/下側の極限）を常に意識する。
- テスト設計：ライブラリや解析コードの単体テストに、分岐境界上と境界近傍のケースを含める。

短く言えば、CAS の「簡約」は数学的に広域で整合するための選択を反映しており、問題はソフトのバグではなく分岐と仮定の扱いです。
