---
layout: post
title: "Show HN: A native macOS client for Hacker News, built with SwiftUI - SwiftUIで作られたネイティブmacOS向けHacker Newsクライアント"
date: 2026-02-20T14:58:08.308Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/IronsideXXVI/Hacker-News"
source_title: "GitHub - IronsideXXVI/Hacker-News"
source_id: 47088166
excerpt: "SwiftUI製macOS向けHNクライアント、広告除去・コメント折畳み・自動更新搭載"
image: "https://opengraph.githubassets.com/0c19f3a2ecb736a308c0d423b13986b1a75151a5c37c21d6a29270c65f46f671/IronsideXXVI/Hacker-News"
---

# Show HN: A native macOS client for Hacker News, built with SwiftUI - SwiftUIで作られたネイティブmacOS向けHacker Newsクライアント

Hacker NewsをMacのデスクトップ体験で快適に読む──SwiftUIで作られたネイティブアプリが公開されています。

## 要約
SwiftUIで実装されたmacOS向けHacker Newsクライアント。DMG配布とMITライセンスのソースがあり、記事閲覧用の組み込みWebビュー（広告・ポップアップブロック）、コメント折りたたみ、HNログイン、Sparkleによる自動更新などを備えます。

## この記事を読むべき理由
グローバルな技術ニュースを効率的に追いたい日本の開発者にとって、ネイティブUI／自動更新／オフの煩わしさを減らすWebビュー機能は実用価値が高い。SwiftUIの実運用例としてコードを読み解けば、macOSアプリ開発の学びも得られます。

## 詳細解説
- 技術スタック: Swift（SwiftUI）で100%実装。Xcodeプロジェクトとして公開。  
- 配布とビルド: リリースからDMGで配布（macOS 14.0以上が必要）。ソースからはgit cloneしてXcode 26+でビルド可能。Swift Package（例：Sparkle）は自動解決。  
- 主な機能: Top/New/Best/Ask/Show/Jobsの閲覧、組み込みWebビュー（記事表示）、広告・ポップアップブロック、コメントスレッドの折りたたみ、HNアカウントのログインとセッション管理、Sparkleによるネイティブ自動更新。  
- UX/設計観点: SwiftUIベースなのでmacOSのネイティブ感を保ちつつ、宣言的UIで状態管理やスレッド表示を簡潔に実装できる点が学習価値。Sparkleなどの既存ライブラリ統合例も参考になる。  
- ライセンスとコントリビューション: MITライセンス、スター20・フォーク1（執筆時）。改造やローカライズの余地が開かれている。

## 実践ポイント
- まずDMGをダウンロードして触ってみる（macOS 14以上）。  
- 学びたいならリポジトリをクローンしてXcode 26+でビルド、WebViewやログイン周りの実装を追う。  
- 日本語化／ローカライズやPocket連携、mastodon/Slack共有などの機能追加は実用的な貢献先。  
- SparkleやSwiftUIの実装パターンを参考にして、自身のmacOSアプリ開発に応用する。
