---
layout: post
title: "MeshTNC is a tool for turning consumer grade LoRa radios into KISS TNC compatible packet radio modems - 消費者向けLoRaラジオをKISS TNC互換パケット無線機に変えるMeshTNC"
date: 2026-02-22T00:30:16.351Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/datapartyjs/MeshTNC"
source_title: "GitHub - datapartyjs/MeshTNC: MeshTNC is a tool for turning consumer grade LoRa radios into KISS TNC compatible packet radio modems"
source_id: 1068698304
excerpt: "安価なLoRa機器をKISS TNC化しAPRS/AX.25で簡単にローカルMesh網を構築"
image: "https://opengraph.githubassets.com/feb101d93cdfe9300dba8b30ed0047d8ef949c15366cdffd84cf6d9241fc8f0f/datapartyjs/MeshTNC"
---

# MeshTNC is a tool for turning consumer grade LoRa radios into KISS TNC compatible packet radio modems - 消費者向けLoRaラジオをKISS TNC互換パケット無線機に変えるMeshTNC
手元の安価なLoRaモジュールが、そのままAPRSやAX.25、イーサネット風の無線リンクになる――MeshTNCで広がるローカル無線ネットワークの可能性

## 要約
MeshTNCは、MeshCore対応の市販LoRa機器に組み込んで「KISS TNC」互換のパケット無線モデムとして使えるオープンファームウェア／ツール群です。シリアルCLI、KISSモード、パケットログ、BLEスニッフィングなどを備え、APRSやAX.25、イーサネット風接続が可能になります。

## この記事を読むべき理由
日本でも災害時通信やローカルコミュニティの低消費電力ネットワーク構築、ハム無線のデジタル実験などでLoRaを活用する需要が高まっています。MeshTNCは既存の安価なLoRa機器を手早くパケット無線化でき、実用的な応用がすぐ試せます。

## 詳細解説
- コア機能  
  - シリアルCLI（デフォルト115200baud）から各種設定や生データ送信（txraw）が可能。LoRaパケットはシリアルへ16進でログ出力でき、BLEパケットのスニッフィングもサポートします。  
  - KISSモードを有効にすると、一般的なTNC対応ソフトやLinuxのAX.25スタックと連携可能。これによりAPRSクライアントやAX.25ルーティング、tncattachを使った「イーサネット風」接続が実現します。  
- ハードウェアと導入方法  
  - MeshCore対応デバイス（リポジトリのvariants参照）で動作。ビルドはPlatformIO（VS Code）で可能、あるいはリリースのバイナリをフラッシュ。公式のmeshcore flasherも利用可能です。  
- 代表的なユースケースとコマンド例  
  - シリアル接続例（Linux）:
```bash
# minicomで接続
minicom -b 115200 -D /dev/ttyACM0
# 退出してKISSモードに入れる
serial mode kiss
```
  - KISS終了（CLIに戻す）:
```bash
echo -ne '\xC0\xFF\xC0' > /dev/ttyUSB0
```
  - AX.25とIP割当（概念）: kissattachでmkissインタフェースを作り ip addr でIPを設定すれば、LoRa経由でpingが通ります。  
  - イーサネット風接続: tncattachを使いMTUやIPv4を指定して仮想ネットワークを構築できます（tncattachリポジトリ参照）。  
- 技術的ポイント  
  - 無線パラメータ（周波数、帯域幅、スプレッディングファクタ、符号化率、syncword）はCLIで設定可能（set radio）。これらが一致しないと通信できないため、ノード間で厳密に合わせる必要があります。  
  - KISS対応により既存のAPRSクライアント（xastir等）やLinux側のAX.25ツール群と直接連携でき、アプリケーションの幅が広がります。

## 実践ポイント
- まずはMeshCore対応機を選ぶ（リポジトリのvariantsを確認）。  
- 法令順守：国内で使う周波数帯域・送信出力は日本の電波法に従う（920MHz台など、用途と免許要否を確認）。  
- 最初は近距離・低速設定で動作確認（同一周波数・SF等を合わせる）。  
- APRSやAX.25の実験から始め、tncattachでIP疎通（ping）を確認してから応用を拡大する。  
- 設定やファーム書き換え前に現在の設定のバックアップを取る。  
- 災害時のローカル通信やコミュニティMesh、IoTトンネリングなど日本の現場用途での応用を検討する。

（詳細・ビルド、リリース、サンプルは公式リポジトリ：https://github.com/datapartyjs/MeshTNC を参照してください）
