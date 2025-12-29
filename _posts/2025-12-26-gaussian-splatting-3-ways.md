---
layout: post
title: Gaussian Splatting 3 Ways
date: 2025-12-26 20:53:19.827000+00:00
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: https://github.com/NullandKale/NullSplats
source_title: GitHub - NullandKale/NullSplats
source_id: 46395273
excerpt: 動画や画像から撮って数分で立体化、ワークフロー解説と3方式のGaussian Splattingを実例で高速比較
---
# [撮ってそのまま3分で立体化？Gaussian Splattingを「3通り」で試すNullSplats紹介]

## 要約
NullSplatsは動画や画像フォルダから自動でフレーム抽出→COLMAPでカメラ復元→GPUでGaussian-splat表現を学習し、3Dスプラット（.ply/.splat）とOpenGLビューアで即確認できるワークフローを提供するデスクトップツールです。3つの異なる生成手法（gsplat, Depth Anything 3, SHARP）を手軽に比較できます。

## この記事を読むべき理由
日本の開発者・クリエイターにとって、低コストなキャプチャで短時間に3Dアセットを作れる技術は、ローカルAR/VR、文化財の簡易デジタル化、ゲーム向けプロトタイプ作成など多用途に応用可能だからです。NullSplatsは「実験→再現→出力」までの工程をまとめてくれるため、既存パイプラインへの取り込みや検証が速くできます。

## 詳細解説
- ワークフロー概要
  - 入力：動画か画像フォルダを与え、フレーム抽出とスコアリングで代表フレームを自動選択。
  - カメラ復元：COLMAPでStructure-from-Motionを実行し、カメラ姿勢とスパース点群を生成。
  - 学習：PyTorchベースのgsplatや別手法（Depth Anything 3、SHARP）で3D Gaussian splatsをGPUで学習。
  - 可視化と保存：組み込みのOpenGLビューアで確認し、.ply/.splatなどでエクスポート。全データはキャッシュツリーに保存され、途中再開が可能。
- 提供される「3つの作り方」と特性
  - gsplat（伝統的なCOLMAP＋gsplat訓練）
    - 多視点（例：50 view）での再現に強く、幾何精度が高い。リポジトリのサンプルではRTX Blackwell系でColmap含め約5分で学習済みに。
    - 推奨：十分な視点がある撮影で高品質出力を狙う場合。
  - Depth Anything 3（3D Gaussian推定）
    - 中程度の視点数（例：5 view）で高速に生成。ただしメモリ消費が大で、サンプルでは約16GB VRAMを使用。
    - 推奨：視点少なめで良質な深度推定ができれば高速に結果を得たいケース。
  - SHARP（単一画像モノキュラ合成）
    - 1 viewでも「立体っぽさ」を出せるのが特徴。サンプルでは約2.5分で結果が出ており、単一ショットのプロトタイプに強い。
    - 注意：単一視点ゆえの形状曖昧さや透明表現の問題が残る場合あり。
- 実行コスト感
  - サンプル環境での時間感：SHARP ~2.5分、DA3 ~3–4分（ただし大Vram）、gsplat ~5分（COLMAP込み）。
  - 解像度：720pサンプルが使われているため、撮影解像度とGPU性能のバランスが重要。

## 実践ポイント
- ハードウェア：なるべくGPU（できれば16GB以上のVRAM）を用意。小型GPUでもSHARPは試しやすい。
- キャプチャ：多視点を撮れるならgsplatを、少数視点で試すならDA3、単一ショットの迅速なデモならSHARPを選ぶ。
- 前処理：フレーム抽出時にバラエティある角度と露出を確保するとCOLMAPの姿勢推定が安定する。
- ワークフロー：リポジトリのrequirements.txt、main.py/run.batを確認して依存を整え、まずはsampleで動作確認してから自分の素材へ適用する。
- 出力活用：.plyはBlenderやUnityにインポート可能。キャッシュ機構を使えば学習途中からの再開や比較実験が容易。
- チューニング：学習反復回数（例：50-viewサンプルは12k iter）やフレーム選定が品質に大きく影響するので、まず少ない反復で試してから増やす。

