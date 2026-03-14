---
layout: post
title: "Microsoft: Windows 11 users can't access C: drive on some Samsung PCs - Microsoft: 一部Samsung製PCでWindows 11のC:ドライブにアクセスできない問題"
date: 2026-03-14T22:11:04.452Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.bleepingcomputer.com/news/microsoft/microsoft-windows-11-users-cant-access-c-drive-on-some-samsung-pcs/"
source_title: "Microsoft: Windows 11 users can't access C: drive on some Samsung PCs"
source_id: 382959493
excerpt: "Windows 11更新で一部Galaxy BookがC:ドライブにアクセス拒否、MicrosoftとSamsungが原因調査中で公式対処法を要確認"
image: "https://www.bleepstatic.com/content/hl-images/2025/03/26/Windows_11.jpg"
---

# Microsoft: Windows 11 users can't access C: drive on some Samsung PCs - Microsoft: 一部Samsung製PCでWindows 11のC:ドライブにアクセスできない問題

魅力的なタイトル: 「突然C:ドライブが“アクセス拒否”に——Samsungノートで発生中の致命的アップデート問題、今すぐ確認すべき対処法」

## 要約
2月のWindows 11セキュリティ更新後、一部Samsung製PC（主にGalaxy Book 4など）で「C:\ is not accessible – Access denied」が出てCドライブや主要アプリにアクセスできなくなる問題が報告されており、MicrosoftはSamsungと協力して原因を調査中です。

## この記事を読むべき理由
日本でもGalaxy BookシリーズなどSamsung製ノートを使う個人・法人ユーザーやIT管理者が被害に遭う可能性があるため、状況把握と安全な対処の方針を知っておく必要があります。

## 詳細解説
- 影響範囲: Windows 11 24H2／25H2を搭載した一部Samsung消費者向け機種（報告は主にブラジル、ポルトガル、韓国、インド）で発生。  
- 症状: ファイルアクセス時やアプリ起動（Outlook、Office、ブラウザ、システムユーティリティ等）がブロックされ、管理者権限昇格や更新のアンインストール、ログ参照ができなくなるケースあり。  
- 疑いのある原因: Microsoftの調査はSamsung Shareアプリが関係している可能性を示唆しているが、確定していない。MicrosoftはSamsungと連携して解析中。  
- 危険な「対応例」: Reddit等で紹介された「C: 以下すべての所有権をEveryoneに変更する」回避策は一時的にアクセスを戻す報告もあるが、TrustedInstaller/SYSTEMが持つ本来の保護を破壊するため重大なセキュリティリスク（マルウェアに対する脆弱化）を招きます。

## 実践ポイント
- 即時対応: 不具合が出ていない端末は、Windows Updateの一時停止/配信遅延を検討（個人は「更新の一時停止」、企業はWSUS/MDMで配信を保留）。  
- 被害を受けた場合: 危険な所有権変更は避け、まずはセーフモード起動で更新のアンインストールやシステム復元を試みる。復旧不能ならWindows回復環境からの復元や、バックアップからのリストアを優先。  
- 管理者向け: 全社展開前に該当セキュリティ更新の影響確認を行い、Samsung製端末を優先的に検証。インベントリにGalaxy Book等があればリスクを共有すること。  
- 情報収集: MicrosoftおよびSamsungの公式サポート情報／アップデート案内を定期的に確認し、公式修正パッチの配布を待つ。

必要なら、被害端末の具体的なログ取りや復旧手順（安全な順序）を案内します。どの環境でお困りですか？
