---
layout: post
title: "The Fediverse deserves a dumb graphical client - Fediverseには“バカな”グラフィカルクライアントが必要だ"
date: 2026-04-15T07:52:10.562Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://adele.pages.casa/md/blog/the-fediverse-deserves-a-dumb-graphical-client.md"
source_title: "The Fediverse deserves a dumb graphical client | Adële&#039;s blog"
source_id: 1677691748
excerpt: "低速回線や旧端末でも画像が見られる、JSゼロの軽量FediverseクライアントSmolFediを紹介"
---

# The Fediverse deserves a dumb graphical client - Fediverseには“バカな”グラフィカルクライアントが必要だ
重たいJavaScriptに疲れた人へ──画像も見られてブラウザで軽快に動く、JavaScriptゼロのFediverseクライアント「SmolFedi」を知っていますか？

## 要約
SmolFediはサーバー側でJSONをHTMLに変換する、PHP＋SQLiteベースの軽量Fediverseクライアント。JavaScriptを一切使わず、画像や投稿操作（投稿、返信、ブースト、いいね、投票、通知など）に対応します。

## この記事を読むべき理由
多くのFediverseクライアントは数メガバイトのJavaScriptや最新端末を前提にしており、低速回線や古いデバイス、プライバシー重視の利用には向きません。日本でも地方や低スペック端末、教育現場やコミュニティ運営で役立つ実用的な代替案だからです。

## 詳細解説
- 問題点：Mastodonなどの公式／モダンなクライアントは大量のクライアントサイドJavaScriptを読み込み、低速環境や古いブラウザでは重い。反対にCLIクライアントは軽いが画像が表示できないため体験が欠ける。  
- SmolFediのアプローチ：Fediverse APIが返すJSONをサーバー側でレンダリングしてプレーンなHTMLを返す古典的な手法を採用。25年以上続く「サーバーサイドHTML生成」の利点を活かし、ブラウザ側にJSエンジンを必要としない。  
- 技術スタック：純粋なPHPアプリケーション（npm/Composer/build不要）、SQLiteによる軽量ストレージ、基本的なPHPセッション管理、CSSはsmolweb Grade B 準拠。コードベースにJavaScriptは一切ない。  
- 機能：複数アカウント、タイムライン、通知、投票、メディア添付（altテキスト対応）、投稿・返信・ブースト・お気に入りなど日常的な操作を網羅。MastodonやGoToSocialなど互換プラットフォームで動作。  
- 動作環境：Firefox/Chromium/Safariはもちろん、DilloやNetsurfなど軽量ブラウザでも画像表示が可能。低速回線や古い端末でも使える設計。

## 日本市場との関連性
- 地方や低速回線、学校や自治体での導入に適合。  
- Raspberry Piや低価格VPSでセルフホストしやすく、コミュニティやローカルインスタンス運営に向く。  
- プライバシーや帯域節約を重視する日本のユーザー（高齢者向け端末、移動中の通信制限など）に有益。

## 実践ポイント
- まずデモで試す：作者はデモ（Pollux）を公開、ソースはCodebergにあり。  
- 自分で立てる：安いVPSやRaspberry PiにPHPとSQLiteを入れて簡単にセルフホスト可能（ビルドステップ不要）。  
- コミュニティ用途に導入：地域コミュニティや教育現場で、低スペック端末でも画像つき投稿が見られる環境を提供できる。  
- アクセシビリティ対策：Altテキストを必ず使う運用ルールを促進すると効果的。  
- JSを減らす選択肢として検討：プライバシー重視や帯域節約が重要なサービス設計時の参考に。

興味があれば、SmolFediのCodebergリポジトリとデモを見てみると、導入イメージがつかめます。
