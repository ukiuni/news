---
layout: post
title: "OpenBSD-current now runs as guest under Apple Hypervisor - OpenBSD-currentがApple Hypervisorでゲストとして動作するように"
date: 2026-01-16T03:42:30.095Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.undeadly.org/cgi?action=article;sid=20260115203619"
source_title: "OpenBSD-current now runs as guest under Apple Hypervisor"
source_id: 46642560
excerpt: "M1/M2上でOpenBSDがAppleハイパバイザ上で安定動作、今すぐ試せる手順付き"
---

# OpenBSD-current now runs as guest under Apple Hypervisor - OpenBSD-currentがApple Hypervisorでゲストとして動作するように
ついに動いた！Apple Silicon上でOpenBSDが実用的に動作するようになった理由と、あなたが今すぐ試すべきポイント

## 要約
OpenBSD/arm64がAppleのハイパーバイザ上でゲストOSとして動作するようになりました。GPUフレームバッファとVirtioネット周りの修正により、以前の黒画面やカーネルパニックが解消されています。

## この記事を読むべき理由
Apple Silicon（M1/M2系）を使う開発者や運用者が増える日本の環境では、ネイティブに近い仮想環境でOpenBSDを動かせることはテスト、開発、セキュリティ検証の選択肢を広げます。特にARM版OpenBSDを試したい人、仮想環境上で安全に実験したい人に有益です。

## 詳細解説
- 何が変わったか（要点）
  - viogpu（仮想GPU）周りの修正：フレームバッファのメモリを扱う関数が仮想アドレス（KVA）を返していたのを、物理アドレスを返すよう bus_dmamem_mmap(9) を使って修正。さらに、ホストにフレームバッファを渡す前に bus_dmamap_sync(9) を呼ぶようにして、別CPU上のホストにも更新が確実に見えるようにしました。これでQEMUでの黒画面やAppleハイパーバイザでのカーネルパニックが解消されています。
  - virtio ネットワーク（if_vio）周りの修正：VIRTIO_NET_F_MTU（ハイパーバイザが提示するハードMTU）をサポートし、現在のMTUをそれに合わせるようにしました。上限は ETHER_MAX_HARDMTU_LEN を使い、もしハイパーバイザがそれを超えるMTUを要求した場合はMTU機能を外して再交渉するようになっています。これでネットワークが安定して動作します。
- 背景技術（初心者向け）
  - Virtio：仮想化環境でゲストとホストが効率良くI/Oをやり取りするための標準的な仕組み。ネットワークやGPUなどが仮想デバイスとして提供されます。
  - フレームバッファとDMA：GUI表示用のバッファはDMAでホストと共有されることが多く、物理アドレスでマッピングしたり同期を取らないと表示が更新されなかったり、最悪カーネルがパニックすることがあります。
  - MTU：ネットワークで一度に運べる最大パケットサイズ。仮想環境ではホスト（ハイパーバイザ）が「これが最大だよ」と教えてくれることがあり、その扱いに対応する必要があります。
- 社会的意味
  - Apple Silicon上でOpenBSDが動くことで、macOS主体の開発環境においてもOpenBSDのテストベッドを容易に持てるようになります。セキュリティツールやネットワーク関連の検証がローカル環境で行いやすくなります。

## 実践ポイント
- 今すぐ試す
  - OpenBSD-current（スナップショット）を使っていることを確認し、Apple Silicon（M1/M2など）搭載Macで仮想化を試す。記事の修正はsnapshotに入っているので最新版を使うこと。
- 確認すべき点
  - X11やフレームバッファの表示（黒画面が出ないか）、カーネルパニックの有無。
  - ネットワークのMTU値：ifconfigなどでハードMTUが正しく反映されているか確認する。
- 問題が出たら
  - dmesgやコンソールログを取得し、OpenBSDの開発メーリングリストやバグトラッカーへ報告するとコミュニティに貢献できます。
- 注意
  - スナップショットは安定版ではないため、本番環境ではなくテスト用途で使うこと。重要なデータは必ずバックアップしてください。

興味があれば、スナップショットでの簡単な立ち上げ手順やトラブルシュートのチェックリストを別途まとめます。どの情報が欲しいか教えてください。
