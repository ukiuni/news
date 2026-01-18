---
layout: post
title: "Microsoft forced to issue emergency out of band updates for Windows 11 after latest security patches broke PC shutdowns and sign-ins - 最新のセキュリティ更新でPCのシャットダウンやサインインができなくなり、Microsoftが緊急の「帯外」パッチを公開"
date: 2026-01-18T14:51:10.718Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.windowscentral.com/microsoft/windows-11/microsoft-issues-emergency-out-of-band-update-for-windows-11-to-address-major-bugs-that-broke-pc-shutdowns-and-sign-ins"
source_title: "Microsoft forced to issue emergency out of band updates for Windows 11 after latest security patches broke PC shutdowns and sign-ins | Windows Central"
source_id: 424970851
excerpt: "Windows11更新でシャットダウン不能・RDP障害、緊急パッチ公開"
image: "https://cdn.mos.cms.futurecdn.net/iSfZLRtdr9rYXFF8StFJcN-2560-80.jpg"
---

# Microsoft forced to issue emergency out of band updates for Windows 11 after latest security patches broke PC shutdowns and sign-ins - 最新のセキュリティ更新でPCのシャットダウンやサインインができなくなり、Microsoftが緊急の「帯外」パッチを公開
魅せるタイトル: Windows Updateがまたトラブル──シャットダウン不能とリモートサインイン障害を即修正した緊急パッチの中身と対処法

## 要約
2026年1月に配信されたWindowsの通常セキュリティ更新で、PCが正常にシャットダウンできなくなる問題や、リモートデスクトップ（RDP）によるサインイン障害が発生。Microsoftは緊急の帯外アップデート（KB5077744 / KB5077797）を配布して修正を行った。

## この記事を読むべき理由
多くの日本企業や個人がリモートデスクトップや最新のセキュリティ機能（Secure Launch／セキュアブート系）を使っており、今回の不具合は業務に直結する可能性があります。アップデート運用やトラブル対応の実務的ヒントを知っておくと被害を最小化できます。

## 詳細解説
- 問題の内容
  - 主要な2つの不具合が報告されました：1) Secure Launchを有効にしているWindows 11（23H2）でシャットダウンや休止（hibernate）が失敗する、2) リモート接続アプリケーション（RDPなど）で接続・認証に失敗する事象（影響範囲はWindows 11 25H2、Windows 10 22H2 ESU、Windows Server 2025などを含む）。
- Microsoftの対応
  - 緊急の帯外パッチKB5077744とKB5077797がWindows Update経由で公開され、順次ロールアウト中。適用後はシャットダウンとリモートサインインが回復することが報告されています。
- 背景と問題の根深さ
  - 最近のアップデートでTask Managerが閉じられなくなる、ダークモードでFile Explorerが白画面になる、WinRE（回復環境）が壊れる等、重大バグが連続。Insiderテストを経ても重大な不具合が本番に混入しており、品質管理の懸念が強まっています。

## 実践ポイント
- すぐやること（個人/小規模環境）
  - Windows UpdateでKB5077744 / KB5077797の適用有無を確認し、適用されていなければインストールして再起動する。
  - リモート接続を多用する場合は、パッチ適用後に接続テストを行う。
- すぐやること（企業/管理者向け）
  - WSUS / Intuneなどで緊急パッチの展開を優先。まずはパイロットグループで検証後、全社展開する。
  - 更新前にイメージバックアップや復旧手順（アンインストールや回復環境の使い方）を確認しておく。
  - Secure Launchや最新セキュリティ機能を段階的に有効化している環境は、影響を受けやすいので特に注意。
- 長期的な対策
  - アップデートの自動適用ルールを見直し（業務影響を最小化するためのスケジュール管理）、テスト環境での事前検証を運用に組み込む。
  - Microsoftの「Known issues」ページやセキュリティアナウンスを購読し、異常が出たら即座に情報収集できる体制を整える。
- トラブル時の一時対処（状況に応じて）
  - シャットダウンが効かない場合、管理者はコマンドプロンプトでのシャットダウン命令（例: shutdown /s /t 0）や、必要に応じて電源長押しでの停止などを検討。ただし強制電源断はデータ損失リスクがあるため最終手段とする。

今回の件は、アップデート運用の「慎重さ」と「即時対応」の両方が求められる良いリマインダーです。まずは自分のPCや社内の重要マシンにパッチが適用されているかを確認してください。
