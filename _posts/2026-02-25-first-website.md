---
layout: post
title: "First Website - 最初のウェブサイト"
date: 2026-02-25T23:44:33.034Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://info.cern.ch"
source_title: "http://info.cern.ch"
source_id: 47159302
excerpt: "CERNの初代ウェブサイトを体験し、Web誕生とHTML/HTTPの礎を実地で学べる解説。"
---

# First Website - 最初のウェブサイト
ウェブはここから始まった――CERNの「最初のウェブサイト」を現代の視点で味わう

## 要約
CERNが公開している info.cern.ch は、ワールド・ワイド・ウェブの最初のウェブサイトへの入口であり、初期のブラウザや誕生の経緯を学べる貴重なアーカイブです。

## この記事を読むべき理由
世界中の情報流通を根本から変えた「Web」の起源を理解することで、技術の設計思想（オープン性・標準化）がどう普及を生んだかが見えてきます。日本の開発者や技術愛好家にとっても、現代の設計判断に活かせる示唆が得られます。

## 詳細解説
- info.cern.ch はCERN（欧州原子核研究機構）で作られた最初のウェブページのアドレスで、初期の説明ページやブラウザのシミュレータ（line-mode browser simulator）へアクセスできます。  
- 背景：ティム・バーナーズ＝リーが1989–1991年に提案・実装した仕組み（HTML, HTTP, URL）がワールド・ワイド・ウェブの基盤です。CERNはこれらを非専有で公開し、急速な普及を可能にしました。  
- 技術的ポイント：  
  - HTMLは当初、文書を相互参照するための極めてシンプルなマークアップでした（リンクと見出し、段落が中心）。  
  - HTTPはリクエスト/レスポンス型のプロトコルで、静的コンテンツ配信の基本形を定義します。  
  - line-mode browser はGUI前のテキストベース端末でも動くよう設計された初期ブラウザの挙動を再現します。  
- 歴史的実物：初期のサーバはNeXTマシン上で稼働しており、現在見る info.cern.ch は当時の構成やドキュメントを辿れる再現・案内ページになっています。

## 実践ポイント
- info.cern.ch を開いて「Browse the first website」「line-mode browser simulator」を試す。初期の体験を実際に触ってみる。  
- ページのソースを表示して、初期HTMLの構造を確認する。簡単なHTMLならすぐに手を動かして理解できる。例：  
  ```html
  <!-- html -->
  <!doctype html>
  <html>
    <head><title>My First Page</title></head>
    <body>
      <h1>Hello, Web!</h1>
      <p><a href="https://info.cern.ch">Info about the first website</a></p>
    </body>
  </html>
  ```
- 自分で簡単な静的サイトを作ってGitHub PagesやNetlifyで公開してみる。HTTPとHTMLの流れが体感できます。  
- オープンスタンダードの重要性を学び、自社プロジェクトやOSS選定で「互換性・標準準拠」を重視する判断材料にする。
