---
layout: post
title: "Fedora 44 on the Raspberry Pi 5 - Raspberry Pi 5でのFedora 44"
date: 2026-03-14T22:16:31.271Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://nullr0ute.com/2026/03/fedora-44-on-the-raspberry-pi-5/"
source_title: "Fedora 44 on the Raspberry Pi 5 &#8211; nullr0ute&#039;s blog"
source_id: 47380512
excerpt: "Raspberry Pi 5でFedora 44をHDMI加速付きで即導入、必須設定手順も掲載"
---

# Fedora 44 on the Raspberry Pi 5 - Raspberry Pi 5でのFedora 44
Pi Day特別：Raspberry Pi 5でFedora 44を試すべき理由とすぐできる設定ガイド

## 要約
Fedora 44のRaspberry Pi 5向けイメージが公開され、デスクトップ（KDE/GNOME）やHDMIアクセラレーションなど主要機能が動作する状態で試せます。ただし一部機能は未対応で手動設定が必要です。

## この記事を読むべき理由
Raspberry Pi 5は日本でも普及が進んでおり、Fedora 44の公式に近いイメージでデスクトップ環境やハードウェアアクセラレーションを試せるのは、開発・検証環境を構築したいエンジニアや趣味のユーザーにとって有益です。

## 詳細解説
- 動作確認済み（抜粋）
  - Raspberry Pi 5B（revC / revD）
  - メモリバリアント：1/2/4/8/16GB（元情報に基づく）
  - シリアルコンソール、microSDスロット（現時点で唯一のOSディスク対応）
  - HDMI（アクセラレートされたグラフィック）、有線LAN、無線、USBポート（OSディスク不可）
  - KDE / GNOME のデスクトップイメージあり
- 未対応または開発中
  - Raspberry Pi 500シリーズ、Compute Module 5（CM5）
  - NVMe、サーマル制御、オーディオ、CMA自動追加 等
- 必要な手動設定
  - カーネルコマンドラインに以下を追加しないとアクセラレーション等が動作しない：
    cma=256M@0M-1024M
  - arm-image-installer 使用時は --args オプションで指定。起動後は /etc/kernel/cmdline に追記して次回以降も有効化。
  - デスクトップイメージでは自動サスペンドを無効化推奨。

## 実践ポイント
- まずはmicroSDへイメージを書き込み、Pi 5で起動して動作確認（HDMI・ネットワーク・USB等）。
- 起動後すぐにカーネルコマンドラインへ cma=256M@0M-1024M を反映する（arm-image-installer --args または /etc/kernel/cmdline 追記）。
- デスクトップ利用時は自動サスペンドをオフにして安定性を確認。
- 現状未対応の機能（NVMeやCM5など）はアップデートを待つか、別環境で検証を継続する。

（提供イメージ：Minimal / KDE / GNOME Workstation — 元記事参照のこと）
