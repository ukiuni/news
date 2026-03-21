---
layout: post
title: "Storing 2 bytes of data in your Logitech mouse - ロジクールのマウスに2バイトを保存してみた"
date: 2026-03-21T21:36:59.034Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.timwehrle.de/blog/what-if-i-stored-data-in-my-mouse/"
source_title: "What if I stored data in my mouse"
source_id: 418690273
excerpt: "ロジクールマウスのDPIレジスタに任意の2バイトを書き込み、別PCでも保持できる裏機能を解説"
---

# Storing 2 bytes of data in your Logitech mouse - ロジクールのマウスに2バイトを保存してみた
「マウスがUSBメモリ代わりになる？」思わず試したくなるガジェット・ハック

## 要約
ロジクール製マウスの非公開機能（HID++）を調べたら、DPI設定レジスタに任意の16ビット値を書き込めて、マウスを別PCに差し替えてもその2バイトが残ることを発見した話。

## この記事を読むべき理由
普段何気なく使っている周辺機器に隠れた機能や保存領域があることを知ると、リバースエンジニアリングの基本やOSとデバイス間の境界（特にmacOSの制約）を学べます。日本でも在宅勤務やマシン間での機器の持ち運びが一般的なため、実用・教育どちらにも面白い題材です。

## 詳細解説
- Logitechは独自拡張「HID++」をUSB HID上に実装しており、デバイスごとに「feature table」と呼ばれる機能一覧がある。各機能は共通のID（例: 0x2201）と、機種固有のインデックスにマップされる。
- 通信は短いパケット（レポートID、デバイスインデックス、機能インデックス、関数ID、最大3バイトのパラメータ）で行われ、応答も同様の形。
- 一部の機能（TemplateBytesNVSなど）は非揮発メモリに相当するが、macOSのIOHIDManagerは必要な長めのHID++レポートを無視してしまい、直接書き込みがブロックされる。回避には低レイヤ（IOKitで直接USB操作）を使う必要がある。
- 著者は最終的にDPI設定レジスタを利用。DPIは16ビット（u16）で受け取り側でバリデーションされず、任意の値を書き込めるため、例えば 0x6869 を書いて別PCで読み返すと「hi」（ASCII）に相当する2バイトがそのまま残ることを確認した。
- 目的は「有用なストレージ」ではなく、プロトコル理解と検証。逆コンパイルやドキュメントでは得られない知見が実地探究で得られる、という点が主題。

## 実践ポイント
- 興味がある人は著者のツールを参照：https://github.com/timwehrle/mouse-fs （Unifyingレシーバー経由のロジクールマウス向け）
- macOSではIOHIDManagerの制約に注意。動作しない場合はIOKit経由やLinux/Windowsで試すと成功しやすい。
- 実験は自己責任で。デバイスの挙動を変える可能性があるため重要データや業務機では行わないこと。
- 学びのポイント：HIDプロトコルの構造、デバイス固有インデックスの扱い、OSのHIDスタックがどこでパケットを切るかを追う練習になる。
