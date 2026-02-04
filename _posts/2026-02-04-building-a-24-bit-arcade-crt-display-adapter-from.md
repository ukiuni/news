---
layout: post
title: "Building a 24-bit Arcade CRT Display Adapter, From Scratch - スクラッチから作る24ビット・アーケードCRTディスプレイアダプタ"
date: 2026-02-04T18:14:38.919Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.scd31.com/posts/building-an-arcade-display-adapter"
source_title: "Building a 24-bit Arcade CRT Display Adapter, From Scratch | Stephen's Site"
source_id: 46888795
excerpt: "USBで現代PCを24bitアーケードCRTに低遅延接続するSTM32/LTDC自作記"
image: "https://www.scd31.com/img/rcade/rev2-top.jpg"
---

# Building a 24-bit Arcade CRT Display Adapter, From Scratch - スクラッチから作る24ビット・アーケードCRTディスプレイアダプタ
レトロCRTを現代PCにつなぐ魔法：USBで24bitアーケードCRTを自作した話

## 要約
Raspberry Pi系マイコンで始めたVGA出力実験から始まり、USB経由でホストのフレームバッファを受け取ってJAMMA/CRTへ出力する「24-bit CRTアダプタ」を設計・実装するまでの技術的挑戦記。最終的にUSBフル/ハイスピードやSTM32のLTDCを用いる設計に落ち着く。

## この記事を読むべき理由
レトロ筐体を現代のPCやノートから動かしたい人、低レイテンシで任意解像度（例：320×240、336×262）をCRTに出す方法に興味がある人、USB経由のディスプレイプロトコル（GUD）やマイコンでのビデオ出力設計の実用的ノウハウを学べる。

## 詳細解説
- CRT/VGAの本質：CRTは横走査（HSYNC）・垂直同期（VSYNC）と、R/G/Bアナログ信号で構成される。フロント／バックポーチなどのタイミング領域も重要で、正確なタイミングでR/G/Bを変調する必要がある。
- 試作1（RP2040 + PIO）：RP2040のPIOでHSYNC/VSYNCとRGBをサイクル精度で生成。PIOは命令数やプログラム長に厳しい制約があり、解像度・タイミングをハードコードする実装になりがち。色深度は当初16bit→12bitと制約あり。
- フレーム伝送とプロトコル：ホスト側はLinuxのフレームバッファをUSBで送る設計を模索。最初は自作カーネルモジュールを試したが、既存のGUD（USBディスプレイプロトコル）を使う方が現実的。GUDは差分転送や圧縮をサポートし、カーネルに上流マージされている利点があるがドキュメントは薄い。
- 帯域の壁：USB Full Speed（11 Mbps）はボトルネック。例：320×240、16bppで1フレームが153.6 kBになり、$153.6\ \mathrm{kB}\times8/11\ \mathrm{Mb/s}\approx9\ \mathrm{FPS}$ 程度にしかならないため実用的フレームレートを得られない。
- 解決策の移行（STM32 + LTDC）：USB HS対応とLTDC（LCD向けタイミング生成）を持つSTM32H7系へ移行。LTDCはHSYNC/VSYNC/RGBをネイティブに扱えるため、USB HSで受けたデータを直接ディスプレイ信号に変換可能。アナログ出力には8bit DAC×3、0.7Vフルスケール、75Ω整合を考慮した回路設計が必要。

## 実践ポイント
- まず要件を整理：解像度・色深度・目標FPS・接続（USB FS/HS/SS）を決める。
- 帯域見積もりを必ず行う：フレームサイズ（バイト）×8 / USB帯域（ビット/s）で最大FPSを算出する。
- GUDを活用：Linux標準のGUDホスト＋gadget実装で互換性を確保。ドキュメント不足は逆コンパイル／デバッグで補う。
- マイコン選定：USB HSとLTDC相当のハードを優先（例：STM32H7系）。RP2040はPIOで面白いがUSB FSの帯域がネック。
- DACとケーブル整合：VGAは0.7Vフルスケール・75Ωインピーダンスを意識。単純な抵抗分圧でも画質に影響するので設計段階で検討する。
- 圧縮と差分転送を活用：帯域不足時はGUDの差分送信や画面圧縮を使って転送量を削減する。

元記事はハード／ソフト両面でのトレードオフと、プロトタイプから実運用に至るまでの現実的な判断が学べる好例。日本のレトロ筐体コミュニティや教育用途にも応用しやすい内容。
