---
layout: post
title: "Terminals should generate the 256-color palette - ターミナルは256色パレットを自動生成すべき"
date: 2026-02-18T00:25:12.216Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://gist.github.com/jake-stewart/0a8ea46159a7da2c808e5be2177e1783"
source_title: "Terminals should generate the 256-color palette · GitHub"
source_id: 727553160
excerpt: "ターミナルがbase16からLAB補間で自動生成する256色パレットでテーマの可読性と一貫性を改善"
image: "https://github.githubassets.com/assets/gist-og-image-54fd7dc0713e.png"
---

# Terminals should generate the 256-color palette - ターミナルは256色パレットを自動生成すべき
面倒なテーマ設定はもう終わり？端末があなたのbase16テーマから賢く256色パレットを作る提案

## 要約
ターミナルの既定256色パレットは多くのbase16テーマと衝突し、可読性に問題がある。提案はユーザーのbase16（背景/前景含む）から216色キューブとグレースケールをLAB空間で補間して生成すること。

## この記事を読むべき理由
日本の開発者も多用するターミナル（tmux/vim/sshなど）で、テーマの一元管理と見やすさを両立できる現実的な手法だから。truecolorの手間を避けつつ表現力を上げられます。

## 詳細解説
- 3つの選択肢  
  - base16: 設定は簡単だが色数が16で不足。  
  - truecolor: 1670万色を扱えるが、各アプリで設定が必要・対応状況やパフォーマンスの問題あり。  
  - 256色: 手間少なく表現力が中間に収まるが、既定パレットはbase16テーマと合わずコントラストや明度が不均一。

- 256色パレットの構成  
  - 最初の16色：base16に対応する基本色。  
  - 216色の6x6x6色キューブ：RGB各チャネルが0〜5の6段階。インデックスは
  $$
  16 + (36R) + (6G) + B
  $$
  （$R,G,B\in[0,5]$）  
  - 24段のグレースケール：
  $$
  232 + S
  $$
  （$S\in[0,23]$）

- 問題点の本質  
  - デフォルトのキューブは黒→各色への補間が不適切（最初の非黒シェードが期待より明るめ）。  
  - 彩度揃えがされておらず、同じ「段」で色ごとに見かけの明るさが変わる。

- 解決アプローチ（提案）  
  - base16の8色（通常色）を6x6x6キューブのコーナーにマップし、背景（bg）と前景（fg）を黒白代わりに使う。  
  - trilinear interpolation（3次元線形補間）で各軸を補間して216色を生成。  
  - グレースケールはbg→fgの線形補間で作る。  
  - 補間はRGBではなくLAB色空間で行い、色相差による「見かけの明るさ」のずれを補正する。

- 実装の核（要点）
  - 色をRGB→LABに変換して補間、結果をLAB→RGBで戻す。  
  - これによりbase16テーマと調和した256色が得られ、可読性と一貫性が向上する。

以下はgistの実装要旨（抜粋）：

```python
def lerp_lab(t, lab1, lab2):
    return (
        lab1[0] + t * (lab2[0] - lab1[0]),
        lab1[1] + t * (lab2[1] - lab1[1]),
        lab1[2] + t * (lab2[2] - lab1[2]),
    )

def generate_256_palette(base16, bg=None, fg=None):
    base8_lab = [rgb_to_lab(c) for c in base16[:8]]
    bg_lab = rgb_to_lab(bg) if bg else base8_lab[0]
    fg_lab = rgb_to_lab(fg) if fg else base8_lab[7]
    palette = [*base16]
    for r in range(6):
        c0 = lerp_lab(r/5, bg_lab, base8_lab[1])
        c1 = lerp_lab(r/5, base8_lab[2], base8_lab[3])
        c2 = lerp_lab(r/5, base8_lab[4], base8_lab[5])
        c3 = lerp_lab(r/5, base8_lab[6], fg_lab)
        for g in range(6):
            c4 = lerp_lab(g/5, c0, c1)
            c5 = lerp_lab(g/5, c2, c3)
            for b in range(6):
                c6 = lerp_lab(b/5, c4, c5)
                palette.append(lab_to_rgb(c6))
    for i in range(24):
        t = (i + 1) / 25
        lab = lerp_lab(t, bg_lab, fg_lab)
        palette.append(lab_to_rgb(lab))
    return palette
```

## 実践ポイント
- まずは手持ちのbase16テーマ（SolarizedやGruvbox等）でこの生成スクリプトを試し、端末での見え方を比較する。  
- tmux/vim/lessなど、256色対応アプリで設定を統一すれば複数アプリのテーマ同期が簡単。  
- ライト／ダーク切替はbase16側を切り替えるだけで自動反映されるため運用が楽に。  
- 実装は公開ドメインで改変可能なので、好みに合わせた補間・色空間調整を行ってみると良い。
