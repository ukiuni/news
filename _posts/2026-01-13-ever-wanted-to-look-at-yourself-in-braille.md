---
layout: post
title: "Ever wanted to look at yourself... in Braille? - 自分を点字で見てみたいですか？"
date: 2026-01-13T18:47:02.769Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/nishantJoshi00/dith"
source_title: "GitHub - NishantJoshi00/dith"
source_id: 1016860118
excerpt: "Zig製の軽量ツールでカメラ映像を点字風にリアルタイム端末表示して遊べる"
image: "https://opengraph.githubassets.com/ce7dd730ef62e5475da895cea4a564a96a58f4357cb5c32e12baa8d8c8be1446/NishantJoshi00/dith"
---

# Ever wanted to look at yourself... in Braille? - 自分を点字で見てみたいですか？
魅せるターミナルアート：カメラや画像を“点字（Braille）”風にリアルタイム描画する小気味よいツール

## 要約
Webカメラや画像を読み込み、5種類の古典的ディザリングアルゴリズムで端末にライブ表示する軽量ツール「dith」。Zigで書かれ、依存無し・ネイティブなmacOSカメラ統合を特徴とします。

## この記事を読むべき理由
・ターミナルで手早くビジュアル実験できるので、デザイナーやフロント寄りエンジニアがプロトタイピングに使える。  
・Zigで書かれた実例は、Zig学習者や軽量バイナリを好む開発者にとって良い教材になる。  
・レトロ表現（ドット絵／点字風）やライブビジュアルが日本のイベント・デモやSNS向けコンテンツ作りに使いやすい。

## 詳細解説
dithは画像を端末表示向けにディザリング（階調を点やパターンで表現）して出力します。特徴的なのは「端末で見たときに点字（Braille）やドット表現のようになる」点と、カメラを直接取り込める点です。

主なモード（アルゴリズム）と適性：
- edge：輪郭や線画向け。線画の強調に最適。  
- atkinson：高コントラストで昔のMac風の見た目。コントラスト強めの表現に。  
- floyd_steinberg：写真や滑らかなグラデーション向けの古典的拡散ディザ。  
- blue_noise：自然でフィルムのざらつきのような有機的ノイズ感。ポートレートに面白い。  
- bayer：8-bit風の格子パターン、レトロゲームやピクセルアート風の表現に。

主なオプション：
- +threshold=N（0–255）：感度、しきい値で出力の粗さを調整  
- +invert：色反転（白黒を反転）  
- +warmup=N：カメラ用のウォームアップフレーム数（デフォルト3）  
- +strategy=pipelined|direct：カメラ処理の戦略（遅延や背景キャプチャの挙動に影響）

実装と環境：
- 言語：Zig（リポジトリはZig 100%）  
- カメラはネイティブなmacOS統合（カメラソースはmacOS必須）  
- 依存なしで単一バイナリが生成されるため配布や組み込みに向く

ビルドと実行（要 Zig 0.15.1+）：
```bash
git clone https://github.com/nishantJoshi00/dith
cd dith
zig build -Doptimize=ReleaseFast
# バイナリは ./zig-out/bin/dith
./zig-out/bin/dith +source=cam +mode=edge
```

使い方例：
```bash
# カメラを使ってエッジ表示
dith +source=cam +mode=edge

# 画像ファイルをBlue Noiseで処理（反転あり）
dith +source=file +mode=blue_noise +path=portrait.png +invert

# しきい値を下げて線画っぽく
dith +source=file +mode=edge +path=drawing.png +threshold=5
```

制約と注意点：
- カメラ入力は現状macOSのみ。Linux/Windowsではファイル入力が中心になる可能性あり。  
- GUIは無し。端末表示に特化しているため、出力キャプチャや配信用途は別途ツールが必要。

## 実践ポイント
- まずは手元の写真でモードを切り替えて違いを体感する（floyd_steinbergは写真向け、bayerはレトロ）。  
- ライブで使うなら warmup を増やして安定したフレームを取得する。  
- threshold を変えて細部の出し方を調整—低めで線画寄り、高めで粗いアーティファクトが出る。  
- blue_noise はポートレートや映画的な粒状感の演出に使える。SNS用の短い動画を作って拡散するとウケが良い。  
- Zigに慣れたいならソースを読んで、カメラ統合部やディザリング実装を学ぶのに最適。PR歓迎のリポジトリなので改良案があるなら参加してみる。  

興味が湧ったらリポジトリをクローンして、まずは手早くビルド→カメラ／画像で遊んでみてください。軽くて即効性のある表現ツールとして、ハックデーやデモにぴったりです。
