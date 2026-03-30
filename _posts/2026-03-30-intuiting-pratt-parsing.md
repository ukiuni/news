---
layout: post
title: "Intuiting Pratt parsing - Prattパーシングを直感する"
date: 2026-03-30T10:01:40.633Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://louis.co.nz/2026/03/26/pratt-parsing.html"
source_title: "Intuiting Pratt parsing"
source_id: 412059401
excerpt: "図で直感、スパインを遡るだけでPrattパーサが優先度通りのASTを簡潔に構築する仕組み"
image: "https://louis.co.nz/assets/img/pratt/ast.png"
---

# Intuiting Pratt parsing - Prattパーシングを直感する
「スパインをたどればOK」――Prattパーサを図で直感的に理解する

## 要約
Prattパーシングは「演算子の優先度が切り替わる場所でスパインを遡る」ことで抽象構文木（AST）を正しく組み立てるシンプルで強力な手法です。

## この記事を読むべき理由
式の解析はコンパイラ・トランスパイラ・言語ツールで必須。Visual Studio Code の拡張開発やDSL、静的解析を手掛ける日本のエンジニアにとって、短く実装できて理解しやすいPratt法は即戦力になります。

## 詳細解説
- 背景：テキスト（a + b * c + d）を評価順に扱うにはASTが必要。演算子ごとの優先度で木が左寄り／右寄りになる。
- 直感：演算子列に対して、優先度が弱くなる（降順・左寄せ）ときはスパインを遡って新しい演算子の左子にそれまでの右寄り部分をまとめる。逆に優先度が強くなると右寄りに伸びる。
- 定義：優先度列 $x_i$ に対して
  - 降順（decreasing）: $x_i \ge x_{i+1}$
  - 上昇（increasing）: $x_i < x_{i+1}$
- アルゴリズム要点：再帰で右辺を解析しつつ、戻りながら while で現在の優先度より強い演算子を貪欲に取り続ける（これが「スパインを遡る」動作）。
- 結合性：各演算子は左結合力（LBP）と右結合力（RBP）を持ち、左結合は LBP = RBP、右結合は RBP を小さくして再帰側で消費させる（例えば RBP = LBP - 1）。

簡潔な実装イメージ（擬似Python）:

```python
# python
def parse(prev_prec=0):
    left = leaf()                     # リテラルや括弧を処理して左辺を取得
    while lbp(peek()) > prev_prec:    # スパインを遡る（優先度が強い限り）
        op = advance()
        right = parse(rbp(op))        # RBP によって結合性を制御
        left = Node(op, left, right)
    return left
```

例：右結合（代入）なら rbp = lbp - 1、左結合（加減乗除）なら rbp = lbp。

## 実践ポイント
- まずは式のみ扱う小さなパーサで試す（数値、識別子、+ - * / = を対象に）。
- 各演算子に LBP / RBP を割り当てて、テスト式（a + b * c, a = b = c, a > b + c * d など）でASTが期待通りになるか可視化する。
- VSCode 拡張や小さなDSLでは、汎用のパーサライブラリより簡潔に実装でき、デバッグもしやすい。
- 右結合と左結合を区別することでパーサの挙動が劇的に変わるので、結合性の設計を明示すること。

短い直感：木は「左寄りか右寄りか」。優先度が下がるところでスパインを遡れば、Prattパーサはほとんど自動的に正しいASTを作ります。
