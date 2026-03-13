---
layout: post
title: "Can I run AI locally? - ローカルでAIは走るか？"
date: 2026-03-13T16:57:35.653Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.canirun.ai/"
source_title: "CanIRun.ai — Can your machine run AI models?"
source_id: 47363754
excerpt: "あなたのPCで動くAIモデルをVRAMや量子化で即判定、最適候補を提示する実用ガイド"
image: "https://canirun.ai/og/home.png"
---

# Can I run AI locally? - ローカルでAIは走るか？
ローカルで本当に動くモデルだけを厳選！あなたのPCで動くか瞬時に分かるAIモデル判定ガイド

## 要約
CanIRun.ai は各モデルの実メモリ要件・コンテキスト長・量子化フォーマットなどを集約し、「あなたのマシンで動くか」をS〜Fで判定するウェブツール。小型モデルから巨大MoEまで、実運用に即した目安を提供する。

## この記事を読むべき理由
日本でも「データを外に出せない」「オンプレで試したい」「スマホや組み込みでAIを動かしたい」というニーズが増加中。どのモデルを選べば手元のGPU/CPUで動かせるかを短時間で判断できる実務的な情報だから。

## 詳細解説
- 判定の肝：VRAM/メモリ要件、コンテキスト長、量子化（Q2_K/Q3_K_M/Q4_K_Mなど）、アーキテクチャ（Dense vs MoE）を組み合わせて「実行可能性」を評価。ブラウザ側はWebGPU推定も提示し、実機と多少差が出る可能性を明記している。  
- モデル例と目安：1Bクラスは0.5GB前後で「エッジ／組み込み向け」、3–8Bは1–4GBでモバイルや軽いデスクトップ、8–14Bは4–12GBで高性能ノートや中級GPU、70B以上は30GB〜200GBと大規模GPU／サーバ前提。  
- MoE（Mixture of Experts）：全体パラメータ数は巨大でも「active params（動作時に実際使われる分）」が小さいケースがあり、実メモリはそこに依存するため一見して判断できない点に注目。  
- 量子化の実利：4-bit/8-bit量子化や専用フォーマットでVRAMを大幅削減でき、例えば8Bモデルを4–8GB帯で動かすことが現実的。ツールとしては llama.cpp、Ollama、LM Studio をデータソース／実行環境として活用している。  
- コンテキスト長：128Kや256Kといった長い文脈をサポートするモデルはメモリ上の追加コストが大きい。チャット履歴や長文処理の用途に応じて選ぶこと。

## 実践ポイント
- まずGPUのVRAMを確認（ノートは一般的に4–12GB）。canirun.aiで候補モデルの「Memory」欄と量子化オプションを比較する。  
- ノートPCやローカル開発なら：Mistral 7B、Llama/Gemma/Qwen の3–8Bクラスから試す。  
- モバイル/組み込み：0.5–1.5GBのTinyモデル（Qwen 0.8B / Llama 1B / Gemma 1B 等）を検討。  
- 大規模用途でコスト圧縮するならMoEの「active params」を確認し、量子化を併用する。  
- 実行はまず llama.cpp / LM Studio / Ollama でプロトタイプ。ブラウザでの推定はWebGPUベースなので差分を考慮して実機で必ずベンチ。  
- セキュリティ/法務：日本国内の企業データを扱う場合はオンプレでのローカル実行がリーガル/プライバシー面で優位。

短時間で「自分の環境で何が動くか」を確かめたいとき、canirun.aiは実用的なショートカットになる。
