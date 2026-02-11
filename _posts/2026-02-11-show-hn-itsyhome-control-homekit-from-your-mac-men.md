---
layout: post
title: "Show HN: Itsyhome – Control HomeKit from your Mac menu bar - Itsyhome：MacのメニューバーからHomeKitを操作"
date: 2026-02-11T12:13:16.811Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://itsyhome.app"
source_title: "Itsyhome - Control HomeKit from your menu bar"
source_id: 46967898
excerpt: "MacのメニューバーからワンクリックでHomeKit操作、ライブカメラや自動化連携も可能"
image: "https://itsyhome.app/opengraph-image.png?opengraph-image.6bbd32d8.png"
---

# Show HN: Itsyhome – Control HomeKit from your Mac menu bar - Itsyhome：MacのメニューバーからHomeKitを操作
Macのメニューバーでスマートホームを一発操作 — 手元のOne‑Click HomeKit

## 要約
ItsyhomeはmacOSのメニューバーからHomeKit機器を即操作できるネイティブアプリ。軽量で高速、AppKit＋Swiftで構築されオープンソース／買い切りモデルです。

## この記事を読むべき理由
- 日本でもApple製品の利用者が増え、Macで日常のスマート家電を手早く操作したい需要が高まっています。  
- Itsyhomeはシステム全体のショートカットやURLスキーム、Webhooks、iCloud同期などで既存のワークフローに馴染むため、仕事中でも違和感なく使えます。

## 詳細解説
- ネイティブ設計：AppKit＋Swiftで実装。ElectronやWebViewを使わず、アイドル時のCPU/メモリ消費が極小。macOS Sonoma（14）以降が必須。  
- メニューバーUI：カメラ、照明、サーモスタット、ロックなどをワンクリックで表示・切替。よく使う部屋やシーンはピン留め可能。  
- グループ＆シーン：アクセサリをグループ化して一括制御。ルーム／ホーム単位で複数HomeKit環境も切替可能。  
- パワーユーザー機能：グローバルなキーボードショートカット、URLスキーム（例: itsyhome://scene/Goodnight）、CLIとWebhookで外部サービスやスクリプトと連携。  
- Pro機能：ライブカメラフィードのメニュー内表示、ドアベルのピクチャ・イン・ピクチャ、より深い自動化やカスタムアイコン。  
- ハード連携：Elgato Stream DeckやApple TVリモート（Itsytv）連携で物理ボタンやメディア操作と統合可能。  
- ビジネスモデル＆透明性：App Storeで買い切り／Family Sharing対応。ソースは公開されており、サブスク不要を評価する声も多い。  
- サポート機器：HomeKit対応なら基本的に動作。18種類のデバイスタイプに対応（照明・ロック・サーモスタット・カメラ等）。

## 実践ポイント
- まずは動作条件を確認：macOS Sonoma以上＋Apple Homeでデバイス設定済み。ダウンロード: https://itsyhome.app  
- よく使うライト／シーンをピン留めしてワンクリック操作を体験。  
- キーボードショートカットを割り当てて作業中の操作を効率化。  
- URLスキーム／WebhookでShortcutsやRaycast、n8n、cronと連携させると自動化が捗る。  
- Proを試すならドアベル通知やカメラの即時確認を実運用で検証。  
- オープンソースなのでGitHubをチェックしてローカルでビルド／拡張することも可能。
