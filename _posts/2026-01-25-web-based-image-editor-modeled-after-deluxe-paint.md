---
layout: post
title: "Web-based image editor modeled after Deluxe Paint - Deluxe Paintを模したWebベースの画像編集ツール"
date: 2026-01-25T15:38:36.639Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/steffest/DPaint-js"
source_title: "GitHub - steffest/DPaint-js: Webbased image editor, modeled after the legendary Deluxe Paint with a focus on retro Amiga file formats: read and write Amiga icon files and IFF ILBM images"
source_id: 46753708
excerpt: "Deluxe Paintを再現、ブラウザで動く本格ドット絵エディタ"
image: "https://opengraph.githubassets.com/ddb054ff4018bc35943070ae53adb3dc8f9ed201941d08d98f96aab70510bfa5/steffest/DPaint-js"
---

# Web-based image editor modeled after Deluxe Paint - Deluxe Paintを模したWebベースの画像編集ツール
レトロなAmiga感をブラウザで――あのDeluxe Paintを再現したDPaint.jsで“ドット職人”になろう

## 要約
DPaint.jsはDeluxe Paintを模したブラウザ上の画像編集器で、AmigaのIFF/ILBMやアイコン形式の読み書き、レイヤーやマスク、細かいディザリング、カラ―サイクリングなどレトロ表現に強い機能を備えています。完全なクライアント実行（純粋なES6 JavaScript、依存なし）でオフライン利用も可能です。

## この記事を読むべき理由
レトロゲームやピクセルアート、ノスタルジックなUI素材が注目される今、実機互換のファイル入出力や色数制限下での表現（ディザ／カラーパレット管理）をブラウザだけで実験・制作できるツールは、日本のインディー開発者・ドット絵クリエイターに即戦力になります。

## 詳細解説
- コア機能：レイヤー、選択ツール、マスキング、変形、エフェクト、複数段階のUndo/Redo、他アプリからのコピペ対応。  
- レトロ特化：Amigaアイコン（全フォーマット）やIFF ILBM（HAM含む24bit読み、最大256色出力）を読み書き。ディスクイメージ（ADF）からの読み書きや、組み込みのAmigaエミュレータで実機表示をプレビュー可能。  
- カラーワーク：色数削減に特化した細かなディザ設定、カラ―サイクリング機能で静止画の擬似アニメ表現が可能。Amiga/Atariの低ビットカラー制限（OCS/ECSやSTモード）もサポート。  
- 実装と配布：100%プレーンなES6モジュールで依存無し。index.htmlをWebサーバで配ればそのまま動作。オプションでParcelを使ったビルド（npm install → npm run build）で配布用に縮小可能。MITライセンス。  
- 注意点：Braveブラウザの「farbling」による表示ノイズの問題あり（回避推奨）。

## 実践ポイント
- まず試す：オンライン版 https://www.stef.be/dpaint/ を開いて操作感を確認。  
- ローカルで使う：リポジトリを落とし、簡易HTTPサーバ（python -m http.server等）でindex.htmlを配信すればオフラインで動作。  
- 開発ワークフロー：npm install → npm run build で最適化ビルドを作成。ゲームアセット制作やレトロ変換の前処理に組み込みやすい。  
- 活用例：インディーゲームのパレット最適化、ドット絵制作、古いAmiga資産の保存・変換、学習教材としての色数制限表現の理解。  
- 貢献：現在はアルファ段階。バグ報告やPRで改善に参加可能（GitHubリポジトリ参照）。

興味があるならまずオンライン版を触ってみて、プロジェクトをフォークして日本のコミュニティ向けテンプレートやチュートリアルを作ると面白い発展が期待できます。
