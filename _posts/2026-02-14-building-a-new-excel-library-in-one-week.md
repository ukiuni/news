---
layout: post
title: "Building a New Excel Library in One Week - 1週間で作られた新しいExcelライブラリを作る話"
date: 2026-02-14T15:07:53.587Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://hackers.pub/@nebuleto/2026/en-us-sheetkit-in-one-week"
source_title: "Building a New Excel Library in One Week"
source_id: 805439890
excerpt: "1週間で作られたRust製SheetKitで、大量Excel処理を高速かつ低メモリで実現"
image: "https://hackers.pub/@nebuleto/2026/en-us-sheetkit-in-one-week/ogimage?l=en"
---

# Building a New Excel Library in One Week - 1週間で作られた新しいExcelライブラリを作る話
1週間で生まれた“超実用”Excelライブラリが、あなたの大量データ処理を劇的に変える理由

## 要約
TypeScript/Node.js向けにRustで書かれたSheetKitは、短期間で開発された高速・低メモリなOOXML（.xlsx等）ライブラリで、バッファIO・ストリーミング・遅延読み込み・Copy-on-Writeなどを備えています。

## この記事を読むべき理由
日本の企業でも大量のExcelテンプレート生成やアップロード処理が頻繁にあり、既存のJSライブラリは機能不足や性能問題に悩まされがち。SheetKitはその課題に対処する現実的な選択肢を提示します。

## 詳細解説
- 何なのか  
  - SheetKitはRustコア＋Node.jsバインディング（napi-rs）で動くOOXMLライブラリ。ZIP化された.xlsxを開き、XMLパートをRust構造体にデシリアライズして編集・保存します。BunやDenoでも動きます。

- 開発の流れ（1週間での主要進展）  
  - v0.1.x: MVP（大量の機能を実装、まずはファイルパスベースの入出力）  
  - v0.2.x: バッファI/O追加（メモリ上で読み書き）  
  - v0.3.x: 生バッファ（raw buffer）プロトコル導入でFFI越しのオブジェクト生成を削減  
  - v0.4.x: 機能ギャップ埋め（チャートや検証等）  
  - v0.5.0: アーキテクチャ見直し（遅延読み込み・ストリーミング・COW保存）

- 主要技術ポイント（初心者向けに平易に）  
  - なぜ高速化できたか：従来は「セルごとにJSオブジェクト」を作ってFFIで渡していたが、これだとGCとメモリが爆発。代わりにシート全体を効率的なバイナリにシリアライズして一度だけ渡す方式を採用し、JS側でパースする（行単位の増分デコードも可能）。  
  - メモリ削減例：あるケースでRSSが361MB→13.5MBに。  
  - 読み込みモード：  
    - lazy（デフォルト）：メタ情報だけ読み、シートは初アクセスで解析。  
    - eager：全解析（従来型）。  
    - stream：順方向のみ、バッチ単位で処理できる（大ファイル向け）。  
  - Copy-on-Write保存：テンプレートを少しだけ書き換えて返す場面で、解析→再構築を避けて未変更のZIPエントリをそのまま通すことで高速化・メモリ節約。  
  - ベンチ結果：同条件でJS専用ライブラリより読み書きが2〜3倍速いケースや、NodeバインディングがネイティブRustより速くなるシナリオも（V8の文字列処理が効いているため）。

- 注意点と互換性  
  - ベンチでの比較ルールを厳格化（行数・セル数の一致、既知座標の値確認）して、他ライブラリの「ゼロを返して高速に見える」問題（欠落要素のパース失敗による誤結果）を検出・回避しています。  
  - まだ実験段階のAPI変化の可能性あり。

## 実践ポイント
- 大量行/列を扱うサーバ処理なら、まず試す価値あり（sheetkit.devでGetting Started）。  
- テンプレートを開いて一部だけ編集して返す用途は lazy + COW save が最適。  
- メモリに乗らない巨大ファイルは stream モードでバッチ処理（for await の例あり）を採用。  
- Node環境でBuffer I/Oを使えばファイル系処理がファイルシステム依存から外れ、サーバレスにも向く。  
- 導入前に既存の処理でベンチを取り、SheetKitのread/writeモードを選んで比較すること（互換性チェックを忘れずに）。

（参考）短期間での開発はエージェントを使った実装分担と綿密な設計が鍵。日本の現場ではテンプレ生成・BIパイプライン・フィンテック等で即戦力になり得ます。
