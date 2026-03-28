---
layout: post
title: "I decompiled the White House's new app - ホワイトハウスの新アプリを逆コンパイルしてわかったこと"
date: 2026-03-28T16:10:24.895Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://thereallo.dev/blog/decompiling-the-white-house-app"
source_title: "I Decompiled the White House&#x27;s New App"
source_id: 47555556
excerpt: "ホワイトハウス公式アプリの逆コンパイルで外部JS注入・位置追跡・同意バイパスが判明"
image: "https://thereallo.dev/api/og?title=I%20Decompiled%20the%20White%20House&#x27;s%20New%20App&amp;description=The%20official%20White%20House%20Android%20app%20has%20a%20cookie/paywall%20bypass%20injector,%20tracks%20your%20GPS%20every%204.5%20minutes,%20and%20loads%20JavaScript%20from%20some%20guy&#x27;s%20GitHub%20Pages."
---

# I decompiled the White House's new app - ホワイトハウスの新アプリを逆コンパイルしてわかったこと
公式アプリが隠していた「追跡」「外部JS読み込み」「同意バイパス」──逆コンパイルで暴かれた実装の全貌

## 要約
逆コンパイルで、ホワイトハウス公式AndroidアプリはReact Native(Expo)製で、WebView経由で外部サイトにJavaScriptを注入して同意やペイウォールを消し、OneSignal経由の位置情報・行動プロファイリングや外部ホスティングのJS読み込みなど、複数のプライバシー／供給網リスクを抱えていることが明らかになりました。

## この記事を読むべき理由
政府公式アプリという高信頼サービスがどのようにユーザー情報や外部コードを扱うかは、日本の政府・企業向けアプリ設計にも直結する問題です。技術的な落とし穴と対策を理解しておけば、自社アプリの安全性向上に役立ちます。

## 詳細解説
- 全体構成  
  - React Native + Expo SDK 54、HermesでJSバイトコードをバンドル。バックエンドはWordPressのカスタムREST APIでコンテンツ配信。
- WebViewでの「同意／ペイウォール除去」  
  - アプリ内ブラウザはページ読み込み時にJS/CSSを注入し、CookieバナーやGDPR同意ダイアログ、ログイン壁、ペイウォール等をDOM操作で常時除去（MutationObserver使用）。evaluateJavascript()で実行。
- 位置情報追跡インフラ（OneSignal連携）  
  - OneSignalネイティブコードに位置取得ロジックが組み込まれており、フォアグラウンドで約4.5分間隔、バックグラウンドで約9.5分間隔で位置取得する定数が存在。起動条件は（1）内部フラグ（setLocationShared）有効、（2）ランタイムの位置権限許可、（3）端末に位置プロバイダがあること。許可されれば緯度/経度/精度/タイムスタンプ/前景背景状態をOneSignalに送信。
- OneSignalによる行動・属性プロファイリング  
  - タグ付け、SMS紐付け、クロスデバイス識別、成果トラッキング、通知やインアプリメッセージのクリック・表示履歴などを収集可能。位置や通知挙動、電話番号などがプロファイリングに使える。
- 供給網／外部スクリプトのリスク  
  - YouTube埋め込みで個人のGitHub Pages（lonelycpp.github.io）をロード。アカウント侵害で任意コードが実行されうる。ElfsightなどのサードパーティJS、Mailchimp（メール収集）、Uploadcare（画像配信）、Truth Social埋め込み等、多数外部サービス依存。
- 証明書ピンニングなし、開発の痕跡が本番に残る  
  - 標準TrustManagerでピンニング未実装。開発用URLやローカルIP、Expo開発クライアントがリリースに同梱。ファイルプロバイダ設定で外部ストレージ全体にアクセス可能などの懸念。
- ライブラリ群（要旨）  
  - OneSignal、Firebase（FCM/Analytics）、OkHttp、Apollo、Fresco/Glide、ExoPlayer、ML Kit等、巨大なエコシステムが混在。

## 実践ポイント
- 一般ユーザー向け  
  - 公式アプリでも位置権限は慎重に与える。機微情報は外部ブラウザで開く。アプリの権限とプライバシーポリシーを確認する。  
- 開発者・審査者向け  
  - WebViewで外部ページを表示する際は注入コードを避けるか明示的に通知する。外部JSは信頼されたCDN/署名済みパッケージのみ許可、可能ならサンドボックス化。  
  - 位置情報や通知SDKのデータ収集範囲を最小化し、ユーザー同意のフローを可視化する。setLocationSharedのようなオン／オフAPIは監査可能に。  
  - 証明書ピンニングや厳格なTLS設定、ビルドに開発アーティファクトが混入しないビルドパイプラインを整備する。ファイルプロバイダのアクセス範囲を限定する。  
  - 政府系・公共系アプリは特にサードパーティ依存と供給網リスクのレビューを必須化する。

原文（参考）: https://thereallo.dev/blog/decompiling-the-white-house-app
