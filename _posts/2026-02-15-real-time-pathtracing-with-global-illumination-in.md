---
layout: post
title: "Real-time PathTracing with global illumination in WebGL - WebGLでのリアルタイム経路追跡（グローバルイルミネーション）"
date: 2026-02-15T19:15:10.926Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://erichlof.github.io/THREE.js-PathTracing-Renderer/"
source_title: "THREE.js-PathTracing-Renderer | Real-time PathTracing with global illumination and progressive rendering, all on top of the Three.js WebGL framework. Click here for Live Demo: https://erichlof.github.io/THREE.js-PathTracing-Renderer/Geometry_Showcase.html"
source_id: 46993014
excerpt: "ブラウザで30–60FPSの本格GIパストレーシングを実現、Three.jsで手軽にフォトリアル表示"
---

# Real-time PathTracing with global illumination in WebGL - WebGLでのリアルタイム経路追跡（グローバルイルミネーション）
魅惑のブラウザCG：Three.js上で“本物の光”を30–60FPSで体験する方法

## 要約
Three.jsベースのWebGLパス・トレーサーで、グローバルイルミネーション、反射・屈折、カオスティクス（光の集中）などをブラウザでリアルタイム（30–60FPS）に実現するプロジェクトの紹介と解説。

## この記事を読むべき理由
ブラウザだけでフォトリアルなライティングが可能になり、プロダクト可視化、建築、教育、軽量ゲームやWebデモの表現力が劇的に向上します。日本の開発現場でも「インストール不要で動く高品質レンダリング」は即戦力です。

## 詳細解説
- 基本概念：パストレーシングは光線をシーン内で何度も反射/屈折させて真の間接照明を計算する手法。プログレッシブレンダリングによりフレーム毎にサンプルが蓄積され、短時間で収束する。
- Three.js上での実装：レンダラはThree.jsをホストにしてGPUシェーダーで経路追跡を実行。画面全体を覆うクワッドに対してピクセルごとのサンプリングを行う構成が多い。
- BVH（Bounding Volume Hierarchy）：多数ポリゴンの高速交差判定のための加速構造。階層的なAABBで射線判定を絞り込むことで、大モデル（Stanford Dragon等）でもリアルタイムに。
- レイトレース＋レイマーチ：水面や大気などはレイマーチ（距離関数）で表現し、レイトレーシングと組み合わせて高品質で効率的に描画。
- 数学プリミティブ（Quadric）：球や円錐などは暗黙関数で定義でき、たとえば単位球は $x^2 + y^2 + z^2 - 1 = 0$ のように表せる。一般的な四次元パラメータは次の形で整理できる：
$$
Ax^2 + By^2 + Cz^2 + Dxy + Exz + Fyz + Gx + Hy + Iz + J = 0
$$
研究手法を使い $A\ldots J$ を 4x4 行列に格納してGPUへ送ることで大量の解析形状を効率的に扱う。
- 実デモ群：コーニルボックス、海と空、ボリューメトリック、GLTFモデルのPBR対応、HDRI環境光、BVHビジュアライザ、モデルインスタンシング（1万〜百万単位のポリゴンを実時間で）など多数。スマホでも30–60FPSを達成するチューニングが施されている。
- 工夫例：トーラスの代替手法（2つの二次曲面を組合せる）など、精度問題や浮動小数点の制約を回避する実用的な近似がある。

## 実践ポイント
- まずデモを見る：著者のライブデモで挙動と性能を体感する（Geometry Showcase 等）。
- Three.jsを基盤に：既存のThree.jsプロジェクトへパス・トレーサーを統合するとGPU経路追跡が試せる。
- BVH最適化：大モデルを扱うならBVHとランダム化された直接光サンプリングを導入してノイズ低減と収束を高速化。
- HDRIとPBRを活用：製品可視化ではHDRI環境とPBRマテリアルで写真寄りの描画が簡単に得られる。
- レイマーチで規模を稼ぐ：海や地形はレイマーチで表現するとメッシュ不要で軽量に表現できる。
- モバイル対応は必須：ターゲットをモバイルにするならサンプル数の調整・分解能スケーリング・低精度シェーダ配慮が効果的。

短時間でブラウザ上に「光の物理的な振る舞い」を持ち込めるこの取り組みは、今後のWebベース3D表現の標準技術になり得ます。
