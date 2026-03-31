---
layout: post
title: "Ollama is now powered by MLX on Apple Silicon in preview - OllamaがApple SiliconでMLX対応（プレビュー）"
date: 2026-03-31T04:56:15.435Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://ollama.com/blog/mlx"
source_title: "Ollama is now powered by MLX on Apple Silicon in preview · Ollama Blog"
source_id: 47582482
excerpt: "OllamaがMLXでApple Siliconを活用、Mac上で大幅にLLM推論が高速化"
image: "https://ollama.com/public/og.png"
---

# Ollama is now powered by MLX on Apple Silicon in preview - OllamaがApple SiliconでMLX対応（プレビュー）
MacでLLMが爆速化！OllamaがAppleのMLXでApple Siliconをフル活用するプレビュー版

## 要約
OllamaがAppleの機械学習フレームワーク「MLX」を使ってApple Silicon上で大幅に高速化されるプレビューを公開。M5系チップのGPU Neural Acceleratorを活用し、トークン生成速度や初動応答が大きく改善されています。

## この記事を読むべき理由
MacでローカルにLLMを動かす開発者やプロダクト担当者にとって、低遅延・高性能なローカル推論が現実的になり、コスト・プライバシー面での利点が得られるからです。日本でもMacを使う開発者は多く、実用性が一気に高まります。

## 詳細解説
- MLXとApple Silicon: Ollama 0.19はAppleのMLX上で動作し、Unified Memoryの利点を生かしてメモリ帯域と処理を最適化。特にM5 / M5 Pro / M5 MaxでGPU Neural Acceleratorを利用し、TTFT（time to first token）やトークン毎の生成速度が向上します。  
- ベンチマーク（抜粋）: AlibabaのQwen3.5-35B-A3B（NVFP4量子化）でテストした結果、prefillは約1810 tokens/s（Ollama 0.19）対1154（0.18）、decodeは112 tokens/s対58 tokens/sと大幅改善。さらにint4動作時は0.19で1851 tokens/s（prefill）、134 tokens/s（decode）を想定。  
- NVFP4対応: NVIDIAのNVFP4量子化をサポートし、メモリ使用を抑えつつ推論品質を維持。クラウドやプロダクションでの結果とローカルでの出力が揃いやすくなる点が利点です。  
- キャッシュ改良: 会話間でキャッシュを再利用することでメモリ使用を削減、プロンプト内の「インテリジェントなチェックポイント」保存で再処理を削減、共有プレフィックスの生存時間を延ばす賢い削除ポリシーを導入し、コーディングやエージェントタスクで応答性向上。

必要条件や注意点:
- 現時点ではプレビューで、32GB以上のUnified Memoryを持つMacを推奨。
- 将来的に他のモデルやアーキテクチャのサポートや、カスタムモデルの導入が予定されています。

コマンド例（参考）
```bash
# Claude Code を起動
ollama launch claude --model qwen3.5:35b-a3b-coding-nvfp4

# OpenClaw を起動
ollama launch openclaw --model qwen3.5:35b-a3b-coding-nvfp4

# モデルとチャット
ollama run qwen3.5:35b-a3b-coding-nvfp4
```

## 実践ポイント
- Macが32GB以上のUnified Memoryか確認してOllama 0.19を試す。  
- Qwen3.5-35B-A3B（NVFP4）でコーディングタスクの応答性をベンチマークして比較する。  
- ローカルでの「NVFP4」出力がクラウドの結果と整合するか確認し、本番移行の検討材料にする。  
- キャッシュの動作（会話ブランチでの応答速度）を試し、共有プロンプト運用での効果を評価する。  
- 今後のモデル対応やカスタムモデル導入情報をウォッチする。
