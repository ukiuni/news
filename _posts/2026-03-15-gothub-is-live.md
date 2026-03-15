---
layout: post
title: "Gothub is live - Gothubが公開"
date: 2026-03-15T11:33:18.759Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://x61.sh/log/2026/03/14032026191148-gothub.html"
source_title: "『 0x61 』- /var/log"
source_id: 723100896
excerpt: "OpenBSD由来の安全なgotホスティングGotHubで、VM単位の隔離環境を今すぐ試そう"
---

# Gothub is live - Gothubが公開
GotHubで始める、OpenBSDネイティブな“got”ホスティング — プライバシー重視のGit代替を今すぐ試そう

## 要約
OpenBSDのバージョン管理ツール「got」をベースにしたホスティングサービス GotHub が公開。自分専用のvmd上VMでgot/gotwebdを動かせるほか、クラウド版で手軽にリポジトリを移行・運用できる。

## この記事を読むべき理由
gotはOpenBSDコミュニティ発の軽量で安全性重視の分散型ツール。日本でもセキュアな社内開発環境や自己ホストを検討するチームにとって、有力な選択肢になります。

## 詳細解説
- gotとは：OpenBSDで開発されたGitに似た分散型バージョン管理。シンプルでセキュアに設計されているのが特徴。
- GotHubの構成：got/gotd/gotwebdを組み合わせ、Web UI（gotwebd）とSSHログイン経路を提供。ユーザーはVM（vmd上）単位で隔離された環境を得られるため、プライベート運用に適している。
- 提供プラン：Small/Medium/LargeのCommunity版と、それぞれに企業向けのプロフェッショナル版が用意され、必要に応じてフルVMを受け取れる。
- セットアップ感覚：ローカルで試す場合はパッケージを入れて起動すればOK（例: doas pkg_add got gotd gotwebd）。gotsysd.confでユーザーやリポジトリ、webサーバ設定を行い、gotwebd経由でブラウザから操作できる仕組み。
- 実際の動線：SSHで「weblogin」コマンドを実行すると一時的なブラウザログインURLが返り、そこでWeb UIへアクセス可能（セッション連携の仕組み）。

## 実践ポイント
- まずはデモを触る：https://demo.gothub.org
- ローカル検証：doas pkg_add got gotd gotwebd を実行して、自分のgotsysd.confを作成し試す。
- 既存GitHubのリポジトリは移行可能（ミラーや手動コピーを検討）。機密性が重要なプロジェクトはGotHubのVMプランを検討する。
- 会社導入では、vmdベースの隔離とOpenBSD由来の安全設計を評価ポイントに。

以上。興味があればデモのURLや設定テンプレートの簡単なサンプルを送ります。
