---
  layout: post
  title: "Cigarette smoke effect using shaders - シガレット（たばこ）の煙エフェクトをシェーダで作る"
  date: 2026-01-05T14:49:31.664Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://garden.bradwoods.io/notes/javascript/three-js/shaders/shaders-103-smoke"
  source_title: "Shaders 103 - smoke"
  source_id: 46497589
  excerpt: "Perlinノイズと頂点ツイストで作る、滑らかでループするリアルなタバコの煙表現"
  image: "https://garden.bradwoods.io/ogImage.jpg"
---

# Cigarette smoke effect using shaders - シガレット（たばこ）の煙エフェクトをシェーダで作る
魅力的タイトル: 「3行のシェーダで作る“リアルな煙”—three.jsでタバコの煙を滑らかに表現する手法」

## 要約
Perlinノイズテクスチャをシェーダでサンプリングし、アルファマスク・リマップ・エッジフェード・頂点ツイストを組み合わせることで、three.js上に半透明で流動的な煙のアニメーションを作る手法を解説する。

## この記事を読むべき理由
フロントエンドやクリエイティブコーダー向けに、GPU上で軽く動く「自然な煙」表現の作り方を具体的に示す。日本のUI/広告/ゲーム制作でも、低コストでビジュアルの質を上げる即戦力テクニックになる。

## 詳細解説
ポイントを段階的にまとめる。

- 基本構成  
  - 平面ジオメトリに ShaderMaterial を適用。頂点シェーダで UV を varying に渡し、フラグメントでテクスチャを読む流れ。

  - 例（骨格）:
  ```javascript
  const material = new THREE.ShaderMaterial({
    uniforms: {
      uTexture: { value: texture },
      uTime:   { value: 0.0 },
      uSpeed:  { value: 0.2 },
      // ...other uniforms
    },
    vertexShader: `...`,
    fragmentShader: `...`,
    transparent: true,
    depthWrite: false,
    side: THREE.DoubleSide,
  });
  ```

- テクスチャ（Perlinノイズ）  
  - グレースケールノイズを読み、`.r` で値を取得。これをアルファや高さ、ねじれの種に利用する。テクスチャは縦繰り返しのために `texture.wrapT = THREE.RepeatWrapping` を設定。

- UV → テクスチャサンプリング  
  - 頂点シェーダで `vUv = uv;` を渡し、フラグメントで `texture(uTexture, vUv).r` を利用してピクセルごとの値を取得する。

- マスク描画（半透明）  
  - 色は白固定にしてアルファにノイズ値を使うと「透ける煙」になる。material に `transparent: true` を忘れずに。

- アニメーション  
  - 時間値 $uTime$ と速度 $uSpeed$ を使ってサンプリング位置をずらす：$textureUv.y -= uTime \times uSpeed$。テクスチャの RepeatWrapping によりループする煙が作れる。

- 明度のリマップ（透明度調整）  
  - `smoothstep(uRemapLow, uRemapHigh, textureImpl)` でノイズ値の閾値を滑らかに調整し、薄いグレーを黒（透明）か白（不透明）に近づけて煙らしさを強調する。smoothstep は次のように振る舞う：
  $$
  smoothstep(a,b,x)=
  \begin{cases}
  0 & x\le a\\
  1 & x\ge b\\
  \text{smooth interp} & a<x<b
  \end{cases}
  $$

- エッジフェード（端の自然化）  
  - 平面の端がベタッと見える問題は、UV座標に基づく smoothstep でフェードをかけることで解決。左右・上下それぞれにパラメータ（uEdgeX, uEdgeY）を持たせ、最終アルファに掛け合わせる。

- トランスフォーム（ねじれ＝ツイスト）  
  - 見た目の立体感を出すために頂点シェーダで位置を回転。UV.y に対応したノイズサンプルを角度に変換し、頂点の xz 平面を回転させる。回転関数は 2D 回転行列を用いる：
  ```glsl
  vec2 rotate2D(vec2 v, float a) {
    float s = sin(a), c = cos(a);
    mat2 m = mat2(c, s, -s, c);
    return m * v;
  }
  ```
  - ツイストのサンプリングはテクスチャの「1px縦スライス」を参照するイメージで、`uTwistSampleX` を固定して `texture(uTexture, vec2(uTwistSampleX, uv.y * uTwistSampleHeight - uTime * uTwistSpeed)).r` のように取得する。

- 奥行きと重なり（オクルージョン）  
  - 半透明の重なりの扱いは厄介。今回の表現では層を透かして見せたいので `depthWrite: false` とし、描画順やブレンドを制御する（必要ならソートを検討）。

## 実践ポイント
- テクスチャは高コントラストの Perlin/FBM を選ぶ。明度調整（uRemapLow/High）で煙の密度を操れる。  
- パフォーマンス：平面の頂点数は最低限に。フラグメントで重い処理をしすぎない（複数サンプルやループ注意）。  
- 見た目調整パラメータ（すぐ触るべきもの）: uSpeed, uRemapLow, uRemapHigh, uEdgeX/Y, uTwistStrength, uTwistSpeed。UI（dat.GUI等）でリアルタイム調整すると効率的。  
- 深度やブレンドの問題は実環境で確認。半透明を重ねる場合は描画順（カメラから遠い順）を意識するか、深度テストの調整を検討する。  
- 日本の案件での活用例：UIの装飾（背景の雰囲気付け）、ゲームの演出、短いプロモ動画の簡易エフェクトなど、リソースを抑えつつ「空気感」を出したい場面に有効。

必要なら、vertex/fragment の最小実装例を付けて、three.js のコード統合手順も出しますか？
