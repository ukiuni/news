---
layout: post
title: "Show HN: DeepDream for Video with Temporal Consistency - 動画向けDeepDream（時間的一貫性付き）"
date: 2026-01-08T14:00:58.307Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/jeremicna/deepdream-video-pytorch"
source_title: "GitHub - jeremicna/deepdream-video-pytorch: DeepDream for video with temporal consistency. Features RAFT optical flow estimation and occlusion masking to prevent ghosting. A PyTorch implementation."
source_id: 46540660
excerpt: "RAFT光学フローと遮蔽で残像を消し滑らかなDeepDream動画を作る方法"
image: "https://opengraph.githubassets.com/fc6f9e3397d42faefa78a6077ce13dcae4530b7015096d709d9475d1152f879b/jeremicna/deepdream-video-pytorch"
---

# Show HN: DeepDream for Video with Temporal Consistency - 動画向けDeepDream（時間的一貫性付き）
動く映像に“幻視”をなめらかに重ねる—DeepDream動画化の実践ガイド

## 要約
PyTorch実装のDeepDreamを動画向けに拡張したプロジェクトで、RAFTという光学フローと遮蔽マスクを使ってフレーム間の「ゴースティング（残像）」を抑えながら幻想的な映像を生成します。動画ごとに毎フレーム処理を繰り返す負荷を抑える設計が特徴です。

## この記事を読むべき理由
映像制作やモーショングラフィックス、ジェネラティブアートに興味がある日本のクリエイター／エンジニアにとって、単純にフレームを独立処理するDeepDreamより遥かに安定して使える実装は魅力的です。アニメ・VFXのリファレンス作成や短尺コンテンツ実験にもすぐ応用できます。

## 詳細解説
- 背景（DeepDreamの考え方）
  - DeepDreamはCNNの内部表現を強調して「夢のような」パターンを出す画像処理手法。単一画像では階層的な特徴を強化して独特の模様を生みますが、動画にそのまま適用するとフレーム間でパターンがズレてチラつきます。

- 時間的一貫性の実現方法（このリポジトリの肝）
  - RAFT（高精度光学フロー）で前フレームから現在フレームへのピクセル移動を推定し、前フレームで生成した「ドリーム画像」を現在フレームにワープして初期値とする。
  - 遮蔽（occlusion）マスクを作って、被写体の重なりで前フレーム情報が不正に残る（ゴースト）箇所を検出し、そこだけ新規計算で置き換える。結果、物体追従が滑らかになり残像が減ります。

- 実装と使い方のポイント
  - 必須ライブラリ：PyTorch, torchvision, OpenCV, NumPy, Pillow。モデルは付属スクリプトでダウンロード。
  - 推奨設定：動画処理では -num_iterations を 1 にするのが基本（時間的一貫性により各フレームの繰り返しは不要）。
  - 主要引数（抜粋）
    - -content_video / -output_video：入力・出力ファイル
    - -blend：前フレームワープ結果と生フレームのミックス比（0.0〜1.0）
    - -independent：有効化すると光学フローを使わず各フレーム独立処理（チラつき発生）
    - -update_interval：処理途中の出力更新で進捗確認
    - -temp_dir / -keep_temp：中間ファイルの保存と保持
    - 画像・最適化関連：-image_size, -dream_layers, -octave_scale, -octave_iter, -optimizer（adam/lbfgs）など
  - 性能面と対策
    - 動画処理は重い（フレームごとにDeepDream＋光学フロー）。解像度を下げる、-num_iterations を 1、-octave_iter を小さくすることで実用化可能。
    - GPU設定：-gpu でデバイス指定、-backend cudnn（GPU向け）でメモリ節約。Apple M1/M2系は -gpu mps。
    - マルチGPUもサポート（-gpu 0,1,2,3 等）。

## 実践ポイント
- 今すぐ試す最短手順
  1. リポジトリをクローンして依存をインストール：pip install -r requirements.txt
  2. モデルをダウンロード：python models/download_models.py
  3. 小さめの動画（例：720×→480p）で試す：
```bash
# bash
python video_dream.py -content_video input.mp4 -output_video out.mp4 -num_iterations 1 -image_size 512 -blend 0.5 -dream_layers inception_4d
```
- チューニングのコツ
  - エフェクト強度：blend を上げると元フレーム寄り、下げると幻想が強くなる。まず 0.3〜0.7 の間で試す。
  - 動きの追従が弱ければ RAFT のパラメータや occlusion を確認、-independent との比較で効果を可視化。
  - メモリ不足対策：-image_size を下げる、-octave_iter を 10〜20 にする、GPU backend を cudnn にする。
- 日本の利用シーン例
  - ショート動画のビジュアル実験、アーティストのプリプロダクション、技術系勉強会での視覚化デモ。著作権や肖像権に注意しつつ短尺素材で試すとコスト低く学べる。

このプロジェクトは、映像に馴染む「動くDeepDream」を手軽に試せる入門かつ研究寄りの実装です。まずは小さな動画で挙動を確認してから解像度や反復を上げるのがおすすめ。
