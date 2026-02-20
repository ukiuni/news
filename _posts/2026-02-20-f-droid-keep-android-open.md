---
layout: post
title: "F-Droid: \"Keep Android Open\" - F‑Droid：「Androidをオープンに保とう」"
date: 2026-02-20T18:22:35.103Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://f-droid.org/2026/02/20/twif.html"
source_title: "F-Droid: \"Keep Android Open\""
source_id: 47091419
excerpt: "Googleの配布変更でAndroidが閉鎖化の危機、F‑Droidの警告と対策を今すぐ確認"
image: "https://f-droid.org/assets/fdroid-logo_bfHl7nsLHOUQxzdU8-rGIhn4bAgl6z7k2mA3fWoCyT4=.png"
---

# F-Droid: "Keep Android Open" - F‑Droid：「Androidをオープンに保とう」
魅力的タイトル: Googleが“扉”を閉める前に知っておくべき、F‑Droidの緊急アラートと今すぐできる対策

## 要約
F‑DroidがGoogleのアプリ配布仕様変更による「Androidの閉鎖化」の危機を警告。時間が限られているとして、利用者への周知と行動を呼びかけています。

## この記事を読むべき理由
Googleの配布方針が変わると、サードパーティストアやサイドロードの自由度が下がり、日本の開発者・ユーザーの選択肢やプライバシーに直結します。今のうちに状況を把握し、対策を取る価値があります。

## 詳細解説
- 問題の本質：昨年8月に発表されたGoogleの変更は未だ予定通り進行中で、Google側のPRで「撤回・解決済み」と受け取られがちだが、実装（いわゆる“advanced flow”）は一般に見えていない。つまり「見かけ上の安心」に騙されるな、という警告。
- F‑Droidの対応：同プロジェクトはKeepAndroidOpenサイトやアプリ内バナーで利用者に現状を周知。IzzyOnDroidやObtainiumなど他の配布チャネルも警告を出し始めている。
- F‑Droid Basic（再設計中）：2.0‑alpha3の新機能群（翻訳更新、インストール履歴、インストール済みアプリのCSVエクスポート、ミラー選択、スクリーンショット防止、Material You対応など）を投入。現1.23系を使う場合はアプリ内で「Allow beta updates」を有効にしないと受け取れない点に注意。
- アプリやビルド周りの変化：多くのアプリが更新。Debianアップグレード対応や、Java 17から21への移行推奨などビルド面での対応が進行中。Play Store向け実装でGoogleライブラリを直接使わずIPC経由に切り替える取り組みが注目（F‑DroidとPlayで同一のFLOSS版を維持する可能性）。
- 目立つアップデート例：Dolphin Emulator大量のリリース、Image ToolboxにAI機能追加、Nextcloudのサーバー／クライアント更新群、ProtonVPNがOpenVPNを廃止してWireGuard/Stealthへ（アプリサイズ約40%減）。
- 削除・追加：数アプリがリポジトリから削除、NeoDB Youが新規追加。多数の小規模アプリも継続して更新。

## 実践ポイント
- まずF‑Droidを開き、表示される警告バナーを確認・拡散する。KeepAndroidOpenサイトもチェック。  
- F‑Droid Basicの新機能を試すなら、アプリ内の三点メニューで「Allow beta updates」をONにする。  
- 自分のインストール済みアプリをCSVでエクスポートしてバックアップ（2.0‑alpha3で可能）。  
- 開発者はビルド環境を確認し、Java 21対応やPlay向けの「Googleライブラリ依存削減」案を検討。  
- 日本の規制担当者やコミュニティに懸念を伝える：選択の自由や競争に関わる点を具体的に示すと効果的。  
- 代替ストア（IzzyOnDroid、Obtainiumなど）やミラーを把握しておき、万一の時に備える。

短くまとめると、Googleの仕様変更は「まだ完了していない」が時間は限られる。今のうちに情報収集・バックアップ・開発準備を進め、コミュニティと連携してAndroidを開かれたプラットフォームに保とう。
