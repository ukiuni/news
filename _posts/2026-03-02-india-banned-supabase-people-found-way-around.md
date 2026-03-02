---
layout: post
title: "India Banned Supabase. People found way around. - インドがSupabaseをブロック。迂回策が見つかった"
date: 2026-03-02T04:48:02.742Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://sushantdhiman.dev/india-banned-supabase-people-found-way-around/"
source_title: "India Banned Supabase. People found way around."
source_id: 393009338
excerpt: "インドでSupabaseがISPごと遮断、回避法とサービス被害の警告"
image: "https://static.ghost.org/v5.0.0/images/publication-cover.jpg"
---

# India Banned Supabase. People found way around. - インドがSupabaseをブロック。迂回策が見つかった
Supabaseが一部ISPで遮断され、フロントエンド直結のアプリが突然使えなくなる事態が発生 — あなたのサービスは他人事ではありません。

## 要約
インド政府がSection 69Aに基づく命令で一部ISPに対して*.supabase.coへの接続を遮断。Supabase自体は稼働中だが、Jioなど一部回線ではフロントエンドSDK経由のアクセスが不安定に。開発者コミュニティはVPN／DNS変更や、リバースプロキシ（例：JioBase）のような迂回策を共有している。

## この記事を読むべき理由
BaaSに依存するモバイル／ウェブアプリは、国やISPのブロックで一夜にして利用不能になり得る。日本でもクラウド依存設計の脆弱性を再評価するきっかけになるため、対策を押さえておく価値があります。

## 詳細解説
- 法的背景：インドのSection 69A命令はISPレベルでのブロックを指示でき、理由は公開されていないケースもある。  
- 影響範囲：Supabaseのインフラ自体は稼働中だが、ドメイン単位でのHTTP/HTTPSブロックにより、ブラウザやフロントエンドSDKを直接使うアプリが影響を受ける。ISPによっては正常な接続が可能なため、断続的／地域差のある障害になる。  
- 一時対処：SupabaseやユーザーはVPNやDNSを1.1.1.1に変えると解消する報告があるが、一般ユーザーに全員にそれを依頼するのは現実的でない。  
- 技術的迂回：コミュニティはJioBaseのようなリバースプロキシを作り、アプリはプロキシ経由でSupabaseにアクセスすることで回避している。ただし、こうした迂回策は法的・運用上のリスクや継続性の問題がある点に注意。

## 実践ポイント
- フロントエンド直結を見直す：公開ドメイン／鍵で直接アクセスする設計はリスク。重要な機能はサーバー側プロキシ／ファンクション経由に移す。  
- カスタムドメイン／CDNの検討：プロバイダ側でドメイン単位のブロックを受けにくくする手段として有効。ただし万能ではない。  
- モニタリングをISP単位で実施：地域・キャリア別の可用性監視を導入し、早期検知と切り分けを可能にする。  
- 代替案とDR（ディザスタリカバリ）を用意：自己ホスティング、他BaaSプロバイダ、オフライン対応などを評価しておく。  
- 法的・運用面の確認：迂回策を採る際は現地法令やベンダーポリシーを確認し、公式対応（プロバイダやISPへの問い合わせ）も並行する。

このケースは「クラウド依存の運用リスク」を端的に示しています。設計段階での冗長化と、ISP・地域ごとの監視／対応手順を今すぐ点検してください。
