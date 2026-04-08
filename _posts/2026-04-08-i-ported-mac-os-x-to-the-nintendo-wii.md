---
layout: post
title: "I Ported Mac OS X to the Nintendo Wii - Mac OS X を Nintendo Wii に移植した"
date: 2026-04-08T16:11:41.285Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://bryankeller.github.io/2026/04/08/porting-mac-os-x-nintendo-wii.html"
source_title: "Porting Mac OS X to the Nintendo Wii | Bryan Keller’s Dev Blog"
source_id: 47691730
excerpt: "Wiiで初代Mac OS X(Cheetah)を動かすブートローダとカーネル改変の実践記録"
---

# I Ported Mac OS X to the Nintendo Wii - Mac OS X を Nintendo Wii に移植した
Wiiで「初代Mac OS X（Cheetah）」を動かした技術ドキュメントを日本語で読むならこれ

## 要約
古いPowerPC版Mac OS X 10.0（Cheetah）を、Wiiのハードウェア上でネイティブに動作させた挑戦の記録。ブートローダ作成、カーネルパッチ、ドライバ実装までの技術的ステップを詳しく書いています。

## この記事を読むべき理由
レトロコンピューティング、組込みOS、ブートプロセスやカーネル改変に興味がある日本のエンジニア／ホビイストにとって、実例を通じて低レイヤ開発の現場感覚が得られるからです。Wiiの普及とHomebrew文化を活かした学習教材にも最適です。

## 詳細解説
- ハード面の相性  
  - WiiはPowerPC 750CL（G3系）を搭載し、メモリは1T-SRAM 24MB + GDDR3 64MB の特殊構成。理論上、Cheetahは128MB推奨だが少メモリでも起動可能で、QEMUで64MB構成でも動作確認済みだったためCPU・メモリは致命的障害ではないと判断された。  
- ソフト面の構造理解  
  - Mac OS X（Darwin/XNU）はオープンソースな核部分と閉源のユーザー空間で成り立つ。PowerPC時代のMacはOpen Firmware→BootX→XNUというブート経路を持つが、XNUが稼働すればBootX/Open Firmware依存は消える。  
- ポーティング方針  
  - Open FirmwareやBootXを丸ごと移植するより、最小限のブートローダを自作してMach-O形式のXNUを読み込み、カーネルへ制御を渡す方針を採用。Wii向けのppcskel等をベースにSD読み出し、フレームバッファ、シリアル出力などを実装。  
- カーネルの読み込みと検証  
  - Mach-Oのロードコマンドに従いセグメントを所定のアドレスに配置し、エントリポイントへジャンプ。ブート直後に通常のデバッグ手段が失われるため、成功検証のためにカーネルのバイナリをランタイムでパッチし、Wiiの前面LEDを点灯させるトリックで進捗確認を行った。例としてLED制御のPowerPC命令は次の通り：  
  ```asm
  lis r5,0x0D80       ; r5 = 0x0D800000
  ori r5,r5,0x00C0    ; r5 = 0x0D8000C0 (LEDレジスタ)
  lwz r4,0(r5)
  sync
  xori r4,r4,0x20     ; ビットをトグル
  stw r4,0(r5)
  ```  
- デバイスツリーとboot_args  
  - XNUは起動時にデバイスツリーを参照するため、Wii用に静的なデバイスツリーをブートローダが作成して渡す必要があった。まずは最小構成（cpus, memory）で始め、段階的に周辺を追加していった。  
- カーネル修正と環境構築  
  - Wiiのメモリ分布（MEM1＝0x00000000、MEM2＝0x10000000）がXNUのBAT設定と衝突したため、BAT周りの修正やコンソール出力のルーティング変更をXNUソースに加えた。古いOSのビルド環境はQEMU上のCheetahゲスト＋ホスト側でソース編集→NFS/SSHでビルドというワークフローで整備した。  
- ドライバ作成（次フェーズ）  
  - rootデバイス（SDカード）やUSB入出力を扱うにはIOKitベースのドライバ実装が必須。IOKitはC++ライクなオブジェクトモデルで、nubとドライバの関係、プローブ／マッチ機構を理解して実装する必要がある。

## 実践ポイント
- 試す前提：WiiにHomebrew ChannelとBootMiiが必要（いわゆる“jailbroken”環境）。作者は wiiMac ブートローダ リポジトリで手順を公開しているので参照すること。  
- ローカルでの検証：QEMUでCheetah環境を用意してカーネルやブートローダの試行を行う。メモリ削減での起動確認は有効。  
- デバッグ：シリアル（USB Gecko）やフロントLEDによるハードウェアサインは、カーネル初期化の可視化に非常に有効。  
- 学びの応用：ブートローダ設計、Mach-Oローダ、デバイスツリー構築、IOKitドライバ作成の各フェーズは組込み系やOS開発スキルとしてそのまま活かせる。日本のレトロコン／組込みコミュニティでの教材化やワークショップネタになります。

興味があればリポジトリを確認し、QEMU上での実験から始めるのが安全です。
