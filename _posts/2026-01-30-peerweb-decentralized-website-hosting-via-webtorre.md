---
layout: post
title: "Peerweb: Decentralized website hosting via WebTorrent - PeerWeb：WebTorrentによる分散型ウェブホスティング"
date: 2026-01-30T21:30:06.270Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://peerweb.lol/"
source_title: "PeerWeb - Decentralized Website Hosting"
source_id: 46829582
excerpt: "WebTorrentでサーバ不要の静的サイトをP2P配信、検閲耐性で低コスト公開"
image: "https://omodaka9375.github.io/portfolio/static/media/peerweb.7559ae56a756e1217679.png"
---

# Peerweb: Decentralized website hosting via WebTorrent - PeerWeb：WebTorrentによる分散型ウェブホスティング
魅了するタイトル: 「サーバ不要でサイト公開？WebTorrentで“消せない”静的サイトを配る新常識 — PeerWeb入門」

## 要約
PeerWebはWebTorrentを使って静的サイトをピアツーピアで配布するツールで、中央サーバに頼らず検閲耐性・コストゼロで公開できるのが特徴です。

## この記事を読むべき理由
日本の個人開発者・コミュニティ運営者にとって、低コストでオフライン対応・検閲耐性のある配布手段は魅力的。災害時やイベント、コミュニティサイトの冗長化にも有効です。

## 詳細解説
- 仕組み：ブラウザ内でWebTorrentクライアントを動かし、サイトを.torrent／マグネットハッシュで配布。受信者はピアからコンテンツをダウンロードしてIndexedDBにキャッシュする。  
- アップロードと共有：ドラッグ＆ドロップでフォルダをアップ→ハッシュ（PeerWeb URL）が発行。タブを開いておくか、常時シードするならデスクトップクライアント（Windows/macOS/Linux）を使う。  
- セキュリティ：DOMPurifyでHTMLをサニタイズ、iframeのサンドボックス実行、リソース検証でXSSや有害なタグを排除。  
- キャッシュと速度：訪問サイトはIndexedDBに格納。即時表示（スマートキャッシュ）、自動クリーンアップは7日間。  
- 制約：静的コンテンツ限定（HTML/CSS/JS/画像等）、ルートにindex.htmlが必要、相互ピア依存なのでピアがいないとダウンロード不可（デスクトップクライアントで解決可能）。  
- 開発者向け：&debug=trueで詳細進行ログ、Advanced Torrent Creatorでカスタム.torrent作成、デモや既存ハッシュのロード機能あり。

## 実践ポイント
- まずは静的サイト（index.html, 相対パス）を用意してドラッグ＆ドロップで試す。  
- 永続公開したければデスクトップクライアントを常時稼働させてシードを維持する。  
- 開発中は ?orc=<hash>&debug=true を使って接続・ダウンロード状況を確認。  
- 日本向け公開ならCDNやGitHub Pagesと併用して「初回配信はCDN、二次配信はPeerWeb」で冗長化を検討。  
- 法的・規約面（配布ファイルの権利やコンテンツ規制）を確認してから公開する。

PeerWebは「サーバを持たない」「検閲に強い」「低コスト」という強みを、個人〜コミュニティ規模のプロジェクトで手軽に試せる技術です。興味があるならまずは小さな静的サイトをアップして、ハッシュを友人に共有してみてください。
