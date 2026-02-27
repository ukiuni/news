---
layout: post
title: "Signed distance field fonts - サインド・ディスタンス・フィールド（SDF）フォント"
date: 2026-02-27T22:58:30.727Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.redblobgames.com/articles/sdf-fonts/"
source_title: "Guide to SDF+MSDF Fonts"
source_id: 394961286
excerpt: "SDF/MSDFでGPUリアルタイムに多言語フォントの縁取り・グローを高品質に実現"
---

# Signed distance field fonts - サインド・ディスタンス・フィールド（SDF）フォント
グラフィック表現が一段上がる！SDF/MSDFで縁取り・グロー・シャドウを自在に作る方法

## 要約
SDF/MSDFは低解像度の「距離場」テクスチャをGPUで解釈して、高品質な拡大・縁取り・グロー・シャドウなどの効果をリアルタイムに得る技術です。msdfgenなどのツールと簡単なフラグメントシェーダで扱えます。

## この記事を読むべき理由
モバイルやゲーム、UIで「複数解像度・多言語・効果付きフォント」を効率的に扱いたい開発者やデザイナーにとって、SDF/MSDFはメモリと描画品質の両立手段になります。日本語の大文字集合や合字を含む多言語対応での実運用に直結する知見を得られます。

## 詳細解説
- 基本概念：SDFは各ピクセルに「文字境界までの距離」を格納する高さマップのようなもの。低解像度の距離場をGPU側で解釈して任意サイズで滑らかな境界を再構成するため、ビットマップを単純拡大したときのジャギーを避けられます。
- SDF vs MSDF：単一チャネルSDFは丸みが出やすい（角が丸くなる）。MSDFはRGBに別々の距離情報を入れ、中央値を取ることで鋭い角を再現します。msdfgenで --type msdf を指定。
- ピクセル値→距離のマッピング：テクスチャの 0–255 をエム（em）単位の距離に線形変換して扱います。msdfgen の aemrange（distanceRangeMiddle/size 等）を使って0→外側,255→内側にマップします。
- 描画（しきい値判定とアンチエイリアス）：閾値で内外を判定する代わりに、滑らかな遷移でアルファを計算します。式は
  $$
  opacity = \operatorname{clamp}\!\left((threshold - distance)\times \frac{1}{width} + 0.5,\ 0,\ 1\right)
  $$
  で、実運用では「画面ピクセルあたり約1px分」をアンチエイリアス幅にすると自然です。サイズが変動する場合は fwidth を使って GPU 側でスケールを推定します。
- MSDFの中央値サンプル（フラグメント内での例）：rgb 各チャネルの中央値を距離として使います（msdfgen推奨）。
- アトラスとレイアウト：文字単体ではなくアトラス（texture atlas）とテキストシェーピング（Harfbuzz 等）で文字の配置・UVを計算。日本語など多言語はグリフ数が多く、アトラス生成時の設計が重要です。
- アウトライン・グロー・シャドウ：閾値範囲を分けて色を重ねることでアウトラインや外側のグローを表現可能。距離に応じて任意の色レイヤーを描画できます。

参考ライブラリ・ツール：msdfgen / msdf-atlas-gen、Text Mesh Pro（Unity）、Unreal SDF、tiny-sdf、stb_truetype 等。

以下は最小のシェーダ断片（概念実装）：

```glsl
// glsl
precision mediump float;
uniform sampler2D u_atlas;
uniform vec2 u_aemrange; // [aem_min, aem_max]
uniform float u_threshold_em;
uniform float u_inverse_width;
in vec2 v_st;
out vec4 o_frag_color;

float median(vec3 c){ return max(min(c.r,c.g), min(max(c.r,c.g), c.b)); }

void main() {
  // MSDF: use median of rgb; SDF: use .r
  float texel = median(texture(u_atlas, v_st).rgb);
  float distance_em = mix(u_aemrange.y, u_aemrange.x, texel);
  float opacity = clamp((u_threshold_em - distance_em) * u_inverse_width + 0.5, 0.0, 1.0);
  o_frag_color = vec4(1.0, 1.0, 1.0, opacity); // premultiplied alpha適用可
}
```

## 実践ポイント
- まずは msdfgen + msdf-atlas-gen でアトラスを作り、WebGL/Unityで上のシェーダを試す。Text Mesh Pro / Unreal での既存実装も活用可能。
- u_threshold_em は通常 0.0、太くしたければ小さく（負に）調整。アンチエイリアス幅は「画面での1px相当」を目安に設定。
- 鋭角が重要なら MSDF、グローやシャドウを重視するなら単一SDFの方が扱いやすい場合あり。フォントごとに比較テストを必ず行う。
- 日本語などグリフ数が多い場合はアトラスの分割と HarfBuzz 等でのシェーピング処理を検討する（合字／プロポーショナル処理）。
- 実装で困ったら Valve(2007) 論文と msdfgen のドキュメントを参照すると実務ノウハウが見つかります。

---

元記事: "Signed distance field fonts"（Red Blob Games）。元記事の具体的なコードや画像はオリジナルを参照してください。
