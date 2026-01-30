---
layout: post
title: "Track Your Routine – Track Your Routine は日課管理アプリ"
date: 2026-01-30T13:56:33.236Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/MSF01/TYR"
source_title: "GitHub - MSF01/TYR: Track Your Routine is a Flutter application that allows users to input and track their daily routines, providing notifications for upcoming events."
source_id: 46823358
excerpt: "Flutter×Firebase製の多機能日課管理アプリ、今すぐ試して日本語化や社内導入を検討"
image: "https://opengraph.githubassets.com/451902139de951a288af5943d2e555491dcfb6ffe048836927840bd67668ac5b/MSF01/TYR"
---

# Track Your Routine – Track Your Routine は日課管理アプリ
毎日の「やること」を習慣化するためのオープンソースFlutterアプリ — 今すぐ試せる生産性ツール

## 要約
Track Your Routine（TYR）はFlutter×Firebaseで作られたクロスプラットフォームなタスク／日課管理アプリ。ローカル通知やリアルタイム同期を備え、PC・モバイル・Webで動作します。

## この記事を読むべき理由
日本でもリモートワークやスマホ中心の生活が定着する中、軽量で自分好みに拡張できる日課管理アプリは有用です。オープンソースなので学習用や社内ツールのベースに最適です。

## 詳細解説
- 基本設計  
  - フロントはFlutter（Dart）で実装、Firebase Authで認証、Cloud Firestoreでタスクをリアルタイム同期。ローカル通知は flutter_local_notifications を利用。
- 主な機能  
  - アカウント登録／ログイン（Email/Password）、パスワード変更、プロフィール更新。  
  - タスク作成（タイトル・説明・日時・カテゴリ）、カテゴリ例：Work／Vacation／Party。作成時に確認通知を発行、予定時刻にリマインド。  
  - モダンなダークテーマ（Material 3）、レスポンシブUI、Google Fonts利用。  
- マルチプラットフォーム対応  
  - Android / iOS / Web / Windows / Linux / macOS をサポート。  
- 技術スタック（要点）  
  - Flutter（SDK >= 2.19.3）／Dart、Firebase Core / Auth / Firestore、shared_preferences、file_picker、intl 等。  
- 開発・実行の流れ（主要コマンド）  
  - リポジトリをクローンして依存取得、Firebase設定を行い実行：  
    ```bash
    git clone https://github.com/MSF01/tyr.git
    cd tyr
    flutter pub get
    flutterfire configure   # Firebase設定の自動生成
    flutter run -d chrome   # 例：Webで実行
    ```
- 注意点（日本向け）  
  - Firestoreにデータが保存されるため、社内で使う場合はデータ保管場所や個人情報管理を確認。iOSの通知権限やAndroidのチャネル設定は手動確認が必要。  
  - 既存READMEに英語中心の説明があるため、日本語化（ローカライズ）とDate/Timeのローカルフォーマット対応が実装ポイント。

## 実践ポイント
- まずはローカルで起動して通知フローを確認：`flutter run` → タスクを作成 → 通知が出るか検証。  
- Firebaseは `flutterfire configure` で `lib/firebase_options.dart` を生成すると楽。  
- 日本語対応：intl を使い文字列と日時フォーマットを翻訳・調整する。  
- カスタマイズ案：定期タスク（Recurring）、タスク編集・削除、カレンダー連携、通知サウンドのカスタム化。  
- 貢献方法：Fork → ブランチ → PR。社内テンプレとして使うなら、認証やデータ保持ポリシーを組み込む。

以上を踏まえ、学習用・プロトタイプ用として手を動かしやすいオープンソースです。興味があればリポジトリをフォークして日本語化や機能追加を試してみてください。
