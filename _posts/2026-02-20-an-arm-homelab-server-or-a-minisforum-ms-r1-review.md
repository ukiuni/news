---
layout: post
title: "An ARM Homelab Server, or a Minisforum MS-R1 Review - ARMホームラボサーバー：Minisforum MS-R1レビュー"
date: 2026-02-20T02:44:10.034Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://sour.coffee/2026/02/20/an-arm-homelab-server-or-a-minisforum-ms-r1-review/"
source_title: "An ARM Homelab Server, or a Minisforum MS-R1 Review &#8211; Sour Coffee Labs"
source_id: 47082548
excerpt: "MS-R1は安価で実用的なARMホームラボだが、NICやM.2互換の確認必須"
---

# An ARM Homelab Server, or a Minisforum MS-R1 Review - ARMホームラボサーバー：Minisforum MS-R1レビュー
Macより安く「使えるARMサーバー」を手に入れた話 — MS-R1を実運用してわかった良し悪し

## 要約
Minisforum MS-R1は手頃な価格で実用的なARM64ホームラボ向けマシンだが、ネットワークドライバやストレージ周りの制約など初期のハードウェア互換性問題に注意が必要。

## この記事を読むべき理由
日本でもARMサーバーが選択肢になりつつある今、実際の導入でぶつかるドライバ問題や物理的制約を知っておけば、購入後のハマりを避けられます。小規模ラボや自宅サーバーを考えている人に有益です。

## 詳細解説
- ハードウェア概要  
  MS-R1はMini PC型のARM64プラットフォーム。MS-01シリーズの代替としてHPEタワーの消費電力を下げる目的で導入された。静音性はMS-01より良好で、性能対消費電力は好印象。MSRPは約$599（筆者は$559で入手）。

- OSインストールとドライバ問題  
  Rocky Linuxを試したが、オンボードNICが認識されず。Realtek RTL8127用ドライバをサイドロードして動作させたが、カーネル更新時の維持が煩雑で不安定だった。そこでFedoraに切替え（Fedora側にRTL8127ドライバが含まれていたため）で安定稼働を達成。要点：ディストリ選定は「必要なカーネル/ドライバが含まれているか」が最優先。

- ストレージと拡張性の制約  
  M.2スロットが2つだが、1つはWi‑Fiモジュールに使われており、外してもM.2 SSDとしては使えずU.2のみ対応という仕様。複数M.2でRAIDを組みたい用途には向かない。

- ネットワーク周りの注意点  
  Marvell AQC107 NICがUEFIで検出されず使用不可（筆者の試行では）。UEFI/ACPIサポートは進化しているが、特定NICやチップセットは未対応のままのことがある。

- 運用挙動  
  「停電後自動起動（power on after outage）」設定が効かないケースを確認。ヘッドレス運用を想定しているなら電源復旧動作は要テスト。筆者はMS-R1上でFreeBSD 15.0のVMにSambaドメインコントローラを稼働させている。

## 実践ポイント
- 購入前に「使いたいOSでNICが標準サポートされているか」を公式ドライバ/カーネル情報で確認する。  
- Rocky/CentOS/RHEL系を使う場合、最新Realtek系は含まれないことがあるのでFedoraやカーネル新しめのディストロを検討する。  
- M.2スロットの用途制約（Wi‑Fi占有やU.2制限）を把握し、ストレージ拡張計画を立てる。  
- 電源復旧動作やUEFIでのデバイス検出は実機テスト必須。遠隔再起動が必要な環境では要注意。  
- 価格・消費電力対性能のバランスを重視するラボ用途には有力な選択肢。ただし「完璧な互換性」は期待しないこと。

以上。MS-R1は「現実的なARMホームラボ」を手頃に始めたい人にとって魅力的だが、ドライバと拡張性の落とし穴だけは先にチェックしてください。
