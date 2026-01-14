---
layout: post
title: "Show HN: Tiny FOSS Compass and Navigation App (<2MB) - 小さくて自由なコンパス＆ナビアプリ（<2MB）"
date: 2026-01-14T11:59:27.438Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/CompassMB/MBCompass"
source_title: "GitHub - CompassMB/MBCompass: Modern FOSS Compass and Navigation app without Ads, IAP or Tracking"
source_id: 46614688
excerpt: "2MB未満で広告・追跡なし、磁場表示対応の高精度オープンコンパス兼ナビアプリ"
image: "https://repository-images.githubusercontent.com/830628742/9e7f6fda-3112-4246-923a-dd8a4eff79a9"
---

# Show HN: Tiny FOSS Compass and Navigation App (<2MB) - 小さくて自由なコンパス＆ナビアプリ（<2MB）
思わず入れたくなる、広告ゼロ・追跡ゼロの軽量ナビアプリ — ポケットに入る“開かれた”方位計

## 要約
MBCompassはJetpack Composeで作られた軽量なオープンソースのコンパス兼ナビアプリ。広告やアプリ内課金、トラッキングなしで方位・現在地・磁場強度を表示します。

## この記事を読むべき理由
プライバシー意識が高まる今、広告やトラッキングのない純粋なナビツールは価値があります。特に日本では登山や防災、通勤時の代替ツールとして実用的で、ストレージが限られた端末にも嬉しい軽さ（<2MB）が魅力です。

## 詳細解説
- 技術スタックと互換性  
  MBCompassはKotlinとJetpack Compose（Material Design）で実装され、Android 5.0+で動作。UIはComposeで組まれているため、レスポンシブでモダンな見た目を保ちつつ軽量に動作します。

- センサーと精度向上  
  単なる方位表示に留まらず、加速度計、磁力計、ジャイロスコープを組み合わせたセンサーフュージョンで精度を高めています。磁場強度（µT）表示や磁北・真北の切り替えもサポートし、コンパスとしての信頼性が高い設計です。

- 地図と位置情報  
  GPSによるライブ位置追跡をOpenStreetMap上で表示（位置権限は地図表示のためのみ使用）。地図の利用はオープンデータ基盤を活用しており、ブラックボックスな追跡は一切ありません。

- UXと機能  
  ライト／ダーク（True AMOLED暗色モード検討中）テーマ、ナビ中に画面を常時点灯させるオプション、ランドスケープ表示対応など実用寄りの機能を備えます。デザイン提案（v2.0）には速度計やUI刷新案もあります。

- ライセンスとコミュニティ  
  GPL‑3.0で公開されており、ソースの閲覧・改変・再配布は可能ですが、派生物を閉源化したり広告やトラッキングを付与して配布することは許されません。翻訳はWeblateで受け付け、寄付・スポンサーで継続的な開発を支援できます。

- 評価と実績  
  Product HuntやHacker News、Android Weeklyで注目されるなどコミュニティでも認められています。

## 実践ポイント
- 今すぐ試す：GitHubリポジトリ（またはF‑Droid配布がある場合はF‑Droid）からAPKを入手、あるいはソースをクローンしてビルド（Android Studioで開き、gradlew assembleDebug）。  
- 開発者・翻訳で貢献：Kotlin/Jetpack Composeのプロジェクトなので、UI改善や機能追加のPRが歓迎。日本語化はWeblate経由で参加可能。  
- 活用シーンの提案：登山・キャンプ・災害時の非常持ち出し、プライバシー重視の街歩きナビとして常備アプリに。  
- ライセンス注意：商用利用や再配布を考える場合はGPL‑3.0の制約（派生物の公開義務など）を確認すること。  
- 寄付で継続を支援：広告を入れない方針を維持するため、作者に寄付で支援するとプロジェクトの継続に貢献できます。

興味が湧ったらまずリポジトリ（compassmb/MBCompass）と公式サイトをチェックしてみてください。軽くてプライバシーに配慮された代替ナビとして、日本でもすぐ役立つはずです。
