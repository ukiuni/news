---
layout: post
title: "MuMu Player (NetEase) silently runs 17 reconnaissance commands every 30 minutes - MuMu Player（NetEase）が30分ごとに17の偵察コマンドを密かに実行する"
date: 2026-02-20T03:56:37.482Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://gist.github.com/interpiduser5/547d8a7baec436f24b7cce89dd4ae1ea"
source_title: "MuMu Player Pro (NetEase) silently runs 17 system reconnaissance commands every 30 minutes on macOS · GitHub"
source_id: 47082496
excerpt: "MuMu Playerが30分ごとに17の偵察コマンドでMacを丸裸にしている事実"
image: "https://github.githubassets.com/assets/gist-og-image-54fd7dc0713e.png"
---

# MuMu Player (NetEase) silently runs 17 reconnaissance commands every 30 minutes - MuMu Player（NetEase）が30分ごとに17の偵察コマンドを密かに実行する
毎30分、あなたのMacを“丸裸”にするエミュレータ――MuMu Playerの挙動を分かりやすく解説

## 要約
NetEaseのMuMu Player Pro（macOS）は、動作中に30分ごとに17種類のシステム情報収集コマンドを自動実行し、ネットワーク構成、プロセス一覧（フル引数含む）、インストール済アプリ、/etc/hosts、カーネルパラメータなどをログ化してSensorsDataに紐づけられる形で保持している。利用規約／プライバシーポリシーには明示されていない。

## この記事を読むべき理由
- 日本でもエミュレータ利用はゲームやアプリ開発で一般的。知らぬ間に機密情報や行動履歴が収集される可能性があり、個人・企業ともにリスクがあるため必読。

## 詳細解説
- どこに保存されるか：  
  ~/Library/Application Support/com.netease.mumu.nemux-global/logs/ 以下にタイムスタンプ付きディレクトリを作成し、1回の収集で約400KB、1日で約16回（約30分間隔）程度の収集が行われる。ログは約23回分保持して順次ローテートする。  
- 実行されるコマンド（抜粋）：  
  - arp -a（ローカルネットワークのIP/MAC列挙）  
  - ifconfig / scutil --dns / scutil --proxy（ネットワーク・DNS・プロキシ設定）  
  - cat /etc/hosts（ローカルのホスト設定、開発用ドメイン暴露の可能性）  
  - netstat（アクティブ接続）  
  - ps aux（全プロセスのフル引数。トークンやパス、VPN設定、開発ツールのコマンドライン情報が露出）  
  - ls /Applications, mdls /Applications/*.app（インストールアプリとSpotlightメタデータ）  
  - sysctl -a（カーネルパラメータ、ハード情報、起動時刻）  
  - launchctl print system / launchctl limit（サービス・リソース情報）  
  - mount（マウントポイント）  
  - curl -v https://pro-api.mumuplayer.com 等（MuMu APIへの接続テスト）  
- 追跡・識別：  
  SensorsDataのplistにMacのシリアル番号やUUIDが含まれ、persistentな識別子として使われる。これにより機械単位での行動トラッキングが可能になる。  
- 問題点：  
  - エミュレータの動作に不要な情報まで定期収集している点（透明性の欠如）。  
  - ps auxでのフル引数収集はセッションIDやログイン情報、内部エンドポイントなどセンシティブ情報を含む可能性がある。  
  - ローカルネットワークやhostsの内容が第三者に知られると、社内リソースや開発環境の露見につながる。

## 実践ポイント
- ログの有無確認（まずは確認）：  
```bash
# bash
ls -la ~/Library/Application\ Support/com.netease.mumu.nemux-global/logs/
plutil -p ~/Library/Application\ Support/com.netease.mumu.nemux-global/logs/<TIMESTAMP>/report/sensorsanalytics-com.sensorsdata.identities.plist
```
- 即対応案（優先度高→低）  
  1. 不要ならアンインストール。業務用マシンでは利用を禁止。  
  2. ネットワーク通信を遮断：Little Snitch / LuLu 等で MuMu の外向き通信（pro-api.mumuplayer.com, api.mumuglobal.com等）をブロック。  
  3. ログを確認・消去し、露出した可能性ある秘密（APIキー、トークン等）はローテーション。  
  4. エンドポイントへの通信を監査ログで監視し、社内ポリシーに照らして対応。  
  5. ベンダー（NetEase）へ説明とプライバシー対応を求める／Appleに報告する選択肢も検討。  
- 開発者・企業向け注意点：  
  - CIや開発環境でMuMuを使う場合、ホストの機密情報や社内ネットワークが漏れるリスクを考慮する。  
  - エンドユーザ向けに配布・導入するソフトウェアの選定ポリシーに通信・収集の明示性を組み込む。

短くまとめると、MuMu Playerの現在の振る舞いは「エミュレータに不要な広範なシステムプロファイリング」を行っており、透明性とプライバシーの観点で問題がある。まずはログ確認と通信遮断、不要ならアンインストールを推奨する。
