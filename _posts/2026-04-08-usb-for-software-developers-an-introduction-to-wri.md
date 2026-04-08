---
layout: post
title: "USB for Software Developers: An introduction to writing userspace USB drivers - ソフトウェア開発者のためのUSB: ユーザー空間USBドライバ作成入門"
date: 2026-04-08T20:23:21.807Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://werwolv.net/posts/usb_for_sw_devs/"
source_title: "USB for Software Developers | WerWolv"
source_id: 47695012
excerpt: "libusbでカーネルを触らずAndroid等のUSB機器を検出・問い合わせし制御する実践ガイド"
image: "https://werwolv.net//_astro/cover.D_ljJUxi.png"
---

# USB for Software Developers: An introduction to writing userspace USB drivers - ソフトウェア開発者のためのUSB: ユーザー空間USBドライバ作成入門
カーネルを触らずにUSB機器を制御する — libusbで始める実践ガイド

## 要約
ユーザー空間からlibusbを使ってUSB機器を列挙・問い合わせ・データ授受する基本を、Android端末（fastboot）を例にやさしく解説する入門記事。

## この記事を読むべき理由
USB機器のドライバは必ずしもカーネルモードで書く必要はなく、ユーザー空間で安全に開発・デバッグできる。日本のAndroid開発者や組み込み・IoTエンジニアが短時間で実機を触り始められる実践的な知識が得られる。

## 詳細解説
- USBの基本概念：ホストが接続直後に「列挙（enumeration）」して機器が送るデバイス識別情報（VID/PID）や各種デスクリプタを取得する流れ。OSはDevice ClassやVID/PIDでドライバを決定する。
- エンドポイントと制御転送：Endpoint 0（Control endpoint）は常に存在し、GET_STATUSやGET_DESCRIPTORといった標準リクエストで機器の情報を取得する。エンドポイントは端末の「ポート番号」のようなもの。
- libusbの役割：ユーザー空間向けに汎用ドライバを提供し、アプリから機器をクレームして直接通信可能にする。カーネルドライバが割り当てられている場合はlibusb_detach_kernel_driverで解除できる（Linux）。WindowsではWinUSBが必要で、Zadigで置換することが多い。
- 実例（fastboot端末）：lsusbでVID:PID（例 18d1:4ee0）を確認し、libusbでホットプラグ検知→open→libusb_control_transferでGET_STATUS/GET_DESCRIPTORを投げてデバイス記述子を取得・解析する手順を示す。
- よく使うツール：lsusb / lsusb -v（詳細デスクリプタ）、ImHex（バイナリ解析）、usbutils、libusbドキュメント、WindowsならUSB Device Tree Viewer / Zadig。

## 実践ポイント
1. まずlsusbで機器を確認：VID/PIDを控える（例: 18d1:4ee0）。  
2. libusbをインストールして簡単なホットプラグ検出プログラムを動かす。簡易例：
```cpp
#include <libusb-1.0/libusb.h>

int hotplug_cb(libusb_context*, libusb_device*, libusb_hotplug_event, void*) {
  puts("Device plugged in!");
  return 0;
}

int main() {
  libusb_context *ctx = nullptr;
  libusb_init(&ctx);
  libusb_hotplug_callback_handle h;
  libusb_hotplug_register_callback(ctx, LIBUSB_HOTPLUG_EVENT_DEVICE_ARRIVED,
    LIBUSB_HOTPLUG_ENUMERATE, 0x18d1, 0x4ee0, LIBUSB_HOTPLUG_MATCH_ANY,
    hotplug_cb, nullptr, &h);
  while (libusb_handle_events(ctx) >= 0) {}
  libusb_hotplug_deregister_callback(ctx, h);
  libusb_exit(ctx);
}
```
3. エンドポイント0へGET_DESCRIPTORでDevice/Config/Interface/Endpoint情報を取得して解析する。データ構造はUSB仕様（DeviceDescriptor等）に従う。  
4. カーネルドライバが邪魔する場合はlibusb_detach_kernel_driver()（Linux）を試す。WindowsではZadigでWinUSBに置換。  
5. 実機でやる際はタイムアウトやバッファ長を適切に設定し、まずは標準リクエスト（GET_STATUS/GET_DESCRIPTOR）から始める。

短時間で「機器を検出して簡単な問い合わせを行う」までの流れが掴めるので、まずは手元のAndroid端末やRaspberry Pi接続機器で試してみてください。
