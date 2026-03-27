---
layout: post
title: "Velxio 2.0 – Emulate Arduino, ESP32, and Raspberry Pi 3 in the Browser - Velxio 2.0 — ブラウザでArduino・ESP32・Raspberry Pi 3をエミュレート"
date: 2026-03-27T22:03:08.290Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/davidmonterocrespo24/velxio"
source_title: "GitHub - davidmonterocrespo24/velxio: Emulate Arduino, ESP32 &amp; Raspberry Pi. in your browser. Write code, compile, and run on 19 real boards — Arduino Uno, ESP32, ESP32-C3, Raspberry Pi Pico, Raspberry Pi 3, and more. No hardware, no cloud, no limits.. Discord: https://discord.gg/rCScB9cG · GitHub"
source_id: 47548013
excerpt: "ブラウザで19種ボードを実機不要で即時エミュレートするVelxio 2.0"
image: "https://opengraph.githubassets.com/7a8ccce276d43a2a504f8bba387b792171d9420f24502b998eb0f62febbc65c9/davidmonterocrespo24/velxio"
---

# Velxio 2.0 – Emulate Arduino, ESP32, and Raspberry Pi 3 in the Browser - Velxio 2.0 — ブラウザでArduino・ESP32・Raspberry Pi 3をエミュレート

実機ゼロで動く！ブラウザ上でマルチボード開発ができる「Velxio 2.0」を使ってみよう

## 要約
Velxio 2.0はブラウザ上でArduino系・ESP32系・Raspberry Pi 3など合計19ボードをリアルCPUエミュレーションで動かせるオープンソースのマルチボードエミュレータです。コード編集・コンパイル・シミュレーション・シリアル監視・コンポーネント接続まで一通りブラウザ内で完結します。

## この記事を読むべき理由
ハードウェアが手元にない、学校や社内でボード配布が難しい、日本語ドキュメントが少ない海外ツールを試したいエンジニア／学生にとって、Velxioは即時検証・学習・CI化ができる強力な代替手段です。日本のプロトタイプ開発やIoT教育現場でコスト削減と学習効率向上に直結します。

## 詳細解説
- サポート範囲：Arduino（Uno/Nano/Mega/ATtiny等）、Raspberry Pi Pico/Pico W、ESP32シリーズ（Xtensa QEMU ベース）、ESP32-C3系（ブラウザ内RISC-V実装）、Raspberry Pi 3（QEMUでRaspberry Pi OS起動）など19ボード、5つのCPUアーキテクチャをカバーします。
- エンジン：avr8js／rp2040js／RiscVCore.tsなどブラウザで動く実機エミュレータと、ESP32やPi等でQEMUベースのバックエンドを組み合わせ、実機に近い挙動を再現します。
- 開発体験：Monacoエディタ（シンタックス、補完）、arduino-cli連携によるコンパイル、ライブシリアルモニタ、48種類以上の仮想コンポーネント（センサやディスプレイ）、ワイヤ配線・ピン注入・オシロスコープなどの可視化ツールを備えています。
- マルチボード・連携：同一キャンバス上で異なるアーキテクチャのボードを接続して通信テストが可能（例：Pi ↔ Arduinoのシリアル通信）。Raspberry Piは実際のOSをブートしてPythonスクリプト実行が可能です。
- オフライン／セルフホスト：velxio.devで即試せるほか、Dockerで簡単にセルフホスト可能。CIでのテスト実行や社内環境での利用に向きます。

## 実践ポイント
- まずは試す：ブラウザで即起動できる https://velxio.dev を開いて、BlinkやSerialの例を動かしてみてください。
- ローカルで動かす（Docker一発）：
```bash
docker run -d --name velxio -p 3080:80 ghcr.io/davidmonterocrespo24/velxio:master
# その後 http://localhost:3080 を開く
```
- 学習・授業利用：ハードなしでワイヤ接続やセンサ入出力を視覚的に学べるため、電子工作やIoT入門教材に最適です。
- プロトタイプ＆デバッグ：複数ボード間のシリアル通信や周辺機能を実機を用意せず検証でき、初期開発コストを削減できます。
- CIへの組み込み：TypeScriptベースのRISC-Vエミュレーションなどはテストランで再現性が高く、自動化に向きます。
- 日本市場での利点：小規模なものづくりコミュニティ、教育機関、企業のPoCでハード調達コストを下げられる点が有益です。

興味があれば公式リポジトリ（https://github.com/davidmonterocrespo24/velxio）とオンラインデモをチェックして、まずは短時間で「動かす」ことをおすすめします。
