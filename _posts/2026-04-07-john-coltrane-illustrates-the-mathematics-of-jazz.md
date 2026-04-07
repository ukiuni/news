---
layout: post
title: "John Coltrane Illustrates the Mathematics of Jazz - ジョン・コルトレーンが示すジャズの数学"
date: 2026-04-07T17:28:03.392Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.americanjazzmusicsociety.com/blog/john-coltrane-draws"
source_title: "John Coltrane Illustrates the Mathematics of Jazz | American Jazz Music Society"
source_id: 47671219
excerpt: "コルトレーンのトーン・サークルでGiantStepsの和声を幾何学的に可視化"
image: "http://static1.squarespace.com/static/5e9496b1ca1cec725d1b5ff1/t/5fead1c7264cc9271ecb980f/1609224655679/Untitled+design.png?format=1500w"
---

# John Coltrane Illustrates the Mathematics of Jazz - ジョン・コルトレーンが示すジャズの数学
コルトレーンの「トーン・サークル」が教える、音楽と幾何学の出会い — エンジニア目線で読み解く

## 要約
ジョン・コルトレーンの描いた「トーン・サークル」は、円環上の音程や対称性を利用した音楽構造を視覚化したもので、幾何学・物理学的な観点からジャズの和声進行を解き明かします。

## この記事を読むべき理由
音楽に潜む数学的構造は、信号処理・アルゴリズム作曲・音楽情報処理（MIR）などテック領域で直接応用できます。日本は楽器メーカーや音楽系スタートアップが多く、コルトレーンの視点はプロダクトや研究の着想源になります。

## 詳細解説
- トーン・サークルとサークル・オブ・フィフス: 伝統的な「五度圏」は半音12分割の等比的配置に基づき、隣接する音の周波数比は等しく表現されます。等温律での半音比は $2^{1/12}$ で、任意の音高は
$$f_n = f_0 \cdot 2^{n/12}$$
  と表せます。
- コルトレーンの応用（例: Giant Steps）: コルトレーンは五度圏だけでなく、オクターブを等しく3分割する「長3度（major third）」による対称配置を多用しました。長3度は周波数比で $2^{1/3}$ に相当し、キー中心が等間隔に並ぶことで独特の循環進行が生まれます。
- 幾何学・対称性の視点: 音高を円に配置すると対称操作（回転、反転）が和声転換やモーダル移動に対応します。これにより、和音進行や転調を「幾何変換」として扱えるため、アルゴリズム的な生成・解析に有利です。
- 科学と霊性の交差: コルトレーンは科学的・哲学的な比喩で自身の理論を語りました。物理学者が指摘するように、音楽の幾何学的直観は物理学的対称性と親和性があります（例：群論的視点や周期性の扱い）。

## 実践ポイント
- まずは可視化：音名を円にプロットして、五度圏／長3度分割（3つに分割）を切り替えてみる。Pythonでの簡単な例：
```Python
import math, numpy as np
notes = 12
angles = [2*math.pi*i/notes for i in range(notes)]
coords = [(math.cos(a), math.sin(a)) for a in angles]
# 長3度(3分割)の位置は角度差 2π/3
```
- 楽曲解析：Giant Steps等の譜面でコードセンターの間隔を数値化（半音差）し、どの対称性が使われているか判定する。
- 応用アイデア（日本の現場向け）：Yamaha／Roland系のMIDIツールやDAWプラグインで「対称進行ジェネレータ」を作る、または機械学習でコルトレーン風進行を学習させ自動伴奏に応用する。

短時間で取り組める実験として、「半音比 $2^{1/12}$ を使って周波数列を生成→円座標にマッピング→回転や反転で和声変換を試す」ことをおすすめします。
