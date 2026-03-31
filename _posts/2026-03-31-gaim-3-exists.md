---
layout: post
title: "Gaim 3 Exists - Gaim 3 の登場"
date: 2026-03-31T23:37:46.198Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://gaim.imfreedom.org/"
source_title: "Gaim"
source_id: 904036503
excerpt: "往年のGaimがGTK4×libpurpleで再始動、軽快な1対1チャットを復活へ"
image: "https://gaim.imfreedom.org/org.imfreedom.Gaim3.webp"
---

# Gaim 3 Exists - Gaim 3 の登場
懐かしのGaimが帰ってきた—GTK4×libpurpleで再構築された“ダイレクトメッセージ”体験

## 要約
Gaim 3はlibpurple 3上に構築されたマルチプロトコルチャットクライアントの再始動プロジェクトで、GTK4を採用してLinux・macOS・Windowsで動作を目指しています。現状は開発初期でリリースは未公開です。

## この記事を読むべき理由
Pidgin系クライアントのUI変更で「1対1のやり取り」を好むユーザーが残された背景があり、日本でも複数チャットサービスを一元管理したい開発者・運用者や、古典的な軽量UIを好むユーザーにとって重要な動向です。

## 詳細解説
- 基盤技術: Gaim 3はlibpurple 3をコアに使うため、libpurpleが対応するIRC、XMPPなど複数のネットワークに接続可能（libpurpleの対応プロトコルに依存）。
- UI: 新しいプロジェクトながらGTK4で既存のGaim/Pidgin 2風の「ダイレクトメッセージ重視」UIを再現する方針。これはPidgin 3の「チャットルーム志向UI」との差別化を意図しています。
- クロスプラットフォーム: 公式はLinux・macOS・Windowsなどでの動作を想定。ただし現時点では開発初期のため正式リリースは無し。進捗やビルド情報はフォーラムで随時更新予定。
- ネーミング: 「Gaim」の名称は歴史的なオマージュで、以前の商標問題が解消されたため復活しています。

## 実践ポイント
- 継続的に追う: リリース前なのでフォーラムやリポジトリをウォッチして進捗を確認する。
- テスト参加: ソースからビルドして試せるスキルがあればフィードバックやIssue報告で貢献できる（GTK4とlibpurple 3の依存に注意）。
- 日本語対応・パッケージ支援: ローカライズ、Homebrew/Debian/Archパッケージ作成、テスト環境提供など日本側で貢献できる余地が大きい。
- 移行計画: 既存のPidgin/Purple設定を使う可能性があるため、チャット履歴やアカウント設定のバックアップを準備しておくと安心。

（参考）現状は開発初期・未リリース。興味があれば公式フォーラムで最新情報を追ってください。
