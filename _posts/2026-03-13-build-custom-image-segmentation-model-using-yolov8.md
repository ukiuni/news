---
layout: post
title: "Build Custom Image Segmentation Model Using YOLOv8 and SAM - YOLOv8 と SAM で作るカスタム画像セグメンテーション"
date: 2026-03-13T06:53:27.597Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://eranfeit.net/segment-anything-tutorial-generate-yolov8-masks-fast/"
source_title: "YOLOv8 SAM Segmentation Python: Generate Fast Object Masks"
source_id: 383912889
excerpt: "YOLOv8で検出→SAMで学習不要の高精度マスクを高速生成"
image: "https://eranfeit.net/wp-content/uploads/2025/11/4-Build-Custom-Image-Segmentation-Model-Using-YOLOv8-and-SAM.png"
---

# Build Custom Image Segmentation Model Using YOLOv8 and SAM - YOLOv8 と SAM で作るカスタム画像セグメンテーション
魅力的タイトル: YOLOv8で「検出」→ SAMで「一発マスク」—初心者でもすぐ使える高速・高精度セグメンテーション実践ガイド

## 要約
YOLOv8で素早く対象を検出し、そのバウンディングボックスをSAM（Segment Anything Model）に渡してピクセル精度のマスクを自動生成するワークフローを、実践的な環境構築とコードの流れ付きで解説します。

## この記事を読むべき理由
YOLOv8 + SAM の組合せは「学習不要で高品質なマスク」を短時間で得られるため、アノテーション削減や試作プロダクトの迅速化に直結します。日本の画像系プロジェクト（EC商品撮影の背景除去、製造ラインの異常検知、社内データ作成など）で即戦力になる知識です。

## 詳細解説
- 基本アイデア：YOLOv8（高速物体検出）で対象の矩形（x1,y1,x2,y2）を得て、その矩形をSAMへの「プロンプト」として与えると、SAMがピクセル単位で精密なマスクを返す。学習し直す必要がない点が最大の魅力。
- 環境：安定動作のために専用のConda環境を作り、PyTorch（CUDA があるならGPUビルド）、Ultralytics（YOLOv8）、segment-anything パッケージ、OpenCV、matplotlib 等を入れる。OpenCVの競合に注意（opencv-python/headlessのアンインストール→再インストール推奨）。
- 実装の流れ：
  1. 画像をOpenCVで読み込む（BGR→RGBに注意）。
  2. YOLOv8（例：yolov8n）で推論し、検出ボックスとクラス・信頼度を取得。複数検出時は面積や信頼度でターゲットを選択。
  3. SAM（例：ViT-H は高品質、ViT-B/L は軽量）をロードし、SamPredictor に画像をセット。YOLOのボックスをプロンプトとして渡してマスクを取得。
  4. マスクの可視化（半透明オーバーレイ）、必要ならクリックで精細化（positive/negative）や multimask_output=True で候補を取得して最良を選択。
  5. マスクをPNGや二値配列としてエクスポート、あるいは合成して完成画像を保存。
- 実践的注意点：
  - GPU があれば高速化。GPU無くても動くが遅い。
  - SAMは set_image で埋め込みをキャッシュするため、同一画像で複数プロンプトを試すと高速。
  - マスクのずれは座標・リサイズ処理の不整合が原因になりやすい（YOLO出力とSAM入力で同じスケーリング/座標系にすること）。
  - バッチ処理はループ化して画像ごとに set_image → predict の流れ。大量処理はGPUメモリに注意。
- デバッグ／拡張：
  - 複数オブジェクトは面積最大や信頼度順で自動選択、または全検出ボックスを順にマスク化して個別に保存。
  - マスクの品質が足りない場合はクリック（ポイントプロンプト）でエッジ修正が可能。
  - 出力をマスク＋アルファ合成して背景差分や切り抜き用素材に利用。

## 実践ポイント
- まずはCPUで動作確認→GPU（CUDA）で高速化。Condaで環境分離を必ず行う。
- 初期は yolov8n + SAM ViT-B から試し、品質/速度のバランスで ViT-L/ViT-H に移行。
- 複数検出は「面積最大／信頼度最高」をデフォルトにして自動化すると実運用で安定。
- マスクは PNG（アルファチャンネル）や二値配列で保存し、アノテーションや合成ワークフローに流用する。
- VSCodeならスクリプト実行→出力確認→修正のサイクルが速い。assets/ フォルダにテスト画像を入れて再現性を保つこと。

この記事で説明したワークフローを1つ作っておけば、日本のプロダクト開発や研究で「早く・安く・高精度」にセグメンテーションを試せます。まずは小さな画像セットで試運転して、利用ケースに合わせてSAMバックボーンやYOLOモデルを調整してください。
