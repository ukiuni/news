---
layout: post
title: "Happy 50th Birthday KIM-1 - KIM-1 50周年おめでとう"
date: 2026-01-11T15:25:56.489Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/netzherpes/KIM1-Demo"
source_title: "GitHub - netzherpes/KIM1-Demo: a little demo for the KIM-1 for it&#39;s 50th birthday"
source_id: 46575804
excerpt: "KIM-1の50周年デモで6502の低レイヤ技術を実例で学べる"
image: "https://opengraph.githubassets.com/6d98a4e68e0bf0a7b74e92abfe6fdb471ca05b28b5205a0dafb1fd1bb06caaeb/netzherpes/KIM1-Demo"
---

# Happy 50th Birthday KIM-1 - KIM-1 50周年おめでとう
50年前の名機が今も教えてくれる「低レイヤー発想」——KIM-1デモで遊んで学ぶレトロハック入門

## 要約
1976年登場のマイコンKIM-1を祝う小さなデモプロジェクト。6502時代の低レイヤー技術（メモリ→画面座標変換、数値のASCII化など）を実例で学べるリポジトリ。

## この記事を読むべき理由
KIM-1はApple Iより先に出た初期マイコンの代表格。アセンブリで「数値を画面位置に変換して描画する」仕組みを見ることで、組み込み・IoT系開発で役立つ低レイヤー思考が身につく。日本のメイカー／教育コミュニティでも実践的に役立つ内容。

## 詳細解説
- 歴史的背景  
  KIM-1は1976年1月に登場したMOSテクノロジー系のワンボードマイコン（6502系）。当時の入出力は非常に低レベルで、今のGUIや高級言語に慣れた人ほど「なぜそんな面倒を…」と感じるが、逆に基礎理解に最適。

- リポジトリの中身（ざっくり）  
  READMEとデモ用のバイナリ／アセンブリソースが含まれている。デモは「メモリ中の16進座標データを取り出して、端末のANSIシーケンスでカーソル移動し描画する」例など、レトロなハックを集約している。

- 技術的ポイント（重要）  
  1) ANSIエスケープでカーソル移動するには ESC [ row ; col H の形で数文字を送る必要がある。  
  2) メモリに入っている値はバイナリ／16進表現なので、画面に送るには桁ごとに分解してASCIIに変換する必要がある。  
  3) リポジトリのPUTDECルーチンは、0–99の値を「十の位・一の位」に分解する単純な減算ループを使い、それぞれに'0'を足してASCIIとして出力している。資源（レジスタとメモリ）が乏しい環境での典型的な実装例。

- サンプル（要点のみ、アセンブリ）  
```Assembly
; ANSIカーソル移動の概念
GOTOXY:
    LDA #$1B    ; ESC
    JSR CHOUT
    LDA #$5B    ; '['
    JSR CHOUT
    LDA CURY
    JSR PUTDEC  ; Row を十進で送る
    LDA #$3B    ; ';'
    JSR CHOUT
    LDA CURX
    JSR PUTDEC  ; Col を十進で送る
    LDA #$48    ; 'H'
    JSR CHOUT
    RTS

; 0-99 の数値を十位・一位に分解してASCII出力
PUTDEC:
    STA TEMP
    LDY #0
PUTDEC_T:
    CMP #10
    BCS PUTDEC_S
    JMP PUTDEC_D
PUTDEC_S:
    SEC
    SBC #10
    INY
    JMP PUTDEC_T
PUTDEC_D:
    TAX
    TYA
    BNE PUTDEC_Z
    JMP PUTDEC1
PUTDEC_Z:
    CLC
    ADC #$30
    JSR CHOUT
PUTDEC1:
    TXA
    CLC
    ADC #$30
    JSR CHOUT
    LDA TEMP
    RTS
```
この手法は、現代のマイクロコントローラ（AVRやARM Cortex-M）でも「最小限のコードで文字列化」したい場面に応用可能。

## 実践ポイント
- まずはエミュレータで動かす：6502エミュレータやKIM-1互換環境でリポジトリのバイナリを試すと敷居が低い。  
- PUTDEC を改造して遊ぶ：座標変換ルーチンを変えて矩形や円を描画させると学びが深い。  
- モダン言語へ移植：同じロジックをCやPythonで実装して、低レイヤーの考え方を言語間で比較する。  
- 実機ハック：KIM-1互換ボードや自作の6502環境があれば、実際に配線・表示して「動く歴史」に触れられる。  
- コントリビュート：アイデアやモジュール、デモをGitHubに追加してコミュニティに参加する。

最後に一言：50年の歴史的産物を“実際に動かして分解する”ことは、ソフトウェアやハードウェアの基礎力を養う近道。KIM-1のシンプルさから得られるヒントは、現代のIoT／組み込み開発でも十分に活きる。
