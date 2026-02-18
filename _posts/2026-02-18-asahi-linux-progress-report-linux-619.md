---
layout: post
title: "Asahi Linux Progress Report: Linux 6.19 - Asahi Linux：Linux 6.19 進捗報告"
date: 2026-02-18T11:09:19.747Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://asahilinux.org/2026/02/progress-report-6-19/"
source_title: "Progress Report: Linux 6.19 - Asahi Linux"
source_id: 47059275
excerpt: "Asahi LinuxがM3・USB-C外部出力と120Hz対応を前進させた最新進捗"
image: "https://asahilinux.org/img/AsahiLinux_logomark_256px.png"
---

# Asahi Linux Progress Report: Linux 6.19 - Asahi Linux：Linux 6.19 進捗報告
Macで本気のLinuxを使いたくなる――Apple Siliconの外部ディスプレイやM3対応が一歩前進した最新事情

## 要約
Asahi Linuxが5周年を迎え、Linux 6.19周辺でUSB-C経由のDisplayPort出力（DP Alt Mode）やM3機種の初期サポート、120Hz動作など重要な前進を報告しています。ただし現状は開発者向けブランチ中心で、まだ安定版リリース前の段階です。

## この記事を読むべき理由
日本でもMシリーズMacの利用が急増する中、「LinuxをMacで快適に動かしたい」ニーズが高まっています。本記事は外部ディスプレイ接続やM3対応、120Hz表示といった実用上の大問題がどう解決されつつあるかを分かりやすく伝えます。

## 詳細解説
- DP Alt Mode（USB-C→ディスプレイ出力）
  - fairydustという下流ブランチで、USB-C経由の表示が実現されつつあります。これはDCP・DPXBAR・ATCPHY・ACEという4つのハードウェアブロックを逆解析・ドライバ化して統合した成果です。
  - 現状の制約：特定のUSB-Cポートのみ「有効化」される、マルチUSB-Cディスプレイ非対応、冷／熱挿し時の動作不安定、一部機種で色味やタイミングが乱れる報告あり。開発者向けの実験的提供のため、一般向けサポートは未提供。

- M3サポートの進捗
  - m1n1やDevicetreeの追加、NVMeや割込みまわりの小修正でM3機種がPlasmaまで起動した報告あり。キーボード、タッチパッド、Wi‑Fi、NVMe、USB3は動作するケースが多いものの、GPU周りやDCP初期化など未解決点が残ります。
  - M3 GPUはM1/M2とISAが大きく変わり（ハードウェアレイトレーシング、メッシュシェーダ、Dynamic Caching等）、逆解析が必要。現状はiBootに頼ってフレームバッファを割り当ててもらっているため効率・表示機能に制限あり。

- 120Hz（ProMotion）問題
  - 14"/16" MacBook Proの120Hz表示は、DCPが要求する「プレゼンテーション用タイムスタンプ」3フィールドを満たす必要があることが判明。現状のワークアラウンドとして静的タイムスタンプを埋める手法で120Hzが動作（Linux 6.18.4以降で利用例）していますが、これは暫定的でVRR（可変リフレッシュ）をサポートしない「ややジャンク」な実装です。

- DCPドライバの再設計と機能拡張
  - 現行ドライバは断片的に積み上げられてきたため、HDR、VRR、異なるフレームバッファ形式、外部ディスプレイ輝度制御、直接スキャンアウト等に対応するには設計改善が必要。Rustによる書き直し構想もある一方、当面は既存ドライバの平面（plane）処理リファクタでY'CbCr、HDR、圧縮フレームバッファのサポート拡張を進めています。

## 実践ポイント
- あなたが開発者・実験好きなら
  - fairydustブランチを試し、特定ポートや外部アダプタの挙動を報告・パッチ提供して貢献すると効果が大きいです（自己責任でカーネルビルドが必要）。
  - M3機での検証やm1n1/devicetree整備、GPU逆解析の手伝いは歓迎されています。AsahiのGitHubやMatrix/IRCで参加を検討してください。
- ユーザー向けの現実的な期待値
  - 日常的に安定して外部ディスプレイや高性能GPUを期待するなら、現時点では「一部機能は実験的」であることを理解しておきましょう。120Hzはカーネルパッチ次第で動きますがVRR対応は未解決です。
- 情報追跡
  - Asahi Linuxの公式ブログとGitHubをウォッチし、fairydustやm3関連のコミット／リリースノートを注視すると最新の対応可否が分かります。

（短く言えば：Apple Siliconでの本格的なLinux体験は確実に前進中。だがまだ“完璧”ではなく、試すなら開発寄りの覚悟を。）
