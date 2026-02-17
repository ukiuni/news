---
layout: post
title: "Show HN: Andrej Karpathy's microgpt.py to C99 microgpt.c – 4,600x faster - Andrej Karpathyのmicrogpt.pyをC99に移植したmicrogpt.c — 4,600倍高速化"
date: 2026-02-17T01:54:57.450Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/enjector/microgpt-c"
source_title: "GitHub - enjector/microgpt-c"
source_id: 47042014
excerpt: "microgpt.pyをC99化し組み込みで学習20ms・推論数百倍〜4,600倍高速化"
image: "https://opengraph.githubassets.com/54f72ad913f00181656f24dca4a383b7bf0ae621b87df920f1cd346fed84b27a/enjector/microgpt-c"
---

# Show HN: Andrej Karpathy's microgpt.py to C99 microgpt.c – 4,600x faster - Andrej Karpathyのmicrogpt.pyをC99に移植したmicrogpt.c — 4,600倍高速化
Python不要・組み込み向けに最適化された「極小GPT」をCで動かすと何が起きるか？20msで学習、マイクロ秒で生成する実例。

## 要約
Andrej Karpathyの教育用ミニGPT実装をC99で再実装したmicrogpt-cは、元のPython実装と同等のアルゴリズムを保ちつつネイティブコンパイルとコンパイラ主導のSIMDで実行速度が桁違いに向上（$4,600\times$程度）。モデルは極めて小さく、組み込みや教育に最適。

## この記事を読むべき理由
- 組み込み／エッジ機器でTransformerを動かしたい人：メモリは数十KBで十分。  
- 学習アルゴリズム（Attention・Adam・バックプロパゲーション）をフレームワーク無しで理解したい学生・研究者。  
- 日本語の省リソース推論やプロトタイピングに興味があるエンジニア。

## 詳細解説
- 目的：Karpathyのmicrogpt.pyと同じアーキテクチャ／学習ループ／サンプリングを、依存無しのC99で実装。教育と実験を重視。  
- アーキテクチャ（この実装の主要スペック）  
  - デコーダ単層Transformer（GPT-2準拠）  
  - 埋め込み次元 16、ヘッド数 4、レイヤ数 1、文脈長 16、総パラメータ約 4,600  
  - 重み（fp64）約 37 KB、INT8量子化時約 4.6 KB、推論メモリ < 50 KB、学習メモリ ~144 KB  
- 学習/最適化：Adamオプティマイザ＋線形LRデケイ（設定は microgpt.h で可変）。  
- 性能：同じワークロードで比較するとトレーニングは約 $4,600\times$、推論も数百倍高速化。INT8量子化ビルドは重み収納が約8倍改善。  
- 最適化手法：コンパイラの自動ベクトル化（--simd / CMakeフラグ）でSSE/AVXを利用。手書きSIMD不要。  
- 量子化：各行列ごとのスケールを使うINT8化。前方ではオンザフライでデクォンタイズし、更新はfp64マスターで行って再量子化する方式。

ビルド/実行の例（簡単な単一ファイルビルド）:
```bash
# bash
cc -O2 -o microgpt microgpt_amalgamated.c -lm
cp data/names.txt . && ./microgpt
```

## 実践ポイント
- まずは single-file 実装（microgpt_amalgamated.c）をビルドして挙動を追う。学習ループやAttentionの実装を逐次読めば理解が深まる。  
- SIMD効果を試す：./build.sh --simd で違いを計測。大きめモデルで効果が顕著。  
- 組み込み用途は INT8 ビルドを検討：ストレージとメモリを節約できる。  
- 日本語で試す場合：この実装は文字レベル（UTF-8扱いに注意）なので、漢字・かな混在データを扱うならトークナイザやエンコーディングの前処理を工夫すること。  
- 教育用途：微小モデルなのでAttentionやAdamの数値挙動を実機で観察しやすい。カスタム最適化や量子化実験のベースとして最適。

リポジトリ：https://github.com/enjector/microgpt-c（ソースとビルドスクリプトあり、MITライセンス）
