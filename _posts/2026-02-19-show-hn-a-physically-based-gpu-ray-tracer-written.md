---
layout: post
title: "Show HN: A physically-based GPU ray tracer written in Julia - Juliaで書かれた物理ベースGPUレイトレーサー"
date: 2026-02-19T12:55:55.355Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://makie.org/website/blogposts/raytracing/"
source_title: "Show HN: A physically-based GPU ray tracer written in Julia"
source_id: 47072444
excerpt: "JuliaとMakieでGPUパストレーシング、データ直結で出版品質の写実レンダリングを即座に実現"
---

# Show HN: A physically-based GPU ray tracer written in Julia - Juliaで書かれた物理ベースGPUレイトレーサー
Julia×Makieで「そのまま」写真品質へ──研究データから対話的にレンダリングする新しいワークフロー

## 要約
Makieに組み込まれたRayMakie/Hikari（およびRaycore）により、既存のMakieシーンをエクスポートなしでGPUパストレーシングで写実的にレンダリングできるようになりました。スペクトルレンダリング、ボリューム、物理ベースマテリアルをGPU上で動かします。

## この記事を読むべき理由
- 研究可視化や産業用途（気候、農業、構造生物学、流体など）で「ただのプロット」が即座に出版品質やプレゼン品質に変わるため。  
- Juliaエコシステム内で完結するため、データ移動や新ツール習得のコストが激減します。日本の研究機関やスタートアップにとって導入の障壁が低い点が魅力です。

## 詳細解説
- アーキテクチャ
  - Hikari：pbrt-v4 をJuliaへ移植した波面（wavefront）ボリュームパストレーサー。スペクトルレンダリング、参加媒体（NanoVDB/RGBグリッド）、PBRマテリアルをサポート。  
  - Raycore：交差判定エンジン（Radeon Rays / HIPRT由来）を切り出した独立パッケージ。  
  - RayMakie：Makieのシーングラフと接続し、既存のAPI（mesh!, surface!, volume! 等）をそのままレンダラー切替で利用可能にする。

- 技術的特徴
  - GPUネイティブ実装：JuliaからGPUカーネルを生成し、パフォーマンスはC++実装に匹敵する設計を目指す。  
  - クロスベンダー対応：KernelAbstractions.jl経由でAMD/NVIDIA/CPU向けに単一コードベースで動作させる方針（現状はAMDが最もテスト済み）。  
  - 拡張性：Juliaのmultiple dispatchにより、カスタム材料や媒体、物理モデルをユーザー定義してGPUにコンパイル可能（例：重力レンズを模したブラックホールデモ）。  
  - インタラクティブ性：RayMakie.interactive_windowでカメラ操作中も逐次洗練されるプログレッシブレンダリング。従来のMakieオーバーレイ（凡例や注釈）との合成も可能。

- 実デモ事例
  - Breeze / Oceananigans：LES雲シミュレーションをNanoVDBで高速表示。  
  - PlantGeom：作物デジタルツインで葉の透過や反射を物理的に表現し、放射・熱収支解析に応用。  
  - ProtPlot：タンパク質構造の写実的可視化とアニメーション。  
  - TrixiParticles：SPH水しぶきの屈折・反射表現。  
  - Geant4連携：大規模検出器ジオメトリの物理ベースレンダリング。  

- 現状の制約
  - 正式リリース前（記事時点）。GPUメモリ管理やBVH・カーネル最適化、NVIDIA/CUDA側の十分なテスト等が今後の課題。SPPM（カスティクス）など未復活の機能あり。

## 実践ポイント
- まず試す：RayDemoリポジトリ（記事のリンク先）とProject.tomlを参照して環境を作り、サンプルを動かす。  
- 最低限のレンダリング例（Julia）:
```julia
using RayMakie, Hikari

scene = Scene(size=(800,600), lights=[SunSkyLight(Vec3f(1,2,8))])
cam3d!(scene)
mesh!(scene, my_geometry; material=Hikari.Gold())
img = colorbuffer(scene; device=AMDGPU.ROCBackend(), integrator=Hikari.VolPath(samples=100, max_depth=12))
```
- 実運用の注意点：複雑シーンはVRAMを大量に消費するため、まず小さな解像度・サンプル数で試し、段階的に品質を上げる。AMD環境での動作確認が最も安定している点にも留意。  
- 応用アイデア：日本の気候シミュレーション、農業デジタルツイン、バイオ可視化や学術プレゼン資料の品質向上に直結します。研究→レンダリング→解析のワークフローをJulia内で完結させたいチームは早めの試用を推奨します。

（原稿内のサンプル・デモは記事執筆時点のプレリリース実装に基づきます。最新の互換性やインストール手順はRayMakie/Hikariのリポジトリを確認してください。）
