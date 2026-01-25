---
layout: post
title: "Introducing Kitty Cards - Kitty Cardsの紹介"
date: 2026-01-25T09:17:15.284Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lmno.lol/alvaro/introducing-kitty-cards"
source_title: "Introducing Kitty Cards"
source_id: 838623676
excerpt: "サインイン不要、ブラウザだけでWalletカードを即作成できるKitty Cards"
image: "https://lmno.lol/share.png"
---

# Introducing Kitty Cards - Kitty Cardsの紹介
魅力的で手間いらずな「Apple Walletカード」作成サービス、試してみたくなるシンプルさ

## 要約
ブラウザだけでサインイン不要、追加アプリ不要でApple Wallet用カード（.pkpass）を作れるウェブサービス「Kitty Cards」の紹介。カスタマイズして「Add to Apple Wallet」を押すだけで完了する手軽さが特徴。

## この記事を読むべき理由
日本でも会員証やクーポン、イベントチケットのデジタル化需要が高まる中、ユーザーにアプリをインストールさせずにWalletカードを配布できる手段は実務でとても有用。小売・イベント運営・開発の導入コストを下げる可能性があります。

## 詳細解説
- 背景：従来、Apple Wallet用のパスはPassKitフォーマット（.pkpass）を生成・署名する必要があり、開発や配布に証明書管理や専用アプリ、または煩雑なウェブUIが必要になることが多かった。作者は以前にiOSツールやEmacsでQRを扱う実験をしていたが、現実運用としては非実用的と判断。
- Kitty Cardsの特徴：ウェブ上でカードをカスタマイズし、追加ボタンで直接Apple Walletに組み込める。サインインやアプリのダウンロードを求めない点が最大の売り。裏側ではPassKit互換のパスを生成してブラウザ経由で配布していると考えられる（.pkpassの一般的な配布フロー）。
- 技術ポイント（初級向けに解説）：
  - .pkpassは複数のリソース（JSON、画像）をまとめ、開発者用の証明書で署名したパッケージ。
  - iOSのSafariやMailから正しいMIME/typeで配布すると「Add to Apple Wallet」ボタンで追加可能。
  - Kitty Cardsはその生成・署名・配送をウェブサービス側で完結させ、ユーザーは設定→追加の手間だけで済む設計。

## 実践ポイント
- すぐ試す：iPhoneのSafariで kitty.cards にアクセス → カードをカスタマイズ → 「Add to Apple Wallet」を押す（iOS対応が前提）。
- 用途例：店舗の会員証、イベントチケット、クーポン、テスト用のサンプルパス作成。
- 開発者向け注意：自前で同様の仕組みを作るにはPassKit証明書が必要。セキュリティや署名の扱いに注意すること。
- 法規・運用：顧客情報を扱う場合はプライバシーや利用規約を確認。Kitty CardsはLMNO.lolが運営、プライバシーポリシー/利用規約がある点を確認する。

元記事（Introducing Kitty Cards）をベースに、まずはブラウザでの手軽さを試してみるのが早道です。
