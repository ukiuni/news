---
layout: post
title: "Flux 2 Klein pure C inference - Flux 2 Klein 純C推論"
date: 2026-01-18T19:19:00.726Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/antirez/flux2.c"
source_title: "GitHub - antirez/flux2.c: Flux 2 image generation model pure C inference"
source_id: 46670279
excerpt: "16GBでPython不要、純C実装のFlux 2 Kleinで高速画像生成を手軽に試せる"
image: "https://opengraph.githubassets.com/4fe13a44ea14d66e633e83e69297d798d4682f080a0e158c73899d5ae92c4036/antirez/flux2.c"
---

# Flux 2 Klein pure C inference - Flux 2 Klein 純C推論
16GB・Python不要。純Cで動く画像生成モデルを、あなたのMacやLinuxで手軽に試す方法

## 要約
Flux 2 Klein（FLUX.2-klein-4B）は、PyTorchやPythonランタイムを使わずに「純C」でテキスト→画像、画像→画像の生成ができるリポジトリです。Apple MPSやOpenBLASで高速化でき、モデルはsafetensors（16GB級）をそのまま読み込みます。

## この記事を読むべき理由
- 日本ではApple Siliconノートやリソース制約のあるサーバで「Python/CUDAなし」に画像生成を組み込みたいケースが増えています。本実装は純Cで依存を最小化しており、組込み系や既存C/C++プロジェクトへの導入が容易です。  
- ライセンスはMITで商用利用も可能。ローカルで完結するためデータ保護や運用面で利点があります。

## 詳細解説
- アーキテクチャ要点  
  - Transformer（5つのdoubleブロック＋20のsingleブロック、hidden=3072、24ヘッド）  
  - VAE（AutoencoderKL、128チャネル、8x空間圧縮）  
  - テキストエンコーダ：Qwen3-4B（36層、hidden=2560）を内蔵  
  - 蒸留済みモデルでサンプリングはデフォルト4ステップ（高速化目的）

- メモリと性能  
  - テキストエンコードに約8GB、Diffusionフェーズに約8GB、ピークで約16GB。テキストエンコーダはエンコード後に自動解放され、ピークを下げられます。  
  - BLAS（OpenBLAS）で約30倍、Apple MPS（Metal）対応でApple Silicon上はさらに高速。依存ゼロでコンパイルする「generic」ターゲットもありますが遅いです。  
  - モデルは量子化されておらずfloatで動作（safetensorsをそのまま読み込む）。

- 機能  
  - text-to-image、image-to-image（strengthで変化度合いを調整）、埋め込みの事前ロード、シード制御による再現性。  
  - 最大解像度は1024×1024、最小64×64。寸法はVAEの因子（16の倍数）に合わせる必要あり。

- ビルド／実行の流れ（概要）  
  - ビルドターゲット：make mps（macOS Apple Silicon 推奨）、make blas（OpenBLAS）、make generic（依存なし）  
  - モデル入手：pipでhuggingface_hubを入れ、download_model.pyで約16GBを取得  
  - 実行例：./flux -d flux-klein-model -p "A fluffy orange cat" -o cat.png

- C API（組み込み向け）  
  - 主要関数：flux_load_dir, flux_generate, flux_img2img, flux_image_save, flux_free, flux_set_seed, flux_get_error  
  - 組み込み例（テキスト→画像）：

```c
#include "flux.h"
#include <stdio.h>

int main(void) {
    flux_ctx *ctx = flux_load_dir("flux-klein-model");
    if (!ctx) { fprintf(stderr, "Load failed: %s\n", flux_get_error()); return 1; }

    flux_params params = FLUX_PARAMS_DEFAULT;
    params.width = 512; params.height = 512; params.seed = 42;

    flux_image *img = flux_generate(ctx, "A fluffy orange cat in a sunbeam", &params);
    if (!img) { fprintf(stderr, "Gen failed: %s\n", flux_get_error()); flux_free(ctx); return 1; }

    flux_image_save(img, "cat.png");
    flux_image_free(img); flux_free(ctx);
    return 0;
}
```

## 実践ポイント
- まず動かす手順（最短）  
  1. 必須：ディスクに約20GBの空きと16GB以上のRAMを確保。  
  2. ビルド（Apple Silicon推奨）:
```bash
# macOS Apple Silicon
make mps
# Linux or Intel mac
make blas
# 依存なし（遅い）
make generic
```
  3. モデルをダウンロード:
```bash
pip install huggingface_hub
python download_model.py
```
  4. 実行例:
```bash
./flux -d flux-klein-model -p "A woman wearing sunglasses" -o out.png -W 256 -H 256
```

- 小技と注意点  
  - 再現性：実行時に出力されるSeedを指定すれば同じ画像が再現できます。  
  - img2imgのstrengthは0.0〜1.0（0.7がスタイル転換で扱いやすい）。  
  - 多数のバリエーション生成時はエンコーダを再ロードするコストに注意。異なるプロンプトで都度エンコーダがロードされます。  
  - 日本の開発環境ではApple Siliconが多く、MPSターゲットが最も手軽で高速。サーバで使うならOpenBLASを整えてmake blasが現実解。

Flux 2 Kleinの純Cアプローチは「Python/CUDAが使えない環境」や「組込みC/C++プロジェクトに組み込みたい」場面で強力です。まずはローカルで一枚生成して、APIを自分のC/C++アプリに組み込む流れを試してみてください。
