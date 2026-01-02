---
layout: post
title: "Igniting the GPU: From Kernel Plumbing to 3D Rendering on RISC-V - GPUに火をつける：RISC-Vでのカーネル配管から3Dレンダリングまで"
date: 2025-12-30T18:38:19.879Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://mwilczynski.dev/posts/riscv-gpu-zink/"
source_title: "Igniting the GPU: From Kernel Plumbing to 3D Rendering on RISC-V"
source_id: 46433352
excerpt: "TH1520でPowerVRをmainline化、電源シーケンスでRISC-V上にフル3Dを点火"
---

# Igniting the GPU: From Kernel Plumbing to 3D Rendering on RISC-V - GPUに火をつける：RISC-Vでのカーネル配管から3Dレンダリングまで
RISC-Vボードで「黒い画面」からフルアクセラレーションを動かした瞬間 — TH1520上のPowerVRをメインラインへ

## 要約
TH1520（Lichee Pi 4A搭載）のPowerVR GPUを動かすために不足していたプラットフォームドライバ群と電源シーケンスを実装し、drm/imagination（Vulkanネイティブ）＋Zinkでフル3Dアクセラレーションを実現した取り組みを解説します。

## この記事を読むべき理由
RISC-V機器や組み込み機器のグラフィックス有効化には、単にGPUドライバを追加するだけでは足りません。メーカー特有の電源・クロック・リセット順序を扱うための「カーネル側の配管作業」が必須で、日本の組み込み/産業機器開発者にとって即戦力になる知見が詰まっています。

## 詳細解説
- 問題の本質  
  PowerVRは長年ベンダー提供のアウトオブツリードライバが主流でしたが、Imaginationのオープン化でmainline化が進行。しかしTH1520のようなRISC-V SoCではGPU周辺の電源・クロック等を扱うプラットフォーム側のドライバが欠けており、GPUがプローブできない状態でした。

- 底辺からの依存関係（実装したもの）  
  1) mailbox-th1520：安全用コプロセッサ（E902）とCPU間の物理的な通信を確立するMailboxドライバ。  
  2) thead-aon-protocol：Mailbox上で動く常時稼働ファームウェアプロトコル。電源要求メッセージのフォーマットを扱う。  
  3) pmdomain-thead：GPU電源レールをGeneric Power Domain (GenPD) として露出。  
  4) clk-th1520-vo / reset-th1520：Video Outputサブシステム向けのクロック／リセット制御を追加。  

- 電源シーケンス問題とpwrseq  
  TH1520のGPUは微妙な時間順序で「電源オン→電圧安定待ち→リセット解除」を行う必要があり、従来のGPIOトグルとは次元が違う。Linuxには汎用のPower Sequencing（pwrseq）フレームワークが導入されており、これを使ってSoC固有のシーケンスを「シーケンサドライバ」として実装（pwrseq-thead-gpu）。重要な設計点は、シーケンサがマッチフェーズでGPUのリソース（クロック／リセットハンドル）を動的に奪い取って管理することにより、順序の厳密な保証を実現している点です。

- DRM側の拡張（drm/imagination）  
  GPUドライバ側にはプラットフォームごとの電源戦略を差し替えられる抽象（pvr_power_sequence_ops）を導入。GPUドライバは具体の順序を知らず、pwr_ops->power_on()を呼ぶだけで済みます。結果としてコアドライバは汎用性を保ちつつ各SoC固有のシーケンスに適応できる構造に。

- 表示パイプラインの統合  
  GPUでレンダリングしたフレームはDMA-BUF経由でVerisilicon DC8200（ディスプレイコントローラ）へ渡され、そこからHDMIブリッジへ。表示ドライバ（Verisilicon向けの汎用DRM）は別途作業が必要で、複数の開発者による協調で「レンダリング→スキャンアウト」の完全パイプラインが完成しました。

- ユーザースペース：Vulkanネイティブな流れとZinkの活用  
  伝統的にはOpenGLとVulkanの両面を実装する必要がありましたが、現代は「Vulkanネイティブ」で進め、MesaでZink（OpenGLをVulkanにブリッジ）を使うことでOpenGL対応の負担を避けています。これにより、PowerVRのVulkanドライバを軸にして既存のOpenGLアプリを動かせる構成に。

## 実践ポイント
- pwrseqを活用する場面：SoCの外部ライクに振る舞う周辺IP（GPUや複雑なPHY）の電源立ち上げで、個別GPIOやドライバ内の遅延ハックでは再現が難しい順序制御が必要なときに投入する。
- ドライバ分割の心得：GPU（レンダリング）とDisplay（スキャンアウト）は別デバイスとして扱われることが多い。両方の「土台（power/clk/reset）」を先に整備してから上位ドライバを有効化する。
- 再現メモ（Lichee Pi 4Aの例）  
  - カーネル：作者のツリー（Linux 6.19ベース）を使うこと。  
  - Mesa：Vulkan-imaginationとZinkを有効にしたビルド。例のmeson設定：
  ```bash
  meson setup build \
    -Dbuildtype=release \
    -Dplatforms=x11,wayland \
    -Dvulkan-drivers=imagination \
    -Dgallium-drivers=zink \
    -Dglx=disabled -Dgles1=disabled -Dgles2=enabled \
    -Degl=enabled -Dtools=imagination -Dglvnd=disabled
  ```
  - ユーザー空間のフラグ（開発中ドライバを強制ロード）:
  ```bash
  export PVR_I_WANT_A_BROKEN_VULKAN_DRIVER=1
  export GALLIUM_DRIVER=zink
  export MESA_VK_DEVICE_SELECT=1010:36104182!
  ```
- 日本の現場での応用例：産業用HMI、車載用途、IoT端末のローカル3D処理やAI可視化で、SoC固有の電源制御を正しく扱えば安定したハードウェアアクセラレーションが可能になる。

