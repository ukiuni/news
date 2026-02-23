---
layout: post
title: "FreeBSD doesn't have Wi-Fi driver for my old MacBook. AI build one for me - FreeBSDに古いMacBook用のWi‑Fiドライバがないので、AIに作らせてみた"
date: 2026-02-23T22:51:10.754Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://vladimir.varank.in/notes/2026/02/freebsd-brcmfmac/"
source_title: "FreeBSD doesn't have Wi-Fi driver for my old MacBook. AI build one for me - Vladimir Varankin"
source_id: 47129361
excerpt: "AIが2016年MacBook用Broadcom Wi‑FiドライバをFreeBSDで動かした実験記録"
---

# FreeBSD doesn't have Wi-Fi driver for my old MacBook. AI build one for me - FreeBSDに古いMacBook用のWi‑Fiドライバがないので、AIに作らせてみた
魅力的なタイトル: AIが“ゴミ箱行き”の2016年MacBookを救った話 — FreeBSD用Broadcomドライバを自動生成して動かしたプロジェクト

## 要約
著者は2016年MacBook ProのBroadcom BCM4350 Wi‑FiをFreeBSDで動かすため、AIエージェント群に設計→実装→テストを繰り返させ、動作するFreeBSDカーネルモジュール（学習用）を作らせた。

## この記事を読むべき理由
古いノートPCや組込機を再利用したい日本の開発者・趣味エンジニアにとって、ドライバ未対応ハードの扱い方、AIを設計と反復実装に活かす具体的ワークフローが参考になるため。

## 詳細解説
- 背景：2016年MacBook ProはBroadcom BCM4350（FullMAC）を搭載。FreeBSDにネイティブ対応がないため、従来はLinux VMへPCIパススルーしてLinuxのbrcmfmacドライバで扱う（wifiboxのような回避策）。
- FullMACの性質：802.11フレーム処理やWPA暗号などはチップ内ファームウェアが担当。OS側ドライバは管理・制御（設定、スキャン、接続管理）を行うため、理屈上は「Linux向けの管理コードをFreeBSD向けに“つなぎ直す”」ことで移植できる。
- 著者の手順：
  1. まずClaude（コード向けAI）でLinux brcmfmacをFreeBSD向けに変換させたが、ハード無しのVMでビルド→実機接続でカーネルパニックや動作不良に遭遇。
  2. 方針転換し、Pi系エージェントに「BCM4350に特化した詳細仕様書」を生成させ、複数エージェントでクロスチェック（clean-roomで仕様作成→別のAIで仕様とソースの整合性検証）。
  3. 仕様に従い新規プロジェクトを立ち上げ、エージェントに逐次実装・ビルド・テスト（VMにPCIパススルー）を任せる。途中でLinuxKPI依存をやめてネイティブ実装にリファクタ。
  4. 最終的にスキャン、2.4/5GHz接続、WPA/WPA2をサポートするFreeBSDカーネルモジュールを得たが、学習目的向けで既知の問題あり。ソースは公開（学習用）。
- 技術的ポイント：
  - 移植の肝は「管理層のGlueコード」とプラットフォーム固有インターフェース（PCI、OSの無線スタック連携）。
  - LinuxKPIは便利だが複雑な依存や不足で手戻りが起きることがある。最小機能に絞ってネイティブ実装する判断が有効。
  - テスト環境はVM＋PCIパススルー。頻繁にクラッシュするためスナップショット運用や問題記録が必須。
  - AIは「仕様作り」「繰り返しのコード生成・テスト」に強いが、必ず人的検証（ソースが最終的なground truth）を行う必要がある。

## 実践ポイント
- まずは回避策を検討：すぐ使いたければwifiboxのようなLinux VM経由が現実的。
- 自前でドライバを作る場合の最短戦略：
  1. チップIDを確認（lspci等）し、対応するLinuxドライバ（brcmfmac）のどの部分が必要か切り分ける。
  2. 最小要件（PCIのみ、クライアント動作、WPA対応）に絞った仕様書を作成する。
  3. VMでPCIパススルー環境を用意し、スナップショット運用で安全にテストする。
  4. AIは「仕様生成」「差分リファクタ」「テストケース作成」に活用し、人間が都度ソースとログを検証する。
  5. production用途では使わない（学習・実験用途に留める）。公開コードは既知の問題があるため注意。

参考：著者は最終的にGitHubで実験的ドライバを公開している（学習用）。本稿は手順と考え方を紹介するもので、実運用の保証はありません。
