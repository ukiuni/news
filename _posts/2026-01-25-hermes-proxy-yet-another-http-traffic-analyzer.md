---
layout: post
title: "Hermes Proxy - Hermes Proxy（ヘルメス・プロキシ）"
date: 2026-01-25T15:41:36.944Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/jp/Hermes-Proxy"
source_title: "GitHub - jp/Hermes-Proxy: Hermes Proxy - the divine middleware for messages in transit."
source_id: 417884178
excerpt: "Electron製軽量HTTP/HTTPSプロキシ—再送・HAR・遅延でAPI検証"
image: "https://opengraph.githubassets.com/7ffc552d511b3981b9e7d4214193721dd19b45e5d5ae93af865a909f783b0b1e/jp/Hermes-Proxy"
---

# Hermes Proxy - Hermes Proxy（ヘルメス・プロキシ）
CharlesやFiddlerの代わりに使いたくなる？軽量Electron製HTTP/HTTPSインターセプター

## 要約
Hermes ProxyはElectron＋Viteで作られたデスクトップのHTTP/HTTPSトラフィック解析アプリ。リクエスト/レスポンスのキャプチャ、再送信（URL/ヘッダ編集可）、HARの入出力、レスポンス保存、ルールによる遅延・上書き・切断が特徴です。

## この記事を読むべき理由
日本の開発現場でもAPIデバッグやモバイル端末のプロキシ、QAでの再現テストは必須作業。Hermes ProxyはOSSで手元ですぐ試せるため、商用ツールに頼らず問題解析や学習に使えます。

## 詳細解説
- アーキテクチャ：Electron（デスクトップUI）＋Vite（レンダラー開発）で構成。パッケージはelectron-builderでmacOS/Windows/Linux向けに出力可能。リポジトリはHTML/JavaScript/CSSが中心。
- 主な機能：
  - ライブトラフィック表：送受信の詳細を一覧で確認。
  - リクエスト再送（Replay）：URLやヘッダを編集して再送信し、APIの挙動を検証。
  - HAR入出力：既存のHARをインポートして解析テーブル化、全トラフィックをHARでエクスポート。
  - レスポンスボディ保存：レスポンスをファイルとして保存し、オフライン解析が可能。
  - ルールエンジン：HTTPメソッド/ホスト/URL/ヘッダでマッチさせ、意図的に遅延を入れたりヘッダを書き換えたり接続を切断したりできる（ネットワーク障害やレイテンシの再現に有効）。
- 開発・ビルド：
  - 依存インストール、開発起動、ビルド、バイナリ生成のnpmスクリプトを同梱。

例：ローカルで試すコマンド
```bash
npm install
npm run dev       # Vite + Electronで開発起動
npm run build     # レンダラーをビルド
npm run dist -- --publish never  # バイナリを作成
```

## 実践ポイント
- まずはローカルでnpm run devして、自分のAPIをキャプチャしてみる。
- HARをエクスポートしてチームで共有、課題の再現手順を明確化。
- ルールエンジンで遅延やヘッダ上書きを設定し、フロントのエラーハンドリングやタイムアウト挙動を検証。
- Charles/Fiddlerに馴染みがあるなら、HermesはOSSで軽量な代替候補として試す価値あり。
- モバイル端末をプロキシ経由にして、実機のトラフィック解析にも活用可能。

リポジトリ状況：小規模なOSS（初期リリース0.0.1、貢献者少数）なので、現場導入前に安定性やセキュリティ設定は確認してください。
