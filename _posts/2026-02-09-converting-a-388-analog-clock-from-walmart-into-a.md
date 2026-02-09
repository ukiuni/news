---
layout: post
title: "Converting a $3.88 analog clock from Walmart into a ESP8266-based Wi-Fi clock - Walmartの$3.88アナログ時計をESP8266でWi‑Fi時計に改造する"
date: 2026-02-09T17:45:47.552Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/jim11662418/ESP8266_WiFi_Analog_Clock"
source_title: "GitHub - jim11662418/ESP8266_WiFi_Analog_Clock: Uses an ESP8266 module and an Arduino sketch to display the local time on a inexpensive analog quartz clock."
source_id: 46947096
excerpt: "たった数百円のアナログ時計をESP8266でWi‑Fi NTP同期のスマート時計に改造する手順"
image: "https://opengraph.githubassets.com/1965181cf80c55d90ae92c4780378e46fda65052336f60aad76cb09e22fb2e94/jim11662418/ESP8266_WiFi_Analog_Clock"
---

# Converting a $3.88 analog clock from Walmart into a ESP8266-based Wi-Fi clock - Walmartの$3.88アナログ時計をESP8266でWi‑Fi時計に改造する
魅力タイトル：たった数百円の壁掛け時計をWi‑Fi対応の「時を覚える」スマート時計に改造してみないか？

## 要約
ESP8266（WEMOS D1 Mini）と小型EERAMを使い、安価なクォーツ式アナログ時計の駆動を制御してNTPで時刻同期するDIYプロジェクト。15分ごとにNTP同期し、停電復帰時も時刻を復元する仕組みを備える。

## この記事を読むべき理由
安価なアナログ時計をIoTデバイスに変える実践的なハード／ソフトの知見が得られる。日本でも多くの現場や家庭にあるアナログ時計を活用でき、電子工作や時間同期を学ぶ入門教材として最適。

## 詳細解説
- ハードウェア：WEMOS D1 Mini（ESP8266）＋Microchip 47L04（4KbitシリアルEERAM）＋改造したクォーツムーブメント。ムーブメントのLavetモータのコイル端子に配線を直付けして制御する。  
- ムーブメント改造：ムーブメントを開け、クォーツ発振子からコイルを切り離してコイル両端に配線をハンダ付けする。コイルの線は髪の毛より細く非常に脆いので慎重に扱う。  
- 駆動方式：ESP8266はコイルに対して双極性パルス（正負交互）を与え秒針を1刻み進める。逆戻しはできないため、時計が先行している場合は「待つ」戦略を取る。ムーブメント固有の特性で最適なパルス幅が変わるので、スケッチ中のPULSETIME（例：30ms）を調整する。  
- 時刻同期：NTPサーバーから時刻を取得し、15分ごとに再同期。夏時間対応機能も実装されている（日本では不要だが海外用途で有用）。日本向けには ntp.nict.jp など地域のNTPに設定すると良い。  
- 状態保存：時計の針位置はEERAMに毎秒保存。ESP8266がリセット・停電してもEERAMから最後の位置を復元して継続動作できる。  
- 初期設定／監視：初回はESP8266が配信する簡易Webページで針の初期位置を入力。稼働中は状態ページ（SVG／Canvas／テキスト表示の切替）で動作確認できる。  
- 実装上の注意：ESPのGPIOだけでコイルを直接駆動すると電流や保護の面で危険な場合がある。必要に応じてトランジスタやHブリッジを介して駆動回路を組むことを推奨。

## 実践ポイント
- 部品リスト（最小構成）：WEMOS D1 Mini（ESP8266）、Microchip 47L04 EERAM、配線用リード、必要ならトランジスタ／Hブリッジ、安価なアナログ時計。  
- 作業順：ムーブメント分解→コイル配線→駆動回路組立（保護回路含む）→ESP8266にスケッチ書き込み→初回Webで針位置設定→NTP同期・PULSETIME調整。  
- 調整ポイント：PULSETIMEを±数ms単位で調整して確実に「1ステップ」動くようにする。コイル線の取り扱いは慎重に。  
- 日本向けの応用例：オフィスの壁時計をネットワーク時刻に合わせる、工房や店舗の見た目をそのままにスマート化、電子工作の教材としての導入（学生や社内ハンズオン）。  
- セキュリティ／運用：ローカルNTP／タイムサーバーを使う、ESPのWi‑Fi設定は適切に管理。停電での挙動を事前に確認しておく。

元リポジトリは機能がまとまっており、初心者でも段階的に取り組める実装例になる。興味があれば日本語での回路図説明や部品の入手先も案内可能。
