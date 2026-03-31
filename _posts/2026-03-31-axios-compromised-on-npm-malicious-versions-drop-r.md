---
layout: post
title: "Axios Compromised on NPM – Malicious Versions Drop Remote Access Trojan - Axiosがnpmで侵害 — 悪意あるバージョンがRATを配布"
date: 2026-03-31T03:59:55.004Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.stepsecurity.io/blog/axios-compromised-on-npm-malicious-versions-drop-remote-access-trojan"
source_title: "axios Compromised on npm - Malicious Versions Drop Remote Access Trojan - StepSecurity"
source_id: 47582220
excerpt: "人気ライブラリaxiosがnpmで乗っ取られ、依存でRATが自動配布される危機"
---

# Axios Compromised on NPM – Malicious Versions Drop Remote Access Trojan - Axiosがnpmで侵害 — 悪意あるバージョンがRATを配布
Axiosがnpmで乗っ取られた：依存関係1つでシステムにRATが落とされる恐るべき手口

## 要約
人気HTTPクライアントaxiosのnpmリリース（axios@1.14.1 と axios@0.30.4）が乗っ取られ、依存パッケージのpostinstallスクリプト経由でクロスプラットフォームのリモートアクセス型マルウェア（RAT）を配布していました。

## この記事を読むべき理由
Axiosは日本でも幅広く使われるライブラリで、CI/CDやフロント／サーバー側問わず影響範囲が大きいです。依存関係だけでマルウェアが動く「見えない侵入」の手口は、初級者でも理解しておくべき実務的リスクです。

## 詳細解説
- 侵害の概要  
  - 被害バージョン：axios@1.14.1、axios@0.30.4（2026-03-31 公開）  
  - 発行者アカウント（jasonsaayman）が乗っ取られ、メールをProtonMailに差し替えてnpm CLIで手動公開。GitHub ActionsのOIDCトラストを介さない手動公開だったため、npmメタデータに「trustedPublisher」「gitHead」が無い点が異常な痕跡です。  
- マルウェアの仕組み  
  - axios本体には悪意あるコードは含まれておらず、package.jsonにphantom依存 plain-crypto-js@4.2.1 を追加。ソース内で一切import/requireされないが、npmは依存をインストールし、そのパッケージのpostinstallが実行される。  
  - plain-crypto-js の postinstall が実行され、obfuscatedな setup.js（ドロッパー）を走らせてC2（http://sfrclak.com:8000/6202033）へ接続し、プラットフォーム別の二次ペイロード（macOS, Windows, Linux）をダウンロードして実行する。  
  - 実行後は自身を消し、package.json をクリーンなスタブ（package.md をリネーム）で置き換え、痕跡を隠蔽する。  
- 攻撃の段取り（要点）  
  1. plain-crypto-js@4.2.0（クリーンなデコイ）を先に公開して履歴を作る。  
  2. plain-crypto-js@4.2.1 にpostinstallとドロッパーを追加。  
  3. 乗っ取ったmaintainerでaxiosの2系統（1.x/0.x）に同時注入して幅広く感染させる。  
- ドロッパーの動作（要点）  
  - macOS：AppleScriptでC2からバイナリを落とし /Library/Caches/com.apple.act.mond に配置して実行。  
  - Windows：VBScript→PowerShell経由でPowerShell RATを取得・実行、%PROGRAMDATA%\wt.exe を恒久配置。  
  - Linux：curlで /tmp/ld.py を取得して nohup python3 で実行。  
  - いずれも実行後に開始スクリプトや一時ファイルを消して痕跡を削除する設計。

## 実践ポイント
- 今すぐ確認・対応（優先）  
  - 影響版をインストールしていたら「被害を前提」に対応。安全版へピン（axios@1.14.0 または axios@0.30.3）。  
  - すぐに秘密情報（トークン、鍵、パスワード）をローテーション。特にCI/デプロイ用のnpmトークンやクラウド資格情報。  
- コマンド例（確認・差し替え）
```bash
# プロジェクト内のaxiosバージョン確認
npm ls axios

# 影響版を安全版へ置換（例）
npm install axios@1.14.0 --save-exact

# plain-crypto-js が入っていないか確認
grep -R "plain-crypto-js" node_modules || true

# npm audit / ローカルスキャン
npm audit --audit-level=high
```
- 検出すべき痕跡（優先チェック）  
  - ネットワークログで http://sfrclak.com:8000/6202033 への通信や外向きPOST（packages.npm.org/... を含むPOSTボディ）  
  - ファイル痕跡：/Library/Caches/com.apple.act.mond、%PROGRAMDATA%\wt.exe、/tmp/ld.py、node_modules/plain-crypto-js 配下の package.json の改変や postinstall スクリプト  
  - npm レジストリのメタデータで該当リリースに trustedPublisher/githHead が無いか確認
- 予防策（組織的対策）  
  - npmの公開にOIDCトラストを必須化、長期トークンは最小権限・短命化、二段階認証（2FA）必須化。  
  - package-lock.json / yarn.lock の固定、依存の定期スキャン（Snyk/Dependabot/OSSスキャナ）。  
  - CIでpublishを限定し、個人トークンでの手動publishを禁止。公開アクションのログとnpmメタを監視して異常を検出。  
  - 開発者に対して「依存に未使用パッケージ（manifestにあるがコードで参照されない）」は重大インジケーターである旨を周知。

短くまとめると、今回の攻撃は「依存宣言だけでマルウェアを走らせる」というシンプルで効果的な手口です。npm公開のガバナンス、トークン管理、依存の監視を早急に見直してください。
