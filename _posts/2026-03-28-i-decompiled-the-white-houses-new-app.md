---
layout: post
title: "I Decompiled the White House's New App - ホワイトハウス公式アプリを逆コンパイルしてみた"
date: 2026-03-28T21:24:44.085Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.thereallo.dev/blog/decompiling-the-white-house-app"
source_title: "I Decompiled the White House&#x27;s New App"
source_id: 1547745262
excerpt: "ホワイトハウス公式アプリに外部JS注入や定期GPS追跡など重大なプライバシー問題"
image: "https://thereallo.dev/api/og?title=I%20Decompiled%20the%20White%20House&#x27;s%20New%20App&amp;description=The%20official%20White%20House%20Android%20app%20has%20a%20cookie/paywall%20bypass%20injector,%20tracks%20your%20GPS%20every%204.5%20minutes,%20and%20loads%20JavaScript%20from%20some%20guy&#x27;s%20GitHub%20Pages."
---

# I Decompiled the White House's New App - ホワイトハウス公式アプリを逆コンパイルしてみた
政府公式アプリに隠された「追跡」「外部スクリプト読み込み」「Paywallバイパス」──あなたのスマホは本当に安全か？

## 要約
公式ホワイトハウスAndroidアプリを逆コンパイルしたところ、WebView内で外部サイトの同意バナーや有料壁を消すJavaScript注入、OneSignal経由で動作可能なGPS追跡（前景4.5分／背景9.5分間隔）、および第三者のGitHub Pagesやウィジェットを読み込むサプライチェーンリスクが確認されました。

## この記事を読むべき理由
政府アプリという「信頼」の前提が崩れると、公衆の信頼やプライバシー保護の基準に直接影響します。日本でも同様の技術スタック（React Native/Expo/サードパーティSDK）が広く使われており、今回の発見は自治体や企業アプリの設計検討・監査に即役立ちます。

## 詳細解説
- アーキテクチャとビルド
  - React Native（Expo SDK 54）＋Hermesで実装。アプリロジックはHermesバイトコード（大容量）にコンパイル。
  - バックエンドはWordPressのカスタムREST API（複数のコンテンツエンドポイント）。

- WebView内のJS注入（Consent/Paywall Bypass）
  - アプリはWebViewで外部ページを開く度にCSS/JSを注入し、Cookieバナー・GDPR同意・ログイン壁・ペイウォール等を自動的に非表示にする。
  - MutationObserverで動的に生成される要素も継続的に削除。AndroidのevaluateJavascript()経由で実行。

- 位置情報（Location）インフラ
  - OneSignal SDKの位置収集コードやバックグラウンドサービスがビルドに含まれる。
  - 有効化条件は（1）JS側でのフラグ(setLocationShared)（2）ランタイム許可（正確／概略）付与（3）端末に位置プロバイダがあること、の3つ。インターバルは前景270,000ms（4.5分）／背景570,000ms（9.5分）。
  - 取得データ：緯度経度、精度、タイムスタンプ、前景/背景判定、GPS/ネットワーク区別。OneSignalのプロパティとして同期。

- OneSignalによるプロファイリング
  - タグ付け、SMS紐付け、クロスデバイス識別、コンバージョントラッキング、通知・インアプリメッセージのライフサイクル追跡など、多面的なユーザーデータ収集が組み込まれている。

- サプライチェーン／外部JS
  - YouTube埋め込みで個人のGitHub Pages（例: lonelycpp.github.io）からHTMLをロード。アカウント侵害で任意コードが実行可能に。
  - Elfsightなど商用ウィジェットを外部読み込み。Mailchimp、Uploadcare、Truth Social CDNなど多数の非政府インフラへの依存。

- その他セキュリティ上の懸念
  - 証明書ピンニングなし（標準のTrustManager利用）。中間者攻撃に弱い。
  - 本番に開発用アーティファクト（localhost URL、開発用IP、Expo開発クライアント、exported PreviewActivity）が残っている。
  - file provider設定が外部ストレージルートを露出している箇所あり。

## 日本市場との関連性
- 日本の自治体・政府系アプリでもReact Nativeや外部ウィジェットが増加中。今回の事例は「開発/運用ガバナンス」「サプライチェーン管理」「プライバシー同意の扱い」に関する警鐘です。
- 個人情報保護法（APPI）や利用者の信頼確保の観点から、外部スクリプトや解析SDKの利用は慎重に。国や自治体の公式アプリは特に監査・公開性が求められます。

## 実践ポイント
- ユーザー向け
  - アプリ権限を確認し、不要なら位置情報や通知権限を拒否または撤回する。
  - 民間サイトへアクセスする際は可能な限り端末の標準ブラウザを使う（アプリ内ブラウザは外部JSの影響を受けやすい）。
- 開発者／運用者向け
  - サプライチェーンを明示的に管理し、外部ホストされるスクリプトを最小化／署名検証する。
  - 証明書ピンニングや厳格なCSP、WebViewの分離（サンドボックス）を検討する。
  - 本番ビルドから開発アーティファクトを除去し、第三者SDKの収集項目を限定する（OneSignal等の設定確認）。
  - 公式アプリは公開前に第三者によるセキュリティ監査を行う。

原典: https://blog.thereallo.dev/blog/decompiling-the-white-house-app
