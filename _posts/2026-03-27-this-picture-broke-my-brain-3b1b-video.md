---
layout: post
title: "This picture broke my brain [3B1B video] - この画像は私の脳を壊した"
date: 2026-03-27T15:43:43.971Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.youtube.com/watch?v=ldxFjLJ3rVY"
source_title: "How (and why) to take a logarithm of an image - YouTube"
source_id: 47490609
excerpt: "画像に対数変換すると色相が一変、線形化と輝度操作で驚きの真相がわかる"
image: "https://i.ytimg.com/vi/ldxFjLJ3rVY/maxresdefault.jpg"
---

# This picture broke my brain [3B1B video] - この画像は私の脳を壊した

思わず見入る「画像の対数変換」が見せる世界 — 色と明暗の裏側をやさしく解き明かす

## 要約
3Blue1Brownの動画は、画像に対数を取ると見える「別の真実」を示し、なぜその結果が直感とズレるのかを数学と色空間の観点から解説します。

## この記事を読むべき理由
スマホ写真の見栄え調整や画像処理の基礎を理解する上で、対数変換が持つ意味（ダイナミックレンジ圧縮、乗算的変化の加算化、色の扱い方）は実務でも役立ちます。日本のカメラアプリ開発者や写真好きにも直結する知識です。

## 詳細解説
- 対数変換とは：画素値 $I$ に対して $I'=\log(I+\epsilon)$ のように変換する操作。暗い部分の差を目立たせつつ明るい部分を押し下げる、ダイナミックレンジ圧縮の基本手法です。$\epsilon$ は $I=0$ を扱うための小さな値です。
- なぜ「脳が壊れる」のか：普通に $R,G,B$ 各チャンネルに対数を取ると、色比（色相）が変わって不自然な色味になることがあります。これは対数が乗算的な係数を加算に変えるためで、元の「色の比率」を保たないからです。
- 色空間の違いが重要：画像ファイル（特にJPEG/sRGB）はガンマ補正がかかって保存されています。画像処理はまず線形RGBに戻す（逆ガンマ）ことが原則。その上で、色を壊さないためには輝度だけに対数を適用するのが安全です。輝度は一般に
  $$
  Y = 0.2126R + 0.7152G + 0.0722B
  $$
  のような係数で求めます。または、CIELABなどの分離された輝度チャンネルを使うと色変化を抑えられます。
- 応用的視点：対数は乗算的ノイズ（影や照明の乗算的変化）を扱いやすくします。HDR画像のトーンマッピングやテクスチャ解析でも有用です。

## 実践ポイント
- まずsRGB→線形RGBに変換してから対数を適用し、最後にガンマ補正して表示する。
- 色を保ちたいならRGB各チャンネルでなく「輝度」に対数を適用し、色は元比率で再合成するか、LabのLチャネルを操作する。
- 実装例（簡易、要ライブラリ）：

```python
# python
import numpy as np
from PIL import Image

eps = 1e-6
img = np.array(Image.open('photo.jpg')).astype(np.float32) / 255.0
# 簡易：各チャンネルに対数（実運用では線形化→輝度操作を推奨）
log_img = np.log(img + eps)
# 正規化して保存
log_img = (log_img - log_img.min()) / (log_img.max() - log_img.min())
Image.fromarray((log_img * 255).astype('uint8')).save('photo_log.jpg')
```

少し手間をかけて線形化→輝度のみ変換→再合成することで、動画で示された「驚き」を安全に再現できます。
