---
layout: post
title: "No-JS web IRC client that uses forms and a persistent HTTP connection - フォームと持続的HTTP接続で動く、JavaScript不要のWeb IRCクライアント"
date: 2026-04-08T03:52:34.135Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/dgl/cgiirc/"
source_title: "GitHub - dgl/cgiirc: CGI:IRC web based IRC client · GitHub"
source_id: 1390569152
excerpt: "JS不要で動くPerl/CGI製の軽量Web IRCクライアント導入法"
image: "https://opengraph.githubassets.com/a236762827e594b75dd258ea76153d8315aea69fd16e3af335ce87c773c3f086/dgl/cgiirc"
---

# No-JS web IRC client that uses forms and a persistent HTTP connection - フォームと持続的HTTP接続で動く、JavaScript不要のWeb IRCクライアント
JSを使わずブラウザだけでIRCに繋がるレトロで実用的なソリューション──CGI:IRCを知っていますか？

## 要約
CGI:IRCはPerl/CGIで書かれた「JavaScript不要」のWebベースIRCクライアントで、フォーム送信と長時間のHTTPストリーム（persistent connection）でIRCサーバとやり取りします。JSやWebSocketが使えない制限環境で有効です。

## この記事を読むべき理由
社内ネットワークや旧来のホスティングでブラウザのJSやWebSocketが制限されるケースは日本でも珍しくありません。代替手段としての仕組み・導入上の注意点が分かれば、実用的な選択肢になります。

## 詳細解説
- 基本構成：Perl CGIスクリプト（irc.cgi 等）がユーザごとにプロセスを立ち上げ、IRCサーバとTCPで接続。ブラウザ側はHTMLフォームで入力を送り、サーバは長時間のHTTPレスポンスをストリームしてIRCの発言を送ります（nph系の仕組みでヘッダ処理を抑えストリーミング）。
- 要件：Perl 5.004+、UNIX系環境、CGI実行が可能なホスト。一般的に各ユーザでWebサーバとPerlプロセスが必要なためメモリ消費が大きくなりやすい点に注意。
- インストール概略：cgiirc.config（または full をリネーム）を編集 → cgi-bin 等へファイル配置（imagesは適切に配置） → パーミッション確認 → irc.cgiにアクセスして動作確認。詳細は docs に豊富。
- 長所：JS/クッキー制限・古いブラウザ・隔離されたネットワークでも動く。シンプルなホスティングで即使える。
- 短所／リスク：スケーラビリティ（プロセス×ユーザでメモリ消費）、セキュリティ（HTTPS化・認証設定が必須）、現代的なUXは期待できない。大量ユーザ向けには不向き。
- サポート：READMEやdocs、メーリングリスト（古くからのプロジェクトらしいコミュニティ）が存在。

## 実践ポイント
- まずローカルや小規模で試す：Dockerや専用テストサーバで動作確認してメモリ使用量を把握する。  
- ホスティング選定：CGI実行とプロセス駆動を許す環境（専用/VPS推奨）。共有ホスティングは要確認。  
- セキュリティ：必ずTLSで公開し、cgiirc.configでアクセス制御（ipaccess等）を設定する。公開チャット用途なら認証検討。  
- 運用：ユーザ数が増えるなら代替（WebSocket + JS クライアント）やプロキシ/コンテナ化で負荷分散を検討する。  
- ドキュメント参照：README と docs ディレクトリ、メーリングリストで既知の問題と設定例を確認する。

CGI:IRCは「制約下で確実に動く」選択肢として今でも価値があります。社内のレガシー環境や限定公開チャットの検討材料として、一度試してみてください。
