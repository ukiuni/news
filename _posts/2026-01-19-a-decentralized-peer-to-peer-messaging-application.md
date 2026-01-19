---
layout: post
title: "A decentralized peer-to-peer messaging application that operates over Bluetooth - Bluetooth上で動作する分散型ピアツーピアメッセージングアプリ"
date: 2026-01-19T07:49:57.593Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://bitchat.free/"
source_title: "bitchat"
source_id: 46675853
excerpt: "インターネット不要で中継可能、Bluetoothメッシュで検閲・停電時も通信する分散型メッセージアプリ"
---

# A decentralized peer-to-peer messaging application that operates over Bluetooth - Bluetooth上で動作する分散型ピアツーピアメッセージングアプリ
ネット不要で届くメッセージ──Bluetoothメッシュでつながる「bitchat」の全貌

## 要約
インターネットやサーバーを使わず、近接する端末同士で自動的に中継して通信するBluetoothメッシュ型の分散メッセージアプリ「bitchat」。検閲や通信遮断に強く、災害時やオフライン環境での通信手段として注目される。

## この記事を読むべき理由
日本は地震や大規模停電が起きやすく、イベントやデモでの通信制限も懸念される。インターネットに頼らないメッセージングは有用な代替手段になり得るため、仕組みや実用上の注意点を理解しておく価値がある。

## 詳細解説
- 動作原理  
  - bitchatはBluetoothメッシュネットワークを使い、近くにいる端末を自動検出してピアツーピアで接続する。各端末がクライアント兼サーバーとなり、メッセージを複数ホップで中継して到達範囲を広げる。  
  - 結果として中央サーバーや電話番号が不要になり、インターネットが使えない状況でも端末同士で通信が成立する。

- セキュリティと耐検閲性  
  - 中央インフラに依存しないため、監視や一元的な遮断に強いという設計思想。実際の暗号化や鍵管理の実装詳細は技術文書（whitepaper）やソースコードを確認する必要がある。

- プラットフォームと入手先  
  - iOS / macOS: App Store版あり。ソースコードは GitHub（permissionlesstech/bitchat）。対応は iOS 16.0+、macOS 13.0+。Xcode/XcodeGen または Swift Package Manager でビルド可能。  
  - Android: Play Store版と GitHub（permissionlesstech/bitchat-android）。Android 8.0+（API 26）対応。iOS版とプロトコル互換。apkリリースも公開されている。  
  - ソフトウェアはパブリックドメインでリリースされているため、フォークや実験がしやすい。

- 制約と実務上の注意点  
  - 範囲はBluetoothの通信距離に依存する（屋内外の環境で大きく変わる）。中継ノードが少ないと到達性が下がる。  
  - バッテリー消費、Bluetoothの常時スキャンの可否、OSごとのバックグラウンド制限、プライバシー設定や規制などの影響を受ける。  
  - 暗号化やメッセージの改ざん防止、ノード認証の実装状態は実装次第なので、機密情報のやり取りには注意が必要。

## 実践ポイント
- まずはユーザー体験を確認：App Store / Play Store でインストールして、友人と近距離で試す。  
- ソースを読む：GitHubリポジトリと whitepaper を確認して暗号化や中継ロジックの実装を検証する。  
- 小規模イベントでの運用テスト：フェスや勉強会など、人が集まる場でメッシュの広がりやバッテリー影響を測定する。  
- 災害対策に組み込む場合：他の通信手段（衛星、FM、ローカル無線）との併用を検討し、安全ポリシーと運用ルールを策定する。  
- 貢献と改良：パブリックドメインなので、日本語ドキュメントの整備やローカル向け改善（省電力最適化、UI日本語化）に貢献できる。

公式情報・コード（参照）  
- プロジェクトページ: https://bitchat.free/  
- iOS/macOS ソース: https://github.com/permissionlesstech/bitchat  
- Android ソース / apk: https://github.com/permissionlesstech/bitchat-android
