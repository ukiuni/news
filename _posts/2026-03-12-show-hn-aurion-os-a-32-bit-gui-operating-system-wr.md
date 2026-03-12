---
layout: post
title: "Show HN: Aurion OS – A 32-bit GUI operating system written from scratch in C - AurionOS：Cとアセンブリで一から作られた32ビットGUI OS"
date: 2026-03-12T19:00:08.846Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/Luka12-dev/AurionOS"
source_title: "GitHub - Luka12-dev/AurionOS: A custom 32-bit x86 operating system built from scratch in C and Assembly. Features a graphical window manager, TCP/IP stack, and custom filesystem. Developed solo in 14 days. by a 13-year-old · GitHub"
source_id: 47355213
excerpt: "13歳が14日で作ったC/ASM製32bit OS、TCP/IPや独自FSで低レイヤ学習に最適"
image: "https://opengraph.githubassets.com/d920c466e7ecf73d03da9a697025794e2c309bfb5eefee66475a443496cefc30/Luka12-dev/AurionOS"
---

# Show HN: Aurion OS – A 32-bit GUI operating system written from scratch in C - AurionOS：Cとアセンブリで一から作られた32ビットGUI OS
13歳が14日で作ったレトロ×モダンな自作OS――中身を読むだけで学べる教育的プロジェクト

## 要約
AurionOSはCとx86アセンブリでゼロから実装された32ビットOSで、ウィンドウマネージャ、独自TCP/IPスタック、カスタムファイルシステムを備える学習向けプロジェクト。開発者は13歳で、14日間のソロ開発でベータ公開している。

## この記事を読むべき理由
- 初学者が実機に近い低レイヤー（ブート→保護モード→カーネル）を短時間で追える数少ない実例であるため。
- 日本の学生や趣味のハードウェア／OS入門者にとって、実装の「生のコード」から学べる教材的価値が高い。

## 詳細解説
- ブート処理：16ビットReal ModeからA20有効化、GDT設定、32ビット保護モードへ遷移してカーネルへジャンプするブートローダ（src/bootload.asm）。
- カーネル初期化：スタックとIDTを設定し、アセンブリのエントリからCのkmainを呼び出して高位初期化を行う（src/kernel.asm）。
- メモリ管理：1MB以降にMCB（Memory Control Block）ベースのヒープを実装し、kmalloc/ kfree相当を提供（src/memory.asm）。
- グラフィックス：VBE（VESA）で線形フレームバッファを利用し、ウィンドウマネージャはZオーダー、クリッピング、再描画を扱う（src/vesa.asm、src/drivers/vbe_graphics.c）。
- ネットワーク：Ethernet→ARP→IPv4→ICMP/UDPを自前で実装し、DHCPクライアントで自動IP取得が可能（src/tcp_ip_stack.c）。
- ファイルシステム：セクタベースのAurionFS（メタデータ開始LBA500、データ開始LBA700）、fs_tableによるキャッシュ、fs_save_to_diskで永続化。FAT12読み取りドライバも用意。
- システムコール：INT 0x80経由で基本サービス（コンソール出力、読み取り、時間取得、ディスク操作、シャットダウン等）を提供。
- シェル／ツール群：100以上のコマンド（DIR, CAT, NANO, NETSTART, GUIMODE, PYTHONなど）を組み込み。新規コマンドはカーネルに登録するだけで追加可能。

## 実践ポイント
- ローカルで試す（推奨：QEMU または WSL2／Ubuntu環境）:
```bash
# 例（Ubuntu/WSL2）
sudo apt update
sudo apt install -y build-essential nasm gcc make binutils qemu-system-x86 genisoimage
make run
```
- 新しいコマンドを追加する手順（例）:
```c
// src/commands.c に関数を実装してテーブルに登録
static int cmd_demo(const char *args) {
    puts("Hello, AurionOS World!\n");
    return 0;
}
// commands[] テーブルの末尾に { "DEMO", cmd_demo } を追加
```
- 学習の進め方：
  1. ブート→カーネル初期化の流れを追ってアセンブリの役割を理解する。  
  2. メモリ管理やシステムコール実装を読み、簡単な改変（ログ出力の追加など）で挙動を確認する。  
  3. TCP/IPスタックやVBEドライバの実装はネットワーク／グラフィックスの低レイヤ学習に最適。  
- 注意事項：実機での起動は不安定とのこと。まずはQEMU/VirtualBoxで確認すること。

このリポジトリは教育用途・実験用途として極めて価値が高く、日本の学生や趣味でOSを学ぶエンジニアに強くおすすめ。
