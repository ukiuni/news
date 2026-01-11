---
layout: post
title: "iCloud Photos Downloader - iCloud写真ダウンローダー"
date: 2026-01-11T20:41:23.125Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/icloud-photos-downloader/icloud_photos_downloader"
source_title: "GitHub - icloud-photos-downloader/icloud_photos_downloader: A command-line tool to download photos from iCloud"
source_id: 46578921
excerpt: "iCloud写真を自動でローカル/NASに同期・一括取得する実践的CLIツール"
image: "https://opengraph.githubassets.com/662431df4b4bbbe07bd7b32c81c92f3deaa0b8a57fc305bfaab14c48b29246fb/icloud-photos-downloader/icloud_photos_downloader"
---

# iCloud Photos Downloader - iCloud写真ダウンローダー
iCloudの写真をローカルやNASに自動で同期・一括取得するCLIツール。手元で写真管理したい人に刺さる実用ツール紹介

## 要約
iCloud Photos Downloader（icloudpd）は、iCloud上の写真・Live Photo・RAWをコマンドラインでダウンロード・同期・移動できるクロスプラットフォームなオープンソースツールです。Linux・Windows・macOSやNASで使え、Docker/PyPI/AUR/npm/実行ファイルで配布されています。

## この記事を読むべき理由
- iCloudの写真をクラウドだけでなくローカル保存やNASで運用したい日本の個人・小規模ビジネス向けに即効性のある実践手順が得られるため。  
- Appleの2段階認証やAdvanced Data Protectionなど日本ユーザー特有の設定課題に対処する要点が分かるため。

## 詳細解説
- 目的：iCloudのフォトライブラリをローカルに取り込み、自動同期や一括移行を行う。開発はボランティア主体、頻繁にアップデートされる（週次目標）。
- 対応環境：Linux、Windows、macOS、NAS（Dockerやビルド済みバイナリで動作）。配布は公式リリース実行ファイル、Dockerイメージ、PyPI、AUR、npmなど。
- 事前条件（重要）：
  - iPhone/iPadの「Access iCloud Data on the Web（Web上のiCloudデータへのアクセス）」を有効化。
  - 「Advanced Data Protection（高度データ保護）」を無効化（有効だとACCESS_DENIEDになる）。
  - Apple IDの2FA/2SAに対応した認証フローが必要（初回はブラウザ承認やワンタイムコード）。
- 主な動作モード：
  - copy（デフォルト）：iCloudの新しい写真をローカルにコピーする。
  - sync（--auto-delete）：iCloud側で削除されたファイルをローカルからも削除して同期状態にする。
  - move（--keep-icloud-recent-days 等）：ダウンロード後iCloudから削除する（移行用）。
- 特長：
  - Live Photo（画像＋動画）やRAW（RAW+JPEG）に対応。
  - ファイル名重複の自動除去、EXIF更新（--set-exif-datetime）などメタデータ処理。
  - 監視モード（--watch-with-interval）で定期的に差分取得、増分最適化オプション（--until-found、--recent）。
  - 実験モードで新機能を試験運用可能。
- 運用上の注意：大量データ転送・ストレージ容量・ネットワーク負荷、Apple側のレート制限、認証の有効期限管理に注意が必要。

例（よく使うコマンド）：
```bash
# 定期監視して/dataに同期（1時間ごと）
icloudpd --directory /data --username you@example.com --watch-with-interval 3600

# 認証だけ行って2FA/2SAを完了させる
icloudpd --username you@example.com --password your_password --auth-only
```

## 実践ポイント
1. 事前設定を確認：iPhoneの「Access iCloud Data on the Web」を有効、Advanced Data Protectionを無効化してから始める。  
2. インストール方法を選ぶ：手軽さ重視は公式実行ファイル、NASやコンテナ運用はDocker、Python環境で拡張したければPyPI。  
3. 初回は --auth-only で認証フローを完了し、2FAコードやブラウザ承認を事前確認する。  
4. 運用例：systemdやcronで定期実行、容量監視と組み合わせて古いファイルをアーカイブする。  
5. メタデータ保持：写真の撮影日時をEXIFで固定したい場合は --set-exif-datetime を利用。  
6. Live Photo/RAW対応を確認：RAWや動画を別ファイルで扱うので保存先のフォルダ設計を検討する。  
7. 法令・プライバシー：社用アカウントや他者データを扱う場合は社内ポリシーと法令に従う。  
8. コントリビュート歓迎：ボランティア開発で更新が早い反面、メンテナンス状態やIssueを確認してから本番運用する。

短時間でiCloudの写真を手元に取り込みたい／NASで長期保存したい日本のユーザーにとって、実用性が高くすぐに試せるツールです。興味があればインストール方法やsystemdでの自動化手順を個別に案内します。
