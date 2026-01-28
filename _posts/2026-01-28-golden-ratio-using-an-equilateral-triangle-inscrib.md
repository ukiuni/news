---
layout: post
title: "Golden Ratio using an equilateral triangle inscribed in a circle - 円に内接する正三角形から黄金比を導く方法"
date: 2026-01-28T03:56:06.339Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://geometrycode.com/free/how-to-graphically-derive-the-golden-ratio-using-an-equilateral-triangle-inscribed-in-a-circle/"
source_title: "Sacred Geometry:Golden Ratio:Equil.Triangle in circle:GeometryCode.com"
source_id: 46735152
excerpt: "辺の中点を通る弦を使い正三角形から黄金比φを作図で導く実践法"
---

# Golden Ratio using an equilateral triangle inscribed in a circle - 円に内接する正三角形から黄金比を導く方法
コンパスと円だけで見つかる「φ」の秘密 — 正三角形と弦が描く自然な比率

## 要約
正三角形を円に内接させ、その辺の中点を通る弦を利用すると、図形的に黄金比 $\phi$ を得られる。相似な三角形関係から $\phi$ の二次方程式が自然に現れる方法の紹介。

## この記事を読むべき理由
黄金比はデザインやUI、プロダクト比率、自然現象の解析で頻出します。手元のコンパスやGeoGebraで再現できる「作図で見つける」手法は、直感と数学をつなぐ良い学習材料で、日本のデザイナー／エンジニアにもすぐ使える実践的な技法です。

## 詳細解説
手順（概念的）：
1. 円を描き、その円に正三角形 $ABC$ を内接させる（頂点間の中心角は $120^\circ$）。
2. 三角形の辺の中点（例えば $AB,\,AC$ の中点）を結ぶ直線を引き、その直線が円と交わる2点を $P,Q$ とする（要するに「辺の中点を通る弦」）。
3. 図中にできるいくつかの三角形を見ると、相似な三角形の組が現れる。相似比を文字で表すと、弦上の区間の比が次の関係を満たすことがわかる：
   $$
   \frac{a+b}{a}=\frac{a}{b}
   $$
   ここで $a,b$ は弦上の隣接する区間の長さ。
4. 上の比から $a$ と $b$ の比率 $r=\dfrac{a}{b}$ は
   $$
   r^2=r+1
   $$
   を満たすため、正の解は
   $$
   r=\phi=\frac{1+\sqrt{5}}{2}
   $$
   となる。

直感的には、正三角形と円の対称性が「極端な分割（extreme）」と「中間の分割（mean）」を同時に満たす配置を作り、これが「極端と中間の比＝中間と残りの比」という黄金比の定義に対応します。

## 実践ポイント
- コンパス＋定規で再現：円→正三角形（120°毎に点を置く）→辺の中点→中点を通る弦を引く。弦上の区間を定規で測り比を確かめる。
- GeoGebraやDesmosで座標を使って検証すると誤差なく数値確認できる（点座標を取って距離比を計算してみてください）。
- デザイン応用：画面やカードの分割にこの作図を取り入れると、直感的で安定した比率（$\phi$）を得られます。
- 学習用途：高校幾何や入門的な証明練習に最適。相似三角形と二次方程式の結びつきを視覚で理解できます。
