---
layout: post
title: "1-Click RCE to steal your Moltbot data and keys - 1クリックでMoltbotのデータと鍵を盗む"
date: 2026-02-01T21:49:08.739Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://depthfirst.com/post/1-click-rce-to-steal-your-moltbot-data-and-keys"
source_title: "depthfirst | 1-Click RCE To Steal Your Moltbot Data and Keys"
source_id: 46848769
excerpt: "1クリックでMoltbot(OpenClaw)の認証トークンとローカル実行権を奪う深刻なRCE脆弱性"
---

# 1-Click RCE to steal your Moltbot data and keys - 1クリックでMoltbotのデータと鍵を盗む
たった1回のクリックでAIアシスタントが乗っ取られる：OpenClaw（旧Moltbot）の論理バグが招いた1-Click RCE

## 要約
depthfirstの調査で、OpenClaw（旧Moltbot）の設定読み込み〜接続処理の論理欠陥とWebSocketの起点検証漏れを組み合わせることで、悪意あるページ訪問だけで認証トークンが漏洩し、最終的にローカルで任意コード実行（RCE）に至るチェーンを作れることが明らかになり、開発側は修正を公開しました。

## この記事を読むべき理由
多くの開発者がAIエージェントに個人データやAPIキー、ローカル操作権限を預け始めており、日本でも同様の運用が増加中。ローカルで動く便利なツールが、ブラウザ経由の小さな論理ミスで致命的な踏み台になる事例は誰にでも関係します。

## 詳細解説
- 発見された論理欠陥の構図（要点）
  - 1) 設定受け取り：URLのquery（例 gatewayUrl）を検証せず保存する箇所がある。  
  - 2) 即時接続：設定適用直後にそのgatewayへ自動接続する処理が走る。  
  - 3) コネクト時の情報送信：接続ハンドシェイクにauthTokenを含めて送信する実装がある。  
  - これらが連動すると、クリックだけでトークンが外部に送られる危険なフローが成立する。

- ローカル実行環境への到達（Pivot）
  - 直接攻撃はインターネット公開インスタンスに限定されるが、WebSocketのOrigin検証漏れを突くと、ブラウザ経由でlocalhostのサーバへ接続させる「Cross‑Site WebSocket Hijacking」が可能となり、ローカルOpenClawへも到達できる。

- サンドボックス回避
  - 盗んだトークンに管理権限が含まれると、API経由で「ユーザー確認の無効化」や「ツールのホスト実行設定」などを変更でき、サンドボックスや承認プロンプトを無効化してホスト上で任意コマンド実行に至る。

- 対応状況
  - OpenClawチームは問題を修正（gateway URL確認モーダル追加等）。該当バージョン以前は脆弱。トークンの回転とアップデートが推奨される。

## 実践ポイント
- いますぐやること
  - OpenClaw/OpenClaw系を最新版に更新し、疑わしいトークンはローテーションする。  
- 開発者向けの対策
  - URLパラメータを鵜呑みにせず検証・確認ダイアログを必須化する。  
  - WebSocketサーバ側でOriginヘッダを厳格に検証する。  
  - 接続ハンドシェイクで認証情報を不用意に露出しない設計（最小権限のトークンを利用）。  
  - サンドボックス／実行ポリシーはAPI経由で容易に切り替えられないよう、実行ガードを実装する。  
  - ローカルで動くエージェントは最小権限で実行し、外部からのアクセス試行をログ・監視する。

短く言えば：「便利さ」と「自動化」は論理フローの検証ミスで致命傷になり得る。日本の開発現場でも設定の扱い・Origin検証・最小権限設計は今すぐ見直すべきポイントです。
