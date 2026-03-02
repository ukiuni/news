---
layout: post
title: "Show HN: Timber – Ollama for classical ML models, 336x faster than Python - Timber：古典的MLモデル向けOllama（Pythonより336倍高速）"
date: 2026-03-02T03:33:10.144Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/kossisoroyce/timber"
source_title: "GitHub - kossisoroyce/timber: Ollama for classical ML models. AOT compiler that turns XGBoost, LightGBM, scikit-learn, CatBoost &amp; ONNX models into native C99 inference code. One command to load, one command to serve. 336x faster than Python inference."
source_id: 47212576
excerpt: "Timberは決定木モデルをC99にAOT変換しPython不要で最大336倍高速化"
image: "https://opengraph.githubassets.com/378839768c8e2f798b271d58b838e6b05a60de4858bd6a0eb9fdd8e9d68bcdb9/kossisoroyce/timber"
---

# Show HN: Timber – Ollama for classical ML models, 336x faster than Python - Timber：古典的MLモデル向けOllama（Pythonより336倍高速）
Pythonを捨ててネイティブCにコンパイルするだけで、決定木系モデルの推論が劇的に速くなる――Timberが示す「実運用で効く」高速化

## 要約
TimberはXGBoost/LightGBM/scikit-learn/CatBoost/ONNXの学習済みモデルをAOTでC99ネイティブコードに変換し、Pythonランタイムなしでマイクロ秒単位の推論を実現するツールです。ワンコマンドでロード・サーブでき、ベンチマークではPython XGBoost単発推論比で最大336×を報告しています。

## この記事を読むべき理由
低レイテンシや小さなデプロイ体積が求められる金融決済、組み込み機器、エッジ推論や規制産業（医療・自動車）に携わるエンジニアにとって、Python依存を排して「決定木系モデルを小さく速く運用する」現実的な選択肢が得られるため。

## 詳細解説
- アーキテクチャ
  - Timberはモデルを解析してC99の推論コードを生成（AOTコンパイル）し、生成物はPythonランタイムを必要としません。結果としてプロセスサイズは小さく、レイテンシはネイティブ呼び出しで数マイクロ秒クラスを狙えます（例： ~2 µs）。
- 対応フォーマット
  - XGBoost（JSON）、LightGBM（text/.model）、scikit-learn（pickle）、CatBoost（JSON）、ONNX（TreeEnsemble opset）をサポート。scikit-learnは主要なツリー系推定器とパイプラインに対応します。
- サーブ体験
  - Ollama風のワークフローで、モデルをロードしてローカルHTTP APIで提供。主なエンドポイント：/api/predict、/api/models、/api/health。
- ベンチマーク概要
  - ベンチはApple M2 Pro、XGBoost（50木、深さ4、30特徴）で実施。ウォームアップ後の単一サンプル推論を計測し、Python XGBoostのin-process予測と比較して336×を報告（詳細は再現可能なスクリプトあり）。
- 制約と注意点
  - ONNXは現状ツリー系演算子にフォーカス。CatBoostはJSONエクスポート推奨。pickleの読み込みは信頼できるアーティファクトのみで利用すること（セキュリティリスク）。XGBoostはJSONモデルが主経路。

## 実践ポイント
- 試す（ローカルでワンライナー）
```bash
# インストール
pip install timber-compiler

# モデルをロード（例: model.json を自動検出して読み込む）
timber load model.json --name fraud-detector

# サーブして単一予測（Ollama風API）
timber serve fraud-detector
curl http://localhost:11434/api/predict -d '{"model":"fraud-detector","inputs":[[1.0,2.0,3.0]]}'
```
- 日本市場での活用ヒント
  - 決済・不正検知のリアルタイム判定、車載や産業IoTのゲートウェイにおける低レイテンシ推論、監査性が求められる金融/医療分野での「可搬なバイナリ」化に有効。ARM/RISC-V対応強化がロードマップにあるため組込み領域への適用性は今後さらに高まります。
- 導入上の注意
  - Pickle等の非信頼モデルは読み込まない、ONNXやCatBoostのエクスポート形式を確認する、ベンチマークは実運用環境で再現して比較する。

以上を踏まえ、低レイテンシ・小容量・監査可能な推論アーティファクトが必要なプロジェクトでは、Timberは検討候補になります。READMEとexamplesに実行可能なサンプルがあるので、まずは手元で簡単なモデルをコンパイルして挙動を確かめてみてください。
