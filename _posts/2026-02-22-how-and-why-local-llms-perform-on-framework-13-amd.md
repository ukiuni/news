---
layout: post
title: "How and Why Local LLMs Perform On Framework 13 AMD Strix Point - Framework 13（AMD Strix Point）でのローカルLLM性能の理由と実測"
date: 2026-02-22T04:03:09.606Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://msf.github.io/blogpost/local-llm-performance-framework13.html"
source_title: "This is how SLOW Local LLMs Are On My Framework 13 AMD Strix Point | Miguel Filipe"
source_id: 1404591315
excerpt: "Framework 13でメモリ帯域が瓶頸だが、下書きモデルで処理速度が最大82%改善"
---

# How and Why Local LLMs Perform On Framework 13 AMD Strix Point - Framework 13（AMD Strix Point）でのローカルLLM性能の理由と実測  
驚くほど速く—or 遅く見える原因は「メモリ帯域」と「小さな下書きモデル」にありました

## 要約
Framework 13（Ryzen AI 9 HX 370、Radeon 890M、DDR5‑5600 128bit）でのローカルLLMは、推論速度の大部分がメモリ帯域に制約される一方、低コストの「speculative decoding（下書きモデル＋検証）」で対策でき、実測でトークン生成速度が+40～+82%向上する。

## この記事を読むべき理由
日本でもノートPCでローカルLLMを回すニーズが増えています。どの設定やソフトスタックで体感速度が変わるか（AC/バッテリ、Vulkan/ROCm/CPU、メモリのアップグレード可否など）を実測に基づき分かりやすく整理しました。実践可能なチューニング案も載せます。

## 詳細解説
- ハードウェア要点  
  - Framework 13: Ryzen AI 9 HX 370（12c/24t）、Radeon 890M（RDNA 3.5, 16 CUs 相当）、64GB DDR5（SO‑DIMM, 最大96GB）。  
  - メモリ帯域が支配的：DDR5‑5600、128bit バスの理論最大帯域は
  $$
  5600 \times 128 / 8 = 89.6\ \mathrm{GB/s}
  $$
  で、ここが「上限（壁）」。

- ソフトスタック比較（同じ物理RAMを使うが経路が違う）  
  - Vulkan (RADV)：グラフィックスAPIを計算向けに使用。インタラクティブなテキスト生成（tg）で優勢。セットアップ容易。  
  - ROCm/HIP：AMDのCUDA相当。プロンプト処理（pp）で有利だが、tgはVulkanより遅い。大きな文脈処理／RAGで効果的。mmapはモデル読み込みでROCmで問題となることあり。  
  - CPU：Infinity Fabric経由で実メモリ帯域がGPU経路より狭く、tgは大幅に遅い。

- 実測サマリ（抜粋、単位: tokens/sec）  
  - Qwen3‑8B (Q4_K_M, 4.68 GiB) on Vulkan: power‑saver tg ≈ 9.87、performance tg ≈ 13.41。pp（プロンプト処理）は power‑saver 146 → performance 322 t/s（大幅改善）。  
  - ROCmはppで有利（例: pp 207 vs Vulkan 146）が、tgではVulkanが2×高速（例: 9.87 vs 4.76）。  
  - MoEモデルは「全重みを読む必要がない」ため、モデル容量以上のtg性能を示すことがある。

- 帯域から見た上限  
  - 理想的100%帯域利用時の理論tg上限は約 17.8 t/s、現実的な優秀ドライバで85%なら約 15.2 t/s。実測13.4 t/s（性能プロファイル）で既に約75%利用。

- 特筆: Speculative decoding（下書きモデル＋検証）  
  - 小さなドラフトモデル（例: Qwen3‑0.6B）で候補を素早く生成し、大モデルで一括検証する手法。検証はpp寄りの処理で、ppがtgより圧倒的に速い本機では非常に効果的。  
  - 実測: Qwen3‑8B 単体 12.9 t/s → ドラフト0.6B（draft‑max=16）で 22.9 t/s（+78%）。タスクによる変動あり（+40～+82%）。  
  - ハードを変えずに「ほぼソフトだけ」で体感速度を大幅改善できる重要手段。

- 電源プロファイルの影響  
  - performanceモードでメモリコントローラやGPUクロックが上がりtg+36%、pp+120%の改善。だがベンチのばらつき（ジッター）も増えるため、測定はモードを明記すること。

## 実践ポイント
- ハード確認（まず自分の帯域を見る）
```bash
# RAM幅確認
dmesg | grep "RAM width"
# GPU info
cat /sys/class/drm/card1/device/pp_dpm_mclk
cat /sys/class/kfd/kfd/topology/nodes/1/properties | grep -E 'gfx_target|simd'
# power profile
powerprofilesctl get
```
- 代表ベンチ（llama.cpp系）
```bash
# Vulkan tg-only
llama-bench -m model.gguf -ngl 99 -fa 1 -p 0 -n 256
# 全体ベンチ
llama-bench -m model.gguf -ngl 99 -fa 1 -p 512 -n 128
```
- Speculative decoding 試し方（劇的改善が期待できる）
```bash
llama-cli -hf Qwen/Qwen3-8B-GGUF:Q4_K_M \
  -hfrd Qwen/Qwen3-0.6B-GGUF:Q8_0 \
  --draft-max 16 -ngl 99 -ngld 99 -fa 1
```
- チューニングの優先順位（効果が大きい順）  
  1. Speculative decoding（小さなドラフトモデルを用意）  
  2. ACに接続して performance プロファイルで計測・運用（ただし熱対策）  
  3. Vulkanをtg用、ROCmを長文／RAG用に使い分ける  
  4. SO‑DIMMで可能ならDDR5‑6400へ換装（約+14%帯域）やメモリ増設（大モデル対応）  
  5. ドライバ/シェーダの改善は数%〜十数%の余地

まとめ：Framework 13のようなAMD APUで「遅い」と感じる根本はメモリ帯域。だが「下書きモデル＋検証」を使えば、ハードそのままで体感が大きく変わる。まずは自分のRAM幅を確認し、speculative decoding を試してみてください。
