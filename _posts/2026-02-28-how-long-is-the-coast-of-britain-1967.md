---
layout: post
title: "How Long Is the Coast of Britain? - イギリスの海岸線はどれくらい長いか"
date: 2026-02-28T19:05:57.309Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.jstor.org/stable/1721427"
source_title: "How Long Is the Coast of Britain? (1967)"
source_id: 47144835
excerpt: "測定尺度で変わる海岸線長のパラドックスとフラクタル次元でGIS・防災に活かす実務的手法を図解"
---

# How Long Is the Coast of Britain? - イギリスの海岸線はどれくらい長いか
海岸線の「長さ」は尺度で変わる──フラクタルで読み解く地図と現実のギャップ

## 要約
マンデルブロが示した「海岸線のパラドックス」は、測定尺度に依存して海岸線の長さが変化することを示し、その複雑さを表す指標として分数次元（フラクタル次元）$D$を導入した。

## この記事を読むべき理由
地図データやGISを扱う日本のエンジニアや自治体担当者にとって、海岸線長さの誤解は測量・防災・環境評価に直結する。尺度依存性を理解すれば、データ解釈と意思決定が正確になる。

## 詳細解説
- コーストのパラドックス：粗いスケールで測れば短く、詳細に測れば長くなる。これは海岸線の凹凸が縮尺を変えても自己相似的に現れるため。
- 分数次元の概念：伝統的な曲線は次元1、面は2だが、複雑な海岸線は1と2の間の値$D$を取り得る。測定尺度$\varepsilon$と推定長さ$L(\varepsilon)$の関係は
  $$L(\varepsilon)\propto \varepsilon^{\,1-D}$$
  で表され、対数プロットの傾きから$D$を推定できる（$\log L = (1-D)\log\varepsilon + \mathrm{const.}$）。
- 推定法：コンパス法（divider／歩測法）やボックスカウント法が代表的。ボックスカウントではサイズ$\varepsilon$の格子で被覆する箱数$N(\varepsilon)$が
  $$N(\varepsilon)\propto \varepsilon^{-D}$$
  と振る舞い、$\log N$対$\log\varepsilon$の傾きで$D$を得る。
- 注意点：衛星解像度、測線の平滑化、潮位や岸辺の季節変動が結果に影響するため、比較には同一の尺度・条件が必須。

## 日本市場との関連
日本はリアス式海岸や無数の小島を抱え、海岸線の複雑さは世界でも高い。防潮堤や津波対策、沿岸生態系評価で「何を基準に長さや面積を定義するか」が政策判断に影響する。フラクタル次元は地域ごとの複雑さ比較やデータ解像度選定の根拠になる。

## 実践ポイント
- 海岸線長を扱う際は、「使用した測定尺度（解像度）」を必ず明記する。
- フラクタル次元$D$を推定して、比較やトレンド分析に使う（同一手法・解像度で比較すること）。
- 実装ヒント（Python・ベクタ/ラスタデータでボックスカウント）:

```python
# python
import numpy as np
from skimage import io, color, transform
# binary maskを読み込み、ボックスカウントでDを推定する簡易例
img = io.imread('coast_mask.png', as_gray=True) > 0.5
sizes = 2**np.arange(1, int(np.log2(min(img.shape))))
counts = []
for s in sizes:
    small = transform.resize(img.astype(float), (img.shape[0]//s, img.shape[1]//s), order=0) > 0.5
    counts.append(np.sum(small))
coeff = np.polyfit(np.log(sizes), np.log(counts), 1)
D = -coeff[0]  # 傾きの符号に注意
print('estimated D ≈', D)
```

- ツール例：QGIS + GDAL、geopandas/shapely、scikit-image を組み合わせると現場データで検証しやすい。

元論文はマンデルブロの古典的短報（1967年）。尺度依存性を押さえるだけで、海岸・河川・道路など地理データの扱いがぐっと実務的になります。
