---
layout: post
title: "I Ported Coreboot to the ThinkPad X270 - ThinkPad X270にCorebootを移植した"
date: 2026-02-24T02:03:21.833Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dork.dev/posts/2026-02-20-ported-coreboot/"
source_title: "I ported Coreboot to the Thinkpad X270! - dork.dev"
source_id: 47130860
excerpt: "X270にCorebootを移植し起動成功、修理とPCIe修正の実践手順"
---

# I Ported Coreboot to the ThinkPad X270 - ThinkPad X270にCorebootを移植した
ThinkPad X270で「純正BIOSを卒業」する方法 — 修理・自由度・起動安定化までのリアルな奮闘記

## 要約
ThinkPad X270（20HM、Kaby Lake）にCoreboot/Librebootを移植して実機起動まで到達。BIOSダンプ、ハードウェア修理、Intel MEの扱い、PCIeクロック振り分け修正が鍵だった。

## この記事を読むべき理由
- 国産・海外含め多くのエンジニアが使うThinkPadで、オープンファームウェアを動かす具体手順と落とし穴が学べる。  
- 日本でも関心の高い「プライバシー／セキュリティ」「修理可能性」「フリーソフトウェア運用」に直結する実例だから。

## 詳細解説
- 対象機種：ThinkPad X270（20HM、Kaby Lake）。X280との差分としてThunderbolt非搭載・SODIMMスロットあり、MEC1653とMEC1663の差異などハード面の違いを把握する必要があった。  
- BIOS操作：SPIフラッシュのバックアップは必須。RP2040-zero上でpico-serprog＋flashprogを使いSOIC-8クリップで読み書き。フラッシュの各領域（Flash Descriptor、GbEなど）をifdtoolで抽出・扱うことが最終イメージ生成に必須。  
- Intel ME（IME）関係：deguardでIME領域のデルタを作成。IMEを「脆弱でない」パッチ済み状態でもデルタ生成は可能で、必ずしも脆弱性が必要という誤解に注意。  
- ハード故障対処：クリップ作業で10µF（0603）コンデンサ（PJ304相当）を破損。基板シルクや回路図で位置を特定し部品交換。小型部品の紛失・取り付け失敗がフラッシュの再試行を長引かせる。  
- 起動トラブルと解決：NVMeやWi‑Fiが消える症状はPCIe割当（CLKREQ/CLKOUT）ミスマップが原因。X280ベースでCLKREQをずらしたところ正常にNVMe・無線が復活。bootsuccessはGuixのGRUB起動とLibrebootのcbmemログ確認で検証。  
- コミュニティ貢献：Libreboot創設者らの協力でROMを複数検証。最終的にX270向けのdeguard/ coreboot変更をアップストリームへ提出中。

## 実践ポイント
- まずBIOSを丸ごとバックアップ（SPIダンプ）。失敗時のリカバリに不可欠。  
- 書き込みはSOIC-8クリップ＋RP2040(pico-serprog)で。クリップ作業中の物理破損に注意し、代替部品（0603コンデンサ等）を事前に手配しておく。  
- ifdtoolでFlash DescriptorやGbEを抽出・保持。これらを欠くと正常イメージにならない。  
- deguardの手順を理解し、IMEはパッチ済みでもデルタ生成可能。me_cleaner等で切り詰める場合はNVMe/Wi‑Fi影響に注意（--whitelist MFSの検討）。  
- ボード差分（ピン割当・CLKREQ）の回路図確認が重要。類似機種の設定をそのまま流用せずピン配置を突き合わせること。  
- 試行錯誤はコミュニティに相談するのが近道。Libreboot/corebootのチャネルとパッチで協力を得やすい。  
- 最後に、実機で動作確認（LiveUSB→GRUB→OS起動、無線・NVMe認識、cbmemログ）を必ず行う。

興味があれば、X270向けのcoreboot/deguardパッチのリポジトリや、使ったツールの簡単な導入手順をまとめて案内します。どの情報が欲しいですか？
