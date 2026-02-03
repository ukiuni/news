---
layout: post
title: "Floppinux – An Embedded Linux on a Single Floppy, 2025 Edition - Floppinux — 単一フロッピー上の組込みLinux（2025版）"
date: 2026-02-03T05:35:41.033Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://krzysztofjankowski.com/floppinux/floppinux-2025.html"
source_title: "FLOPPINUX - An Embedded 🐧Linux on a Single 💾Floppy - 2025 Edition       (v0.3.1)"
source_id: 46866544
excerpt: "3.5インチフロッピー1枚で起動する最小Linuxを短時間で作る実践ガイド"
---

# Floppinux – An Embedded Linux on a Single Floppy, 2025 Edition - Floppinux — 単一フロッピー上の組込みLinux（2025版）
3.5インチひとつでLinuxが動く！レトロ＆組込み入門に最適な「Floppinux 2025」を短時間で試す方法

## 要約
Floppinuxは1.44MiB（3.5"）フロッピー1枚で起動する最小限のLinuxディストリビューション／ワークショップで、i486互換CPU向けにカスタムカーネル（Linux 6.14.11）＋BusyBox（静的ビルド）を使い、rootfsを圧縮してフロッピーに焼く手順を丁寧に解説します。

## この記事を読むべき理由
- レトロPCや極限リソース環境でのLinux動作を学べる入門ワークショップとして最適。  
- カーネル最小設定、クロスコンパイル、BusyBoxベースの組込みツール群、initスクリプト、フロッピーイメージ作成まで一連の流れが学べるため、Linuxの内部理解が深まる。

## 詳細解説
- 目的と狙い  
  - 「Linux From Scratch」を小さくした形で、学習目的のために最小構成を自分で作るプロジェクト。最終的に3.5"フロッピーで起動し、端末・vi・簡単なスクリプトと永続ストレージ（約264KiB）を提供。

- 対応環境と要点  
  - カーネル：Linux 6.14.11（6.15以降でi486サポートが外れるため互換性の最後の版）  
  - ツール：BusyBox 1.36.1（静的ビルド推奨）  
  - ホスト：64-bit（著者はArch系/Omarchyを使用）、クロスコンパイラでi486ターゲットを生成（musl クロス等）  
  - エミュレータ：qemu-system-i386でのテスト推奨（実機は注意が必要）

- 主要手順の流れ（要点のみ）  
  1. 作業ディレクトリ作成。  
  2. カーネル取得 → make ARCH=x86 tinyconfig → menuconfigで必要オプション（i486、initramfs/XZ、floppy/ramdisk、FATサポートなど）を有効化 → ビルドしてbzImageを取得。  
  3. BusyBox取得 → allnoconfigから必要コマンドを選択（vi、ash、mdev、mount等）、静的ビルド設定 → クロスコンパイラ指定してmake installで_filesystem_生成。  
  4. filesystemに/dev、/proc、/sys、/etc/inittab、/etc/init.d/rc（initスクリプト）などの最小構成を追加。rcでフロッピーを/mntにマウントし/homeにbindする等の処理を記述。  
  5. rootfsを cpio でまとめて xz 圧縮（サイズ調整用に辞書サイズ指定）→ rootfs.cpio.xz。  
  6. フロッピーイメージ作成（1,440KiB）→ mkdosfs + syslinuxでブート構成書き込み → ループマウントして bzImage, rootfs, syslinux.cfg 等をコピー。  
  7. qemu-system-i386 -fda floppinux.img -m 20M -cpu 486 でテスト。動作確認後に実機へ dd で書き込み（デバイス指定は慎重に）。

- 注意点  
  - カーネル設定でi486を外すと実機互換性が失われる。  
  - フロッピー書き込み時のデバイス指定ミスはデータ消失につながる（sudo dd if=floppinux.img of=/dev/XXX … のXXXを厳密に確認）。  
  - BusyBoxは「静的ビルド」を推奨（共有ライブラリが無い方が小さく安定）。

## 実践ポイント
- まずはエミュレータで試す（qemuコマンド例）:
```bash
# qemuでの起動例
qemu-system-i386 -fda floppinux.img -m 20M -cpu 486
```
- i486互換性を確保するならカーネルは6.14.x系を使用する。  
- クロスコンパイラは musl.cc 等の i486 クロスツールチェーンを使うと簡単。  
- rootfs を作る際は最小限の /etc/inittab と /etc/init.d/rc を用意しておくと早く起動する。  
- フロッピーイメージ作成の流れ（要点コマンド）:
```bash
# イメージ作成・フォーマット
dd if=/dev/zero of=floppinux.img bs=1k count=1440
mkdosfs -n FLOPPINUX floppinux.img
syslinux --install floppinux.img
sudo mount -o loop floppinux.img /mnt
# ファイルをコピーしてアンマウント
sudo cp bzImage rootfs.cpio.xz syslinux.cfg /mnt
sudo umount /mnt
```
- 実機に焼くときは必ずデバイス名を二重確認。ミスるとパーティションが丸ごと消える。GUIツールでの書き込みを併用すると安全。

短時間で試せて学びが大きいプロジェクトです。レトロ好き、組込み／OSを学びたい方はまずエミュレータで起動してみてください。
