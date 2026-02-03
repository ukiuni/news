---
layout: post
title: "A browser benchmark that actually uses all your CPU/GPU cores - ブラウザベンチマークで本当に全CPU/GPUコアを使うもの"
date: 2026-02-03T08:47:47.465Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://speedpower.run/?ref=reddit-programming-1"
source_title: "SpeedPower.run | The Modern Web & AI Benchmark"
source_id: 410458968
excerpt: "60秒でCPU/GPU全コア動員、400MB消費の実機向けブラウザベンチ"
image: "https://cdn.prod.website-files.com/66548e1dd5423c792829c467/694961916426235dfdd931a3_Copy%20of%20Webflow%20Thumbnails.png"
---

# A browser benchmark that actually uses all your CPU/GPU cores - ブラウザベンチマークで本当に全CPU/GPUコアを使うもの
ブラウザで“全コア”を動員する新ベンチマーク、SpeedPower.run――あなたの端末の本当の実力を60秒で暴く

## 要約
SpeedPower.run はブラウザ上でCPUとGPUの全コアを積極的に使って性能を計測するベンチマークで、実行に約60秒、実データで約400MBをダウンロードするBETA研究プロジェクト（ScaleDynamics）。

## この記事を読むべき理由
現実的な負荷を再現するベンチマークは、Webアプリやブラウザ上でのAI推論の最適化に直結する。特に日本ではモバイル利用やデータ制限、端末の多様性があるため、実機での実測が重要になる。

## 詳細解説
- 動作時間とデータ量：実行は概ね60秒だが回線品質や端末性能で前後する。実行中に約400MBをダウンロードするためモバイル回線では注意が必要。  
- コア活用の仕組み：ブラウザ上で複数スレッド（Web Workers）や低レイヤ（WASM／WebGL／WebGPU）の描画・計算を併用し、CPUとGPUを同時に動かす設計と推定される。これにより単一スレッド指標では見えないボトルネックを露出できる。  
- 測定上の注意点：ブラウザのタスクスケジューラ、OSの省電力・サーマルスロットリング、モバイルのCPU制限やバックグラウンド制御によりスコアが変動する。SharedArrayBufferなどの機能はクロスオリジン隔離を要求する場合がある。  
- 用途：モダンWebやブラウザAI（WebInference）を想定した総合負荷試験として有用。既存のSpeedometer／JetStream／MotionMarkとは補完関係にある。

## 日本市場との関連
- モバイル中心の利用実態やデータ通信のコスト意識が強い日本では、400MBのダウンロードは実行前に確認が必要。  
- 多くの企業が社内ネットワークや端末管理でブラウザ挙動を制限しているため、社内検証や導入判断に有用。  
- 高性能デバイス普及地域（最新iPhone、Androidフラッグシップ、デスクトップPC）では、実装の最適化点が明確になりやすい。

## 実践ポイント
- 実行前にWi‑Fi／有線で接続し、モバイル回線での実行は避ける（400MB）。  
- 最新のChrome/Edgeを使い、可能ならWebGPUやWASMサポートを有効化してから複数回実行して中央値を取る。  
- 比較目的で最適化前後や別ブラウザ／別端末で計測し、CPU負荷・温度・バッテリー挙動も観察する。  
- 企業環境での実行はネットワーク/ポリシー確認を行う（BETAかつ研究プロジェクトのため）。
