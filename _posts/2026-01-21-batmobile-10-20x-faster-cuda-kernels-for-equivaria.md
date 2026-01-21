---
layout: post
title: "Batmobile: 10-20x Faster CUDA Kernels for Equivariant Graph Neural Networks - Batmobile：等変グラフニューラルネットワークのCUDAカーネルを10〜20倍高速化"
date: 2026-01-21T12:13:16.958Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://elliotarledge.com/blog/batmobile"
source_title: "Elliot Arledge"
source_id: 46663931
excerpt: "L_max=3特化で等変GNNのCG演算をGPU上10〜20倍高速化し実運用可能に"
---

# Batmobile: 10-20x Faster CUDA Kernels for Equivariant Graph Neural Networks - Batmobile：等変グラフニューラルネットワークのCUDAカーネルを10〜20倍高速化
GPU最適化で分子シミュレーションが現実的に──Batmobileが等変GNNの計算ボトルネックを潰す

## 要約
Batmobileは、等変（equivariant）GNNで重い計算を担う球面調和関数とClebsch–Gordanテンソル積を、L_max=3 に特化した手書きCUDAカーネルで高速化し、重要な演算を10〜20倍速くすることで実運用を現実的にしたプロジェクトです。

## この記事を読むべき理由
等変GNN（MACE、NequIP、Allegroなど）は分子動力学や材料探索で高精度を示す一方で計算コストが高く、日本のバッテリー材料開発や創薬の大規模スクリーニング実務にとっては「精度は良いが遅い」が致命的です。Batmobileはそのギャップを埋め、実問題での採用可能性を大きく高めます。

## 詳細解説
背景（等変GNNの要点）
- 等変GNNは回転・平行移動・反転に対して対称性を保つ表現を扱い、物理現象の学習で高い精度を出す。
- 方向情報の符号化に球面調和関数 ($Y_{l}^{m}$)、特徴を結合する際にClebsch–Gordan（CG）係数によるテンソル積を用いる。

球面調和関数の役割
- 方向ベクトル$(x,y,z)$から回転に対して決まった変換特性を持つ成分を取り出す。
- 例えば $L_{\max}=3$ の場合、各 $l$ の成分数は $1,3,5,7$ で合計 $1+3+5+7=16$。これが1辺方向あたりの表現次元になる。

テンソル積（Clebsch–Gordan）
- 2つの等変特徴を結合しても等変性を壊さないよう、CG係数で重み付けをして和を取る：
$$
\text{out}[l_{\text{out}},m_{\text{out}}]
= \sum_{m_1,m_2} \text{CG}[l_1,m_1,l_2,m_2,l_{\text{out}},m_{\text{out}}] \cdot \text{in1}[l_1,m_1]\cdot \text{in2}[l_2,m_2]
$$
- $L_{\max}=3$ では有効な結合パスが34本ある（元記事の定義）。

なぜ従来実装（e3nn）は遅いのか
- 小さな演算ごとにPyTorchカーネルを多数起動（例えば16成分分の個別カーネル）。カーネル起動オーバーヘッドが大きい。
- 中間結果をグローバルメモリに書いて読み出すためメモリ帯域を浪費。
- 動的な表現（任意のirrep組合せ）に対する一般実装のためコンパイル時最適化が効きにくい。

Batmobileの最適化ポイント
1. コンパイル時定数化  
   - $L_{\max}=3$ の全CG係数・ループ境界をカーネルに埋め込み、分岐やループを展開する。これにより分岐予測やインデックス計算のコストを削減。
2. レジスタのみの中間計算  
   - 球面調和関数の16成分をグローバルメモリに書かず、GPUレジスタで計算→即座にテンソル積に使用。
3. 演算のフュージョン（SH + TensorProduct）  
   - 球面調和の計算とテンソル積を1つのCUDAカーネルに統合し、メモリ移動とカーネル起動を大幅に削減。
4. 逆伝播の最適化  
   - 勾配計算用のバックワードカーネルも手作業で最適化し、学習時にも高速化を維持。

ベンチマーク（RTX 3090, N=1000, 32チャネル, 平均近傍数~20）
- 球面調和 (L=3): e3nn 0.142 ms → Batmobile 0.012 ms （11.8×）
- テンソル積: e3nn 1.847 ms → Batmobile 0.089 ms （20.8×）
- バックワード: e3nn 3.21 ms → Batmobile 0.156 ms （20.6×）
- フュージョン SH+TP: e3nn 0.574 ms → Batmobile 0.413 ms （1.39×）

解釈
- 最大利得はテンソル積（CG結合）で、一般実装の柔軟性を捨てて特化したことで大幅な改善を得ている。
- フュージョンの効果はデータ・モデル設定に依存するが、全体のワークロードでは十分に実用的。

簡単な利用例（PyTorch）
```python
import torch
import batmobile

edge_vectors = torch.randn(1000, 3, device="cuda")
edge_vectors = edge_vectors / edge_vectors.norm(dim=1, keepdim=True)
Y_lm = batmobile.spherical_harmonics(edge_vectors, L_max=3)  # [1000, 16]

node_feats = torch.randn(1000, 32, 16, device="cuda")  # [N, C_in, 16]
weights = torch.randn(34, 32, 64, device="cuda")       # [paths, C_in, C_out]
output = batmobile.tensor_product(node_feats, Y_lm, weights)  # [N, 64, 16]
```

## 実践ポイント
- 即試せる：GitHubレポジトリ（元記事参照）のexamplesにあるMACE風レイヤーで手元のモデルに差し替えてベンチ。まずは推論で効果を確認する。
- プロファイル必須：自分のワークロード（バッチサイズ、近傍数、チャネル数）で速さが出るかを測る。Batmobileは $L_{\max}=3$ に最適化されている点に注意。
- トレードオフを理解：特化実装は高速だが柔軟性は下がる。研究実験でirrepを頻繁に変えるならe3nnの方が便利な場合もある。
- 日本のユースケース：大規模材料スクリーニング、電池材料探索、分子動力学の長期シミュレーションなど、推論/学習における反復回数が多いタスクで特に恩恵が大きい。
- ハード依存性：CUDA対応GPU（例：RTX 3090）で効果を発揮。導入前に使用GPUとドライバの互換性を確認する。

（参考）Batmobileは「特化車両」として汎用性を捨て、実務的な速度を取ったアプローチ。等変GNNを実用に落とし込みたいエンジニアには必読の最適化事例であり、日本の材料・医薬分野のパイプライン高速化に直結する可能性が高い。
