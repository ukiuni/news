---
layout: post
title: "Linux Runs on Raspberry Pi RP2350's Hazard3 RISC-V Cores - Raspberry Pi RP2350のHazard3 RISC‑VコアでLinuxが動作"
date: 2026-01-09T12:20:47.524Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.hackster.io/news/jesse-taube-gets-linux-up-and-running-on-the-raspberry-pi-rp2350-s-hazard3-risc-v-cores-19088b87bb2c"
source_title: "Jesse Taube Gets Linux Up and Running on the Raspberry Pi RP2350&#39;s Hazard3 RISC-V Cores - Hackster.io"
source_id: 46478558
excerpt: "RP2350のHazard3 RISC‑Vコア上でPSRAM搭載ボードに最小Linuxが動作"
---

# Linux Runs on Raspberry Pi RP2350's Hazard3 RISC-V Cores - Raspberry Pi RP2350のHazard3 RISC‑VコアでLinuxが動作
Pico 2のRISC‑Vコアで「ちょっとだけ」Linuxが動いた —— Hobbyist向けRISC‑V入門の扉が開く

## 要約
開発者Jesse Taubeが、Raspberry Piの新マイコンRP2350に搭載されたオープンなHazard3 RISC‑Vコア上で、Buildrootベースの最小限のLinux（NOMMU対応）を起動することに成功しました。公式Pico 2（PSRAM未搭載）では動かせませんが、SparkFunのPro Micro RP2350などPSRAM/外付けフラッシュを備えたボードで動作確認されています。

## この記事を読むべき理由
Raspberry Piブランドの新しいマイコンが、従来の「マイコン＝RTOS」「アプリ向け＝Linux」という枠を越え、RISC‑Vで“Linuxを動かす”可能性を示しました。日本のホビイストや組込みエンジニアにとって、安価なボードでLinuxの学習やプロトタイピングができる点は実用的な意味があります。

## 詳細解説
- RP2350の構成  
  RP2350はRP2040の後継で、従来のArm Cortex‑Mコアに加え、オープンソースのHazard3 RISC‑Vコアを2つ搭載しています。これによりRISC‑V命令がネイティブ実行できます。

- なぜ「特別な」Linuxが必要か  
  一般的なLinuxカーネルはMMU（メモリ管理ユニット）を前提に設計されていますが、RP2350のRISC‑VコアにはMMUがないため、MMU非依存（NOMMU）版のカーネルとユーザー空間が必要になります。TaubeはBuildrootで最小限のルートファイルシステムを構築し、NOMMU対応の構成で動かしています。

- メモリ／ストレージの制約と回避策  
  内蔵SRAMは約520KBと非常に小さく、そのままではLinuxは動きません。RP2350は外付けPSRAM（疑似SRAM）やフラッシュをサポートするため、SparkFun Pro Microのように16MBフラッシュ＋8〜16MB PSRAMを載せたボードで動作確認が取れています。つまり、追加ハードウェアが前提です。

- 性能と用途  
  実用的に速いわけではなく、現状は教育・実験用途が中心。組込みLinuxの基礎を学ぶ、カーネルやデバイスドライバの研究をする、といった用途に向きます。

- 入手性とエコシステムへの影響  
  Raspberry Piブランドの普及力と、RP2350にRISC‑Vコアを載せたことで、国内のハードウェアベンダーや教育機関がRISC‑Vを体験する敷居が下がります。SparkFunなどサードパーティ製ボードは日本の流通経路でも入手可能です（取り扱い店舗や通販を確認）。

## 実践ポイント
- 試したい人は：PSRAMと外付けフラッシュを載せたRP2350ボード（例：SparkFun Pro Micro RP2350相当）を用意する。Pico 2の標準ボードだけでは動作しない点に注意。
- ビルド環境：Taubeが公開しているBuildroot構成と手順を参照してビルドする（GitHubに手順あり）。ポイントはNOMMU用カーネル設定とRISC‑Vクロスツールチェーンの準備。
- 学習の狙い：NOMMU Linuxの制約、デバイスツリーの扱い、PSRAM/フラッシュをブートストレージとして使う方法など、組込みLinuxの基礎を実機で学べる。
- 注意点：現状は実験的な取り組みで安定性・性能は限定的。プロダクト用途には十分な検証が必要。
- 日本向けの活用案：教育カリキュラムへの導入（RISC‑V入門＋Linux）、プロトタイプでの機能検証、ローカルコミュニティでのハッカソン素材。

興味が湧いたら、まずは対応ボードの入手とTaubeのBuildroot設定を参照してみてください。RISC‑Vで“本当に”Linuxが動く経験は、組込みの視点を大きく広げてくれます。
