---
layout: post
title: "I have written gemma3 inference in pure C - Gemma3推論を純粋Cで実装した"
date: 2026-01-28T20:09:25.556Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/robitec97/gemma3.c"
source_title: "GitHub - robitec97/gemma3.c: Gemma 3 pure inference in C"
source_id: 46765772
excerpt: "Python/GPU不要の純C実装でGemma 3（4B）をCPUで高速推論"
image: "https://opengraph.githubassets.com/5b0f6b98eed18244eb2f86f5b9062e0235207f52486ecc468055b5d730e416ef/robitec97/gemma3.c"
---

# I have written gemma3 inference in pure C - Gemma3推論を純粋Cで実装した
Gemma 3をPython/GPU無しで走らせる――「純C」だけで動く4B級LLMエンジンの全貌

## 要約
C11だけで書かれたGemma 3（4B IT）のCPU推論エンジン。PyTorchやGPUに依存せず、Memory‑mappedなBF16 SafeTensors、ネイティブTokenizer、ストリーミング出力など実用的な機能を持つ。

## この記事を読むべき理由
日本でもローカル実行や組み込み環境でのLLM利活用が注目される中、Python/GPU非依存で動く純C実装は運用コスト低減や組込み適用の可能性を開くから。

## 詳細解説
- コード基盤：100% C (C11)、外部依存ゼロ。ライブラリ＋CLIで利用可能。POSIX優先（Linux/macOSネイティブ）、WindowsはWSL/MingWで対応。
- モデル対応：Gemma 3 4B IT アーキテクチャ完全対応（GQA、ハイブリッド注意機構、SwiGLU）。語彙262,208、レイヤ34、隠れ2560、コンテキスト最大128K。
- 重みとIO：BF16のSafeTensorsをmmapでメモリマップして効率的に読み込み（ディスク約8GB、ランタイム総RAM約3GB程度。設定で下げ可能）。
- トークナイザー：ネイティブSentencePiece実装で外部ツール不要。
- 推論機能：トークン単位のストリーミング出力、対話モード、システム/温度/Top‑k/Top‑p等のデコーダ制御。
- 実行性能（CPU）：プレフィル約2–5 tok/s、生成1–3 tok/s。最適化ビルド（make fast）推奨。
- 開発・配布：MITライセンス（モデル重みはGemmaのライセンス）。ダウンロード用Pythonスクリプト付属（HuggingFaceトークン対応、途中再開・検証機能）。

ライブラリ使用例（簡易）:
```c
// c
gemma3_ctx *ctx = gemma3_load_dir("./gemma-3-4b-it");
gemma3_gen_params params = gemma3_default_params();
char *out = gemma3_generate(ctx, "Hello!", &params, NULL, NULL);
printf("%s\n", out);
free(out);
gemma3_free(ctx);
```

## 実践ポイント
- まずは model を取得：export HF_TOKEN=your_token && python download_model.py
- ビルド：make（デバッグは make debug、最速は make fast）
- 実行例：./gemma3 -m ./gemma-3-4b-it -p "Explain quantum computing simply."
- メモリ節約：-c 512 等でコンテキスト短縮、ランタイムRAMを削減
- Windows利用はWSL推奨（mmapが効くため）
- 制限：CPU専用・量子化未対応。実運用前に速度と容量要件を確認すること

以上を踏まえ、ローカルで低レイヤーからLLMを動かしたい開発者や、組み込み／オンプレ環境での実装を検討するエンジニアに特に価値があるプロジェクト。興味があればリポジトリをチェックしてビルド→実行してみると良い。
