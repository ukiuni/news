---
layout: post
title: "The Book of PF, 4th Edition - PFの書 第4版"
date: 2026-02-01T09:27:29.084Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://nostarch.com/book-of-pf-4th-edition"
source_title: "The Book of PF, 4th Edition | No Starch Press"
source_id: 46844350
excerpt: "IPv6対応のPF実践書：冗長化(CARP)・帯域制御やauthpf実例まで網羅"
image: "https://nostarch.com/sites/default/files/BookPF4e_frontcover.jpg"
---

# The Book of PF, 4th Edition - PFの書 第4版
OpenBSD流・実戦で使えるPF大全：これ1冊でファイアウォール運用が変わる

## 要約
OpenBSDのパケットフィルタPFを実務レベルで解説する第4版。IPv6、デュアルスタック、トラフィック制御、冗長化、無線やスパム対策まで網羅し、OpenBSD/FreeBSD/NetBSDの最新リリースに対応している。

## この記事を読むべき理由
日本でもISP、クラウド、企業ネットワークでIPv6導入や帯域管理、可用性確保のニーズが急増中。PFは軽量で堅牢な選択肢であり、本書は初級者から現場運用者まで即戦力になる具体的手順と実例を提供する。

## 詳細解説
- 対象プラットフォーム：OpenBSD 7.x、FreeBSD 14.x、NetBSD 10.xに対応。  
- コア機能：IPv4/IPv6双対応のルール作成、NAT／ポートリダイレクション、ブリッジ越しのフィルタリング。  
- トラフィック制御：OpenBSDの「queues and priorities」システムを中心に、FreeBSD向けのALTQ/Dummynet設定例も収録。品質保証や帯域制御の実運用手順を解説。  
- 冗長化と可用性：CARPによる仮想IP冗長化、relaydを使ったフェイルオーバー／リレー設定、リダイレクションでの可用性確保。  
- 無線とアクセス制御：AP構成とauthpfを使った動的認証・アクセス制限の実践例。  
- 防御／監視：スパム対策やプロアクティブな攻撃防御、ログ収集・可視化（NetFlowなど）による運用監視術。  
- 著者：Peter N. M. Hansteen — 長年のBSD系実務経験と人気チュートリアルを持つ実践者が執筆。

## 実践ポイント
- まずはラボで基本ルールセット（IPv4/IPv6両方）を作って挙動を確認する。  
- 帯域問題は「queues and priorities」から試し、FreeBSD環境ではALTQ/Dummynetを参照する。  
- 可用性はCARP＋relaydの組合せで検証し、フェイルオーバー手順を自動化する。  
- 無線はauthpfで局所的なアクセス制限を実装してから本番投入する。  
- ログとNetFlowでトラフィック傾向を可視化し、ルールのチューニングに活かす。  

購入・詳細は原著ページ（No Starch Press）で。
