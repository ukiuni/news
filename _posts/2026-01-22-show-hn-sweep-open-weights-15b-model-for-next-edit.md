---
layout: post
title: "Show HN: Sweep, Open-weights 1.5B model for next-edit autocomplete - Sweep、次の編集を予測する1.5Bオープンモデル"
date: 2026-01-22T05:35:27.328Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://huggingface.co/sweepai/sweep-next-edit-1.5B"
source_title: "sweepai/sweep-next-edit-1.5B · Hugging Face"
source_id: 46713106
excerpt: "ノートPCで500ms未満の応答、差分から次編集を予測する1.5Bオープンモデル"
image: "https://cdn-thumbnails.huggingface.co/social-thumbnails/models/sweepai/sweep-next-edit-1.5B.png"
---

# Show HN: Sweep, Open-weights 1.5B model for next-edit autocomplete - Sweep、次の編集を予測する1.5Bオープンモデル
魅力タイトル: ノートPCで瞬時に次の編集を予測するAI — 1.5Bパラメータの「Sweep Next-Edit」

## 要約
Sweep Next-Edit は、ファイルの文脈と差分を元に「次に行う編集」を予測する1.5Bパラメータのオープンモデル（GGUF Q8_0）。ローカルで動き、推論は投機的デコーディングで500ms未満を実現し、同種のベンチマークで4倍以上巨大なモデルを上回る性能を示します。

## この記事を読むべき理由
・コード補完を「入力の補完」から「次の編集を先回りする」体験へ変える可能性があり、日本の企業や開発者がプライバシーを担保しつつ高速な支援を得られる点で有用です。

## 詳細解説
- モデル: Sweep Next-Edit 1.5B（GGUF, Q8_0 quantized）  
- ベース: Qwen2.5-Coder をベースに調整  
- パラメータ: 1.5B、コンテキスト長 8192 トークン  
- サイズ: Q8_0 量子化で約1.54GB（GGUF）  
- 性能: ローカル実行で投機的デコーディングを使えば500ms未満の応答。次編集ベンチで4x以上大きなモデルを上回る報告あり。  
- 使い方（概要）: run_model.py とモデルファイルをダウンロードし、llama-cpp-python と huggingface_hub をインストールして実行。プロンプトは「ファイル全文 + 最近の差分 + 現在の状態」を与えて次の編集を出力する形式。  
- ライセンス: Apache-2.0（商用利用可だが個別条件は確認を）  
- エコシステム: 技術ブログに詳細ベンチマーク、JetBrains 用プラグインあり。現時点でクラウド推論プロバイダによる直接デプロイは限定的。

## 実践ポイント
- すぐ試す手順（ローカル）：  
```bash
# bash
pip install llama-cpp-python huggingface_hub
# モデルファイルと run_model.py をダウンロードしてから
python run_model.py
```
- ハード要件: 8-bit (Q8_0) 量子化でメモリ負担を低減。普通のノートPCでも試せるがCPU/GPU性能で体感速度は変わる。  
- IDE導入: JetBrainsプラグインがあるためまずはIDE連携で試すのが手早い。VSCode なら拡張や簡易スクリプトで同様のワークフローを組める。  
- 運用上の利点: オフライン動作でコードや差分が社外へ流れないため、機密コードを扱う日本企業で導入しやすい。  
- 注意点: プロンプト設計（ファイル＋差分）で精度が大きく変わる。ライセンス条項と企業ポリシーを確認の上、まずは非本番で評価を。

元記事（Hugging Face モデルページ）と公式ブログでベンチマーク／プロンプト例を参照してから導入を検討することを推奨。
