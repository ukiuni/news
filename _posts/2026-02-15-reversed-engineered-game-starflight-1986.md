---
layout: post
title: "Reversed engineered game Starflight (1986) - リバースエンジニアされたゲーム「Starflight」（1986）"
date: 2026-02-15T16:03:31.121Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/s-macke/starflight-reverse"
source_title: "GitHub - s-macke/starflight-reverse: Reverse engineered game Starflight (1986)"
source_id: 47022943
excerpt: "ForthバイトコードからStarflight（1986）を丸ごと復元し内部実装を暴く解析"
image: "https://opengraph.githubassets.com/2f8907409914682d60ca3592161fcc54040a19ec54d7f43ae03e0324b512e0b5/s-macke/starflight-reverse"
---

# Reversed engineered game Starflight (1986) - リバースエンジニアされたゲーム「Starflight」（1986）
クリック必至：80年代名作をForthレベルで丸ごと解剖したリバースプロジェクトの全貌

## 要約
80年代の名作SFゲーム「Starflight」をForthそのままの構造で復元・解析したGitHubプロジェクト。実行ファイル解析からデータ構造、スレッド化されたForthバイトコードの再現まで、ゲーム内部を高精度に復元している。

## この記事を読むべき理由
レトロゲーム好きだけでなく、低レイヤー言語やインタプリタ設計、バイナリリバースに興味がある日本のエンジニア／学生にとって、生の教材として格好のリポジトリだから。Forthの思想や間接スレッディング（indirect threading）といった低級実装の理解に最適。

## 詳細解説
- 背景：Starflightはサンドボックス型探索RPGの古典。オリジナルはForthで実装されており、実行ファイルにはForthの構造がほぼそのまま残っていた。
- Forthと特徴：空白区切りの「語（word）」で動くスタックマシン。例：RPNで 2 3 + . のように記述する。構文が極端にシンプルで、インタプリタやリーダーを非常に短く実装できる。
- バイナリの中身：解析で判明した点
  - 実行ファイル内の大部分が16bitポインタ（ほぼ“バイトコード”）で占められている。
  - コンパイラ最適化はほぼ無しで、元ソースの語構造が保たれている。
  - 一部の語名は暗号化されて残っており、復元に役立つ手がかりがある。
  - Forthインタプリタ自体が実行ファイルに含まれ、動的に実行される（実行時にコードポインタを読み進めてjmpするIndirect Threading）。
  - 速度面では非常に非効率（頻繁なジャンプとオーバーレイ使用）。
- 間接スレッディングの仕組み（要点）
  - 実行ポインタが指す場所には16bitの値（語ごとのコードアドレス）が並ぶ。
  - その値を読み、さらに参照して実際の機械語ルーチンへジャンプする—二段参照による呼び出しの連鎖。
- ファイル構成：ゲームは STARFLT.COM（initialization + I/O）、STARA.COM / STARB.COM（データ＆オーバーレイ） に分かれる。STARBには巨大なINSTANCEツリーやテーブル、絵やオーバーレイが格納されている。
- 解析成果：6256語の識別、3711語が他語を実行（関数相当）、多数のテーブル・データ構造・オーバーレイなどが復元されている。解析結果はC風にトランスパイルされ、一部はそのままコンパイル可能。

## 実践ポイント
- リポジトリをクローンしてまずREADMEとsrcディレクトリを読む（解析レポート・トランスパイル済コードがある）。
  - git clone https://github.com/s-macke/starflight-reverse
- ローカルで元バイナリを動かすならDOSBoxを利用。解析成果を追うならVS Codeでソースを開くと理解しやすい（ファイル分割とオーバーレイ構造を比較）。
- Forthの基礎を先に学ぶと理解が早い（スタック操作・RPN・スレッディングの概念）。
- 学習用途：間接スレッディングやインタプリタ設計の実例として、組み込みインタプリタや教育用VMの設計に応用可能。
- 保存・再現の観点からも価値が高く、日本のレトロゲーム文化保存や翻訳プロジェクトの素材にもなる（元記事はGOGで購入可能という情報あり）。

興味が湧いたらまずリポジトリを開いて、トランスパイルされたCコードやオーバーレイ定義を覗いてみてください。
