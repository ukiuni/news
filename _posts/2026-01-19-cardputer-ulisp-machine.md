---
layout: post
title: "Cardputer uLisp Machine - Cardputer uLisp マシン"
date: 2026-01-19T10:58:37.112Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "http://www.ulisp.com/show?52G4"
source_title: "uLisp - Cardputer uLisp Machine"
source_id: 1036015685
excerpt: "M5Stack Cardputerで携帯Lisp機を作り即プロトできる"
---

# Cardputer uLisp Machine - Cardputer uLisp マシン
手のひらサイズでLispを動かす楽しさ──M5Stack Cardputerで始めるuLispハック

## 要約
M5StackのCardputer（ESP32-S3搭載）にuLispを入れて、ディスプレイと小型キーボードを備えた携帯Lispマシンを作る手順と使いどころを分かりやすくまとめる。

## この記事を読むべき理由
手軽な価格で実機Lisp環境を触れるうえ、IoTや組み込み開発の学習に最適。日本の個人や教育現場でも短時間でプロトタイプや教材として活用できるため、その導入・利用ポイントを押さえておくと役立つ。

## 詳細解説
- ハードウェア概要  
  CardputerはESP32-S3（デュアルコアLX7、Wi‑Fi/BT）を搭載したカードサイズ端末。1.14インチ 240×135のカラーTFT、56キーの小型キーボード、SDカードスロットを持つ。バッテリとバックパックで携帯性も十分。

- uLispとは  
  uLispは組み込み向けのCommon Lispサブセット。数百の関数・特殊形式を備え、リスト・数値・文字列・配列・ストリームなどを扱える。小型デバイス向けにGC（マークリーベース）やシンプルなREPLが実装されている。

- インストールのポイント（要約）  
  1. Arduino IDEの追加ボードにM5StackのURLを追加し、M5Stackコアをインストール。  
  2. M5CardputerライブラリをLibrary Managerから導入。  
  3. Cardputer向けuLispファームウェアを入手し、USB接続でアップロード。  
  4. Macで長いスケッチを貼り付ける際やアップロード失敗時は、背面のG0を押しながらRstでブートローダに入れると安定して書き込みできる（G0→Rstの手順を参照）。

- 主要機能・拡張（Cardputer版uLisp）  
  - 画面：テキストは最大40×16行、フォント切替で30×9行も可能。  
  - キーボード：小型ながら大文字・記号対応。Autocompleteや括弧マッチ機能で入力支援あり。  
  - SDカード：ファイル一覧、画像保存、Lispワークスペースの保存が可能。  
  - グラフィックス：ドット描画やプロット、拡張関数群でTFTに直接描画できる。  
  - 入出力便利関数：get-key（キー待ち）、read-pixel（画面ピクセル読み出し）、save-bmp（画面をBMPで保存）など。  
  - サウンド：内部スピーカーでnote関数を使った音出力が可能。  
  - 画面出力の無効化：制御コード (write-byte 14)／(write-byte 15) でテキスト出力を一時的に抑止し、グラフィックス表示を保護できる。

- 注意点  
  - 内蔵USBの挙動に未解決の問題があり、特にMacのシリアルモニタから長いプログラムを貼り付けるとハングする報告あり。対策はフォーラムやブートローダ経由の書き込み。  
  - モジュール（StampS3）はディスプレイに接続されているため、分解して取り外すとコネクタ破損の恐れがあるので非推奨。  
  - キーボードは小さめなので、大きな指の人は外部キーボードやシリアル経由の編集を検討。

## 実践ポイント
- まずやること（導入の最短手順）
  - Arduino IDEにM5Stackボードを追加 → M5Cardputerライブラリを入れる → Cardputer用uLispをGitHubからダウンロードしてUpload。
  - アップロード失敗時は背面G0を押しながらRstでブートローダにし、書き込みを試す。

- 便利なコマンド例
  - SD内ファイル一覧: 
    ```lisp
    (directory)
    ```
  - 画面をBMPで保存:
    ```lisp
    (save-bmp "screen.bmp")
    ```
  - テキスト出力を停止／再開:
    ```lisp
    (write-byte 14) ; 出力停止
    (write-byte 15) ; 出力再開
    ```
  - ピクセル読み取り:
    ```lisp
    (read-pixel x y)
    ```

- カスタマイズのコツ
  - 大きな文字が欲しい場合はソースの#define largerfontを有効にして再ビルド。  
  - SDを使わずにワークスペース保存したければ sdcardsupport をコメントアウトして、save-image が内部フラッシュを使うようにする。  
  - Autocompleteや括弧マッチは入力生産性を大きく上げるのでまず試す。

- 活用アイデア（日本の現場で）
  - 組み込み向けLisp入門教材：REPLで即時評価できるので授業やワークショップに最適。  
  - センサ実験や小型IoTプロトタイプ：Wi‑Fi/BLEを使った簡易クライアントやデモ作成。  
  - アート&グラフィックス：小型ディスプレイでアルゴリズム描画（フラクタル、音響可視化など）を手軽に実演可能。

Cardputer + uLispは「手で触れて学ぶLisp」として非常に魅力的なプラットフォーム。まずは簡単なスクリプトを打ち込んで、画面に線を描いたり音を鳴らしたりしてみることを勧める。
