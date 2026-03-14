---
layout: post
title: "You gotta think outside the hypercube - ハイパーキューブを越えて考える"
date: 2026-03-14T06:45:42.739Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lcamtuf.substack.com/p/you-gotta-think-outside-the-hypercube"
source_title: "You gotta think outside the hypercube - lcamtuf’s thing"
source_id: 47323625
excerpt: "テッセラクトを回転・等角・透視で可視化する実践ガイド（実装図解付き）"
image: "https://substackcdn.com/image/fetch/$s_!Punz!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F73d9c28a-f287-4b29-abc2-40d701fcdf60_1409x1012.jpeg"
---

# You gotta think outside the hypercube - ハイパーキューブを越えて考える
驚くほどわかる！4次元「テッセラクト」を画面に描くための発想とテクニック

## 要約
テッセラクト（4次元の立方体）をワイヤーフレームで作り、4次元回転と2D画面への投影を段階的に解説する。複数の投影法（斜投影・等角・透視・フィッシュアイなど）を比較して、見た目と情報性の折衷を示す。

## この記事を読むべき理由
図形の次元概念や可視化手法は、ゲーム開発、データ可視化、教育教材、研究プロトタイピングで直接役立ちます。日本のエンジニアや学生が4D表現を理解し、実装に移せる実践的知見が得られます。

## 詳細解説
- エッジの定義（低次元から一般化）  
  - 2D（正方形、辺の集合）: $|x|\le a,\;|y|=a$（横線）と $|x|=a,\;|y|\le a$（縦線）。  
  - 3D（立方体）: これを $z$ 軸に複製し、さらに $|x|=a,\;|y|=a,\;|z|\le a$ のような $z$ 方向の辺を追加。  
  - 4D（テッセラクト、4次元軸を $\omega$ と表記）: 各ルールに $|\omega|=a$ を付け、$\omega$ 方向の辺 $|x|=a,\;|y|=a,\;|z|=a,\;|\omega|\le a$ を追加。結果、頂点16、辺32。

- 回転（平面回転の組合せ）  
  - 2D の回転：  
    $$x_{new}=x\cos\alpha - y\sin\alpha,\quad y_{new}=y\cos\alpha + x\sin\alpha$$  
  - 4D でも基本は「二次元平面での回転」を使う（XY, XZ, YZ, Xω, Yω, Zω）。例：XZ 回転  
    $$x_{new}=x\cos\alpha + z\sin\alpha,\quad z_{new}=z\cos\alpha - x\sin\alpha$$  
    Zω 回転：  
    $$z_{new}=z\cos\alpha - \omega\sin\alpha,\quad \omega_{new}=\omega\cos\alpha + z\sin\alpha$$

- 2D への投影（代表的手法の比較）
  - キャヴァリエ（Cavalier）: 単純に $z$ を斜めに射影。  
    $$x_{screen}=x + z\cos45^\circ,\quad y_{screen}=y + z\sin45^\circ$$  
    見た目が伸びて不自然になることがある。
  - キャビネット（Cabinet）: $z$ 成分を半分に縮めて長さ感を調整。  
    $$x_{screen}=x + \frac{z\cos45^\circ}{2},\quad y_{screen}=y + \frac{z\sin45^\circ}{2}$$
  - 等角投影（Isometric）: 軸を60°等間隔に見せる。3D の等角は自然で安定。  
    $$x_{screen}=(x - z)\cos30^\circ,\quad y_{screen}=y + (x + z)\sin30^\circ$$  
    4D を拡張すると軸を詰めて表現する案があるが、3D形状の歪みを招きやすい。
  - 透視投影（Rectilinear one-point）: $x,y$ を $z$（さらに $\omega$）に応じて割ることで消失点を表現。ネストした立方体（内外のキューブ）になる視覚は理解しやすいが、$z$ と $\omega$ が混ざり次元識別が曖昧に。
  - フィッシュアイ（Fisheye）: カメラ位置からの距離で座標を非線形に縮め、重なりを減らす。線の手前・奥の順序を Euclidean 距離で決めることで奥行き感を強化。
  - 混合手法（実用的）: x,y,z は等角、$\omega$ は透視で扱うと「安定して見やすい」テッセラクト表示が得られる。回転に合わせて深度計算に $\omega$ を混ぜる／無視することで演出を変えられる。

## 実践ポイント
- まずはワイヤーフレームで実装：辺は座標条件（$|.|$）で生成し、頂点配列と辺リストを作ると扱いやすい。  
- 回転は平面単位で適用（行列積で実装すると拡張が楽）。複数平面の連続回転で4Dの挙動を再現。  
- 投影は用途で選ぶ：情報重視→混合（等角＋透視）、直感的表現→透視、アート的→フィッシュアイ／等角。  
- 描画時は深度ソート（距離に基づく描画順）と不透明度／線の太さで手前・奥を分かりやすくする。  
- 実装例：WebGL/Canvas、Three.js（カスタム投影）、Unity（4Dデータを2Dに投影して表示）や MATLAB のスクリプト（元記事リンクの例）を参考にすると早い。

元記事の MATLAB コードやアニメーションは実装の良い参照になります。テッセラクトは「美しいだけでなく、投影の選択が情報性をどう変えるか」を学ぶ教材として最適です。
