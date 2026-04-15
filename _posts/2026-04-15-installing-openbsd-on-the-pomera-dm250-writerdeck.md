---
layout: post
title: "Installing OpenBSD on the Pomera DM250 Writerdeck - Pomera DM250 WriterdeckにOpenBSDをインストールする"
date: 2026-04-15T04:34:41.975Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://jcs.org/2026/04/09/openbsd-dm250"
source_title: "Installing OpenBSD on the Pomera DM250{,XY?} - joshua stein"
source_id: 47725897
excerpt: "Pomera DM250をOpenBSDで開発機化する具体手順と復旧法"
---

# Installing OpenBSD on the Pomera DM250 Writerdeck - Pomera DM250 WriterdeckにOpenBSDをインストールする
Pomera DM250を“書く道具”から“自分で直し・拡張する開発機”に変える方法 — 安定版ではないが実用的な手順と回復策をまとめました

## 要約
日本モデルのPomera DM250系（DM250 / DM250X / DM250XY）にOpenBSDを入れる手順、必要なカスタムU-Boot／カーネル、注意点、そして万一壊したときの復旧法を簡潔に解説します。

## この記事を読むべき理由
Pomeraは日本で人気のテキスト専用端末。公式サポート外でもLinuxやOpenBSDを動かせば、軽量な執筆環境や開発機として新たな可能性が広がります。特に日本モデル固有のデバイス周りの注意点（電源・充電・キーボード配列）を押さえることは重要です。

## 詳細解説
- 概要：筆者はOpenBSD-current用のカスタムカーネルとU‑Bootイメージを提供。公式に未統合の変更が多く、導入は自己責任です。
- リスク：バッテリーが完全放電すると起動できなくなる、U‑Bootを書き換えると工場Linuxやリカバリが使えなくなる、最悪は内部を開けてUARTやeMMC操作が必要になる可能性があります。特に「DM250US」は充電ICや配列が異なるため注意。
- 流れ（概略）：
  1. eMMCのフルバックアップ（推奨）。
  2. SDカードをGPTで作り、EFIパーティション（>=100MB）とOpenBSD領域を作成。
  3. EFIにOpenBSDのARMv7ブートローダ（BOOTARM.EFI）と提供されるuboot.img、_sdboot.sh（工場リカバリから実行され、eMMCへ新U‑Bootを書き込む）を配置。
  4. OpenBSDのセット（INSTALL.armv7, base, comp…）やカスタム bsd / bsd.rd をOpenBSDパーティションへ置く。
  5. 電源投入時に Right Shift + Left Alt を押して工場リカバリを起動し、SDのスクリプトでU‑Bootを書き換え、以降は新U‑Boot経由でOpenBSDインストーラを起動。
  6. インストール後、カスタムカーネル（/bsd）とreorder_kernelの無効化、Wi‑Fi用firmwareファイルの配置などを行う。
- 主要な注意点：
  - 起動時のキー操作はシビア（押す時間で挙動が変わる）。
  - 電源ケーブル接続中は完全シャットダウンしない挙動、バッテリー残量が重要。
  - eMMCへインストールする際はRockchipのID領域やU‑Boot領域を壊さないよう、EFIパーティションのオフセットを確保する（インストーラの「whole disk」で自動調整可）。
- 復旧法：
  - Rockchip MaskROMモード経由でxrockを使い、U‑BootをアップロードしてUSBマスストレージとしてeMMCをマウント、バックアップから復元可能。
  - 最後の手段は筐体を開けてUARTやeMMCのショート操作など物理的リカバリ。

## 実践ポイント
- まず必ずeMMCをフルバックアップする（外部手順やスクリプトを利用）。
- SDカード準備の最小コマンド例：
```sh
# fdisk -ygb 204800 sd1
# echo -e "a\n\n\n\n\nw\nx" | disklabel -E sd1
# newfs /dev/rsd1a
# newfs_msdos /dev/rsd1i
# mount /dev/sd1i /mnt
```
- EFIにBOOtローダ、uboot.img、_sdboot.sh、bsd{,.rd}を置く。メーカー回復は/mnt/_sdboot.shを実行します。
- インストール後は必ずカスタム/bsdを上書きし、/usr/libexec/reorder_kernelを無効化して元カーネルに戻されないようにする。
- Wi‑Fi: bwfmファームウェアとnvramファイルを正しいパスへコピーする必要あり。
- 復旧手順を事前に確認しておく（xrockやrestoreスクリプトの使い方）。バッテリーを完全放電させないこと。

短く言うと：準備とバックアップを徹底すれば、Pomera DM250でOpenBSDを実用レベルまで動かせますが、電源まわりとブートローダの書き換えは十分な注意が必要です。興味があれば、元記事の提供イメージやスクリプトを参照して手順を進めてください。
