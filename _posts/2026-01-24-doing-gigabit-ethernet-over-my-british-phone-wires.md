---
layout: post
title: "Doing Gigabit Ethernet over My British Phone Wires - 英国の電話線でギガビット・イーサネットを実現する方法"
date: 2026-01-24T10:41:26.754Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://thehftguy.com/2026/01/22/doing-gigabit-ethernet-over-my-british-phone-wires/"
source_title: "Doing Gigabit Ethernet Over My British Phone Wires &#8211; The HFT Guy"
source_id: 46742362
excerpt: "Gigacopperで既存英国電話線を使い配線不要で低遅延かつ実測ギガ級有線化"
image: "https://thehftguy.com/wp-content/uploads/2026/01/photo_gigacopper.png"
---

# Doing Gigabit Ethernet over My British Phone Wires - 英国の電話線でギガビット・イーサネットを実現する方法
家の「電話ジャック」を使って実質ギガビットを出す――配線を引き直さず速度と低遅延を手に入れる英国ハック

## 要約
英国の古い電話配線（RJ11/Cat5）を利用して、Gigacopper製機器で家庭内にギガ級の有線ネットワークを構築した実例。電力線アダプタより安定・高速で、実運用でフルスピード確認済み。

## この記事を読むべき理由
新築でもEthernet配線が入っていない住宅が多い海外事情の中、既存の電話線や同軸を活かして手早く高速有線を実現する手法は、日本でも古い集合住宅や配線改修が難しいケースで役立つ実用的な選択肢を示します。

## 詳細解説
- 背景：電力線アダプタ（HomePlug/G.hn）だとノイズで不安定になる環境が多く、専用の電話線や同軸を使えば理論上ははるかに良好。英国は電話ジャックが家中に残るため需要が高い。
- 製品：Gigacopper G4201TM（電話線側：RJ11、機器側：Gigabit RJ45）。同軸向けのG4201C/G4204CやRJ45をそのまま使うG4202TMもある。
- 性能：PHY表示で ~1713 Mbps、デバイスのデバッグでPHONE 200MHz接続で1385 Mbps。実運用では500 Mbps回線を超える速度をiperf3で確認（USB‑C→Ethernetアダプタ経由でフルスピード）。
- ファーム差分：InHome（最大16機器・ピア間通信・サブms遅延）とClient/Server（ペア構成で帯域分割）あり。用途に合わせてInHome推奨。
- 配線の現実：英国住宅は電話線がデイジーチェーンされていることが多く、マスターソケットや結線が混乱しているためEthernet化が難しいケース多数。機器は2線(SISO)／4線(MIMO)で動作。
- 輸入注意点：E‑commerceで独独から購入可だがVAT・通関手続きや追跡問題あり（英国向け配送後に関税・手数料発生）。

## 実践ポイント
- InHomeバージョンを選ぶ（家庭内複数端末向け、低遅延）。
- 購入前に販売者へ問い合わせて輸送・インボイス処理（VAT除外）を相談する。
- UK標準のBT631A→RJ11ケーブルや電源アダプタ形状に注意。テスト用にUSB‑C→GigEアダプタを用意。
- 既存電話ソケットの配線がデイジーチェーンか確認（マスターソケット探し）。不明なら現地で開けて確認するか専門家へ依頼。
- 同軸がある家ではG4201C/G4204Cを検討。用途はゲームや大容量DLでの低遅延改善が最大メリット。
- 共有媒体である点（帯域分配）と導入コスト・輸入手間を天秤にかけること。
