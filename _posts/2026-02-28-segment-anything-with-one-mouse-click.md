---
layout: post
title: "Segment Anything with One mouse click - ワンクリックで何でもセグメントする"
date: 2026-02-28T20:12:16.811Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://eranfeit.net/one-click-segment-anything-in-python-sam-vit-h/"
source_title: "Segment Anything In Python - One-Click Segmentation"
source_id: 394134954
excerpt: "SAM ViT‑Hでワンクリックから高精度な候補マスク3つを即生成、ECや検査で即戦力"
image: "https://eranfeit.net/wp-content/uploads/2025/11/Segment-Anything-with-One-mouse-click.png"
---

# Segment Anything with One mouse click - ワンクリックで何でもセグメントする
ワンクリックで対象を切り出す――SAM ViT‑Hで始める超高速セグメンテーション入門

## 要約
単一のマウスクリックで高品質な候補マスクを最大3つ返す、MetaのSegment Anything (SAM) ViT‑H を使った「ワンクリック」ワークフローを、環境構築からクリック取得、推論、マスク保存まで実用コード付きで解説します。

## この記事を読むべき理由
日本のプロダクト写真加工、製造検査、アノテーション作業やプロトタイピングで「素早く」「手間なく」対象を切り出せる手法は即戦力です。少ないラベルで効率的にデータを作れるため、コストや時間を抑えたい開発現場に特に役立ちます。

## 詳細解説
- 仕組み：ViT‑H が画像特徴を一度抽出し、クリック（正例）を軽量なプロンプトエンコーダが解釈、マスクデコーダが複数候補を返す。これにより単一点で複数の高品質マスクを生成でき、見た目とスコアで最適なマスクを選べる。
- ワークフロー：
  1. Python 3.9 の分離環境を作り、PyTorch（CUDA任意）、opencv-python、matplotlib、segment‑anything を導入。
  2. OpenCVのウィンドウで1点クリックを取得（左クリック→'q'で確定）。クリック座標がSAMの唯一の必須入力。
  3. SAM ViT‑Hのチェックポイントを読み込み、可能ならGPU/MPSへ転送。SamPredictorに画像をセットして特徴を固定化。
  4. point_coords と point_labels（正例=1）を渡し、multimask_output=True で最大3つのマスクとスコアを取得。可視化・PNG出力も可能。
- 実用上のコツ：
  - model_type はチェックポイント名（例：vit_h）と一致させる。
  - GUIのimshowが開かない場合は headless版ではなく opencv-python（GUIビルド）を使う。
  - 背景抑制には負例クリック（label=0）を混ぜると効果的。
  - GPU/MPSが無くても動くが遅い。Apple SiliconユーザーはMPSを活用すると良い。
- 応用例：ECの背景除去、部品の外観検査、手早いアノテーションブートストラップ、YOLO等の検出結果から自動マスク生成へ組み合わせる運用。

## 実践ポイント
- 最小導入コマンド（環境例）
```bash
# bash
conda create -n sam-tutorial python=3.9 -y
conda activate sam-tutorial
# PyTorchは環境に合わせて選ぶ（ここは例）
conda install pytorch==2.2.2 torchvision==0.17.2 pytorch-cuda=11.8 -c pytorch -c nvidia -y
pip install opencv-python matplotlib
pip install git+https://github.com/facebookresearch/segment-anything.git
# headless問題でGUIが必要なら：
pip uninstall -y opencv-python-headless && pip install opencv-python
```
- まずは手持ちの1枚写真で試し、マスク候補（3つ）のスコアと見た目で最良を選ぶ習慣をつける。
- 日本語案件での実運用：製品写真や検査画像なら負例クリック／ボックスで精度向上、バッチ処理で大量画像の半自動ラベリングに活用するのが効率的。

この流れを一度動かせば、画像セグメンテーションの試作とデータ作成が格段に速くなります。必要ならコード例や日本向け導入注意点（権利や個人情報）も続けて書けます。
