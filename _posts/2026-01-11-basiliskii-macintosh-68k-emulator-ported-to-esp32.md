---
layout: post
title: "BasiliskII Macintosh 68k Emulator Ported to ESP32-P4 / M5Stack Tab5 - BasiliskII を ESP32-P4 / M5Stack Tab5 に移植"
date: 2026-01-11T14:28:40.631Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/amcchord/M5Tab-Macintosh"
source_title: "GitHub - amcchord/M5Tab-Macintosh: BasiliskII Macintosh 68k emulator ported to ESP32-P4 / M5Stack Tab5 - Run classic Mac OS on embedded hardware"
source_id: 46574961
excerpt: "M5Stack Tab5上でSystem 7〜8.1を実機ROMで動かす携帯型BasiliskII移植プロジェクト"
image: "https://opengraph.githubassets.com/fe256ce008e5b89ccd20d687b9fc26f64fbf09d6474f5520d39a5876916d6b25/amcchord/M5Tab-Macintosh"
---

# BasiliskII Macintosh 68k Emulator Ported to ESP32-P4 / M5Stack Tab5 - BasiliskII を ESP32-P4 / M5Stack Tab5 に移植
ポケットで動く「クラシックMac」──M5Stack Tab5上でSystem 7〜8.1を走らせるプロジェクト

## 要約
ESP32-P4搭載のM5Stack Tab5にBasiliskII（Motorola 68kエミュレータ）を移植し、実機ROMとディスクイメージでSystem 7〜Mac OS 8.1を動作させるプロジェクト。タッチ操作・USBキーボード/マウス・SDカードストレージに対応したポータブルな古典Mac環境を提供する。

## この記事を読むべき理由
- レトロPCや組み込みエミュレーションに興味がある国内のエンジニア／ホビイストにとって、手軽に古いMac環境を持ち歩ける実例だから。  
- M5StackやESP32系の活用法、デュアルコア活用、メモリ配置や描画パイプラインなど、組み込み最適化の良い学習材料になる。

## 詳細解説
- 何をしているか：Motorola 68040（68881 FPU含む）をソフトウェアでエミュレートし、実際のMac ROM（例：Q650.ROM）とディスク/CDイメージを使って古典Mac OSを起動する。BasiliskIIコアをESP32向けに最適化して移植している。  
- ハードウェアポイント：M5Stack Tab5はESP32-P4（400MHz デュアルコア RISC‑V、32MB PSRAM、MIPI‑DSI出力）とESP32‑C6を組み合わせたプラットフォーム。PSRAMから4〜16MBをMac RAMとして割当て、残りはフレームバッファやその他に使用する。表示はエミュレータ側で640×360（8bitインデックス）を生成し、Core0でパレット変換→2×2スケーリング→RGB565へ変換して1280×720表示へDMA転送する構成。  
- デュアルコア分担：Core1で68040の命令解釈とメモリ／割り込み／ディスクI/Oを処理。Core0はビデオレンダリング、タッチ処理、USB HIDポーリングを担当。命令量は1ティックあたり約40,000命令の量子で走らせ、表示は約15FPS程度に最適化されている。  
- ストレージ・入力：SDカードからROM・.dsk/.isoを読み込む。タッチは絶対座標でMacのマウス相当、USB Type-Aに外付けキーボードやマウスを接続可能。起動前にタッチGUIでディスク・RAMサイズを選べる。  
- ソフトビルド／導入：PlatformIOでビルド可能。プリビルドのファームウェアをダウンロードしてesptool.pyでフラッシュする方法も用意。  
- ライセンス＆注意点：BasiliskIIはGPLv2ベース。Mac ROMや商用Mac OSのROM/インストーラは著作物なので、入手・利用は自身が所有する実機に基づく正当な手段で行う必要がある。

## 実践ポイント
- 用意するもの：M5Stack Tab5本体、容量8GB以上のmicroSD（FAT32推奨）、必要ならUSBキーボード/マウス、合法的に入手したMac ROMとディスクイメージ。  
- 最短トライ手順（経験者向け）：  
  1. SDカードにプリセットイメージを展開、または /Q650.ROM と Macintosh.dsk をルートに置く。  
  2. プリビルドファームを使う場合は最新リリースをダウンロードしてフラッシュ。自前でビルドする場合はPlatformIOで pio run → pio run --target upload。  
  3. タブ5を起動してブートGUIで設定を確認、起動。  
- フラッシュ例（USBポート名は環境に合わせて変更）：
```bash
# bash
esptool.py --chip esp32p4 --port /dev/ttyACM0 --baud 921600 write_flash 0x0 bootloader.bin 0x10000 firmware.bin 0x8000 partitions.bin
```
- よくあるトラブルと対処：
  - SD初期化失敗 → FAT32でフォーマットし直す、カードスロットの接触確認。  
  - ROMが見つからない → /Q650.ROM をSDルートに配置。ファイル名の大文字小文字に注意。  
  - タッチが動かない → 起動GUIが完了しているか確認。USBキーボードを試して入力確認。  
  - 想定より遅い/カクつく → 元々約15FPSで動作する想定。RAMやディスクI/Oを見直す。シリアルでログを確認すると原因特定が早い。  
- 日本市場での活用アイデア：教育用の組み込みプログラミング教材、ハードウェアミュージアムの小型展示、レトロソフト／界隈のデモ端末、ESP32チューニングの学習プラットフォームとして実用的。

この移植は、組み込みでの大規模エミュレーション（CPU解釈＋専用描画パイプライン）を学ぶ格好のサンプル。手元のM5Stackで古いMacを起動してみたい人、組み込み最適化の実践例を見たい人に推奨される。
