---
layout: post
title: "LittleSnitch for Linux - Linux向けLittle Snitch"
date: 2026-04-09T00:39:56.643Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://obdev.at/products/littlesnitch-linux/index.html"
source_title: "Little Snitch for Linux"
source_id: 47697870
excerpt: "Linuxでアプリの隠れた外部接続を可視化し、ワンクリックで即ブロック可能なツール"
image: "https://obdev.at/Images/social-graphs/opengraph-obdev.jpg"
---

# LittleSnitch for Linux - Linux向けLittle Snitch
Linuxでアプリの“こっそり外部接続”を可視化して即ブロックできる新ツール。あなたのPCの通信を一目で監視・制御する方法。

## 要約
Little Snitch for Linuxは、アプリの送信接続を可視化してワンクリックで遮断できるツール。eBPFでカーネルの接続を監視し、Web UI（http://localhost:3031/）から操作します。

## この記事を読むべき理由
日本でもプライバシーや不要なテレメトリを意識する開発者や個人利用者が増加中。外向き通信の可視化は、侵害検出や不要通信の削減、社内ポリシー運用に即役立ちます。

## 詳細解説
- 動作要件：Linuxカーネル6.12以上、BTFサポート必須。インストール後はターミナルで littlesnitch を起動するか http://localhost:3031/ を開く（Chromium系はPWA対応、Firefoxは拡張でPWA化可能）。  
- 仕組み：eBPFプログラムがアウトゴーイング接続を監視しデータをデーモンに渡す。eBPFとWeb UIはGPLv2で公開、デーモン（littlesnitch --daemon）はプロプライエタリだが無償配布。  
- UIと機能：Connectionsビューでアプリ別・送信先別の通信履歴とデータ量を確認。ワンクリックで接続ブロック、時間範囲選択でトラフィックを絞り込める。  
- ブロックリスト：ドメイン単位、ホスト1行、/etc/hosts形式、CIDRに対応。ワイルドカード・正規表現・URLベースは非対応。既存リスト例：Hagezi、Peter Lowe、Steven Black、oisd.nl。macOSの .lsrules は互換性なし。  
- ルール：プロセス、ポート、プロトコルなど細かい条件で許可/拒否を定義可能。ルールビューで整理・フィルタも可。  
- セキュリティと設定：デフォルトだとローカル上の誰でもUIにアクセス可能。複数ユーザで使うなら web_ui.toml で認証を有効化し、UIがループバック以外に公開される場合はTLSを設定する。設定ファイルは /var/lib/littlesnitch/config/ にあり、直接編集せず /var/lib/littlesnitch/overrides/config/ にコピーして編集する。主要ファイル：web_ui.toml（アドレス・ポート・TLS・認証）、main.toml（デフォルト挙動：許可/拒否）、executables.toml（実行ファイルの正規化ルール）。  
- 制限事項：プライバシー監視ツールとしては強力だが、セキュリティ強化ツールではない。eBPFのストレージ/複雑度制約や高負荷でのキャッシュ溢れにより、すべてのパケットを確実にプロセスやDNS名に結びつけられない場合がある。厳密な防御を目的とするなら他手段が必要。

## 実践ポイント
- カーネル要件（≥6.12・BTF）を確認してから導入する。  
- 起動後はまずConnections画面で「見慣れない通信」をチェックし、ワンクリックでブロック。  
- ブロックリストはドメインベースを優先して導入。既存の信頼できるリストを活用する。  
- 複数ユーザ環境やGUIを外部公開する場合は web_ui.toml で認証とTLSを必ず設定。  
- 設定は overrides に置いて運用。main.toml を deny モードに切り替えると自己ロックのリスクがあるため注意。  
- 開発者向け：eBPFとWeb UIのソースはGitHubで確認・カスタム可能（デーモンは非公開）。

少人数の日本企業や個人開発者が、自分の端末の“外向き通信”を把握・制御する入門ツールとして特に有用です。
