---
layout: post
title: "PicoPCMCIA – a PCMCIA development board for retro-computing enthusiasts - PicoPCMCIA — レトロ向けPCMCIA開発ボード"
date: 2026-01-21T17:41:18.394Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.yyzkevin.com/picopcmcia/"
source_title: "PicoPCMCIA &#8211; yyzkevin"
source_id: 46708096
excerpt: "PicoPCMCIAで古いノートが現代ネットと高音質音源を獲得"
---

# PicoPCMCIA – a PCMCIA development board for retro-computing enthusiasts - PicoPCMCIA — レトロ向けPCMCIA開発ボード
レトロノートが現代ネットと高音質サウンドを手に入れる――PicoPCMCIAで“古いけど使える”をアップデート

## 要約
PicoPCMCIAはType II、5V、16ビットのオープンソースPCMCIA開発ボードで、Wi‑Fi/Bluetooth、Sound Blaster互換音源、Gravis UltrasoundやCD-ROM/フラッシュのエミュレーションなどをレトロ機に提供します。既製ファームもあり、低レベル実験から手軽な動作確認まで対応します。

## この記事を読むべき理由
PCMCIAスロットを持つ古いノート／モバイル機（日本でもNECや富士通の旧機種含む）を現代ネットワークや音源で活用したい人、あるいはレトロHWの拡張を試したいエンジニア／趣味者にとって即戦力になる情報です。

## 詳細解説
- ハードウェア概要: RP2350ベースでPicoGUS/PicoMEMとコード互換性を持ち、16ビットPCカード（Type II、5V）として多くのPCMCIA対応機で動作を狙う設計。公開プロジェクトでコミュニティ拡張が速い。
- 無線: Infineon CYW43439（Raspberry Pi Pico Wと同じ）を積み、2.4GHz 802.11b/g/n（WPA2）で接続。NE2000イミュレートやダイヤルアップモデムとしてホストからは有線アダプタやモデムに見えるため、古いOSでもドライバ互換性が高い。BluetoothはA2DP等を想定中（現状PoC）。
- オーディオ: TI TLV320AIC3254によるi2s DAC＋ヘッドフォンアンプ／ライン出力と、DREAM SAM2695シンセを搭載。MPU‑401エミュや内蔵/外部MIDI出力、ゲームやDOS向けの音源再現をサポート。
- サウンド互換性: PCMCIAでのSound BlasterはDMA非対応が課題だが、DMAエミュレーションを実装し多数の実モード／保護モードゲームと互換性を確保。Adlib/OPLは既存実装を流用。
- GUS（Gravis Ultrasound）やCD-ROM: PicoGUS由来の成果でPCMCIA GUSやPanasonic MKE CD-ROMエミュを実現。音声はTLV320経由で高品質で同時使用可能。
- ストレージ/USB: microSDにBIN/CUE/ISOを置いてエミュレーション。HP 200LX向けの“Doubleslot”互換など特殊ケース対応。USBは主にフラッシュ用だが、USBゲームパッド／マウスやストレージ転送の実績あり。
- 電力と互換性: ネットワーク＋ストレージの動作で約150mA以内を目標に設計済み。超低消費機（例：HP 200LX）ではオーディオ＋ネット同時利用で外部電源が必要な場合あり。動作確認済み機種にIBM PC110、HP 200LX、Amiga 1200、Apple Newton等。

## 実践ポイント
- まずは既製ファームで動作確認：microSDにイメージを置き、対応ドライバでNE2000／モデムとして認識させると手早くネット接続確認できる。  
- 電源制約を確認：HP 200LX等低消費機はネット＋音声の同時利用で外部電源検討。  
- MIDI/ゲーム音源を試す：DOSゲームやMIDI対応アプリでSAM2695／Sound Blaster互換を動かして互換性評価。  
- ソースを追う／貢献する：オープンソースなのでPicoGUS/PicoMEMとのコード共有により機能拡張が可能。日本のレトロコミュニティ向け改善を共有すると恩恵が還元されやすい。  
- 注意：趣味・開発用途向けで商用認証は無し。使用前に対応機種と消費電力を必ず確認すること。
