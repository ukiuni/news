---
layout: post
title: "Second Win11 emergency out of band update to address disastrous Patch Tuesday - Windows 11：Patch Tuesday地獄を受けた緊急修正の第2弾リリース"
date: 2026-01-25T04:10:29.432Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.windowscentral.com/microsoft/windows-11/windows-11-second-emergency-out-of-band-update-kb5078127-released-address-outlook-bugs"
source_title: "Microsoft issues SECOND emergency out of band update for Windows 11 to address disastrous Patch Tuesday bugs &mdash; KB5078127 released globally | Windows Central"
source_id: 46750358
excerpt: "KB5078127でOutlookやOneDriveの業務停止リスクを即修正、今すぐ更新を確認"
image: "https://cdn.mos.cms.futurecdn.net/vV9qZsEjjQzM3p2vDiyXUQ-2560-80.jpg"
---

# Second Win11 emergency out of band update to address disastrous Patch Tuesday - Windows 11：Patch Tuesday地獄を受けた緊急修正の第2弾リリース
Windows 11で発生したPatch Tuesday以降の致命的な不具合を修正する緊急配布更新（KB5078127）が配信開始

## 要約
1月13日のPatch Tuesdayで発生した不具合でOutlookやOneDrive/Dropboxなどクラウド連携アプリが動作不能になる問題を受け、Microsoftが1月24日に2度目の「out‑of‑band」累積更新KB5078127を公開しました。以前の緊急パッチ（1月17日）での修正も取り込み済みです。

## この記事を読むべき理由
企業のメール・ファイル同期が止まると業務停止に直結します。日本でもOneDriveやDropboxを業務で使う組織は多く、影響範囲が大きいため、早急に状況把握と対策が必要です。

## 詳細解説
- 問題の経緯：1月13日の定例セキュリティ更新で複数の不具合が発生。1月17日に最初の緊急OOB更新でリモートデスクトップ接続やスリープ/休止問題を修正したものの、その修正が原因でOutlookやクラウドストレージ連携が不安定に。
- 今回の修正（KB5078127、1月24日配信）：クラウドベースのストレージ（OneDrive/Dropbox等）からファイルを開閉する際にアプリが応答しなくなる問題を修正。PSTをOneDrive上に置く一部のOutlook構成でハングし再起動が必要になる（送信済みアイテムが消える、既存メールが再ダウンロードされる等）症状も解消されます。
- 対象：Windows 11 24H2/25H2を中心に、23H2やWindows Server系も同様の修正が展開されています。更新は累積で、1月13日・1月17日の修正内容を含みます。
- 補足：暫定対処として「最新のセキュリティ更新をアンインストールする」との運用が取られていましたが、今回のKBでその必要は原則解消されます。最新の影響情報はWindows release health dashboardで確認してください。

## 実践ポイント
- 個人/管理者はまずWindows UpdateでKB5078127を確認して適用する（設定 → 更新とセキュリティ → Windows Update）。
- 既に1月の更新をアンインストールしていた環境は、KB5078127適用で復旧する可能性が高いので再適用を検討。
- 企業管理者はまず非本番環境で適用テストを行い、業務システム（OutlookのPST配置、OneDrive同期、RDP環境）を重点確認する。
- 詳細な影響や緊急情報はWindows release health dashboardを定期チェック。問題が続く場合はイベントログやOfficeの診断ログを取得してサポートへ問い合わせを。
