---
layout: post
title: "We intercepted the White House app's traffic. 77% of requests go to 3rd parties - ホワイトハウス公式アプリの通信を傍受したら…リクエストの77%がサードパーティへ"
date: 2026-04-01T02:53:44.087Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.atomic.computer/blog/white-house-app-network-traffic-analysis/"
source_title: "We Intercepted the White House App&#39;s Network Traffic. Here&#39;s What It Sends. | atomic.computer"
source_id: 47595865
excerpt: "ホワイトハウス公式iOSアプリの通信77%が第三者へ送信され個人情報追跡の懸念"
image: "https://www.atomic.computer/atom.jpg"
---

# We intercepted the White House app's traffic. 77% of requests go to 3rd parties - ホワイトハウス公式アプリの通信を傍受したら…リクエストの77%がサードパーティへ

魅力的なタイトル: 「公式アプリなのに他社だらけ？ホワイトハウス公式iOSアプリの“裏側”を覗いてみた」

## 要約
公式ホワイトハウスiOSアプリをMITMで解析した結果、全通信の約77%（206件中158件）がOneSignal、Elfsight、Google、Facebookなどのサードパーティへ送られていた。プライバシー宣言と実際の挙動に大きな乖離がある。

## この記事を読むべき理由
政府や公共機関の公式アプリが外部トラッキングを多用している問題は、日本の公共系アプリ開発や利用者のプライバシー意識にも直結する。どのデータが、どの第三者に送られるかを知っておくことは、市民・開発者双方にとって重要だ。

## 詳細解説
- 手法：mitmproxyを導入したMac上でiPhoneのHTTPSを復号（CA証明書を端末にインストール）、アプリv47.0.4を通常利用しつつ全タブを巡回して通信を観察。通信は傍受のみで改変なし。  
- トラフィック概要：アプリ発起のリクエストは31ホストに対して行われ、206件中48件（約23%）のみがwhitehouse.gov。残り158件（約77%）はサードパーティ（Elfsight、OneSignal、YouTube/Google、Facebook、Twitterなど）。  
- OneSignal：起動時にOneSignalへ送られるデータは、言語・タイムゾーン・国・IPアドレス（フル）、初回/最終アクティブ時刻、端末モデルとOS、ネット接続種別、キャリア、脱獄判定、セッション回数・時間、永続的な識別子など。複数のPATCHでプロファイルを更新し、IP変化を同一IDで追跡する仕組みが確認された。  
- Elfsight：Socialタブで多数のElfsightドメインに接続。サーバーはウィジェットIDごとに「assets（実行するJS）」を返す二段階ローダーで、受信したスクリプトを動的に注入する。動的配信により外部コードがアプリ内で実行され、Elfsight系で複数のドメインcookie（Cloudflare含む）が設定された。  
- 広告／トラッキング：YouTube埋め込みによりDoubleClick広告トラッキングがロードされるなど、広告配信・解析インフラが動作。アプリのプライバシー表示（NSPrivacyCollectedDataTypes: []、NSPrivacyTracking: false）とは矛盾していた。  
- 影響：公式アプリの“見えない”外部依存が利用者のIP・行動・デバイス情報を第三者に渡し、長期的なプロファイリングやクロスサイト／サービス追跡が可能になる。

## 実践ポイント
- 公共系アプリを使う前にプライバシー表示と実際の通信を確認する習慣を持つ（Wireshark/mitmproxy等での検証は開発者向け）。  
- 重要な操作時は信頼できるネットワーク（VPN含む）を利用し、不要なトラッキングを減らす。  
- 開発者は外部ウィジェットや解析サービス導入時に「コード配信の制御」「最小限のデータ送信」「透明なプライバシー表記」を徹底する。  
- 日本の自治体・政府向けアプリでは、個人情報保護法（APPI）や公共調達の観点から外部サービス依存のリスク評価を強化すべき。

参考：解析元はAtomic ComputerによるMITMキャプチャ報告（記事本文の手法・観察結果に基づく要約）。
