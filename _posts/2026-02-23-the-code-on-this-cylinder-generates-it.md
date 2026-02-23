---
layout: post
title: "The code on this cylinder generates it - シリンダー上のコードがそれを生成する"
date: 2026-02-23T15:08:15.167Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://youtu.be/wLh1TeC1JI4?si=hsv15xxTbMXZGbfT"
source_title: "The code on this cylinder generates it - YouTube"
source_id: 398568248
excerpt: "円筒に刻まれたコードを読み取って現場で即座に形状を再生成する手法を紹介"
image: "https://i.ytimg.com/vi/wLh1TeC1JI4/maxresdefault.jpg?sqp=-oaymwEmCIAKENAF8quKqQMa8AEB-AG-B4AC0AWKAgwIABABGGUgZShlMA8=&amp;rs=AOn4CLBB5n8I6Bhkx7KEiHG7mjbIR1mmvw"
---

# The code on this cylinder generates it - シリンダー上のコードがそれを生成する
シリンダーに刻まれた“コード”が形を生み出す瞬間──物理とプログラムがつながる新しいモノづくり

## 要約
短い動画タイトルから示唆されるテーマは、物理オブジェクト上の「コード」（文字列やパターン）がそのまま生成プロセスの指示になり、形状や動きを生み出すというアイデアです。これはプロシージャル生成、コード＝データ、物理とデジタルの双方向インタフェースを扱います。

## この記事を読むべき理由
日本の製造・デザイン現場やメーカームーブメントでは、少量多品種やカスタマイズが重要です。物体そのものに再生可能な“設計情報”を埋め込む手法は、現場でのオンデマンド再生成や検証、作品の自己記述性（self-describing objects）に直結します。エンジニア、プロダクトデザイナー、ファブリケーション愛好者は応用の幅を知っておく価値があります。

## 詳細解説
- コア概念
  - コード＝データ：オブジェクト上に刻まれたテキストやパターンを、読み取って解釈することで形状を生成する。プログラム的には「パーサー → ジオメトリ生成 → レンダリング／CAM出力」の流れ。
  - 円筒（シリンダー）特有のマッピング：平面上の指示を円周方向にラップ（円筒座標系）して扱うと、新しいモチーフや繰り返し構造を簡潔に表現できる。
- 代表的な技術スタック（例）
  - 記述言語：簡易DSL（例：命令列で押し出しや回転を指定）、JSON/YAMLなど
  - パーシング／生成：OpenSCAD、Blender（Geometry Nodes）、three.js、OpenJSCAD
  - 読取手段：カメラ＋OpenCVで円筒の展開画像を取得し、OCRや特徴量でコードを抽出
  - 出力：3Dプリント（STL）、CNC用G-code、リアルタイムレンダリング
- 応用例
  - 製品に刻印したコードから現場で同一部品を再生成
  - アート／インスタレーションで「読むと変わる」オブジェクト
  - IoTタグと組み合わせ、物理オブジェクトが自身の設計データを配信

## 実践ポイント
- まず試すなら：OpenSCADで簡単な命令（例：RADIUS=…; EXTRUDE X）を受け取り円筒にマッピングしてみる。
- ツール案内：BlenderのGeometry Nodesでテキスト→ジオメトリ変換、three.jsで円筒UVマッピングを試す。
- OCR／読み取り：スマホで撮影→OpenCVで円筒を展開（cylindrical unwarp）→Tesseractで文字認識。
- 小さなプロジェクト案：短いDSLを作り、紙に印刷して筒に巻き付け、スマホで読み取って3Dモデルを生成して3Dプリントするワークフローを構築してみる。

元動画の具体的な実装を参照する場合は、動画と併せて上記ツールで同様のパイプラインを再現してみてください。
