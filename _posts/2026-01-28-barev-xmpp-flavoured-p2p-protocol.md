---
layout: post
title: "Barev - XMPP flavoured p2p protocol - Barev：XMPP風P2Pプロトコル"
date: 2026-01-28T14:51:21.088Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://discourse.imfreedom.org/t/barev-xmpp-flavoured-p2p-protocol/348"
source_title: "Barev - XMPP flavoured p2p protocol - Plugins - Instant Messaging Freedom&#39;s Discourse"
source_id: 1410370602
excerpt: "Yggdrasilで動作するサーバーレスXMPP風チャットBarevの実用手順と利点"
image: "https://discourse.imfreedom.org/uploads/default/original/1X/710000fd6258f923809b5d2489be8e7f1013c612.svg"
---

# Barev - XMPP flavoured p2p protocol - Barev：XMPP風P2Pプロトコル
サーバー不要でXMPPの利便性をそのまま持ち込む—Yggdrasil上で動作する新しいP2Pチャット実装「Barev」

## 要約
Barevは、暗号化かつルーティングをYggdrasilに委ねることで「サーバーレスなXMPP風」コミュニケーションを実現するプロジェクトで、Pidgin用のpurpleプラグインとPascalライブラリ＋CLI実装がある。メッセージ、プレゼンス、ステータス、入力通知、アバター、ファイル転送など主要機能をサポートする。

## この記事を読むべき理由
プライバシー重視・分散型ネットワークへの関心が高まる日本で、サーバー依存をなくしたリアルタイム通信の実用例とその導入手順を知ることは、コミュニティ運営・災害時通信・プライベート社内ネット構築で即戦力になるため。

## 詳細解説
- 基盤技術：BarevはYggdrasil（暗号化されたIPv6メッシュオーバーレイ）を下層に使い、ルーティングとエンドツーエンド暗号化を担わせる。これにより独自の鍵管理やトラフィック暗号化をほぼ意識せずに利用できる。  
- 実装：主要な実装は（1）Pidgin用purpleプラグイン、（2）Pascalで書かれたライブラリとテスト用CLI。既存のXMPP仕様（ストリーム・メッセージ・プレゼンス・ファイル転送等）を「サーバーレス前提」で再利用している。  
- 履歴と設計判断：最初はBonjour/MDNSの上でYggdrasilを使う試みがあったが、MDNS依存のためステータス管理やファイル転送がうまく行かなかった。そこでXMPP標準をベースに「ピアを明示的に登録する」方式へ移行した。  
- セキュリティ／接続モデル：ユーザーは相互に nick@ipv6 形式で相手を登録する。Barevは登録済みのニックとIP/ポートのみ受け入れ、未登録からの接続は早期に切断されるためなりすましリスクが低い。Yggdrasil側で経路が見つかれば自動で暗号化される。デフォルトポートは1337で、ファイル転送用にポートレンジも設定可能（ファイアウォール運用を考慮）。

## 実践ポイント
- まずYggdrasilノードを立てる（IPv6アドレスを取得）。  
- Pidginを用意し、Barevのpurpleプラグインをビルドして ~/.purple/plugins に配置（システムインストールも可能）。  
- Pidginでアカウントを追加しニックを設定。相手は nick@YggdrasilIPv6 で登録する（相互登録が必須）。  
- デフォルトポート1337を基本に、ファイル転送のための許可ポートレンジをファイアウォールで開ける。  
- Pascalライブラリ／CLIでの自動化や研究用途も可能。コミュニティやローカルネットワーク、災害時メッシュ通信の実験プラットフォームとして有望。

興味があれば、Pidginプラグインのビルド手順やYggdrasilの導入ステップを別記事でまとめますか？
