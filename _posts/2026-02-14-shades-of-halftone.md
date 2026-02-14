---
layout: post
title: "Shades of Halftone - ハーフトーンの色合い"
date: 2026-02-14T16:03:48.569Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.maximeheckel.com/posts/shades-of-halftone/"
source_title: "Shades of Halftone - The Blog of Maxime Heckel"
source_id: 46959531
excerpt: "WebGL/GLSLで写真や動画をレトロなハーフトーン風に自在に変える技法と実装の入門ガイド"
image: "https://blog.maximeheckel.com/static/og/87476d3b0871838ae8917d401ba03be5.png?v1"
---

# Shades of Halftone - ハーフトーンの色合い
魅せるドット表現で写真も動画も3Dもアートに変える：初心者でも作れるハーフトーン・シェーダー入門

## 要約
古い印刷技法「ハーフトーン」をWebGL/GLSLで再現し、ドットの配置・サイズ・形状・アンチエイリアスを組み合わせることで多彩な表現が可能になる、という解説記事です。

## この記事を読むべき理由
ハーフトーンはレトロでありながら現代のUIや映像表現で強い個性を与えます。日本のデザイン／ゲーム／広告制作でも需要が高く、ツール（Paper, Efecto, Unicorn Studio 等）で手軽に扱えるため、基礎を押さえておくと表現の幅が広がります。

## 詳細解説
- ハーフトーンの本質：小さなドットの密度やサイズを変えることで、人間の視覚が平均化し「階調」を知覚する現象を利用する。
- 基本要素
  - 円（距離場）：UV座標で中心からの距離を求め、閾値でマスクする。滑らかにするなら `smoothstep` を使う。
```glsl
// glsl
float dist = length(cellUv - 0.5);
float circle = smoothstep(radius - 0.01, radius + 0.01, dist);
```
  - グリッド（タイル化）：`fract(uv * gridSize)` でセル単位のUVを作り、各セルに同じ円を描く。
  - ピクセライズ：`floor` を使ってテクスチャのサンプリング座標をセル単位に揃える（ドットとテクスチャを1:1にするため）。
```glsl
// glsl
vec2 pixelSize = uPixelSize / uResolution;
vec2 uvPixel = pixelSize * floor(uv / pixelSize);
vec4 tex = texture(inputBuffer, uvPixel);
```
  - 輝度連動（Luma-based radius）：セルの輝度に応じてドット半径を変えると原画像の階調が再現される。
```glsl
// glsl
float luma = dot(tex.rgb, vec3(0.2126, 0.7152, 0.0722));
float radius = uRadius * (0.1 + luma);
```
- バリエーション
  - オフセットグリッド（交互にずらす）で密度を上げる。
  - 白点混合（暗部に白い小点を重ねる）や四角/リングなど「ドットに隣接する形」を作ることでテクスチャ保存性や印象を変える。
  - リングは2つの円の差で表現できる（内円 AND NOT 外円）。
- アンチエイリアス：単純な `step` はジャギーになるため `smoothstep` と `fwidth` を組み合わせて解像度依存のエッジ幅を計算する。

## 実践ポイント
- まずはShaderToyやThree.jsのフラグメントシェーダーで、上の最小構成（fract + distance + smoothstep + floor）を実装してみる。
- 調整するパラメータ：Grid Size（セル数）、Radius（ドット半径）、Pixel Size（ピクセル化）、Luma Weight、Grid Offset、Antialiasing Strength。
- モバイル注意点：大きなグリッドやフルスクリーンのポスト処理はGPU負荷が高い。静止画像ならサーバ側でプリレンダーしておくのも有効。
- 日本的応用例：マンガ風テクスチャ、レトロ広告、ゲームのUIエフェクト、プロモーション動画のフィルターなど。

この記事で紹介した要点を押さえれば、既存のビジュアルに対して短時間でハーフトーンの個性を付与できます。興味があれば、試作用の簡単なGLSLスニペットを渡します。どの環境（ShaderToy / Three.js / Unity）で試したいですか？
