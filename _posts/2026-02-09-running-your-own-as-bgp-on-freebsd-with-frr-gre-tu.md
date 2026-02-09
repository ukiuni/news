---
layout: post
title: "Running Your Own AS: BGP on FreeBSD with FRR, GRE Tunnels, and Policy Routing - 自分のASを持つ：FreeBSD上でのBGP（FRR）、GRE/GIFトンネル、ポリシールーティング"
date: 2026-02-09T04:37:07.127Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.hofstede.it/running-your-own-as-bgp-on-freebsd-with-frr-gre-tunnels-and-policy-routing/"
source_title: "Running Your Own AS: BGP on FreeBSD with FRR, GRE Tunnels, and Policy Routing"
source_id: 1003620373
excerpt: "FreeBSD＋FRRで個人ASを運用しIPv6/48を広告、GRE/GIFで拠点接続する実践手順"
---

# Running Your Own AS: BGP on FreeBSD with FRR, GRE Tunnels, and Policy Routing - 自分のASを持つ：FreeBSD上でのBGP（FRR）、GRE/GIFトンネル、ポリシールーティング
個人でもできる！FreeBSD + FRRでグローバルIPv6プレフィックスを公告し、“住所を持ち運べる”ネットワークを作る方法

## 要約
個人でRIPE経由のAS番号とIPv6プレフィックスを取得し、FreeBSD上のFRRでBGPを立てて複数アップストリームとピアリング、GRE/GIFトンネルでリモートサーバへルーティングする手順と設計上の注意点をまとめる。

## この記事を読むべき理由
プロバイダ依存のIPアドレスから解放され、マルチホーミングや移行を簡素化できる。日本の小規模事業者やテック趣味者が自分のアドレス空間を管理する実践的な手引きになる。

## 詳細解説
- リソース取得  
  - RIPEからASと/48等を取得する際は、個人でも「sponsoring LIR」を経由可能。要求書類、aut-num/inet6num/route6 オブジェクト作成、RPKI ROA設定を行う。
- 全体アーキテクチャ  
  - 中央にFreeBSD VM（router01）を置き、2つのアップストリームとBGPピアを張る。ローカルの/48をアナウンスし、サブネット（/64, /62等）をGRE/GIFトンネルで各サーバへ配る。トンネルはGIF（IPv6-in-IPv4, proto 41）を下流向けに多用し、プロバイダ要件でGREを使う場合あり。
- トンネル運用の設計要点  
  - トンネルのエンドポイントは点対点として/128を割当て、管理用のリンクサブネット（例: 2a06:...:ffff::/64）を使用。サブネットごとに遠端にルートを追加。
  - ローカルに aggregate の「ブラックホール」ルートを入れる（ルーティングループ防止のため）。例: ipv6 route 2a06:9801:1c::/48 blackhole
- FRR（BGP）設計の重要点  
  - Outbound: 自分の/48のみを広告。アップストリームごとに route-map を使い、コミュニティ付与や AS-path プリペンドでトラフィックエンジニアリングを行う。  
  - Inbound: 総当たりの bogon フィルタ（リンクローカル、ULA、マルチキャスト、ドキュメント範囲、過度に具体/広域なプレフィックス除外）で受信ルートを厳格にフィルタ。  
  - セキュリティと安定性: no bgp default ipv4-unicast（IPv6専用）、ttl-security hops 1（GTSM）、soft-reconfiguration inbound、maximum-prefix（閾値でセッション落とす）を設定。
- ファイアウォール（FreeBSD pf）  
  - BGP/TCP179やトンネル（GRE/proto 47、proto 41）を既知ピアに限定。ICMPv6はNDPやPMTUDのため必須のタイプだけ許可。スクラブでMSS調整、制御面はSSHを信頼できる発信元だけ許可。
- 運用と検証  
  - RPKI/ROAを作成して正当性を担保。ルート伝播はLooking GlassやRouteViewsで確認。トラブルはトンネルのMTU/PMTU、フィルタ、ブラックホール設定を最初に確認。

## 実践ポイント
- 手順チェックリスト  
  1. スポンサLIRを決め、ASと/48取得、aut-num/inet6num/route6を登録。  
  2. ROAを作成してRPKIでオーソライズ。  
  3. FreeBSD VMを用意し、トンネル（gif/gre）とloopbackエイリアスに/48の一部を割当て。  
  4. FRRでPL-MY-NET（自分の/48）とPL-BOGONS（受信用）を作成、route-mapで出口ポリシーを調整。  
  5. pfでBGPおよびトンネルだけを厳格に許可、ICMPv6を必要最小限で許可。  
  6. Looking Glass / RouteViewsで広告状態を検証。障害時はまずブラックホール、フィルタ、トンネルMTUを確認。  
- 重要な設定例（抜粋）
```text
# FreeBSD: aggregateをローカルで破棄
ipv6 route 2a06:9801:1c::/48 blackhole
```
```text
# FRR: outboundでASパスプリペンド例
route-map RM-LAGRANGE-OUT permit 10
  match ipv6 address prefix-list PL-MY-NET
  set as-path prepend 201379 201379
```

以上を押さえれば、個人運用で安全かつ実用的な自前AS＋IPv6アドレッシングが実現できる。日本の小規模事業者や複数クラウドを使う開発者にとって、可搬なアドレス空間は運用負荷と障害耐性の向上に直結する。
