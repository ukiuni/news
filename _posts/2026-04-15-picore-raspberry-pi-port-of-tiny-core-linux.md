---
layout: post
title: "PiCore - Raspberry Pi Port of Tiny Core Linux - PiCore：Tiny Core Linux の Raspberry Pi 移植版"
date: 2026-04-15T21:02:39.647Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "http://tinycorelinux.net/5.x/armv6/releases/README"
source_title: "PiCore - Raspberry Pi Port of Tiny Core Linux"
source_id: 47784244
excerpt: "超軽量RAM駆動のpiCoreでラズパイを常時クリーンに高速起動、学習や組込みに最適"
---

# PiCore - Raspberry Pi Port of Tiny Core Linux - PiCore：Tiny Core Linux の Raspberry Pi 移植版
超軽量・RAM駆動で“いつでもクリーン”なRaspberry Piシステムを作るならこれ

## 要約
piCoreはTiny Core LinuxのRaspberry Pi向け移植で、OSをRAM上で動かす超小型ツールキット。IoT機器や学習用途、古いSDカード活用に最適。

## この記事を読むべき理由
日本でもラズパイは教育・プロトタイピング・業務用途で普及中。小容量SDや常時クリーンな環境が欲しい場面（カフェ端末、組込みデバイス、学習用イメージ）でpiCoreは有力な選択肢になるため。

## 詳細解説
- コンセプト：piCoreはフルOSというより「カスタムシステムを作るためのツールキット」。起動後はシステムをRAM上で動作させ、ブートメディアは参照しない設計（Cloud Modeがデフォルト）。拡張（アプリ）はリポジトリから取得し、読み取り専用でマウント。再起動で変更は消え、常にクリーンな初期状態に戻る。
- モード：  
  - Cloud Mode：永続領域不要。ネット接続して拡張を取得。  
  - Mounted Mode：永続化が必要な場合はSDの第2パーティション（ext4）を使い、取得した拡張やバックアップを保存。保存は手動またはスクリプトで制御可能。
- インストール：.zipに入った生イメージをSDへ書き込む（Linuxならdd、WindowsならWin32 Disk Imager等）。有線LAN推奨（時刻同期・パッケージ取得・SSHのため）。
- SDパーティション構成：  
  - mmcblk0p1：VFAT、ブートローダ・ファームウェア・基本システム（起動後はアンマウントされ読み書きしない）。  
  - mmcblk0p2（Mounted Mode用）：ext4で拡張保持。容量は数百MB〜数GB。
- 既プリインストール版：SSHやX付きイメージは第2パーティションに拡張を含むので、追加用に拡張が必要ならパーティション拡大→ファイルシステム拡張を行う。
- パーティション拡大（要注意）：fdiskで第2パーティションを再作成してサイズ変更し、再起動後に resize2fs でファイルシステムを拡大する。
- スワップ：デフォルトはzlib圧縮スワップをRAM上に自動確保（メモリの25%）。不要ならNOZSWAPで無効化。大きなコンパイル等では専用スワップパーティション推奨。
- ブートコード・ログイン：ブートパラメータは /mnt/mmcblk0p1/cmdline.txt に記載。デフォルトユーザは tc（通常パスワードなしで自動ログイン）。SSHイメージではtcのパスワードが設定される場合あり。rootログイン不可。
- サポート：公式フォーラムやCore Book（基本概念の解説）が参考資料。

## 実践ポイント
- イメージ書き込み（例）:
```bash
# Linuxの場合
sudo dd if=piCore-5.x.img of=/dev/mmcblk0 bs=4M status=progress && sync
```
- 第2パーティションを作る／拡張する手順（要バックアップ）:
```bash
sudo fdisk /dev/mmcblk0     # p で確認、dで2を削除、nで再作成（同じ開始セクタ）、wで保存
sudo reboot
sudo resize2fs /dev/mmcblk0p2
```
- zswapを無効化したい・専用スワップ作る場合:
```bash
# スワップパーティション作成後
sudo mkswap /dev/mmcblk0p3
sudo swapon /dev/mmcblk0p3
```
- すぐ使う小ワザ：学習やテストならCloud Modeで手早く立ち上げ、永続化が必要になったらMounted Modeへ切り替える。古い512MBカードでも運用可能。
- 参考リンク：公式フォーラムとCore Bookで概念とツールの詳細を確認。

piCoreは「軽さ」と「再現性」が武器。ラズパイで軽量・確実な実行環境を作りたいなら試す価値あり。
