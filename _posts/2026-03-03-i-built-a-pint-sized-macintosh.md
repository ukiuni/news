---
layout: post
title: "I built a pint-sized Macintosh - 小さなマッキントッシュを作った"
date: 2026-03-03T08:48:41.640Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.jeffgeerling.com/blog/2026/pint-sized-macintosh-pico-micro-mac/"
source_title: "I built a pint-sized Macintosh - Jeff Geerling"
source_id: 47229119
excerpt: "Picoで20ドル、手のひらサイズの初期MacをVGAとmicroSDで再現する懐かし学習プロジェクト"
---

# I built a pint-sized Macintosh - 小さなマッキントッシュを作った
Raspberry Pi Picoで手のひらサイズの“Macintosh”を再現——懐かしさと学びが詰まった20ドルプロジェクト

## 要約
Raspberry Pi Pico（RP2040）とPico Micro Macファームウェアで、640×480 VGA出力の初期Mac風マシンを組み上げられる。制約は多いが学習用途とレトロ体験に最適。

## この記事を読むべき理由
国内でも高まるレトロPC・電子工作ブームにぴったりの短時間で組めるプロジェクト。Raspberry Piエコシステムに親しむ入門者がOSやハードの基本を実機で学べるから。

## 詳細解説
- ハード構成：Raspberry Pi Pico（RP2040）＋PicoMicroMacアダプタ（v2/v3）、microSD（umac0.imgを配置）、VGAモニタ（640×480@60Hz）、USBキーボード/マウス（OTG経由）、電源。パーツは安価で揃う。Jeff Geerlingは約$20で構築。
- ファームウェア：Matt Evansのpico-macベースの.uf2をPicoにフラッシュすると、初期のMac OS（System 5.xなど）を起動可能。v3アダプタはmicroSD統合＆Pico WH直挿し対応で半田不要。
- フラッシュ手順（要点）：
  1. PicoのBOOTを押しながらPCに接続してマスドライブ化。
  2. ダウンロードした.uf2をドライブのルートにコピー（自動再起動）。
  3. microSDはFAT32でフォーマットし、umac0.imgをルートにコピー（SD HAT使用時）。
- 起動手順（要点）：VGA接続、USB OTGでキーボード/マウス接続、PicoMicroMacに電源投入 → “Welcome to Macintosh”画面からデスクトップ表示。
- 制約と拡張性：
  - SRAMの制約でOSに割けるRAMは最大約208KB（オリジナルの128K Macより実メモリは多いが限定的）。
  - サウンドやAppleTalk/SCSIなど特殊機能は未対応。重めのアプリや一部のエミュは動作しない。
  - RP2350など新しいRP系ボードでメモリ拡張（実験的に最大4MBでSystem 7.5.5）を試す動きあり。

## 実践ポイント
- 必要なパーツ（代表）：Pico Micro Macアダプタ（v3推奨）、Raspberry Pi Pico（WH推奨）、microSDカード、VGAモニタ、microUSB→USB OTGケーブル。
- フラッシュはUF2を使えば簡単：BOOTを押しながら接続して.uf2をコピーするだけ。
- microSDはFAT32でumac0.imgをルートに置くこと（SD HAT利用時）。
- 面倒を減らすならv3アダプタ＋Pico WHで半田不要。学習用途ならまずはサンプルイメージで動作確認を。
- 期待しすぎない：これは「学びとノスタルジー」が主目的。実用マシンや本格エミュレーションは別途環境を検討すること。

（Jeff Geerlingによる実際の組み立て動画やPicoMicroMac UF2 Creatorページを参照すると手順が分かりやすい）
