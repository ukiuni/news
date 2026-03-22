---
layout: post
title: "Teaching Claude to QA a mobile app - ClaudeにモバイルアプリのQAを教える"
date: 2026-03-22T20:59:52.894Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://christophermeiklejohn.com/ai/zabriskie/development/android/ios/2026/03/22/teaching-claude-to-qa-a-mobile-app.html"
source_title: "Teaching Claude to QA a Mobile App"
source_id: 47480900
excerpt: "ClaudeでAndroidは高速自動QA、iOSはSimulator制約を克服してバグ自動報告"
---

# Teaching Claude to QA a mobile app - ClaudeにモバイルアプリのQAを教える
朝イチで自動スクリーン走査・スクショ解析しバグ報告までやるAI QAの正体 — Androidは90分、iOSは6時間超の理由

## 要約
単一コードベース（React + Capacitor）で3プラットフォームを維持する個人開発者が、LLM（Claude）にモバイル版の自動QAをさせた事例。AndroidはWebViewのCDPで短時間に自動化できたが、iOSはSimulatorの制約で苦戦し大量のワークアラウンドを要した。

## この記事を読むべき理由
モバイルクロスプラットフォーム開発と自動化の“現実”がわかる。特に日本のスタートアップや少数精鋭チームが、限られたリソースで信頼できるQAを回す際の実践的ヒントが得られる。

## 詳細解説
- 背景：作者はReactでサーバ駆動UIを作り、Capacitorで同じWebコードをAndroid/iOSネイティブシェルに包んだ。一コードで素早く展開できる反面、テストは「ネイティブでもない、ブラウザでもない」中間領域に陥る。
- Androidのやり方（短時間で成功）
  - エミュレータのlocalhostは別扱いなので adb reverse が必要：
```bash
adb reverse tcp:3000 tcp:3000
adb reverse tcp:8080 tcp:8080
```
  - Android WebViewはChrome DevTools Protocolのソケットを公開するため、それをローカルポートにフォワードするとPlaywrightと同等の操作が可能：
```bash
# WebViewソケットを特定してフォワード
WV_SOCKET=$(adb shell "cat /proc/net/unix" | grep webview_devtools_remote | grep -oE 'webview_devtools_remote_[0-9]+' | head -1)
adb forward tcp:9223 localabstract:$WV_SOCKET
curl http://localhost:9223/json
```
  - CDP経由でlocalStorageにJWTを注入し navigate すれば座標推測不要。adb shell screencapでスクショを取り、画像解析→S3アップ→フォーラムに自動でバグ報告するパイプラインを構築。25画面を約90秒で巡回。
- iOSの地獄（長時間のトラブルシューティング）
  - WKWebViewはCDPを公開せず、Safari側のプロプライエタリプロトコルやツールの制約（ios-webkit-debug-proxyは実機向け等）で制御が難しい。
  - Simulator固有の問題：メール入力で「@」が送れない（キーボードショートカットに変換される）、macOS⇄Simulatorのペースト問題、ネイティブ通知ダイアログが外部操作では消せない等。
  - 対処例：バックエンドとフォーム（type="email"→type="text"）を一時的に変更してユーザ名でログイン、TCC.db（権限DB）に直接書き込みして通知権限を事前承認、ui_describe_pointでアクセシビリティ情報を調べてからidbで正確にタップするなどの複合的ワークアラウンドを適用。これにより全画面巡回が可能になったが、手順は壊れやすく順序依存。
- 工夫と落とし穴：CLAI﻿DE（エージェント）でリポジトリのworktreeを使う意図があったが、誤ってメイン作業ツリーでcommit→PR→自動mergeをしてしまい大量の不要差分を混入。最後はテストをローカルで回して解決する羽目に。教訓は「隔離と先にテストを回すこと」。

## 実践ポイント
- まずAndroidでCDPが使えないか探す（/proc/net/unix に webview_devtools_remote があればチャンス）。
- エミュレータでlocalhost接続は adb reverse で解決。
- 可能ならCDP経由でlocalStorageにJWTを注入してログインすると堅牢（座標依存を減らす）。
- iOSはSimulatorの制約が多い：テスト用の回避策（ユーザ名ログイン、事前権限設定、アクセシビリティで座標検出→正式タップ）を用意するが、脆弱性を理解しておくこと。
- CIに流す前に必ずローカルでテストを実行し、変更は必ず隔離されたworktreeで行う。
- 要望：AppleはSimulatorのWebViewにCDPか安定したWebDriver相当を公開してほしい。

以上。必要なら、AndroidのCDPスクリプト例やiOSで使ったui_describe_point/idbコマンドのサンプルを出します。
