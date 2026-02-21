---
layout: post
title: "Show HN: Llama 3.1 70B on a single RTX 3090 via NVMe-to-GPU bypassing the CPU - 単一RTX 3090でNVMe→GPUダイレクトによりLlama 3.1 70Bを動かす"
date: 2026-02-21T23:36:31.642Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/xaskasdf/ntransformer"
source_title: "GitHub - xaskasdf/ntransformer: High-efficiency LLM inference engine in C++/CUDA. Run Llama 70B on RTX 3090."
source_id: 47104667
excerpt: "RTX3090でNVMe直結＋3層キャッシュによりLlama3.1 70Bを動かす実験的手法を公開"
image: "https://opengraph.githubassets.com/626ccc3a830d811e0fced0531a461e60dfdfdcb7a2a32e20c0b22bc958723fd9/xaskasdf/ntransformer"
---

# Show HN: Llama 3.1 70B on a single RTX 3090 via NVMe-to-GPU bypassing the CPU - 単一RTX 3090でNVMe→GPUダイレクトによりLlama 3.1 70Bを動かす
24GBで「70B」を回す――NVMe直結＆3層キャッシュでCPUを経由せずモデルをストリーミングする話

## 要約
NVMe上のGGUFモデルをGPU側に直接DMAし、VRAM不足を3層（VRAM / ピン留めRAM / NVMe）で自動管理するC++/CUDA推論エンジン。RTX 3090（24GB）でLlama 3.1 70Bを動かす実験的実装を公開している。

## この記事を読むべき理由
日本でも個人・研究室レベルで大規模モデルをオンプレで試したい需要が増えている中、クラウド依存を減らしコストやデータ漏洩リスクを下げる現実的な手法を示しているため。

## 詳細解説
- コアアイデア：モデル重みをNVMe→（ユーザ空間NVMeドライバ）→ピン留めCUDAメモリ→PCIe H2DでGPUへ送るパスを作り、CPUコピーを極力排する。これにより大きなレイヤーを順次ストリーミングしてGPUで計算可能にする。  
- 3-Tier Adaptive Caching：  
  - Tier A（VRAM常駐）：頻繁に使う上位レイヤーをVRAMに置きI/Oゼロに。  
  - Tier B（ピン留めRAM）：H2D DMAで非同期転送、ダブルバッファで転送と計算を重ねる。  
  - Tier C（NVMe/mmap）：NVMeからピン留めステージへ読み出し→H2D。  
- SLEPストリーミング：二重バッファでNVMe読み・PCIe DMA・GPU計算を重ね、スループットを最大化。  
- gpu-nvme-direct：VFIOでNVMeデバイスをユーザ空間にバインドし、直接CUDAピンメモリへDMAを発行する実験的バックエンド。  
- 性能目安：70B Q6_Kでmmapベースから約33倍高速化。ボトルネックはPCIe H2D帯域（Gen3 x8で約6.5GB/s）。Gen4 x16なら更に改善し得る（著者推定で ~0.5 tok/s 程度）。  
- サポート：GGUFフォーマット（Q4/ Q6/ Q8 / F16 / F32 等）、カスタムCUDAカーネル（GEMV, RoPE, SwiGLU 等）。  
- 要件：Linux（Ubuntuで検証, kernel 6.17+）、CUDA Toolkit 13.1、gcc/g++-14、NVIDIA Compute Capability 8.0+（RTX 3090 動作確認）、CMake 3.24+。

## 実践ポイント
- リスクと前提：NVMeをVFIOへバインドする操作はroot権限が必要で、デバイスの内容を生書きする（ddでraw書込）ためバックアップ・注意必須。作業は予備機・テストSSDで行う。  
- まずは小モデルで検証：8BなどVRAMに乗るモデルでビルドと動作確認を行い、その後70Bのストリーミングへ移行する。  
- 必要コマンド（短縮）：

```bash
# build (例)
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_C_COMPILER=gcc-14 \
  -DCMAKE_CXX_COMPILER=g++-14 \
  -DCMAKE_CUDA_COMPILER=/usr/local/cuda-13.1/bin/nvcc
cmake --build . -j
```

```bash
# 実行例（ストリーミングモード）
./ntransformer -m /path/to/llama-70b-q6_k.gguf -p " Hello " -n 32 --streaming
```

```bash
# NVMe直結を試す時の流れ（要root）
sudo dd if=model.gguf of=/dev/nvme0n1 bs=1M oflag=direct status=progress
sudo ./scripts/setup_nvme.sh   # VFIOバインドなど
sudo GPUNVME_PCI_BDF=0000:01:00.0 GPUNVME_GGUF_LBA=0 \
  ./build/ntransformer -m /path/to/model.gguf -p "Hello" -n 32 --streaming
sudo ./scripts/restore_nvme.sh # 終了時に戻す
```

- 日本市場での示唆：多くの自作PCやワークステーションでRTX 30シリーズは普及済。B550/X570などGen4対応マザーボードを使えば帯域の利得が期待でき、オンプレ推論のコスト効率が向上する。プライバシー重視の組織や低コストでプロトタイピングしたいスタートアップに有益。

以上を踏まえ、まずは小モデルでビルド→動作確認→NVMeストリーミングへ段階的に進めるのが現実的。興味があればリポジトリ（xaskasdf/ntransformer）を参照して実験してみてください。
