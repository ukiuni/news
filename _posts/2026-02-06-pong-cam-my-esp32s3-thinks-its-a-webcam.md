---
layout: post
title: "Pong Cam – My ESP32S3 Thinks It's a WebCam - Pong Cam — ESP32‑S3が自分をウェブカメラだと思い込む"
date: 2026-02-06T03:41:34.778Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.atomic14.com/2026/02/01/pong-cam"
source_title: "Pong Cam - My ESP32S3 Thinks It's a WebCam! | atomic14"
source_id: 46845135
excerpt: "ESP32‑S3でカメラ無しUVC仮想カメラを作りPongをMJPEGでUSB配信"
image: "https://www.atomic14.comhttps://img.youtube.com/vi/zhTTmRQLNws/0.jpg"
---

# Pong Cam – My ESP32S3 Thinks It's a WebCam - Pong Cam — ESP32‑S3が自分をウェブカメラだと思い込む

ESP32‑S3を“カメラなし”でUVCウェブカメラに見せかけ、静止画→アニメGIF→リアルタイムPongまでMJPEGでPCへストリーミングする工作プロジェクト。

## 要約
ESP32‑S3のネイティブUSB＋EspressifのUVCコンポーネントで、カメラを接続せずにソフト生成フレームをJPEG化してMJPEGでUSBに流す。最終的にPongを30FPS相当で配信可能にした。

## この記事を読むべき理由
USB UVCを使えばPC側は「普通のウェブカメラ」として扱うため、安価なESP32‑S3でダッシュボード表示・ビジュアライズやデバッグ用の仮想カメラを手早く作れます。日本のIoT/Makerコミュニティや教育用途に実用性高めです。

## 詳細解説
- 基本構成：ESP32‑S3（ネイティブUSB）＋Espressifのusb_device_uvc（TinyUSBベース）でUSB列挙とUVCプロトコルを扱う。ホストと解像度/フレームレート交渉後、MJPEG（連続JPEGフレーム）を送出。
- デモ構成：1) 埋め込み静止JPEG（テストカード） 2) 埋め込みアニメGIFをデコード→JPEG再エンコード→時間に合わせて送出 3) ゲームループで描画→JPEG化→UVC要求に応じて送信（Pong）
- 主要ライブラリ／手法：
  - ESP‑IDF（CMake）でバイナリ資源をEMBED_FILESで埋め込み、アセンブリシンボルで参照。
  - AnimatedGIF（Larry Bank）でGIF解凍、esp_new_jpegでJPEGエンコード。
  - TinyUSB/UVCはMJPEGやH.264をサポート。Isochronousモードで乱れが出たため、作者はmenuconfigでBulkモードに切替えて安定化。
- 性能とタイミング：30FPS目標だと1フレームあたりの時間予算は約 $1000\ \mathrm{ms}/30 = 33\ \mathrm{ms}$。実測ではGIFデコードが約$33\ \mathrm{ms}$、JPEGエンコードは最適化後で約$21$〜$23\ \mathrm{ms}$。ホストのフレーム要求に応じてESP32がフレームを用意することで実現。
- 実装の肝：UVC用のフレーム取得コールバック（fb_get_cb）がJPEGデータを返す。ホストがペースを取るのでループは「要求待ち→描画→エンコード→送信」の順。

簡単なコールバック例（概念）：

```C++
uvc_fb_t *camera_fb_get_cb(void *cb_ctx) {
    // now_us は esp_timer_get_time() などで取得
    memset(&fb_, 0, sizeof(fb_));
    fb_.buf = jpeg_data_;
    fb_.len = jpeg_data_len_;
    fb_.width = FRAME_W;
    fb_.height = FRAME_H;
    fb_.format = UVC_FORMAT_JPEG;
    fb_.timestamp.tv_sec = now_us / 1000000ULL;
    fb_.timestamp.tv_usec = now_us % 1000000ULL;
    return &fb_;
}
```

## 実践ポイント
- 開発環境：ESP‑IDF推奨。EMBED_FILESでJPEG/GIFを埋め込むと楽。
- 転送モード：Isochronousで問題が出たらmenuconfigでBulkに切替えて安定化を試す。
- 画面サイズと品質：320×240程度にリサイズするとフラッシュに入りやすく、エンコード時間も短縮。GIFは事前に最適化（例：ezgif）。
- パフォーマンス管理：JPEGエンコード時間を測定し、描画＋ロジックが残る時間が$33\ \mathrm{ms}$以内になるよう調整。必要なら描画とエンコードを別コアで並列化。
- ハード面の注意：USBデータピンやストラッピングピンの取扱、macOS/Windowsの挙動差をチェック。
- 参考・コード：元プロジェクトのソースを参照（記事のURL）して実装を流用・学習すると早い。

（元記事参照: https://www.atomic14.com/2026/02/01/pong-cam）
