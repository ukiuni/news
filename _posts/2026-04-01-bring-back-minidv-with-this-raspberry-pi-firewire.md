---
layout: post
title: "Bring Back MiniDV with This Raspberry Pi FireWire Hat - MiniDVをRaspberry Pi用FireWire HATで復活"
date: 2026-04-01T05:06:47.885Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.jeffgeerling.com/blog/2026/minidv-with-raspberry-pi-firewire-hat/"
source_title: "Bring back MiniDV with this Raspberry Pi FireWire HAT - Jeff Geerling"
source_id: 47558101
excerpt: "Raspberry Pi＋FirehatでMiniDVテープを持ち運べるMRUに"
---

# Bring Back MiniDV with This Raspberry Pi FireWire Hat - MiniDVをRaspberry Pi用FireWire HATで復活
懐かしのMiniDVを“持ち歩ける”保存機に変える：Raspberry Pi + Firehatで作るポータブルMRU

## 要約
古いMiniDVカメラをテープのまま使い続ける代わりに、Raspberry Pi用のFireWire HAT（Firehat）とバッテリを組み合わせて持ち運べる「Memory Recording Unit（MRU）」を作り、テープのアーカイブやFireWire機器の接続を実現するプロジェクトです。

## この記事を読むべき理由
まだMiniDV資産（動画テープ）を持っているクリエイターや、FireWire接続の古いオーディオ機器／HDDを活用したい技術者にとって、手頃な自作ソリューションでテープ資産を保全・現代的ワークフローに取り込めるからです。中古の専用MRUは数万円〜数十万円するため、コスト面でも魅力があります。

## 詳細解説
- ハードウェア要点
  - 使用例：Raspberry Pi 5（4GBで十分）、Computer Equipment GroupのFirehat、PiSugar 3 Plus（5000mAh）、4pin→6pin FireWireケーブル、MiniDVカメラ（例：Canon GL1）。
  - FirehatはPiのGPIO/I2Cを使い、録画ボタン、ブザー、LED、OLED表示で操作状態を表示。試作段階のものは配線補修（bodge wires）がある場合あり。
  - PiSugarを用いるとポータブル化でき、5000mAhで録画条件により約2〜4時間（筆者は64GB microSDへ3時間超を確認）。

- ソフトウェア要点
  - Raspberry Pi OSはデフォルトでLinuxのFireWireサポートが有効でないため、カーネル再構築が必要（FireWireモジュール有効化）。
  - Firehat用ソフトをインストールし、起動時にUIを有効化するとOLEDに状態表示、録画ファイルはユーザーのホーム下のcapturesディレクトリに保存。
  - テープ取り込みはdvgrabが定番。取り込んだファイルはUSBやWi‑Fi経由（scp/rsync/SFTPなど）で転送可能。

- 互換性と代替案
  - 代替はMini PCIe型のFireWireアダプタ（例：StarTechのMini PCIe FireWire）をPiに組み込む「Open MRU」方式。制御はコマンドライン中心になるが安価。
  - 動作確認済みのコントローラは主にTI XIO2213A（Open MRU系）とVIA VT6315N（Firehat系）。他コントローラは未確認のものあり。
  - FireWireネットワークは最大400Mbpsで、Piの有線Ethernetより遅い場合もあるが、オーディオインターフェイスや古いMac接続で有用。
  - Linuxカーネル側のFireWireサポートは少なくとも2029年までは動作見込みだが、それ以降の保証は不確定。

- コストと入手
  - 新規で揃えると概ね$150〜$200相当（部品や輸入で変動）。専用の中古MRUを買うより安価に済むケースが多い。
  - Firehat/equip-1はCrowd Supply等での流通を予定（在庫や出荷状況に注意）。

## 実践ポイント
- 今すぐ：手元のMiniDVテープをデジタル化したければ、FirehatかMini PCIe＋StarTechの組み合わせどちらかを選ぶ。
- 必要機材：Raspberry Pi 5、Firehat（またはMini PCIeアダプタ＋カード）、PiSugar等のバッテリ、MicroSD（録画先）、dvgrab。
- ソフト手順（概略）：
  1. Pi用にFireWireモジュール有効でカーネル再構築。
  2. Firehatソフト（Equip-1セットアップ）をインストール・起動。
  3. カメラ接続→OLEDで認識を確認→dvgrabで録画／capturesに保存。
  4. 保存ファイルをUSB/Wi‑Fiでバックアップ。
- 注意点：使用するFireWireコントローラの互換性を事前確認。長期保管のためにも早めにテープをデジタル化しておくこと。

古い映像資産を手軽に救出したい日本のクリエイターやAV好きにとって、有用で実践的なDIYアプローチです。
