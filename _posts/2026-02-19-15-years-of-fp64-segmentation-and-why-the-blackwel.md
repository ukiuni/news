---
layout: post
title: "15 years of FP64 segmentation, and why the Blackwell Ultra breaks the pattern - 15年にわたるFP64の分断と、Blackwell Ultraがその常識を壊す理由"
date: 2026-02-19T03:50:25.401Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://nicolasdickenmann.com/blog/the-great-fp64-divide.html"
source_title: "Fifteen Years of FP64 Segmentation, and Why the Blackwell Ultra Breaks the Pattern - Nicolas Dickenmann"
source_id: 47068890
excerpt: "Blackwell UltraがFP64を大幅削減、低精度最適化でGPU調達を再定義"
---

# 15 years of FP64 segmentation, and why the Blackwell Ultra breaks the pattern - 15年にわたるFP64の分断と、Blackwell Ultraがその常識を壊す理由
Blackwell Ultraで「倍精度の常識」が崩れる──データセンターGPUはもうFP64で区切られないのか？

## 要約
NVIDIAは15年にわたり消費者向けと企業向けGPUをFP64性能で差別化してきたが、Blackwell Ultra（B300）でFP64比率を劇的に下げ、低精度（FP8/FP4）を前提とする方向へ大きく舵を切った。

## この記事を読むべき理由
日本の研究者・エンジニアは、HPC調達や機械学習のワークフロー設計で「どの精度を使うか」がコストと性能に直結するため、この変化を理解しておく必要がある。

## 詳細解説
- 歴史的経緯：2010年Fermi時点ではハードは$1:2$のFP64:FP32を持ちつつGeForceはドライバで$1:8$に制限。以降、世代ごとに消費者向けのFP64比率は劣化し、Keplerで$1:24$、2014年で$1:32$、Ampere（2020）で$1:64$に。RTX 5090はFP32で約104.8 TFLOPS、FP64は1.64 TFLOPS（$1:64$）。  
- 市場セグメンテーション：NVIDIAはFP64を差別化軸にしてきた（企業向けは$1:2$や$1:3$を維持）。2017年にはGeForceのEULAでデータセンター使用を明確に制限し、契約で境界を設けた。  
- FP64エミュレーションと代替手法：1971年のDekkerのアイデアでは64bitを2つの32bitで表す（$A=a_{hi}+a_{lo}$）。有効仮数は53bit→約48bitへ減るが、スループット面で有利な場合がある。行列積専用のOzaki法は数値を複数の低精度スライスに分割してテンソルコアで高速化し、最終的に復元する：
  $$
  AB=\sum_i A_i B_i
  $$
  cuBLASがOzakiをサポートし始めるなど、低精度テンソルコアを使ったFP64代替が実用化している。  
- Blackwell Ultraの転換点：最新のB300はFP64:FP32比率を$1:64$へ落とし、B200のピークFP64 37 TFLOPS→B300は約1.2 TFLOPSに。つまり「企業GPUがFP64で差をつける」構図が逆転し、低精度資源の拡充が優先されている。

## 実践ポイント
- 精度トレードオフの評価を必ず行う：FP64が本当に必要か、FP32/FP16やエミュレーションで代替可能かを検証する。  
- OzakiやcuBLASの低精度→高精度復元手法を試す：行列演算中心の処理は恩恵を受けやすい。  
- ハード選定と契約に注意：消費者GPUのEULAやクラウドのインスタンスタイプ（企業向けGPUの有無）を確認する。  
- 日本の研究機関・企業は調達戦略を見直す：Blackwell世代はFP64を専有資源にしなくなったため、コスト対性能で新しい選択肢（低精度最適化＋ソフトウェア）を検討する価値が高い。

簡潔に言えば、FP64は「これまでの差別化軸」から「ソフトで補う対象」へ移りつつあり、設計・調達・実装の現場で精度戦略の再評価が必要です。
