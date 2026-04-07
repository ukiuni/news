---
layout: post
title: "Using Discord on Plan 9 - Plan 9でDiscordを使う"
date: 2026-04-07T01:22:42.872Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://pmikkelsen.com/plan9/discord"
source_title: "plan9 - discord"
source_id: 959293219
excerpt: "9frontでGo製ボットとスクリプトでacmeからDiscordに参加する方法"
---

# Using Discord on Plan 9 - Plan 9でDiscordを使う
手元の9frontからDiscordに参加するための「小さくて賢い」ボット連携術

## 要約
9front上で動く小さなGo製サーバとシェルスクリプト群で、Discordのチャットをacmeや端末から送受信できる仕組みを紹介する記事の日本語要約。

## この記事を読むべき理由
Discordを使うチームでも、レガシー/実験的なOS（ここではPlan 9/9front）で作業していると同僚と同じチャットに参加できない。日本のニッチな開発環境や趣味のサーバ運用で、既存インフラを壊さずDiscordに接続したい人に実用的な手法を提供します。

## 詳細解説
- 構成
  - 中核はDiscordと通信するGoプログラム（事実上のサーバプロセス）。これがDiscord APIとやり取りする。
  - シェルスクリプト群はログ整形や操作のラッパー。実際の送受信はGoプログラムが行う。
  - 通信の入り口はPlan 9のファイルシステム経由：`/srv/discordfront` というパイプが公開され、ここに書き込む/読むことでメッセージのやり取りを行う設計。

- 動作の流れ
  1. Discord側でBotを作成しアクセストークンを取得、サーバへ招待する。
  2. 9frontでサーバプロセスを起動：
```bash
# bash
discordsrv YOURTOKEN
```
  3. discordsrvは`/srv/discordfront`を公開し、受信メッセージはログファイルへ整形出力される：
    $home/lib/discord/logs/$serverName/$channelName
  4. クライアント側スクリプト（例：discord, discordacme）がログをtail -fしつつ標準入力を読み、書き込みを`/srv/discordfront`へ送ることで双方向チャットを実現。

- acme統合とリモート運用
  - `discordacme`を使えばacme内でチャネル一覧（$home/lib/discord/channels）を開き、ワンクリックでチャットウィンドウを作れる。
  - サーバ側は常時稼働させるのが推奨。クライアント側はrimportでリモートの`/srv`やログツリーをインポートして利用可能：
```bash
# bash
rfork rimport -ac -p serverhost /srv
rimport -c -p serverhost /usr/glenda/lib/discord
```

- 既知の制約
  - 過去ログの取得はサーバでログを残しておかないと難しい（クライアントは過去メッセージを取得しない）。
  - 機能は最小限、名称や実装は簡素。事前の検証も限定的。

- 実装入手
  - 元プロジェクトはソースと9front amd64向けのプレコンパイル版を提供。

## 実践ポイント
- 最短手順
  1. DiscordでBot作成・トークン取得・サーバ招待。
  2. 9front上で`discordsrv YOURTOKEN`を常時稼働させログを残す。
  3. ローカル/別ホストの9frontからrimportで`/srv`とログをマウントし、`discord`スクリプトや`discordacme`で会話。

- 運用のコツ
  - サーバは常時オンラインのマシンに置いてログを残す（過去メッセージ参照のため）。
  - acmeで複数チャンネルを管理すると視認性が上がる。
  - セキュリティ：Botトークンは秘匿、権限は最小限に絞る。

- 日本での活用例
  - 研究室やニッチな開発コミュニティで、古典的なOS/ツール群を使いながらDiscord中心のチームに参加する際に有用。

元記事の趣旨は「既存のシンプルな道具立てを活かして無理なくDiscordに接続する」こと。興味があれば、ソースを落としてdockerや実機上で試すところから始めてください。
