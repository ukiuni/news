---
layout: post
title: "Hardware Image Compression - ハードウェアイメージ圧縮"
date: 2026-03-30T05:49:48.992Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.ludicon.com/castano/blog/2026/03/hardware-image-compression/"
source_title: "Hardware Image Compression &#8211; Ignacio Castaño"
source_id: 47557299
excerpt: "GPUが自動で画像を固定率圧縮、主要ベンダーの差と導入法を短時間で把握"
image: "http://www.ludicon.com/castano/blog/wp-content/uploads/2026/03/afrc-card.jpg"
---

# Hardware Image Compression - ハードウェアイメージ圧縮
GPUが「勝手に」圧縮する時代：Apple・ARM・ImgTecの実力を短時間で把握する

## 要約
ハードウェア側で画像を固定率（主に $1:2$）で圧縮する機能が主要ベンダーで普及しつつあり、品質・速度ともにリアルタイムエンコーダーと競合しています。各社の実装（AppleのMetal lossy、ARMのAFRC、ImgTecのPVRIC4）には得手不得手があるため、実機での検証が必須です。

## この記事を読むべき理由
モバイル／組込向けアプリやゲームでメモリ帯域・ストレージを節約しつつ描画性能を維持するには、各ベンダーのハードウェア圧縮の違いを理解しておくことが重要です。日本のデベロッパーも対象デバイス（iPhone/Mac、Pixel系、各Android端末）で挙動が異なるため、採用判断と最適化に直結します。

## 詳細解説
- 概要
  - ハード圧縮はドライバ／GPUがテクスチャを自動で固定率圧縮する仕組み。標準化の遅れを回避して新フォーマットを広めやすい利点がある。
  - 主要実装：Apple（Metal lossy）、ARM（AFRC）、ImgTec（PVRIC4）と、Vulkanの拡張 VK_EXT_image_compression_control。

- Apple / Metal lossy
  - A15/M2世代から導入、主に $1:2$。APIはシンプルで MTLTextureDescriptor の compressionType を設定するだけで有効化できる。
  - 対応ピクセルフォーマットが広く、R・RG フォーマットの画質はEACより良いが、BC4/BC5には劣る場面もある。RGBA は $1:2$ 固定のため ASTC 等の $1:4$ と直接比較しにくい。
  - ブロックは 8×4 相当でブロック毎に1バイトのメタデータが割り当てられるため実効比率は若干変わる。
  - Metalでの有効化例（Objective-C）:

```objective-c
// Objective-C
MTLTextureDescriptor *descriptor = [MTLTextureDescriptor texture2DDescriptorWithPixelFormat:MTLPixelFormatRGBA8Unorm width:width height:height];
descriptor.usage = MTLTextureUsageRenderTarget | MTLTextureUsageShaderRead;
descriptor.storageMode = MTLStorageModePrivate;
descriptor.compressionType = MTLTextureCompressionTypeLossy;
id<MTLTexture> texture = [device newTextureWithDescriptor:descriptor];
```

- Vulkan + VK_EXT_image_compression_control
  - VkImageCreateInfo に VkImageCompressionControlEXT をチェーンして固定レートを要求可能。BPC（bits per component）で圧縮率を指定する考え方。
  - 例（C）:

```c
// C
VkImageCompressionControlEXT compression_control = {0};
compression_control.sType = VK_STRUCTURE_TYPE_IMAGE_COMPRESSION_CONTROL_EXT;
compression_control.flags = VK_IMAGE_COMPRESSION_FIXED_RATE_DEFAULT_EXT;
compression_control.pFixedRateFlags = NULL;
```

- ARM / AFRC
  - 2021発表、Mali-G715 等で普及。柔軟な BPC（2/3/4/5 bpc など）をサポートし、ブロックは 8×8。RGB/RGBA は同一フォーマットで alpha フラグで切替。
  - 内部は YCoCg + Haar ライクの係数表現で、各 4×4 サブブロックに16係数を持ちモード依存量子化を行う。
  - 画質は非常に良好で、同じ圧縮比なら ASTC より低いRMSEを示すことが多い。ただし滑らかな画像で拡大表示するとディザ／ブロック感が目立つ場合がある（フレームバッファ用途では問題になりにくい）。
  - 実機例（Pixel 8）では AFRC がほとんどのケースで高品質かつ高速。

- ImgTec / PVRIC4
  - 理論上複数の BPC を持つが、手元の Pixel 10 ではドライバが常に 4 bpc（$1:2$）で動作しており疑問点あり。ブロックは 16×16、メタデータ1バイト。
  - 画質面では他社に劣るケースが多く、Spark（リアルタイムエンコーダ）より悪い結果が出る場合もあった。

- パフォーマンス比較（抜粋）
  - M4 Pro（Apple）では Metal lossy のブリットがメモリ帯域を飽和させるほど高速。Spark のコーデックは固定オーバーヘッドがあり小サイズで不利。
  - Pixel 8（Mali）では AFRC が高速かつ高品質。Spark の ASTC が競合しうる場面もあり、リアルタイムエンコードは依然として有効。
  - 実測値はデバイス/テクスチャサイズに依存するため、必ず自環境でベンチを取ること。

## 実践ポイント
- 実機で必ず確認：同じAPI呼び出しでもデバイス／ドライバごとに実際の圧縮比・品質が変わる（例：PVRIC4のドライバ実装差）。
- iOS/macOS（Metal）では簡単に試せるので、手早くメモリ削減を試すならまず MetalのLossyを有効化してベンチを回す。
- Androidでは VK_EXT_image_compression_control を使えるか確認し、AFRC対応端末なら積極的に利用を検討。AFRCはフレームバッファ用途で特に効果的。
- テクスチャ用途では拡大表示やフィルタリングでの見え方を必ずチェック。AFRCのようにテクスチャ拡大でブロック感が出るケースがある。
- リアルタイムエンコーダ（例：Spark等）もまだ競争力あり。開発パイプラインに組み込む前に品質・速度・メモリのトレードオフをテストして最適解を選ぶ。

短く言えば：ハード圧縮は急速に実用域に入りつつあり、採用前に「対象デバイスでの品質確認」と「パフォーマンス計測」が不可欠です。
