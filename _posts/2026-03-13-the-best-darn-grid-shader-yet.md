---
layout: post
title: "The Best Darn Grid Shader (Yet) - 最高のグリッドシェーダ（これまでで）"
date: 2026-03-13T14:54:25.191Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://bgolus.medium.com/the-best-darn-grid-shader-yet-727f9278b9d8"
source_title: "The Best Darn Grid Shader (Yet)"
source_id: 1156931648
excerpt: "fwidthとsmoothstepでテクスチャ不要、遠景でも崩れない高品質グリッドを実現する手順"
---

# The Best Darn Grid Shader (Yet) - 最高のグリッドシェーダ（これまでで）
テクスチャ以上にキレイなグリッドを描く――誰でも使える「究極のグリッドシェーダ」入門

## 要約
テクスチャベースのグリッドに匹敵（あるいは超える）見た目をシェーダで実現する試み。主要問題は遠景でのエイリアスやモアレ、パースによる線幅表現で、著者は実用的な解法を段階的に示す。

## この記事を読むべき理由
ゲーム、3Dツール、VR、設計ソフトなど日本の開発現場でも「見やすく正確なグリッド」は必須。テクスチャ任せにせずシェーダ側で安定した描画を得る方法を知れば、パフォーマンスと画質の両立が可能になります。

## 詳細解説
- 問題点の整理  
  - テクスチャグリッド：遠景で線が太くなったり切れたり、テクスチャ解像度に依存。  
  - 単純なチュートリアル実装（UV空間で smoothstep + fwidth）：近景はシャープだが遠景でセルが1ピクセル未満になると塊になり、モアレやエイリアスが目立つ。  
  - 高度な既存手法：RenderMan の filtered pulsetrain や Inigo Quilez の box-filtered は「見た目の明るさ」や理論的なフィルタリングは優れるが、中〜遠距離のモアレや精度ノイズが残る。

- 著者の目標  
  1) ユーザーが指定できる線幅  
  2) 遠近感に合った線幅（パースで細くなる）  
  3) あらゆる距離・向きでのエイリアス抑制  
  4) 0/1 の極端値が正しく出る  
  5) モアレ低減、テクスチャグリッドに近い遠景のフェード

- 実装の核（要点）  
  1) 単一ラインは smoothstep を使い、abs と UV 変換で線を作る。  
  2) エッジ幅は fwidth（画素ごとの偏微分）で求め、スクリーンスペースで安定したアンチエイリアスを行う。  
  3) 繰り返しは frac を使ってソーベル→三角波へ変換し、軸ごとに同じ処理をしてからプリマルチブレンド（lerp）で合成する（max や単純積ではなくアルファ合成を模した合成が自然）。  
  4) UV幅固定（ワールド／UV空間で一定幅）とピクセル幅固定（fwidth を掛ける）を切り替え可能にする。  
  5) smoothstep の幅は経験則で 1.5px 相当を使うと線の知覚的シャープネスと AA のバランスが良い。  

- 重要な小ネタ  
  - ピクセル幅指定にするには lineWidth を fwidth(uv) と掛け合わせる。  
  - 軸合成は premultiplied alpha 式（lerp）を使うと自然な重なりが得られる。  
  - RenderMan 系の解析的フィルタ（pulsetrain）は「輝度の振る舞い」は良いがモアレを完全に消せない。

小さなコード断片（要点）
```hlsl
// HLSL
float2 uvDeriv = fwidth(uv);
float2 lineAA = uvDeriv * 1.5;
float2 gridUV = 1.0 - abs(frac(uv) * 2.0 - 1.0);
float2 grid2 = smoothstep(lineWidth + lineAA, lineWidth - lineAA, gridUV);
float grid = lerp(grid2.x, 1.0, grid2.y); // premultiplied-like blend
```

## 実践ポイント
- まずは fwidth を使う：アンチエイリアス性能が格段に向上する。  
- UV→三角波（frac + abs）で繰り返しラインを作り、軸合成は lerp（プリマルチ）で。  
- ピクセル幅が欲しいなら lineWidth *= fwidth(uv)。  
- テクスチャグリッドと見た目を近づけたい場合は RenderMan の filtered pulsetrain を試すが、モアレ対策（フィルタリングや回転サンプリング）を併用する。  
- Unity/Unreal 等ではシェーダ実装前に高解像度での見え方、異なる mip/anisotropic 設定、VRの片目表示で必ず確認すること。

以上を踏まえれば、テクスチャに頼らない「表現力が高く、遠景でも崩れにくい」グリッドシェーダを自作できます。元記事は実装の試行錯誤が丁寧なので、実装参照とデバッグのヒントに最適です。
