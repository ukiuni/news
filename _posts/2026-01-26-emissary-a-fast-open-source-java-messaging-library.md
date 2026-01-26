---
layout: post
title: "Emissary, a fast open-source Java messaging library - Emissary：高速オープンソースJavaメッセージングライブラリ"
date: 2026-01-26T09:53:28.196Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/joel-jeremy/emissary"
source_title: "GitHub - joel-jeremy/emissary: Emissary is simple, yet 🗲FAST🗲 messaging library for decoupling messages (requests and events) and message handlers 🚀"
source_id: 46723049
excerpt: "反射を使わず1000%高速化可能な軽量Javaメッセージングライブラリを試す"
image: "https://repository-images.githubusercontent.com/532778554/923c0b0a-6aff-48b0-b6e5-44bf9b2fe796"
---

# Emissary, a fast open-source Java messaging library - Emissary：高速オープンソースJavaメッセージングライブラリ
1000%スループット向上も？反射を使わず軽量に動くJavaメッセージングライブラリ「Emissary」を試す

## 要約
Emissaryは依存を最小限に抑え、java.lang.invoke.LambdaMetafactoryを活用して反射コストを避けることで高速なメッセージ（Request/Event）ディスパッチを実現する軽量ライブラリです。CQRSやイベント駆動設計と相性が良く、DI（Spring/Guiceなど）との統合も簡単です。

## この記事を読むべき理由
SpringのApplicationEventPublisherなど既存の仕組みでパフォーマンスが気になる場面や、ドメイン層に余計な依存を入れたくない設計（Hexagonal/DDD）を採るプロジェクトに、低レイテンシ／高スルループットな代替を素早く導入できるため。

## 詳細解説
- 基本概念  
  - Requests: 単一ハンドラが処理するコマンド／クエリ。  
  - Events: 複数ハンドラに配信される発生通知。  
  - ハンドラはアノテーション（@RequestHandler / @EventHandler）でマークし、Dispatcher/Publisher経由で送受信する。

- 高速化の仕組み  
  - リフレクションを直接呼ぶ代わりにLambdaMetafactoryでメソッド参照を動的生成し、ハンドラ呼び出しをほぼ通常メソッド呼出し並みに高速化。著者のベンチマークでは類似ライブラリ比でスループットが大幅に向上したと報告されています。

- DI統合と拡張性  
  - InstanceProviderでインスタンス取得戦略を差し替え可能（SpringのApplicationContext::getBeanやGuiceのInjector::getInstance、手動new等に対応）。  
  - ドメイン層に依存を持たせたくない場合はカスタムアノテーションを使ってハンドラをマークし、外側でEmissaryに紐づけられます。  
  - 同期／非同期など呼び出し戦略はプラグイン可能（Sync/Asyncの既定実装あり、独自実装も登録可）。

- モジュール/配布  
  - Maven/Gradleで導入可能。v2以降はアーティファクトが emissary-core に改名されています。

- 日本市場との関連性  
  - 日本の多くのプロジェクトはSpring Bootやマイクロサービス、オンプレでの低レイテンシ要件が多く、ApplicationEventPublisherの代替やCQRS導入時の軽量ミドルウェア候補として有力です。ドメイン層の軽さを重視する企業文化にも合います。

## 実践ポイント
- まずは依存を追加して評価（Gradle/Mavenの例）。
```java
// Gradle
implementation "io.github.joel-jeremy.emissary:emissary-core:${version}"
```
- SpringプロジェクトではInstanceProviderにapplicationContext::getBeanを渡して差し替えテストを実施。  
- 既存のApplicationEventPublisherと比較ベンチを取り、スループット／レイテンシの改善効果を確認する。  
- ドメインパッケージにEmissary依存を入れたくない場合はカスタムハンドラアノテーションを定義して外側でマッピングする。  
- 複数ハンドラを並行処理したい場合はAsyncEventHandlerInvocationStrategy等を利用・カスタム実装も検討する。

短時間で組み替えて効果が実感しやすいので、イベント駆動やCQRSを試すPoCとしてまず導入してみることを推奨します。
