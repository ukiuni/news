---
layout: post
title: "How many branches can your CPU predict? - CPUはどれだけの分岐を予測できるか？"
date: 2026-03-20T03:17:06.277Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lemire.me/blog/2026/03/18/how-many-branches-can-your-cpu-predict/"
source_title: "How many branches can your CPU predict? &#8211; Daniel Lemire&#039;s blog"
source_id: 47432779
excerpt: "Zen5は約3万、M4は約1万、Intelは約5千、分岐予測差が性能を左右"
image: "https://lemire.me/blog/wp-content/uploads/2026/03/Capture-decran-le-2026-03-18-a-17.52.22.png"
---

# How many branches can your CPU predict? - CPUはどれだけの分岐を予測できるか？
あなたのCPUは何千個の「if」を覚えられる？最新CPUで分岐予測能力を比べた結果に注目

## 要約
簡単なループベンチマークを使うと、現代CPUの分岐予測器は数千〜数万の分岐パターンを「学習」できることが分かった。AMD Zen 5は約30,000、Apple M4は約10,000、Intel Emerald Rapidsは約5,000という結果が報告されている。

## この記事を読むべき理由
分岐予測は単一コアで「多命令同時実行」を達成する鍵であり、ベンチマークや実運用パフォーマンスの見積もりを大きく左右するため、性能改善や公平な評価のために知っておくべき基礎知識になる。

## 詳細解説
- ベンチマークの要点：著者は乱数を生成してその奇偶で分岐するような単純ループを繰り返し、理論上は50%のミス予測率になるはずの分岐が、同じ乱数列を繰り返すことでCPUに「学習」される様子を観察した。  
- 分岐予測の仕組み（入門レベル）：CPUは過去の分岐履歴を保持して次の分岐を推測する。テーブルや履歴を使ってパターンを記憶するため、同じパターンを繰り返せばミス予測が激減する。  
- 測定結果：同じ手法で3種のプロセッサを比較。AMD Zen 5 ≒ 30,000、Apple M4 ≒ 10,000、Intel Emerald Rapids ≒ 5,000。値は「完璧に予測できる分岐数」の目安で、アーキテクチャごとの予測器容量や設計方針の差を反映している。  
- ベンチマークへの示唆：小さなデータセットや繰り返しパターンの多いテストは分岐予測器に有利で、実運用データでは同じ高速化が得られないことがある。言語（C/C++/Rust等）自体よりも生成される命令列やデータパターンが重要という指摘もある。

## 実践ポイント
- 本番に近いデータでベンチを回す：ランダム性や大規模データで分岐学習の影響を確認する。  
- 分岐を減らす／分岐を予測しやすくする：分岐レス（ビット演算や条件無しの選択）やデータレイアウト改善を検討する。  
- プロファイリングを行う：perf / VTune 等でミス予測率を測定し、ホットパスを最適化する。  
- ターゲットCPUを意識する：モバイル（Apple系）かサーバ（AMD/Intel）かで効率的な最適化方針が変わる。  
- マイクロベンチに注意：小さいテストで得た「高速化」は実アプリで再現されないことがあるため、検証は複数規模で行う。

出典：Daniel Lemire, "How many branches can your CPU predict?", March 18, 2026（ベンチ実装は元記事のソースあり）。
