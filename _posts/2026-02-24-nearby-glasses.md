---
layout: post
title: "Nearby Glasses - 近くのスマートグラス検出"
date: 2026-02-24T19:36:18.707Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/yjeanrenaud/yj_nearbyglasses"
source_title: "GitHub - yjeanrenaud/yj_nearbyglasses: attempting to detect smart glasses nearby and warn you"
source_id: 47140042
excerpt: "満員電車やカフェで近接スマートグラスを検出し顔撮影の懸念を可視化するアプリ"
image: "https://opengraph.githubassets.com/fd89ace78ce6c1305ea07ae1b0e61eed6e5e92f5dc57aad5c22ee6acb569ba57/yjeanrenaud/yj_nearbyglasses"
---

# Nearby Glasses - 近くのスマートグラス検出
電車やカフェで「見られている？」を可視化する—スマートグラス検出アプリの実用ガイド

## 要約
Nearby Glassesは、Bluetooth LEの広告パケットに含まれる「メーカーID」を手掛かりにスマートグラスを検出し、近くにあれば通知するオープンソースAndroidアプリです。誤検知や検出漏れの可能性があるため、まずは「気づき」を得るためのツールと考えてください。

## この記事を読むべき理由
日本の満員電車や飲食店など人が密集する場所では、「カメラ搭載デバイスによる撮影・顔認識」への不安が高いです。本アプリはプライバシー意識の高い人向けに近接する可能性のあるスマートグラスを知らせ、行動判断の助けになります。

## 詳細解説
- 検出手法：BLE広告（ADV）パケットのManufacturer Specific Dataに含まれるBluetooth SIG割当のCompany IDを利用。MACランダム化やサービスUUIDの非永続性のため、デバイス名やUUIDでは安定検出できないケースが多く、メーカーIDが現状で最も実用的。
- 既定で検出対象となるCompany ID（例）：
  - 0x01AB（Meta Platforms, Inc.）
  - 0x058E（Meta Platforms Technologies, LLC）
  - 0x0D53（Luxottica Group S.p.A.／Ray-Ban）
  - 0x03C2（Snapchat, Inc.／Spectacles）
  ただし同じメーカーのVRヘッドセットなど他製品も含むため誤検知あり。
- RSSI（受信信号強度）による「近さ」判定：デフォルト閾値は -75 dBm。
  - 参考距離（開放空間概算）：-60 dBm ≈ 1–3 m、-70 dBm ≈ 3–10 m、-80 dBm ≈ 10–20 m  
  屋内では距離は短くなります。RSSIは電波環境・障害物で大きく変動します。
- 動作と設定：フォアグラウンドサービスで持続スキャン、通知クールダウン（デフォルト10秒）、デバッグログのエクスポート、独自のCompany ID上書きが可能。
- プライバシー：アプリ自体は位置情報やテレメトリを収集しない設計。ログは端末内にのみ保存。ライセンスはPolyForm Noncommercial License 1.0.0。

## 実践ポイント
- インストール：GitHub ReleasesのAPKか、将来的にはPlayストア版を利用。権限（Bluetooth、必要に応じて位置）を許可する。
- 推奨設定：Foreground ServiceをON、RSSI閾値は初期の -75 dBmのまま様子を見る。通知クールダウンは10秒。
- 調整：誤検知が多いなら閾値を下げる（より近いものだけ通知）。特定メーカーを追加したければCompany IDを上書き。
- 運用上の注意：あくまで「気づき」を与える補助ツール。誤検知や検出漏れがあるため、人に対して即断・行動（挑発や追跡など）は絶対にしないこと。ソースが公開されているためコードを確認して自分で安全性を確かめるのも有効です。

短く言えば、Nearby Glassesは「スマートグラスの存在を察知して注意喚起するためのオープンソースの試作ツール」です。日本の公共空間でのプライバシー不安を可視化する一助として、まずは自分の端末で試してみる価値があります。
