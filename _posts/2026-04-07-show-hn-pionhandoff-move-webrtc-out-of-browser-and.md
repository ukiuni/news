---
layout: post
title: "Show HN: Pion/handoff – Move WebRTC out of browser and into Go - ブラウザで始めるWebRTCをGoプロセスへ移行する"
date: 2026-04-07T13:21:16.227Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/pion/handoff"
source_title: "GitHub - pion/handoff: Start WebRTC in the browser—run it somewhere else · GitHub"
source_id: 47673880
excerpt: "ブラウザ発のWebRTC接続をGoへ移行し、サーバで録画・FFmpeg連携を容易にする手法"
image: "https://opengraph.githubassets.com/a5de111209c204af63b24f6bc6e91f030418bccbe5d251e6a7aa11bc9a27f8e6/pion/handoff"
---

# Show HN: Pion/handoff – Move WebRTC out of browser and into Go - ブラウザで始めるWebRTCをGoプロセスへ移行する

ブラウザで開始したWebRTCセッションをそのままサーバ側（Goプロセス）へ“引き継ぎ”し、録画・外部送出・解析などを簡単に実現するツール。

## 要約
Pion/handoffは、ブラウザ側でWebRTCのシグナリングを行いつつ、実際のピア接続をGo製のプロセスへ移して扱えるようにするOSS（GitHub: https://github.com/pion/handoff）。これによりサーバ側でメディアの録画やFFmpeg連携、RTP注入・解析が可能になる。

## この記事を読むべき理由
日本でもリモート会議、配信、通話録音、オンプレ運用の需要が高まっています。ブラウザ中心のWebRTCをサーバ側で安全かつ柔軟に扱えると、運用・品質管理・法令順守（録音保存等）がぐっと現実的になります。

## 詳細解説
- 基本アイデア：ブラウザにRTCPeerConnectionを「モック」させ、シグナリングだけ通常通り行わせる。シグナリングはhand offプロセスへ転送され、Go側で本物のWebRTC接続（Pion）を確立する。
- 技術要素：
  - シグナリング転送：既存のサイトとブラウザは通常通り認証・シグナリングを行うが、hand offがそのシグナリングを受け取り代行する。
  - Pion（Go）側：ICE候補処理、DTLSハンドシェイク、RTP/RTCP/SCTPの取り扱いを行い、メディアを保存したり外部に送信したりできる。
  - メディア操作例：バックエンドでVP8を保存、バックエンドからRTPで映像を注入、FFmpegと連携して任意の映像を差し替え。
  - デプロイ手法：ブラウザ用のuserscript（greasemonkey）で自動的にRTCPeerConnectionを差し替える方法や、examplesディレクトリのサンプルを使う。
- セキュリティ／注意点：ICE/DTLS情報やメディアをサーバで扱うため、鍵管理やアクセス制御を厳格にする必要あり。商用利用や機密データ取扱い時はオンプレ・専用ネットワークを検討。

## 実践ポイント
- すぐ試す手順（概略）
  1. リポジトリをクローン（https://github.com/pion/handoff）。
  2. Goでhand offプロセスを実行（examplesフォルダを参照）。
  3. greasemonkey/userscriptをブラウザに入れてRTCPeerConnectionをモック。
  4. examples/media-saveやmedia-sendで録画・注入を確認。FFmpegで動画ソースを差し替え可能。
- 活用シーン
  - 会議サービスのサーバ録画・トランスコーディング
  - サーバ側でのメディア品質監視／解析
  - オンプレ環境での法令準拠（録音保存要件）対応
- 注意：プロダクション導入時はDTLSキー管理・プライバシー規約・帯域設計を必ず検討すること。

リポジトリ： https://github.com/pion/handoff
