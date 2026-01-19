---
layout: post
title: "Microsoft issues emergency fix after a security update left some Windows 11 devices unable to shut down - セキュリティ更新により一部の Windows 11 がシャットダウンできなくなった問題、Microsoft が緊急修正を配布"
date: 2026-01-19T00:38:46.916Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.engadget.com/computing/microsoft-issues-emergency-fix-afer-a-security-update-left-some-windows-11-devices-unable-to-shut-down-192216734.html"
source_title: "Microsoft issues emergency fix after a security update left some Windows 11 devices unable to shut down"
source_id: 423368472
excerpt: "一部Windows11でシャットダウン不能の不具合、Microsoftが緊急パッチ配布—今すぐ確認を"
image: "https://s.yimg.com/ny/api/res/1.2/aHP7qmdVByu86SEaHGGrnA--/YXBwaWQ9aGlnaGxhbmRlcjt3PTEyMDA7aD02NzU-/https://s.yimg.com/os/creatr-uploaded-images/2026-01/16bf1630-f49d-11f0-8b2f-05edc4e91cab"
---

# Microsoft issues emergency fix after a security update left some Windows 11 devices unable to shut down - セキュリティ更新により一部の Windows 11 がシャットダウンできなくなった問題、Microsoft が緊急修正を配布
Windows 11が「電源オフできない」不具合、Microsoftが即時パッチで対応 — あなたのPCは大丈夫？

## 要約
1月のセキュリティ更新で、一部の Windows 11 がシャットダウンや休止（ハイバネート）しようとすると再起動してしまう問題と、Windows 10/11 のリモートログインで資格情報のプロンプトが失敗する問題が発生。Microsoftは「out-of-band（緊急）」アップデートで修正を配布した。

## この記事を読むべき理由
日本でもリモートワークや厳格なセキュリティ設定を採用する企業が多く、シャットダウン不能やリモート接続障害は業務に直結します。個人ユーザーも含め、今すぐ自分の環境が影響を受けていないか確認する必要があります。

## 詳細解説
- 問題の内容  
  - シャットダウン/休止が「再起動」になる不具合：対象は Secure Launch を有効にしている一部の Windows 11 デバイス。Secure Launch は起動時にファームウェアレベルの攻撃から守るためのセキュリティ機構で、今回の更新で不整合が生じたと見られます。  
  - リモートログインの資格情報プロンプト失敗：Windows 10/11 でリモート接続アプリ（RDP 等）を使う際に認証プロンプトが正しく動作せずログインできないケースが報告されました。
- 対応：Microsoft は通常の月例更新とは別に「out-of-band」アップデートを公開し、上記不具合を修正しました。既往の事例としては、以前にも Windows Recovery Environment に関する緊急修正が配布されたことがあります。
- 残る報告：一部では更新後に画面が真っ白になる、Outlook Classic が落ちる等の不具合も報告されています。完全な安定化には追加の修正が必要な場合があります。

## 実践ポイント
- 個人ユーザー向け
  - Windows Update を開き、更新を確認して「緊急」パッチを適用する。自動更新設定なら既に配布済みの可能性が高い。  
  - シャットダウンやリモート接続を一度テストして異常がないか確認。問題がある場合は、電源長押しで強制停止→再起動後に更新を適用して再確認。  
  - 不安があるなら、すぐに重要作業の前にアップデートを当てるか、逆にアップデート直後で不具合が出ている報告がある場合は適用を一時保留して公式の追加情報を待つ（ただしリスクを理解した上で判断）。

- IT管理者/企業向け
  - まずは Microsoft's Known Issues ページと配布された KB（パッチ番号）を確認し、修正の適用状況と既知の副作用を把握する。  
  - WSUS/Intune 等で段階的ロールアウト（まずはパイロットグループ）を実施し、Secure Launch を利用する端末やリモートワーク環境で入念にテストする。  
  - Windows 10 を使い続ける必要がある場合は、Extended Security Updates（ESU）オプションの利用を検討して、サポート継続を確保する。  
  - エンドユーザーへは「シャットダウンできない」「リモート接続できない」といった現象が出た場合の対処手順（更新の確認、強制シャットダウン後の更新適用、IT窓口への報告）を周知する。

短く言えば：まずは公式パッチを当てて、重要な環境では段階的な配布とテストを。セキュリティ機能（Secure Launch）を有効にしている場合は特に注意を。
