---
layout: post
title: "Rolling your own serverless OCR in 40 lines of code - 40行で作るサーバーレスOCR"
date: 2026-02-16T12:53:14.572Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://christopherkrapu.com/blog/2026/ocr-textbooks-modal-deepseek/"
source_title: "Rolling your own serverless OCR in 40 lines of code | Christopher Krapu"
source_id: 46988538
excerpt: "40行でModal＋DeepSeekで数式PDFを数ドルで高速全文OCR化する方法"
---

# Rolling your own serverless OCR in 40 lines of code - 40行で作るサーバーレスOCR
数百ページの数学書を数ドルで全文検索可能にする、たった40行のサーバーレスOCR術

## 要約
DeepSeek の数式対応OCRを Modal（サーバーレスGPU）で動かし、FastAPI＋バッチ推論で大量のPDFページを高速・安価にテキスト化する手法を紹介します。

## この記事を読むべき理由
大学の教科書、研究論文、講義ノートなど「数式あり」の資料は既存OCRで苦戦しがち。低コストでGPUを借りて高品質な数式OCRを自前で回せる実装パターンは、日本の研究者・エンジニア／教育関係者に実用的な価値があります。

## 詳細解説
- 構成の要点
  - Modal：サーバー管理不要でコンテナ＋GPUを短時間課金で使えるプラットフォーム。関数にデコレータを付けるだけでコンテナ構築・GPUプロビジョニング・HTTPルーティングを自動化します。
  - モデル：HuggingFace の DeepSeek-OCR（数式に強い）。このモデルはリポジトリにカスタムコードを含むため `trust_remote_code=True` が必要です。
  - API：FastAPI を Modal の ASGI アプリとしてデプロイし、画像（ページ）をまとめて受けて一括推論（バッチ）で高速化します。
  - 前処理：PyMuPDF で PDF をページ単位にレンダリング。解像度は 2x（fitz.Matrix(2,2)）など高めにして小さい数式も読みやすくします。
  - 推論：入力をパディングして一度に model.generate を呼ぶ。`torch.autocast(..., dtype=torch.bfloat16)` や `model.cuda().to(torch.bfloat16)` でメモリ/速度を改善。`temperature=0.0` で決定的出力に。
  - 出力整形：モデルの座標タグ（grounding tags）を正規表現で削るなどしてマークダウン（.mmd）に保存。

- 小さなコード例（要旨）
```python
# python
image = modal.Image.from_registry("nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04", add_python="3.11") \
    .pip_install("torch==2.6.0","transformers==4.46.3","PyMuPDF","Pillow")

app = modal.App("deepseek-ocr")
@app.function(image=image, gpu="A100")
def process(): pass
```

```python
# python
@app.function(image=image, gpu="A100", timeout=7200)
@modal.asgi_app()
def fastapi_app():
    from fastapi import FastAPI, File, UploadFile
    api = FastAPI()
    # モデルはコンテナ起動時に一度ロードして以降は再利用
```

- 数式の例（モデル出力のイメージ）
  - 本文中の数式は LaTeX 風に抽出されることが多い。例：$p(y\mid\theta)=\theta\exp(-y\theta)$ や
$$p(y|\theta)=\theta\exp(-y\theta),\quad y>0.$$

- 実行感覚とコスト
  - 著者実績：A100 で600ページをバッチ4で約45分、コストは数ドル。日本での同様の利用でも手元GPUが非対応なら有力な選択肢です。

## 日本市場との関連性
- 大学や企業の研究室、教育プラットフォームでは膨大なPDF資産が眠っており、数式対応OCRで検索可能にする価値は高いです。
- 社内ナレッジや講義資料の全文検索、QAエージェントの知識ソース化に直結します。
- 著作権には注意（商用再配布や公開に関しては権利者の許諾を得ること）。まずはパブリックドメインや自前資料で試すのが安全です。

## 実践ポイント
- まずは小さな公開PDFで動作確認→解像度は2xでレンダリングすること。
- バッチサイズを増やすとGPU効率は上がるがメモリ要件も増えるので調整を。
- Modelロードはコンテナ起動時に1回だけ行い、ASGIでリクエスト再利用する設計にする。
- 必須フラグ：HuggingFaceモデルでカスタムコードがある場合は `trust_remote_code=True`。
- 出力の後処理（座標タグの削除、改ページマーク付与）を入れて検索インデックス化すると有効。
- コスト管理：短時間課金のModalは小規模処理〜実験用途に適する。商用運用は見積もりを。

以上を踏まえれば、数式多めの資料でも短時間で高品質にテキスト化し、検索やLLM連携に活用できます。興味があれば、まずは無料枠や小さなGPUで試してみてください。
