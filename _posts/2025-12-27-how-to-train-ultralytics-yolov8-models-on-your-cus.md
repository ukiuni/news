---
layout: post
title: How to Train Ultralytics YOLOv8 models on Your Custom Dataset | 196 classes - カスタムデータセットでUltralytics YOLOv8モデルをトレーニングする方法 | 196クラス
  | Image classification
date: 2025-12-27 17:43:06.589000+00:00
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: https://eranfeit.net/yolov8-tutorial-build-a-car-image-classifier/
source_title: 'YOLOv8 Tutorial: Build A Strong Car Classifier'
source_id: 438094718
excerpt: YOLOv8で196クラスの車種分類を高精度学習し、軽量化・エッジ展開まで実践するガイド
---
# How to Train Ultralytics YOLOv8 models on Your Custom Dataset | 196 classes - カスタムデータセットでUltralytics YOLOv8モデルをトレーニングする方法 | 196クラス

## 要約
UltralyticsのYOLOv8を使い、Stanford Carsの196クラスで学習・推論するフルパイプラインの解説。インストールからデータ整備、学習、推論、エッジ向け出力までの実践ノウハウを短時間で把握できる。

## この記事を読むべき理由
日本は自動車産業、検査・流通市場、自治体のスマートシティ化で車種認識の需要が高い。YOLOv8は軽量・高速でエッジ導入しやすく、日本の現場で即戦力になる技術を短期間で試せる。

## 詳細解説
- YOLOv8の位置づけ  
  YOLOv8はYOLOシリーズの再設計版で、検出・セグメンテーション・分類を同一APIで扱える。分類タスク向けには「-cls」系モデルが用意され、バウンディングボックス不要の画像全体分類を効率良く実行できる。

- 主要な技術的特徴（実務観点）  
  - 自動アンカー生成と動的入力サイズ対応により、サイズやアスペクト比のバラつきがある実データに強い。  
  - 事前学習済み重みを活用したファインチューニングで少量データでも収束しやすい。  
  - モデル剪定・量子化やONNX/TensorRT/CoreML出力により、Jetsonやスマホ、サーバーへ容易にデプロイ可能。  

- 学習パイプラインの流れ（要点）  
  1. 環境：PyTorch + CUDA、ultralyticsパッケージ、OpenCVを用意。  
  2. データ構成：train/ val/ の下にクラス毎サブフォルダ（ImageFolder形式）またはdata.yamlでパス指定。Stanford Cars 196のようなクラス多数データで実験。  
  3. モデル準備：軽量モデル(yolov8n-cls)でプロトタイプ→精度が必要なら中～大型へ切替。  
  4. 学習：model.train(...)でエポック・バッチ・画像サイズを調整。学習中は検証精度でベストウェイトを保存。  
  5. 推論：学習済み重みで画像を推論→確率・上位クラスを取り出し、OpenCVでアノテーション表示。  
  6. 最適化：ONNX/TensorRT変換やFP16で推論高速化。  

- 技術的留意点  
  - 196クラスなど多数クラスではクラス不均衡が発生しやすく、重み付けやデータ拡張、クラス別サンプル数の確認が重要。  
  - 入出力サイズ・バッチサイズはGPUメモリに依存。まず小モデル・小バッチで動作確認を行う。  
  - 精度確認は混同行列・Top-K精度で評価。用途に応じてTop-3や確信度閾値運用を検討。

（簡単な実行例）
```bash
# bash
pip install ultralytics opencv-python torch torchvision
```

```python
# python
from ultralytics import YOLO
model = YOLO('yolov8n-cls.pt')          # 事前学習済み分類モデル
model.train(data='data.yaml', epochs=20, imgsz=640)
results = model.predict(source='test.jpg', imgsz=640)
# 結果から確率・クラス名を取り出し、OpenCVで描画する
```

## 実践ポイント
- まずは軽量モデル（yolov8n-cls）で素早くプロトタイプ化、問題なければ上位モデルへスケールアップ。  
- データ不足や偏りがある場合はクラス拡張・画像増強（回転・色調変換等）を適用。  
- 学習ログはTensorBoard等で監視し、早期停止・最良モデル保存を有効化。  
- 推論はONNX→TensorRTやFP16化でJetson/サーバーに最適化。スマホ向けならCoreML/ONNX→TFLiteを検討。  
- 日本固有の車種/モデルに対応するには、国内データ（ナンバープレート非保存での収集、肖像権や個人情報配慮）で追加微調整を行うこと。

