---
layout: post
title: "Ray Marching Soft Shadows in 2D - 2Dでのレイマーチングによるソフトシャドウ"
date: 2026-02-11T11:13:38.922Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.rykap.com/2020/09/23/distance-fields/"
source_title: "Ray Marching Soft Shadows in 2D &#8211; Ryan Kaplan"
source_id: 444442128
excerpt: "距離場×レイマーチングで速く描く2Dのふわっとしたソフトシャドウ実装指南"
image: "http://rykap.com/images/voronoi.png"
---

# Ray Marching Soft Shadows in 2D - 2Dでのレイマーチングによるソフトシャドウ
魅せる2DタイポやUIに使える高速ソフトシャドウの作り方 — 距離場とレイマーチングで「ふわっと」影を描く

## 要約
距離場（distance field）を使ってピクセル毎に光線を進め、最小距離情報を活用して高速にソフトシャドウを生成する手法をわかりやすく解説します。シャドウの「にじみ（ペンumbra）」は距離比と光源距離で調整します。

## この記事を読むべき理由
WebGL／Canvasで動くグラフィクス表現は日本のUI・ゲーム・広告でも需要大。フォントやベクターシェイプに対して軽量に見栄えの良い影を付けられるため、実装コストを抑えつつ表現力を上げたい開発者に有用です。

## 詳細解説
- 距離場とは  
  画素ごとに「最近接シェイプまでの距離」を保持する画像。サンプルすると任意点からの最短距離が得られ、それを使って安全に光線を進められます。

- レイマーチングのコアアイデア  
  ピクセルから光源へ向かうレイ上で、現在点からの距離 sceneDist を取得し、その値だけ進める。これにより“飛び越し”を防ぎつつステップ数を稼げます。最大ステップ数を設けて重いケースを回避します。

- シャドウ判定（硬い影）  
  進めた先で sceneDist <= 0 なら遮蔽物に当たっており影。光源まで到達できれば明るい。

- ソフトシャドウの近似（非物理だが速い）  
  3つのルールを組み合わせてペンumbra を作る。
  1. あるレイ上で最小の sceneDist が小さいほど“影寄り”にする。  
  2. その“ほぼ接触点”からサンプル点までの距離（rayProgress）が大きいほど影を広げる。  
     → 各ステップで sceneDist / rayProgress の最小値を取るのがキー。  
  3. 光源からの距離で減衰（例：半径 R で二乗減衰）して全体の寄与を落とす。  
     つまり最終的な寄与は min(sceneDist / rayProgress) * distanceFactor。

- バンディング対策  
  ステップ数が少ないと近似が粗く帯状ノイズ（バンディング）が出る。対策として：
  - Inigo Quilez の改良（最小値取得の改善）を適用する。  
  - 進行量にランダムジャッター（sceneDist * jitter）を掛けてステップ位置をずらし、ピクセル間の同期を崩す（グレインは増えるがバンディングは減る）。

- 実装上の注意  
  - getDistance は事前に生成した距離場テクスチャをサンプリングする。  
  - ループ上限（例 64 ステップ）や光源半径 R を調整して性能と品質のバランスを取る。  
  - モバイルの一部デバイスでは高精度なテクスチャや分岐が重い点に注意。

## 実践ポイント
- 距離場はフォント・SVGから高速生成してキャッシュする（UIの文字列影に最適）。  
- GLSL のループで maxSteps を決め、getDistance の呼び出しを最小限に。  
- ソフト化パラメータ：光源半径 R、最大ステップ数、ジャッター比（0〜1）を調整する。  
- バンディングが気になるならランダムジャッター（ピクセル毎にシード）か Inigo Quilez の改良を導入。  
- 日本のプロダクト向けには、画面解像度とタッチ端末の性能を考慮してフォールバック（低品質モード）を用意する。

参考として簡潔なコアアルゴリズム（GLSL風）：

```glsl
vec2 rayOrigin = ...;
vec2 rayDir = normalize(lightPos - samplePt);
float rayProgress = 0.;
float stopAt = length(lightPos - samplePt);
float lightContrib = 1.0;
for (int i = 0; i < 64; ++i) {
  if (rayProgress > stopAt) {
    float R = 800.0;
    float fade = 1.0 - clamp(stopAt / R, 0.0, 1.0);
    float distanceFactor = pow(fade, 2.0); // $$distanceFactor=\left(1-\min(1,\frac{stopAt}{R})\right)^2$$
    return lightContrib * distanceFactor;
  }
  float sceneDist = getDistance(rayOrigin + rayProgress * rayDir);
  if (sceneDist <= 0.0) return 0.0;
  lightContrib = min(lightContrib, sceneDist / max(rayProgress, 1e-4));
  rayProgress += sceneDist;
}
return 0.0;
```

この手法は見た目の良さと軽さのバランスが魅力です。UIや2Dゲームのライティングに取り入れて、まずはパラメータをいじりながら挙動を確認してみてください。
