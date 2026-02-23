---
layout: post
title: "QRTape – Audio Playback from Paper Tape with Computer Vision - QRTape：コンピュータビジョンで紙テープから音声再生"
date: 2026-02-23T10:30:11.884Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "http://www.theresistornetwork.com/2021/03/qrtape-audio-playback-from-paper-tape.html"
source_title: "The Resistor Network: QRTape | Audio Playback from Paper Tape with Computer Vision"
source_id: 47120196
excerpt: "段ボールで作る紙テープ×QR再生器がWebカメラでOPUS音声を鳴らす"
---

# QRTape – Audio Playback from Paper Tape with Computer Vision - QRTape：コンピュータビジョンで紙テープから音声再生
紙テープ＋QRコード×Webカメラで「段ボールプレーヤー」が音を鳴らす──レトロな媒体に最新の圧縮とCVを組み合わせたユニークなハック

## 要約
QRコードを連続印刷した紙テープを段ボール製の簡易トランスポートで送ってWebカメラで読み取り、低ビットレートのOPUS音声を再生するプロジェクト。ハードは紙・段ボール中心、要はソフトウェアの組合せで成立している。

## この記事を読むべき理由
レトロな「紙テープ」概念を最新のオーディオ圧縮とコンピュータビジョンで再解釈した実験は、安価な部品でデータ媒体やアート的表現、教育用デモを作るヒントになる。日本のメイカーカルチャーやプロトタイプ用途に刺さるアイデアだ。

## 詳細解説
- 全体構成：OPUSで圧縮した音声ファイルをバイト列に分割→各チャンクをCRC16やシーケンス番号を付けてQRコード化→連続した紙テープに印刷→Webカメラ(zbar)で読み取り→qrtapeツールでデコード→mplayerで再生。
- ハード：紙タオル芯＋段ボールで作る供給/巻取りスプール、走行は小型ステッパ＋Arduinoで1〜2コード/秒程度。センタリングや巻き戻しは改善余地あり。
- 画像符号化：QRは最大177x177モードでMedium ECCを利用。payloadはチャンクごとに固定長（例：2331バイト）にして最後はゼロパッド。
- 誤読対策：QR固有のECCに加えアプリ側でCRC16を付けて二重防御。読み飛ばし許容（音声は小さな時間跳躍で許容）。
- ソフトウェア：zbar（zbarcam）でカメラ出力をバイナリで吐き、qrtapeで組み立て、mplayerでストリーム再生。QR生成はqrencode、印刷はBrother QLシリーズなどで自動連続印刷。
- 重要ポイント：OPUSの可変ビットレート（例：12kbps VBR）を使うことで低容量で比較的良好な音質を達成。

## 実践ポイント
- 必須部品：Arduino（ステッパ駆動）、小型ステッパ、Webカメラ（近接フォーカスできるもの）、高解像度印刷できるプリンタ（Brother QL等）、紙テープ素材。
- 主要コマンド例（原著の手順を要約）：

```bash
# OPUSでエンコード
opusenc --discard-comments --framesize 60 --bitrate 12 input.flac output.opus
```

```bash
# ファイルをチャンク化（qrtapeツールを使用）
qrtape --encode -s 2331 --input output.opus -p prefix_
```

```bash
# QR化（qrencode）
for i in {0..156}; do qrencode -8 -m 0 -s 16 -l M -r prefix_$i.bin -o prefix_$i.png; done
```

```bash
# 再生用パイプライン（zbarcam -> qrtape -> mplayer）
zbarcam /dev/video0 --raw -Sqrcode.enable -Sbinary | ./qrtape -d -s 2331 --allow-skip | mplayer -
```

- 日本での応用例：メイカーワークショップの教材、アート展示（物理的メディア×デジタル再生）、災害時の低帯域伝送デモ、教育目的での情報符号化実験に向く。
- 改善案：テープのセンタリング機構、両側モータでの巻き戻し、ソフトの閉ループ速度制御、カメラ/照明最適化でスループット向上。

短く言えば、安価な部材と既存ソフトを組み合わせるだけで「動く」試作品が作れ、アイデア次第で芸術・教育・プロトタイピングに広がる。興味があればオープンソースのqrtapeや各種ツールを試してみると良い。
