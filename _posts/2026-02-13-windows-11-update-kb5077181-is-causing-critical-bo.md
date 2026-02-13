---
layout: post
title: "Windows 11 update KB5077181 is causing critical boot loops for some users - Windows 11更新 KB5077181が一部ユーザーで致命的な起動ループを引き起こす"
date: 2026-02-13T19:08:39.015Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.neowin.net/news/windows-11-update-kb5077181-is-causing-critical-boot-loops-for-some-users/"
source_title: "Windows 11 update KB5077181 is causing critical boot loops for some users - Neowin"
source_id: 442606955
excerpt: "KB5077181適用で無限再起動やログイン不能が多発、即時アンインストールと対策手順を確認せよ"
---

# Windows 11 update KB5077181 is causing critical boot loops for some users - Windows 11更新 KB5077181が一部ユーザーで致命的な起動ループを引き起こす
Windows 11更新でPCが再起動地獄に—KB5077181の実情と即効対策

## 要約
KB5077181（Build 26200.7840）適用後、15回以上の無限再起動やログイン不能（SENSエラー）、DHCPによるネット切断、エラーコード0x800f0983／0x800f0991が多数報告されています。暫定対処は更新のアンインストールと一時停止です。

## この記事を読むべき理由
日本でもWindows 11は企業・個人とも広く使われており、パッチ適用で業務停止やリモートワーク断絶が起きる可能性があります。早めに影響確認と対処手順を知っておくことで被害を最小化できます。

## 詳細解説
- 問題の症状：インストール後に「無限起動（15回以上の再起動）→壊れたログイン画面」に陥る報告があり、System Event Notification Service（SENS）に「指定されたプロシージャが見つかりません」等のエラーが出るためログイン不可になります。  
- ネットワーク問題：DHCP関連の不具合でSSIDには接続するがインターネットに繋がらないケースがあると報告されています。  
- インストール失敗：0x800f0983／0x800f0991等のエラーが出る事例。SFC（System File Checker）で回復した例もあるため、ファイル破損が絡む可能性があります。  
- Microsoftの対応：一時的な案として「該当更新のアンインストール」や「更新の一時停止」が案内されていますが、恒久対策はMicrosoftの追加パッチ（out-of-band含む）待ち。Windows Release Healthダッシュボードで公式情報の確認を推奨。

## 実践ポイント
- まず被害確認：複数台に展開している環境は即座に展開を停止・保留。個人は再起動・ログイン状況を確認する。  
- アンインストール（回復モードやControl Panel経由）例：
```powershell
wusa /uninstall /kb:5077181 /quiet /norestart
```
- SFCでの修復試行：
```powershell
sfc /scannow
```
- 一時回避：Windows Updateを一時停止、メータ接続設定を使って自動再インストールを防ぐ。企業はWSUS/Intuneで配布をロールバック。  
- 事前対策：重要データのバックアップ、システムイメージ作成、復旧用USBの準備。  
- 情報収集：Windows Release Healthダッシュボードとメーカー（OEM）および社内ITのアナウンスを注意深く確認する。

影響を受けたらまず落ち着いてネットで同症状の報告を確認し、アンインストール→SFC→必要ならリカバリの順で対応してください。
