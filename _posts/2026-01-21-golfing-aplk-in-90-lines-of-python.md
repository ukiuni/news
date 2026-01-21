---
layout: post
title: "Golfing APL/K in 90 Lines of Python - APL/Kを90行のPythonでゴルフ"
date: 2026-01-21T23:06:31.259Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://aljamal.substack.com/p/golfing-aplk-in-90-lines-of-python"
source_title: "Golfing APL/K in 90 Lines of Python - by Mohammed Alrujayi"
source_id: 46651027
excerpt: "90行のPythonでK風配列言語を再現、入れ子リストを自動拡張で処理する技法"
image: "https://substackcdn.com/image/fetch/$s_!tpX2!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0e35f49d-a7b1-4a5b-8b38-38319ed492cb_1968x1352.heic"
---

# Golfing APL/K in 90 Lines of Python - APL/Kを90行のPythonでゴルフ
90行のPythonで「配列の言語」を再発見する：LispとAPLの交差点を遊ぶ実験

## 要約
Arthur WhitneyのK（Lisp的なリスト操作とAPL的なベクトル化を融合した言語）を、わずか90行程度のPythonで再現する試みを紹介。核は「スカラー拡張（scalar extension）」を高階関数で実現するアイデアです。

## この記事を読むべき理由
配列プログラミング（NumPyや深層学習フレームワークの基盤概念）の起源と設計思想が分かり、Pythonで軽量に試作する方法が学べます。日本のデータエンジニアや機械学習入門者にも応用しやすい考え方です。

## 詳細解説
- 背景：Lispは「コード＝データ」のミニマリズム、APLは記法の密度で数学表現を圧縮しました。Arthur Whitneyは両者の利点を組み合わせ、Kを設計。Kは多次元配列モデルを捨て、入れ子リストを中心に扱います。
- 核心技術：APL系の強みは「すべての演算が配列に対して自動的に拡張される」点。これをPythonで再現するには、任意の関数を「原子（数値/文字列）」に到達するまで再帰的に適用する高階関数があればよい、という発想です。
- 実装要点：monad（単項のスカラー拡張）とdyad（二項のスカラー拡張）を定義すると、任意のスカラー関数がリストや入れ子構造に自然に適用されます。これに簡易パーサと評価器（eval）を乗せれば、K風の短い言語が出来上がります。

簡易例（要旨）:
```python
# python
atom = lambda x: isinstance(x, (int, float, str))
monad = lambda f: lambda x: f(x) if atom(x) else [monad(f)(xi) for xi in x]
dyad = lambda f: lambda x,y: f(x,y) if atom(x) and atom(y) \
    else [dyad(f)(xi,y) for xi in x] if not atom(x) \
    else [dyad(f)(x, yi) for yi in y]
```
この仕組みで sqrt や 加算 をラップすれば、スカラーもベクトルも同一の関数で扱えます。

## 実践ポイント
- まずは上の monad/dyad をコピーして、Python REPLで小さな例（リストや入れ子リストへの適用）を試す。
- NumPyとの比較実験：同じ処理をNumPyとモノリシックなmonad/dyadで実装して、可読性と柔軟性の違いを確認する。
- 興味があれば「90行実装」を手元で写経して、パーサ／eval部を少しずつ拡張してみる（演算子追加、簡易REPLなど）。
- 日本語ドキュメントや入門記事を翻訳・補足して、コミュニティで共有すると学びが深まります。
