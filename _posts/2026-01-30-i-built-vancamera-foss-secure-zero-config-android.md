---
layout: post
title: "I built VanCamera: FOSS, secure, zero-config Android webcam for Windows - VanCamera を作った：FOSS・安全・ゼロコンフィグで Android を Windows のウェブカメラに"
date: 2026-01-30T05:03:56.526Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/danielbolivar/vancamera"
source_title: "GitHub - danielbolivar/vancamera: Turn your Android into a webcam for Windows. Open source, secure, zero-config."
source_id: 46820631
excerpt: "VanCameraでスマホを安全かつ低遅延のWindows対応ウェブカメラに"
image: "https://opengraph.githubassets.com/17da328cc10901d8dd89fd8d1733892d67473009daaeec6da7bccbe834ab5283/danielbolivar/vancamera"
---

# I built VanCamera: FOSS, secure, zero-config Android webcam for Windows - VanCamera を作った：FOSS・安全・ゼロコンフィグで Android を Windows のウェブカメラに
魅力タイトル: スマホがそのまま高品質ウェブカメラに—VanCameraで低遅延＆安全なリモート会議を手に入れる

## 要約
VanCamera は Android を Windows の DirectShow 対応ウェブカメラに変えるオープンソースプロジェクト。TLS 1.3 とハードウェア H.264 を使い、低遅延で安全に動作する点が特徴。

## この記事を読むべき理由
日本でもリモート会議や配信が当たり前になり、高品質な外付けカメラ需要が高い。既存のスマホを活用してコストを抑えつつ、セキュアに運用できる実用的な選択肢だから。

## 詳細解説
- 主な特徴
  - 自動検出（USB と WiFi）でゼロコンフィグに近い接続体験
  - 低遅延：ハードウェア H.264 エンコードを活用してリアルタイム性を確保
  - セキュリティ：TLS 1.3 による暗号化で公衆ネットワークでも安全
  - ネイティブ互換：DirectShow 対応のため Discord、Zoom、Teams 等で「OBS-Camera」などを選ぶだけで利用可能
  - オープンソース（MIT ライセンス）でコード監査や改変が可能

- 動作要件（要点）
  - Android 7.0+（カメラ搭載）
  - Windows 10+
  - Python 3.8+
  - OBS-VirtualCam Legacy v2.0.5（Windows 側の仮想カメラ）
  - USB モードでは ADB 必須

- 接続モード
  - USB：最も低遅延で安定。USBデバッグを有効にして接続。
  - WiFi：配線不要で便利だが同一ネットワーク推奨。TLS により暗号化される。

- 開発・配布
  - GitHub リポジトリに Android（Kotlin）と Windows（Python）ソースあり。ビルド手順、プロトコル仕様、トラブルシューティングがドキュメント化されている。

## 実践ポイント
- まずは公式リリース（ビルド済 APK と Windows インストーラ）があればそちらを利用して試す。
- 低遅延を優先するなら USB 接続＋USB デバッグ有効にして使用する。
- Zoom/Teams 等では入力デバイスを「OBS-Camera」または VirtualCam に切り替える。
- 社内で使う場合は TLS による暗号化とオープンソースである点を説明して、セキュリティ承認を取りやすくする。
- 自分でビルドする場合は Python 要件、OBS-VirtualCam、ADB の準備を確認する。

VanCamera は「手元のスマホをすぐに安全なウェブカメラにしたい」人向けの実用的なオープンソースソリューション。まずは公式リポジトリでリリースとドキュメントをチェックして試してみてください。
