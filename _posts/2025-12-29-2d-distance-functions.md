---
layout: post
title: 2D Distance Functions - 2D距離関数
date: 2025-12-29T08:51:52.602Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://iquilezles.org"
source_title: "Inigo Quilez :: computer graphics, mathematics, shaders, fractals, demoscene and more"
source_id: 1045548953
excerpt: "SDFで短時間に滑らか合成や繰り返し模様を作る実践ガイドと最適化テクニック"
---

# 2D Distance Functions - 2D距離関数

## 要約
2D距離関数（Signed/Unsigned Distance Functions）は、形状を「点からの距離」として定義し、合成や変形が容易でリアルタイム表現に強い。シェーダやゲーム、ビジュアルアートに直結する強力なツールだ。

## この記事を読むべき理由
シェーダやプロシージャル生成が現場で当たり前になった今、距離関数の考え方を知るだけで短時間で多彩な表現（ブーリアン合成、滑らかなブレンド、繰り返しモチーフなど）を実装できる。日本のゲーム開発、CG制作、インディーのデジタルアート制作で即戦力となる知識です。

## 詳細解説
- 基本概念  
  距離関数は点 $p$ に対して形状までの距離 $d(p)$ を返す関数。符号付き（SDF）は内部が負、外部が正になるため、境界は $d(p)=0$ で表せる。SDFは境界の法線や最近接点の取得、衝突判定にも使える。

- 代表的なプリミティブ（2D）  
  - 点/円: $d(p, c) = \|p-c\| - r$  
  - 軸合わせ長方形（半辺ベクトル $b$）: $q = |p| - b,\quad d(p)=\| \max(q,0)\| + \min(\max(q_x,q_y),0)$  
  - 線分: 最近接点をパラメータで射影し、端点との距離を取る  
  これらを組み合わせるだけで多くの形が作れる。

- ブーリアン演算（合成）  
  - 和（Union）: $d_{\cup}(a,b)=\min(a,b)$  
  - 積（Intersection）: $d_{\cap}(a,b)=\max(a,b)$  
  - 差（Subtraction）: $d_{\setminus}(a,b)=\max(a,-b)$  
  ただの min/max だと境界が鋭くなるため、滑らかにするスムージングを入れるテクニックがよく使われる。

- スムーズブレンド（例）  
  パラメータ $k$ による平滑化の一例：
  $$
  h = \max\!\left(0, 1 - \frac{|a-b|}{k}\right),\quad
  d = \min(a,b) - h^2 \frac{k}{4}
  $$
  この式で2つの形が自然に繋がる。

- 幾何変換と反変換  
  描画側では点を逆変換してからプリミティブの距離を評価する。回転・平行移動・拡大縮小は座標系に対する簡単な逆適用で実装できる。

- パターン生成／繰り返し  
  繰り返しは座標を周期的に折り返すだけで簡単に実現でき、タイル状のパターンやフラクタル風表現に有効。

- 実行環境と最適化  
  SDFはピクセル毎の計算（フラグメントシェーダ）と相性が良い。早期脱出（バウンディングボックスでの判定）や反復を減らすことでパフォーマンスを確保できる。法線は距離場の勾配で得られるため、ライティング計算も容易。

## 実践ポイント
- まずはShadertoyやUnityのFragment Shaderで円・箱・線分のSDFを実装してみる。境界がゼロになることを可視化すると直感がつかめる。  
- スムーズなブレンド（smooth min）を使って複雑な形状を“黙って”合成する。パラメータ $k$ を変えて表現の幅を見る。  
- 繰り返し（mod）と回転を組み合わせてテクスチャ不要のモチーフや背景を作成。タイルやパターンの解像感を動的に制御可能。  
- SDFは衝突判定や簡易的な物理（距離に基づく押し戻し）にも応用でき、2Dゲームのプロトタイプで役立つ。  
- 実務ではGPUメモリや描画コストを考慮して、まずは粗い解像度で試し、必要箇所だけ詳細化する（LOD的手法）。

簡単なGLSL例（円と箱の和）:
```glsl
// glsl
float sdCircle(vec2 p, vec2 c, float r){
  return length(p-c) - r;
}
float sdBox(vec2 p, vec2 b){
  vec2 q = abs(p) - b;
  return length(max(q,0.0)) + min(max(q.x,q.y),0.0);
}
float opUnion(float a, float b){ return min(a,b); }

void mainImage(out vec4 fragColor, in vec2 fragCoord){
  vec2 uv = (fragCoord.xy - iResolution.xy*0.5)/iResolution.y;
  float d1 = sdCircle(uv, vec2(-0.2,0.0), 0.2);
  float d2 = sdBox(uv - vec2(0.25,0.0), vec2(0.15,0.12));
  float d = opUnion(d1,d2);
  float e = smoothstep(0.01, -0.01, d); // 境界を描画
  fragColor = vec4(vec3(e),1.0);
}
```

日本のCG制作現場やインディー開発、デジタルアートに直接役立つ実践的なテクニックなので、まずは手を動かして小さなシェーダやツールを作ってみてください。
