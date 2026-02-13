---
layout: post
title: "A Deep Dive into Apple's .car File Format - Appleの .car ファイル形式を深掘りする"
date: 2026-02-13T19:11:10.295Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dbg.re/posts/car-file-format/"
source_title: "A Deep Dive into Apple's .car File Format · DBG.RE"
source_id: 748973994
excerpt: "Xcodeが作る.carの構造と画像復元手順を詳述し図解で解説"
---

# A Deep Dive into Apple's .car File Format - Appleの .car ファイル形式を深掘りする
Xcodeがビルドで作る資産バイナリ(.car)を“分解”して中身をブラウザで覗く方法 — 初心者でもわかる核心ガイド

## 要約
Appleアプリが配布する資産は.xcassetsからコンパイルされて.appに含まれるバイナリ .car に格納される。本稿はその内部構造（BOMコンテナ、CARHEADER、KEYFORMAT、RENDITIONSのB+ツリー、CSI＝Core Structured Image など）をわかりやすく解説する。

## この記事を読むべき理由
- iOS/macOSアプリの画像・色・アイコンの実体を理解すると、デバッグ・セキュリティ調査・独自ツール開発に直結するため。  
- 日本の開発現場でもXcode依存を減らすツールや解析が求められており、本知見は実務的価値が高い。

## 詳細解説
- 基盤（BOM）：.car は BOMStore という古い「Bill of Materials」コンテナで始まる。ファイルの先頭に "BOMStore" マジックがあり、ヘッダでブロック数やインデックス位置を持つ。ブロックは (offset,length) ペアでランダムアクセス可能。  
- Named Blocks：代表的なブロックに CARHEADER（カタログ全体のメタ情報）、KEYFORMAT（各アセットのキーに含まれる属性の並び定義）、EXTENDED_METADATA などがある。  
- CARHEADER：小端（little-endian）で格納される固定長（約436バイト）のメタデータ。CoreUIバージョン、storageVersion、renditionCount、UUID、ツール文字列などを含む。  
- KEYFORMAT：各レンディションキーがどの属性（例：idiom＝iPhone/iPad、scale＝@2x、appearance＝Dark/Light、identifier など）をどの順で持つかを定義する。属性値は通常 uint16_t で格納され、キー長は属性数×2バイト。古いフォーマット互換性のチェックもある。  
- RENDITIONS（B+ツリー）：実際のアセット索引は B+ ツリーで管理。キーがレンディション属性の組（KEYFORMATに準拠）で、値が CSI（画像など実データ）を指すブロックID。ツリーノードはヘッダ（isLeaf, count, forwardLink, backwardLink）を持ち、葉ノードは forwardLink で連結され連続走査が速い。  
- CSI（Core Structured Image）：各アセットのペイロードを格納するブロック。CSIヘッダには pixelFormat（'ARGB','JPEG','DATA' 等、offset 24）、layout/rendition type（offset 36, uint16）、幅・高さ・scale（scaleは整数で倍率×100）などが含まれる。レンディションの種類に応じてピクセルデータ、圧縮（例：lzfse）やパレット形式などで格納される。  
- 実装メモ：上記解析は逆コンパイルと実装から導かれており、著者はWASMにコンパイルした独自パーサを作成してブラウザで動かしている（サーバへアップロード不要の対話デモあり）。

## 実践ポイント
- まず公式ツールで中身確認：macOSの assetutil -I Assets.car は JSON ダンプを出すので手始めに有効。actool はコンパイル側で使われる。  
- 自作解析フロー（優先度順）：
  1. BOM ヘッダを読んでブロックインデックスと変数テーブルを取得。  
  2. KEYFORMAT ブロックを解析してレンディションキーの属性順を決定（属性は uint16_t）。  
  3. RENDITIONS B+ツリーを走査：左端の葉へ降り、葉のエントリを順次読み forwardLink を追う。  
  4. 各エントリの valueBlockID から CSI ブロックを取得し、CSIヘッダ（pixelFormat, layout, width, height, scale 等）に従ってデータを復元。  
  5. 圧縮（lzfse等）や特殊フォーマット（KCBC, CELM 等）に対応する処理を用意する。  
- 注意点：エンディアン差（BOMはbig-endian、CARHEADERはlittle-endianの混在）や KEYFORMAT のバージョン差、属性ID最大値チェックを必ず行う。  
- 活用例：アセットの抽出・差分検査、アプリのテーマや解像度別画像の調査、CIでの自動検証ツール作成、ブラウザ上での安全な解析（WASMを使えばローカルで完結）。

以上を踏まえれば、.car の内部は「順序付けられた属性キー → ブロック参照」の組合せで管理されており、正しくパーサを実装すれば Xcode に依存しない資産ツールが作れる。
