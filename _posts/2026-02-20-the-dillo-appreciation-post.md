---
layout: post
title: "The Dillo Appreciation Post - Dillo 賞賛ポスト"
date: 2026-02-20T08:54:03.904Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://bobbyhiltz.com/posts/2026/02/dillo-appreciation/"
source_title: "The Dillo Appreciation Post"
source_id: 706759128
excerpt: "Dilloとdillocで作るRSS・Wallabag連携の超軽量Webツール"
---

# The Dillo Appreciation Post - Dillo 賞賛ポスト
もう重いブラウザは要らない？Dilloで作る自分用ミニWebツールキット

## 要約
軽量ブラウザ「Dillo」を日常ツールとして活用する実例。dilloc / page_action を使ったワークフロー、RSS→HTML の小スクリプト、Wallabag や mpv との連携など、実践的なカスタマイズ例を紹介します。

## この記事を読むべき理由
日本の開発者や軽量環境愛好者にとって、低リソース環境やプライバシー重視のワークフロー構築は有用です。Dillo は古典的ながら実用的で、手軽に自分仕様のツール群（ブックマーク共有、読みかけ管理、動画再生リスト）を作れます。

## 詳細解説
- Dillo の基本
  - 軽量かつシンプルなレンダリングを行うブラウザ。現代の「重い」サイトには向かないが、多くのテキスト中心サイトやミニサイトは問題なく表示できる。
- page_action と dilloc
  - ~/.dillo/dillorc の page_action でページコンテキストを呼び出し、外部スクリプトへ URL / ページダンプを渡せる。
  - 例：ページの URL と <title> を取得してクリップボードに Webmention 用の HTML を生成するワンライナー（抜粋）。
```bash
#!/usr/bin/env bash
url=$(dilloc url)
pagetitle=$(dilloc dump | grep -P -o "(?<=\<title\>).*(?=\<\/title\>)")
echo "* <div class=\"h-entry\"><a href=\"/\">You</a> liked: <a href=\"$url\">$pagetitle</a></div>" | xclip -selection clipboard
```
- 共有連携（Wallabag / linkhut）
  - page_action から wallabag-client や外部投稿用の URL を開いて「あとで読む」やブックマーク投稿を自動化できる。
- RSS→HTML（dillPype）
  - feedparser を使い、複数の YouTube チャンネル RSS を読み込んで最新動画リストを HTML 化。Dillo 上でリストを開き、mpv で再生するワークフローを実現。
```python
#!/usr/bin/env python3
# python (抜粋): feedparser で RSS を読み、HTML を生成
import feedparser
feeds = ["https://.../feed"]
entries = []
for f in feeds:
    parsed = feedparser.parse(f)
    entries += parsed.entries[:3]
# 日付でソートして簡易 HTML を出力（省略）
```
- Wallabag 連携
  - Wallabag のフィードを取得して記事リストを生成。Dillo で軽く一覧して rdrview 等で記事を整形して読む、という流れが可能。
- 実用的なサイト例
  - text ベースのニュースや軽量フロントエンド（例: lite CNN, text.npr.org, wttr.in, ブログ群）が快適に表示される。
- dotfiles と配布
  - 著者は設定やスクリプトを dotfiles リポジトリで管理しており、同様の環境を参考にできる。

## 実践ポイント
- まずは Dillo をインストール（ディストリで古ければソースから最新を取得）。
- ~/.dillo/dillorc に page_action を追加し、dilloc を用いる小さな Bash スクリプトを作る（上の例をコピペして試す）。
- feedparser を使って RSS→HTML を自動化し、Dillo＋mpv の再生ワークフローを構築する（cron や systemd timer で定期更新）。
- Wallabag を使って外出先で保存→家で Dillo で読む、という運用を検討する。
- まずは自分の dotfiles に少量ずつ取り入れて、過度な変更は避ける。

元記事（英語）の詳細やスクリーンショット、スクリプト全体は元記事を参照してください。
