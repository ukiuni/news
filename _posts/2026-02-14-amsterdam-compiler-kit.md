---
layout: post
title: "Amsterdam Compiler Kit - アムステルダム コンパイラ キット"
date: 2026-02-14T18:12:43.977Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/davidgiven/ack"
source_title: "GitHub - davidgiven/ack: The Amsterdam Compiler Kit"
source_id: 47016008
excerpt: "レトロや組込み向けにACKで実機実行ファイルを低コストで作る方法"
image: "https://opengraph.githubassets.com/bac70979b8b276f936e80d5b491930e815c9e2400a5e8a01fe2e1a87053a9943/davidgiven/ack"
---

# Amsterdam Compiler Kit - アムステルダム コンパイラ キット
魅惑のレトロ×クロスコンパイル：古典的コンパイラツールチェインで“動く実機”を作る方法

## 要約
Amsterdam Compiler Kit（ACK）は、ANSI CやPascalなど複数言語のフロントエンド、コード生成器、ランタイムやツール群を揃えた古典的かつ実用的なコンパイラツールチェインで、さまざまなレトロ／組込みプラットフォーム向けにビルドできます。

## この記事を読むべき理由
レガシー資産の移植、組込み／レトロ環境での実行ファイル生成、あるいはコンパイラ内部を学ぶ教材として、低コストで多プラットフォーム対応の実践的ツールを探している日本のエンジニアや学生に有益です。

## 詳細解説
- 対応言語：ANSI C（K&R互換含む）、Pascal、Modula-2、Basic など。  
- 主要ターゲット：Linux（i386, m68k, MIPS, PowerPC）、OSX（i386/ppc）、MS-DOS、Minix、Raspberry Pi（GPUバイナリ）や古典的なPDP/11・CP/Mなど幅広いプラットフォームをサポート。  
- インストール要件：ANSI Cコンパイラ（通常gcc）、flex/yacc、GNU make、Lua＋lua-posix、Python3.4+、ターゲット用に約1GBの空き。  
- ビルドの流れ：リポジトリを取得 → Makefile先頭でPREFIXやPLATSを設定 → make（並列可能）→ sudo make install。  
- 使い方（概念）：主コマンドは ack。-m<platform> でターゲット指定、-o 出力、-c/.s/.e などで中間・アセンブリ出力、-O 最適化（0–6）、-ansi 等。拡張子で言語判別（.c/.p/.mod/.bas 等）。例：ack -mlinux386 -O examples/paranoia.c  
- 注意点：ライブラリは限定的（ANSI C レベル程度）。ACK独自の.oフォーマットを使うため他コンパイラのオブジェクトと混在不可。古いコードやビルドスクリプトが混在しており、現代環境でのビルドに微調整が必要な場合あり。BSDではファイルディスクリプタ数調整等の対処が必要なケースあり。

## 実践ポイント
- まずは examples フォルダのサンプルをビルドして動かす（ack -m<plat> -O examples/...）。  
- MakefileのPREFIXとPLATSを編集して、まずは1プラットフォームだけビルドする（時間短縮）。  
- レトロPCやRaspberry Pi向けに小さなCプログラムをビルドして、クロス実行ファイル作成を体験する。  
- 他のツールやオブジェクトと混ぜない／ライブラリ不足を補う準備をする。問題発生時はプロジェクトのメーリングリストやIssueで情報を集める。  

ACKは「古典的だが手堅い」ツールチェインで、レガシーソフトの蘇生や教育用途、ニッチな組込みターゲットに強みがあります。興味があればリポジトリをクローンして小さな実験から始めてください。
