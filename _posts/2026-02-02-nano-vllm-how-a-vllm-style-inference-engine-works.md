---
layout: post
title: "Nano-vLLM: How a vLLM-style inference engine works - Nano-vLLM：vLLM風推論エンジンの仕組み"
date: 2026-02-02T14:02:41.809Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://neutree.ai/blog/nano-vllm-part-1"
source_title: "Understanding LLM Inference Engines: Inside Nano-vLLM (Part 1) - Neutree Blog"
source_id: 46855447
excerpt: "約1200行で読めるvLLM風推論の設計図と最適化で遅延削減とコスト削減の秘訣を解説"
image: "https://neutree.ai/images/og-image.png"
---

# Nano-vLLM: How a vLLM-style inference engine works - Nano-vLLM：vLLM風推論エンジンの仕組み
たった1,200行で読む、LLM推論エンジンの「設計図」—スケジューリング、メモリ管理、GPU最適化の全体像

## 要約
Nano-vLLMは簡潔な実装（約1,200行）でvLLMの核を抽出した推論エンジンの学習用レンズ。プロンプト→トークン→出力までのパイプライン、スケジューラ、KVキャッシュ管理、マルチGPU実行の要点を明快に示す。

## この記事を読むべき理由
LLMを実運用する際の遅延・スループット・コストのトレードオフを理解できれば、日本のプロダクトでのレスポンス改善やクラウド費用削減に直結するため。

## 詳細解説
- トークナイズとシーケンス：プロンプトはモデル固有トークナイザでトークン列（sequence）に変換され、これが処理単位になる。  
- プロデューサー／コンシューマー：add_request がシーケンスを Scheduler に入れ、別ループがバッチを取り出して処理。これにより複数リクエストをまとめてGPUの固定オーバーヘッドを分散する。  
- バッチのトレードオフ：大きいバッチはスループット↑だが個別レイテンシ↑。パラメータで調整が必須。  
- Prefill vs Decode：入力トークンを一括処理する「prefill」と、出力を1トークンずつ出す「decode」を区別してスケジューリング。  
- Scheduler と Block Manager：Waiting/Running キューで実行順を決め、Block Manager は可変長シーケンスを固定長ブロック（デフォルト256トークン）に分割して管理。ブロックごとにハッシュを取り、共通プレフィックスはキャッシュ再利用（参照カウント）することで計算とメモリを削減。制御プレーン（CPU側のメタデータ）とデータプレーン（GPU上のKVデータ）を分離。  
- リソース枯渇時は実行中シーケンスを先頭に戻すプリエンプトで公平に進行。完了でリソース解放。  
- Model Runner と並列実行：モデルが大きい場合は Tensor Parallelism（TP）で複数GPUに分割。リーダー／ワーカーパターンで共有メモリ経由のコマンド伝達を行う（単一マシンの高速化に最適）。  
- CUDA Graphs：decodeの単トークン処理での起動オーバーヘッドを低減するため、よくあるバッチサイズごとにCUDAグラフをキャプチャして再利用。  
- サンプリング（確率分布→トークン）：ロジットを温度で調整してソフトマックスで確率化する。例えば温度$T$を用いると
$$
p_i = \frac{e^{z_i / T}}{\sum_j e^{z_j / T}}
$$
となり、$T\to0$で決定的、$T$大で多様性が増す。

## 実践ポイント
- バッチサイズはスループットとレイテンシのトレードオフを踏まえてチューニングする（運用SLAで決定）。  
- プレフィルとデコードを分けて扱い、prefillは大きめ、decodeは低レイテンシ重視で設定。  
- プレフィックス共有が多いアプリ（チャットbot等）はブロックハッシュによるキャッシュ恩恵が大きい。ブロックサイズ256を起点に調整。  
- KVキャッシュ使用量を監視してプリエンプト/再スケジューリングを設計する（メモリ枯渇時のデグラデーション対策）。  
- マルチGPUサーバではTP検討とCUDAグラフの事前キャプチャでレイテンシを抑える。  
- まずはNano-vLLMのような小さな実装で動作原理を確かめ、本番では同様の原則をスケールアップして導入する。

（続編では attention/KV の物理配置やテンソル並列の計算面を掘り下げる予定）
