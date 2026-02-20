---
layout: post
title: "Reading the undocumented MEMS accelerometer on Apple Silicon MacBooks via iokit - AppleシリコンMacBookの未公開MEMS加速度計をiokitで読み取る"
date: 2026-02-20T07:56:55.482Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/olvvier/apple-silicon-accelerometer"
source_title: "GitHub - olvvier/apple-silicon-accelerometer: reading the undocumented mems accelerometer on apple silicon macbooks via iokit hid"
source_id: 47084000
excerpt: "AppleシリコンMacの未公開加速度計をiokitで読み心拍検出まで可能にする手法"
image: "https://repository-images.githubusercontent.com/1161415745/b2755726-3964-4bfa-942c-19de5583e0fd"
---

# Reading the undocumented MEMS accelerometer on Apple Silicon MacBooks via iokit - AppleシリコンMacBookの未公開MEMS加速度計をiokitで読み取る
トラックパッド裏に隠れた“振動センサ”を覗く：MシリーズMacで未公開の加速度データを取り出す方法

## 要約
AppleSPU（Sensor Processing Unit）配下の未公開MEMS加速度センサをiokit/HID経由で読み取り、心拍（BCG）などの振動検出デモを動かすオープンソース実装。root権限で動作し、実験的・非公式な手法です。

## この記事を読むべき理由
- AppleシリコンMac（M1/M2/M3/M4系）に内蔵されたセンサをソフト的に利用する手法は日本の開発者や研究者にとって新しく、振動センシングや装置側のセンシング応用でアイデアが広がるため。

## 詳細解説
- デバイス情報  
  - iokitレジストリ上のデバイス名：AppleSPUHIDDevice  
  - ベンダー使用ページ/usage：vendor page 0xFF00, usage 3  
  - ドライバ：AppleSPUHIDDriver（SPUに所属）

- アクセス方法（技術要点）  
  - IOHIDDeviceCreateでデバイスを開き、IOHIDDeviceRegisterInputReportCallbackで非同期コールバックを登録。  
  - 受信されるHIDレポートは22バイト長。X/Y/Zはそれぞれint32リトルエンディアンで、バイトオフセットは6, 10, 14。値を65536で割ると[g]単位の加速度になる（raw / 65536 → g）。  
  - サンプリング/コールバック頻度についてはリポジトリで「~800Hz」との記載がある一方で、観測上は約100Hz程度のコールバックになるとの注記もあり、環境やドライバ挙動で変わる可能性あり。

- 実装構成（リポジトリ）  
  - spu_sensor.py：iokitバインディング、デバイス探索、HIDコールバック、共有メモリリングバッファ（再利用しやすいコア実装）。  
  - motion_live.py：振動検出パイプライン（BCGフィルタ0.8–3Hz、自己相関でBPM推定）、ターミナルUI、メインループ。  
  - ライセンス：MIT。動作確認はMacBook Pro M3 Pro（macOS 15.6.1）、Python 3.14で実施。

- 注意点  
  - 非公開APIへのアクセスであり将来のmacOSアップデートで動かなくなる可能性あり。  
  - sudoが必要（iokit HIDデバイスへのアクセス権限のため）。  
  - 医療用途ではない（BCGデモは実験的）。

## 実践ポイント
- 環境確認（デバイス存在確認）:
```bash
ioreg -l -w0 | grep -A5 AppleSPUHIDDevice
```
- 動かし方（リポジトリをクローンしてデモ実行）:
```bash
git clone https://github.com/olvvier/apple-silicon-accelerometer
cd apple-silicon-accelerometer
pip install -r requirements.txt
sudo python3 motion_live.py
```
- すぐ使える応用アイデア：  
  - spu_sensor.pyを流用して簡易的な動き検出、振動解析、机上の触感センシングプロトタイプを作る。  
  - BCGデモは腕をトラックパッド付近に置いて10–20秒待つと心拍由来の微小振動が観測できる可能性あり（不安定・実験的）。

注意：非公開経路のため自己責任で。商用や医療用途への利用は避けること。
