---
layout: post
title: "How to Make a Damn Website - とにかくウェブサイトを作る方法"
date: 2026-01-12T21:45:08.777Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lmnt.me/blog/how-to-make-a-damn-website.html"
source_title: "How to Make a Damn Website"
source_id: 1622174163
excerpt: "プレーンHTMLで即公開し、手作りRSSで読者獲得する最短実践ガイド"
image: "https://lmnt.me/files/images/opengraph/lmnt.webp"
---

# How to Make a Damn Website - とにかくウェブサイトを作る方法
とりあえず公開しよう：手早く、シンプルに「動く」サイトを作るための最短ルート

## 要約
まずは完璧を目指さず、プレーンHTMLで最初の投稿を書いて公開する。RSSで配信を用意し、徐々にスタイルや構成を追加すればOK、というシンプルなワークフローを勧める記事です。

## この記事を読むべき理由
日本でも「作る前に調べすぎて先に進めない」人が多いです。フレームワークやCMSに迷うより、最初のコンテンツを出すことが一番の一歩になる──その実践的な手順と考え方が学べます。個人開発やテックブログを始めたい人、プロジェクトを素早く公開したいエンジニアに有益です。

## 詳細解説
1. 「最も簡単な方法」が最短の学びになる  
   - ウェブページは1ファイルのHTMLで十分です。CSSも最初は不要。まずは本文を書き、サーバーにアップしてブラウザで確認する。これだけで「公開されたサイト」です。
   - 重要なのは「コンテンツを出す」こと。デザインやCMS探しで時間を浪費するより、本文を書いて公開する習慣をつけるのが先。

2. 手順（概略）  
   - プレーンテキストエディタでHTMLを書き、ファイル名は意味のあるものにする（例: how-to-make-a-website.html）。  
   - FTPやホスティングの方法でサーバーにアップロード。ブラウザで直接ファイルにアクセスして動作確認。  
   - 最初はベーシックな構造（h1, p, ol/ul, imgなど）だけ使う。divや過度なクラス付けは後回しに。

3. RSS（フィード）を手動で作る価値  
   - RSSを用意すると、読者が購読できるようになる。XMLを手書きするのは数分で可能で、公開後の流通に有利。  
   - フィードにはチャンネルメタデータ（title, link, description, language, atom:link）と、各投稿を表す item 要素（title, pubDate, guid, link, description）を入れる。記事本文は description のCDATAに入れても良い。  
   - pubDateは正しいフォーマット（GMTなど）で、画像等は絶対URLを使うこと（RSSリーダーが外部で表示するため）。

4. インデックスとスタイルは後から  
   - まずはルートにホーム、/blog に投稿へのリンク、投稿ページを置く。ページ数が増えたらインデックスを整備する。  
   - CSSは基本要素（h1, p, ol, ul, strong 等）から少しずつ適用。小さな変更を頻繁に公開する方が改善が速い。

5. なぜ手動で良いのか  
   - 自動化やCMSは便利だが、最初の障壁と複雑さを増やす。手作業で始めると「何が重要か（コンテンツ）」が明確になる。自動化は必要になってから導入しても遅くない。

例：とにかく動く最小のHTML（参考）
```html
<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <title>はじめての投稿</title>
</head>
<body>
  <h1><a href="first-post.html">はじめての投稿</a></h1>
  <p>これは最初のブログ投稿です。まず出してみましょう。</p>
</body>
</html>
```

例：簡単なRSSフィード（参考）
```xml
<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>サイト名</title>
    <link>https://example.com/</link>
    <description>サイトの説明</description>
    <language>ja-jp</language>
    <atom:link href="https://example.com/feed.xml" rel="self" type="application/rss+xml"/>
    <item>
      <title>はじめての投稿</title>
      <pubDate>Mon, 01 Jan 2024 12:00:00 GMT</pubDate>
      <guid>unique-id-12345</guid>
      <link>https://example.com/blog/first-post.html</link>
      <description><![CDATA[
        <h1><a href="first-post.html">はじめての投稿</a></h1>
        <p>これは最初のブログ投稿です。</p>
      ]]></description>
    </item>
  </channel>
</rss>
```

## 実践ポイント
- まず書いて公開：CMSやデザインは後回し。最低限のHTMLで投稿を1つ出すこと。  
- RSSを用意する：手書きのfeed.xmlで購読を可能にすると発信力が上がる。  
- 相対URLではなく画像等は絶対URLを使う（RSSで正しく表示されるように）。  
- スタイルは「一要素ずつ」追加：h1→p→リスト→画像、という順でCSSを当てていく。  
- 継続が最優先：小さく早く出し、改善を繰り返す習慣を作ること。

まとめ：ツールや流行に振り回されず、とにかく「動くもの」を出す。そこから学び、拡張していけば十分強いサイトが作れます。
