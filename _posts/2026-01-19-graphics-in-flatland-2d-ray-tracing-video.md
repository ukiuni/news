---
layout: post
title: "Graphics In Flatland – 2D ray tracing [video] - 平面のグラフィックス — 2Dレイトレーシング［ビデオ］"
date: 2026-01-19T22:03:44.017Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.youtube.com/watch?v=WYTOykSqf2Y"
source_title: "Graphics In Flatland - 2D ray tracing - YouTube"
source_id: 46649781
excerpt: "平面世界で光と影・反射を学ぶ2Dレイトレーシング実演動画、SDFとShaderToyで解説"
image: "https://i.ytimg.com/vi/WYTOykSqf2Y/hqdefault.jpg"
---

# Graphics In Flatland – 2D ray tracing [video] - 平面のグラフィックス — 2Dレイトレーシング［ビデオ］
クリックしたくなる日本語タイトル: 平面世界で描く光の魔法——2Dレイトレーシング入門（実演動画つき）

## 要約
2D空間（Flatland）でレイトレーシング的な手法を使って光や影、反射を描くアプローチを実演する動画の解説。3Dより直感的で学びやすく、シェーダーやゲーム表現の基礎を掴むのに最適。

## この記事を読むべき理由
レイトレーシングは高品質なライティング表現の王道だが、3Dだと数学や実装が重く感じられます。2D版で原理を学べば、シェーダー開発やゲームのライティング・エフェクト実装に必要な直感と技術が効率よく身につきます。日本のインディーゲームやWeb表現、Unity/ShaderToyでのプロトタイプ作りにも役立ちます。

## 詳細解説
- レイトレーシングと2D
  - 通常のレイトレーシングは光線をカメラからシーンへ飛ばし、最初に当たる物体で色を計算します。2Dでは同じ考え方を平面上で適用し、光線（線分）と円・線・ポリゴンの交差や距離場（Signed Distance Field, SDF）を使って効率的に判定します。学習コストが低く、可視化もわかりやすいのが利点です。

- 距離関数（SDF）の基本
  - 物体を数学的な距離関数で表現すると、ある点から物体までの最短距離が得られます。例えば円のSDFは次のように表されます。
  $$
  d(\mathbf{p}) = \|\mathbf{p} - \mathbf{c}\| - r
  $$
  ここで $\mathbf{p}$ は評価点、$\mathbf{c}$ は円心、$r$ は半径。負の値は内部、正は外部、ゼロが境界を示します。

- レイマーチング（歩行による当たり判定）
  - レイを進める際に各ステップでSDFの値を参照し、その距離だけ安全に進めます。これにより不要な交差判定を減らし、適度な反復回数で物体に到達できます。ただしステップ数上限や最小距離閾値を設定し、性能と正確さのトレードオフを管理します。

- 法線とライティング
  - 法線はSDFの勾配から近似できます。2Dでは数値的差分で求めることが多く、これを使ってLambert反射や反射ベクトルを計算します。陰影やソフトシャドウも距離場を応用して表現可能です。

- 反射・再帰的トレース
  - 単純な反射は、衝突点で反射ベクトルを計算してもう一度レイを飛ばすことで実装できます（再帰やループで深さ制限）。2Dなので処理は軽く、反射や透過の視覚効果を試しやすいです。

- 実行環境と実装例
  - 動画でよく使われるのはWebGL/GLSLやShaderToyのフラグメントシェーダー。短いコードで視覚的にわかりやすいデモが作れます。UnityではURP/HDRPのカスタムシェーダーやShader Graphで応用可能です。

## 実践ポイント
- まずはShaderToyやWebGLで試す
  - GLSLのフラグメントシェーダーで円や長方形のSDFを書き、レイマーチングのループを実装してみる。視覚フィードバックが早く得られるため学習効率が高い。
- 最低限の実装方針
  - 1) SDFを用意（円・箱） 2) カメラからピクセル方向にレイを飛ばす 3) 各ステップでSDFを参照して進める 4) 当たれば法線・ライティング・反射を計算する
- 最適化のコツ
  - 最大ステップ数・最小距離（epsilon）を調整する。オクルージョンや遠方の判定はLOD的に省略する。可能なら距離場の簡易キャッシュや粗解像度でのプルーフを使う。
- 日本の現場での応用例
  - 2Dインディーゲームのライト/影表現、メニューやUIのリッチなビジュアル、技術デモや教育コンテンツ。モバイルでも軽量な2D版なら実運用しやすい。
- 学習リソース
  - ShaderToyのサンプル、SDF入門記事、Unity/GLSLのチュートリアルを並行して読むと理解が速い。

短いGLSLの例（フラグメントシェーダーの骨格）:
```glsl
// glsl
precision mediump float;
uniform vec2 u_resolution;
float sdCircle(vec2 p, vec2 c, float r){ return length(p - c) - r; }
void main(){
  vec2 uv = (gl_FragCoord.xy / u_resolution) * 2.0 - 1.0;
  vec2 cam = vec2(0.0);
  vec2 dir = normalize(uv - cam);
  vec2 p = cam;
  float dist;
  for(int i=0;i<64;i++){
    dist = sdCircle(p, vec2(0.5,0.0), 0.3);
    if(dist < 0.001) break;
    p += dir * dist;
  }
  vec3 col = (dist < 0.001) ? vec3(1.0,0.6,0.2) : vec3(0.0);
  gl_FragColor = vec4(col,1.0);
}
```

最後に一言：動画で実演を見ると「光の進み方」が直感的に理解できます。まずは短いシェーダーを書いて、平面世界での光の“挙動”を手で確かめてみてください。
