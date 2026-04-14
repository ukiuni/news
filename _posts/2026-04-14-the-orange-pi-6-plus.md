---
layout: post
title: "The Orange Pi 6 Plus - オレンジパイ6プラス"
date: 2026-04-14T21:04:24.303Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://taoofmac.com/space/reviews/2026/04/11/1900"
source_title: "The Orange Pi 6 Plus - Tao of Mac"
source_id: 47732535
excerpt: "Orange Pi 6 PlusをDebianで整備し実用AI端末化する具体手順"
image: "https://taoofmac.com/media/reviews/2026/04/11/1900/gXPeL88wnWdIRTzHXp4uBm8vFnU=/hero.jpg"
---

# The Orange Pi 6 Plus - オレンジパイ6プラス
魅力的な小型ARMボードで「使えるAI端末」にするまでの現実と裏技

## 要約
高性能スペックを詰め込んだOrange Pi 6 Plusはハードは魅力的だが、GPU/NPUや起動周りのソフト面で手を入れないと実用にならない――著者はDebian Trixieベースで自前ビルドして実用域のAI推論環境を構築した。

## この記事を読むべき理由
手頃な価格で「5GbE×2」「16GB RAM」「Mali G720」「専用NPU」を持つSBCは日本のホームラボやエッジAI用途で魅力的。だが現物で動かすにはブート、GPU/NPUユーザースペース、ドライバ周りの知識が必須で、実務で使えるまでの具体的手順と落とし穴を知る価値がある。

## 詳細解説
- 主要スペック（検証機）
  - SoC: CIX P1 (CD8180/CD8160)：4×Cortex‑A520 + 8×Cortex‑A720（Max A720 ≈2.6GHz）
  - GPU: Mali G720（Immortalisクラス）／NPU: 3コア Zhouyi
  - RAM: 16GiB（Linux上は約14GiB見える）
  - ネットワーク: Realtek RTL8126 5GbE ×2、RTL8852BE Wi‑Fi/BT
  - UEFI（Cix 1.3）、カーネルはベンダー系 6.6.89‑cix
- ソフト面の主な課題
  - ベンダー公式イメージは起動やパッケージ信頼性で不安があり、著者はorangepi‑buildをフォークしてDebian 13 (Trixie)ベースの再現可能イメージを作成。
  - 起動系：GRUBのEFI/DTB指定不整合、ルートfsリサイズの失敗→ブートエントリやリサイズスクリプトの修正が必要。
  - GPU：初期はVulkanがllvmpipeにフォールバック。ベンダーのユーザースペース（cix‑gpu‑umd、cix‑libdrm、cix‑mesa、Vulkan ICD(libmali.so)等）を導入し、ドライバをvendor mali_kbaseにバインドして /dev/mali0 を有効化。
  - NPU：カーネルはNPUを検出するが、ユーザースペース／パッケージが断片的で入手性が悪く、手作業で整備が必要。
- 実用性と性能
  - ローカル推論で多数のランタイム／モデルを試行。視覚向けNPUはLLMには最適化されておらず、現実的にはGPU(Vulkan)またはCPUランタイムで運用するケースが多い。
  - 安定運用できた構成例：llama.cpp のVulkanパッチ版 + Qwen3.5 4B Q4_K_Mで生成速度 9 tok/s 程度、RSS 約5.3GB、応答安定性良好。
  - Vulkan周りはメモリ・ディスクリプタセットの制約（マイクロバッチで破綻するケース）があり、-ub（micro‑batch）等のチューニングが重要。
- 運用面の追記
  - NVMeブート移行（SD→NVMe）や /dev/kvm、Docker、Proxmox の導入が可能で、サーバ系ワークロードにも応用できる一方、GPU/NPU周りはベンダー依存が強い。

## 実践ポイント
- 公式イメージに頼らず、自前でDebian (Trixie)ベースの再現可能イメージを作ることを検討する（orangepi‑buildのフォークが有効）。
- 起動前にUEFI/DTB/GRUB設定を確認、rootfsリサイズ処理の動作検証を行う。
- GPUを使うならベンダーのユーザースペース（libdrm/mesa/ICD）を揃え、ドライババインドを固定化する（再起動で元に戻らないようポリシー設定）。
- NPUはパッケージが断片化しているため、対応ランタイムとバイナリの入手性を事前チェックする。
- LLMはまずVulkan対応のllama.cpp系で試し、-ub 等のマイクロバッチ設定で安定性を探る。メモリ使用量に注意してモデルサイズを選ぶ。
- 5GbE×2やNVMeなどハード拡張は魅力的なので、ホームラボでの仮想化・ネットワーク実験機としての採用候補にできるが、導入前にソフト面の労力を見積もること。

短評：ハードは一級品だが「箱から出して即使える」わけではない。少し手をかけられる技術者なら、低消費で安価なエッジAI／ホームラボ機として非常に有望。
