---
layout: post
title: "Exploring Linux on a LoongArch Mini PC - LoongArch ミニPCでLinuxを探る"
date: 2026-01-26T09:52:16.669Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.wezm.net/v2/posts/2026/loongarch-mini-pc-m700s/"
source_title: "Exploring Linux on a LoongArch Mini PC - Wesley Moore"
source_id: 821965322
excerpt: "LoongArch搭載ミニPCでLinuxを実機検証し、性能・互換性と実用上の課題を詳解"
---

# Exploring Linux on a LoongArch Mini PC - LoongArch ミニPCでLinuxを探る
中国発RISC「LoongArch」を実機で触ってわかった、Linux互換性と実務での使いどころ

## 要約
LoongsonのLoongArch64搭載ミニPC（MOREFINE M700S）を使い、Chimera Linuxを導入→グラフィックは現状X11が安定、性能はRaspberry Pi以上だが消費電力高め。パッケージ互換性は概ね良好で、古いRust依存での問題が一部にある。

## この記事を読むべき理由
- 中国発の新しい64bit RISC（LoongArch）が実運用レベルでどこまで使えるかは、日本でもARM/x86以外の選択肢を検討する際に重要。  
- 組込み・検証用ハードやディストリビュション担当者、Linuxパッケージの移植を検討するエンジニアに実践的な知見を提供する。

## 詳細解説
- ISA概要：LoongArch64（LA64）はMIPSやRISC‑Vに似た64ビットRISC。汎用レジスタ32本、浮動小数点32本。ベクトル拡張にLSX（128-bit）とLASX（256-bit）があり、レジスタは重複共有される設計。  
- ハードウェア（M700Sの主な仕様）：Loongson 3A6000（4コア/8スレッド @2.5GHz）、16GB DDR4、Loongson LG100 GPU、Wi‑Fi RTL8821CE、2×HDMI、2×Gigabit LAN、M.2/SATA拡張。サイズはMac mini程度でアルミ筐体。  
- 起動・インストール：UEFIの初期表示は中国語だが英語に切り替え可能。Chimera LinuxのISOから通常の手順でインストールでき、systemd‑bootが使えるなどx86系とほぼ同様。  
- グラフィックス：Wayland系（EGL）でDRI/EGL初期化エラーが出る例があり、現状はX.Org上のXfceが安定動作。GPUドライバの成熟度に依存する問題。  
- 性能・電力：アイドル約27W、負荷で約65W。ブラウザSpeedometer 3.1は約4.45（Intel N100で12.7、ハイエンドCPUで大幅上回る）。Rustビルドなどの実作業はPi系より速いが、効率はx86に劣る。  
- 互換性：多くのパッケージは問題なく動作。壊れているパッケージは少数で、主に古いRust crate（nix、rustix、protobuf系）やcgo/リンク周りの問題。簡単な修正（crate更新）で直るケースもあり、作者はPRを提出している。

## 実践ポイント
- まずUEFIを英語に切替えておくと操作が楽。  
- デスクトップは当面X11（Xfce等）が安定。Waylandはドライバ成熟待ち。  
- ファンノイズと消費電力は覚悟する（常時ファン回転が速め）。省電力用途には向かない可能性。  
- Rust系ビルドでエラーが出たら依存crate（nix/protobuf/rustix等）のバージョン更新を試す。パッケージメンテは比較的少ない工数で貢献可能。  
- 日本の開発／検証用途では、低コストな代替アーキテクチャとして手元で試す価値あり。Linux対応状況を確認しつつ、互換性テストやパフォーマンス比較に使うのが実用的。

（元記事：Wesley Moore「Exploring Linux on a LoongArch Mini PC」）
