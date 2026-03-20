---
layout: post
title: "Emacs Internal #01: is a Lisp Runtime in C, Not an Editor - EmacsはエディタではなくCで書かれたLispランタイムだ"
date: 2026-03-20T19:23:15.865Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://thecloudlet.github.io/technical/project/emacs-01/"
source_title: "Emacs Internal #01: is a Lisp Runtime in C, Not an Editor | The Cloudlet"
source_id: 378980595
excerpt: "C実装のEmacsElispランタイムが現代エディタとの違いと長寿の秘密を示す"
image: "https://thecloudlet.github.io/favicon.svg"
---

# Emacs Internal #01: is a Lisp Runtime in C, Not an Editor - EmacsはエディタではなくCで書かれたLispランタイムだ
40年選手の“エディタ”の正体を解剖する — なぜEmacsを離れられないのか、その設計と現代のエディタ比較で見える本質

## 要約
Emacsは単なるテキストエディタではなく、Cで実装されたEmacs Lispインタプリタを核にする「可変化可能なランタイム」だ。歴史的背景と実装トレードオフを理解すると、現代エディタとの違いが見えてくる。

## この記事を読むべき理由
日本の開発現場でも長期に使い続けられるツール選定や、拡張性・運用コストの評価は重要。Emacsの設計史と実装手法は、エディタだけでなく「長寿ソフトウェア」の作り方を学ぶ格好の教材になる。

## 詳細解説
- 歴史的背景：1970年代のTECOのマクロ文化から発展し、「マクロが言語化するなら本物の言語を埋め込もう」という流れでEmacs（Editor MACroS）が生まれた。Lispはマクロ性と小さなインタプリタ性が都合よく、GNU EmacsはUnix環境にLispを持ち込むためにCでElispランタイムを実装した。
- 実装の本質：GNU EmacsはモノリシックなCコア＋組み込みElispインタプリタ。Lisp_Objectのタグ付け、メモリ管理、動的束縛などがC実装の中心テーマになる（次回以降で具体的に分解可能）。
- 設計トレードオフ：C上の軽量インタプリタは移植性と単純さをもたらす一方、性能や非同期処理の面で新しいランタイム（LuaJITを採るNeovimやV8を採るVSCode）に及ばない点がある。これが「Worse is Better」やGreenspunの法則と結びつく。
- 近年の対比：NeovimはLuaJIT＋RPCでプラグインを分離・非同期化、VSCodeはChromium/V8上の大規模JSランタイムを採用。いずれも「VMをコアに据える」点はEmacsと共通だが、実装手法とエコシステムが異なる。

## 実践ポイント
- まず使ってみる：Org-modeやMagitなど、Emacs固有の生産性ツールを試して「離れにくさ」を体験する価値がある。
- 比較の視点：拡張性（組み込み言語）、非同期性、プラグイン分離、性能の優先度をプロジェクトで明確にする。
- 学び方：Emacsのソース（Cで書かれたElispランタイム部分）を追うと、ランタイム設計、タグ付け、メモリ戦略の実践例が得られる。小さな「LispインタプリタをCで実装する」演習は理解を深める近道。
