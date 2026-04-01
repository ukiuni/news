---
layout: post
title: "Jax's true calling: Ray-Marching renderers on WebGL - JAXの本領発揮：WebGL上のレイマーチングレンダラー"
date: 2026-04-01T22:35:59.481Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://benoit.paris/posts/jax-ray-marcher/"
source_title: "JAX&#39;s true calling: Ray-Marching renderers on WebGL - benoit.paris"
source_id: 47605494
excerpt: "JAXでSDFレイマーチングをGPU化し、ブラウザで高速に動くインタラクティブ3Dアートを即作成"
---

# Jax's true calling: Ray-Marching renderers on WebGL - JAXの本領発揮：WebGL上のレイマーチングレンダラー
ブラウザで動くPython×GPUの3Dアート入門 — JAXで描く「距離関数ベース」のリアルタイムレンダリング

## 要約
JAXの自動微分・ベクトル化・コンパイル機能を使って、Signed Distance Functions（SDF）ベースのレイマーチングレンダラーをPythonで書き、WebGLでブラウザ実行する手法を紹介する記事の解説。

## この記事を読むべき理由
- Pythonで書いた数式をGPUで高速実行して、ブラウザ上でインタラクティブな3D表現を作れる点は、教育・プロトタイピング・Webデモ作成に即役立つため。  
- JAXの特徴（vmap, grad, jit）がグラフィクス実装に自然に効く具体例として学べる。

## 詳細解説
- Signed Distance Function（SDF）: 位置を入力に取り、物体表面までの距離を返す関数。内部は負、外部は正になるよう定義する。これにより形状の合成（和=min, 積=max、滑らかな合成はsmooth min）や変形が容易。
- レイマーチング（sphere tracing）: レイに沿って現在位置からSDFの返す距離だけ進めることを繰り返し、表面に到達するまでサンプリングする手法。SDFの性質から安全にステップ幅を決められる。
- JAXの利点:
  - ベクトル化: pixel単位の関数をjax.vmapで一気に並列評価できる（画素全体をGPUで並列化）。
  - 自動微分: 表面法線は距離関数の勾配で得られるため、光源処理や反射が簡潔に書ける。$$\text{normal}(p)=\nabla d(p)$$
  - コンパイル: jit/コンパイルで実行速度が高速になり、ブラウザ向けにエクスポートしてWebGLで動かす実験が可能。
- 実装の核（要点）:
  - SDFを小さな関数群（球、立方体、円柱 等）として定義し、min/maxやsmooth minで合成する。  
  - 画素ごとのray_color関数を2重のvmapで並列化:
```python
# python
ray_colors = jax.vmap(jax.vmap(ray_color, (None, 0, None)), (0, None, None))
```
  - 法線は自動微分で一行:
```python
# python
normal_at_surface = jax.grad(distance_function)(point_at_surface)
```
- 拡張可能性: jax-jsやWebGPUサポート、幾何的代数（JAXGA）、関数のテイラー展開（jet）などでさらに高度な最適化や表現が期待できる。

## 実践ポイント
- まず小さなSDF（球と箱）を実装してレイマーチングの流れを理解する。  
- jax.vmapで画素並列化、jax.jitで速度改善、jax.gradで法線を取得する流れを押さえる。  
- ブラウザ実行には jax-js / WebGPU 経由のエクスポートを検討（社内デモやポートフォリオに最適）。  
- 日本のWebやゲーム系のプロトタイプ、教育コンテンツ作成に向くため、クラウドGPUやブラウザ配信と組み合わせて試すと効果大。
