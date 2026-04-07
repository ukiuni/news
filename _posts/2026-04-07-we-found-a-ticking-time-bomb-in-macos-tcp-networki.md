---
layout: post
title: "We Found a Ticking Time Bomb in macOS TCP Networking — It Detonates After Exactly 49 Days - macOSのTCPに潜む“タイムボム” — ちょうど49日で爆発する"
date: 2026-04-07T01:25:58.902Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://photon.codes/blog/we-found-a-ticking-time-bomb-in-macos-tcp-networking"
source_title: "We Found a Ticking Time Bomb in macOS TCP Networking — It Detonates After Exactly 49 Days - Photon Blog"
source_id: 1216530994
excerpt: "macOSのTCPが49日で死ぬ？常時接続が突然止まる原因と今すぐの対策"
image: "https://framerusercontent.com/images/YXr1OxGxAmSLi60593nzjskSwM.png?width=2400&amp;height=1260"
---

# We Found a Ticking Time Bomb in macOS TCP Networking — It Detonates After Exactly 49 Days - macOSのTCPに潜む“タイムボム” — ちょうど49日で爆発する

魅力的な見出し: 49日で死ぬTCP接続？macOSの「長時間接続崩壊」の正体と今すぐできる対策

## 要約
macOSのTCPスタックに、システム稼働約49日で長期TCP接続が機能不全に陥る致命的な不具合が見つかりました。原因は時間を扱う内部カウンタのオーバーフローで、切断されていないのに通信が止まる事象が再現されます。

## この記事を読むべき理由
企業や開発現場で「常時稼働するMac」や長時間維持するSSH/VPN/HTTP2/gRPC接続を使っているなら、気づかないうちにサービスや開発ワークフローが止まるリスクがあります。日本のオフィスやクラウド開発環境、リモートワーク環境でも無関係ではありません。

## 詳細解説
- 発生条件：システム稼働時間（あるいは内部ミリ秒カウンタ）が約49.7日（≈2^32ミリ秒）に達すると発生。カウンタの桁あふれ（wrap）でTCPのタイマ計算が狂うため、再送やタイムアウトの判定が誤動作します。
- 症状：ソケットはESTABLISHEDのまま見えるがデータが通らない、再送無限ループや応答停止、アプリ側で切断検知されない等。現象は決まった周期で再現可能で「時間」の要因が鍵。
- 影響範囲：macOSのTCPスタックを使うすべてのアプリ。特に長時間アイドルのコネクション（VPN常時接続、長寿命のWebソケット、ストリーミング、SSHトンネル、CIエージェント等）が影響を受けやすい。
- 対応状況：原則はOS側の修正が必要。暫定的な緩和策はアプリ側・運用側で実施可能。

## 実践ポイント
- OSアップデートを適用：Appleの修正パッチが出ていれば最優先で当てる。
- 長期接続を避ける／定期再接続：可能なら数日単位で再ネゴシエート（自動再接続）する設計にする。
- アプリ層のハートビートを導入：TCPの状態に依存せず、アプリ層で定期的に生存確認を行い、応答がない場合はソケットを再生成する。
- TCPキープアライブ／短めの間隔を設定：SO_KEEPALIVEやアプリ独自のping間隔を用いてアイドル検出を早める（OSデフォルトのまま放置しない）。
- 監視と運用ルール：長時間稼働するMacは再起動やネットワークスタック再初期化をスケジュールに組み込む（例：7〜14日ごと）。接続のスループット監視やnetstatでの状態チェックを自動化する。
- テストを作る：長時間接続の健全性を検証する簡易スクリプトを用意し、運用機で定期検査を行う。

以上を踏まえ、まずは環境の稼働時間と「常時接続」の運用を見直し、OSアップデートとアプリ側の再接続・監視対策を優先してください。
