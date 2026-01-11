---
layout: post
title: "Admins finally get the power to uninstall Microsoft Copilot on Windows 11 Pro, Enterprise, and EDU versions — devices must meet specific conditions to allow the removal of the AI app - 管理者がついにWindows 11（Pro/Enterprise/EDU）でMicrosoft Copilotをアンインストール可能に——ただし削除には条件あり"
date: 2026-01-11T00:25:45.504Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.tomshardware.com/software/windows/admins-finally-get-the-power-to-uninstall-microsoft-copilot-on-windows-11-pro-enterprise-and-edu-versions-devices-must-meet-specific-conditions-to-allow-the-removal-of-the-ai-app"
source_title: "Admins finally get the power to uninstall Microsoft Copilot on Windows 11 Pro, Enterprise, and EDU versions &mdash; devices must meet specific conditions to allow the removal of the AI app | Tom's Hardware"
source_id: 466134129
excerpt: "管理者必見：過去28日未起動など条件を満たせばWindows11でCopilotを削除可能に"
image: "https://cdn.mos.cms.futurecdn.net/SggxDWMWbaUEcy6UZAtp3k-2560-80.jpg"
---

# Admins finally get the power to uninstall Microsoft Copilot on Windows 11 Pro, Enterprise, and EDU versions — devices must meet specific conditions to allow the removal of the AI app - 管理者がついにWindows 11（Pro/Enterprise/EDU）でMicrosoft Copilotをアンインストール可能に——ただし削除には条件あり

魅力的なタイトル: 管理者必見：Windows 11で“勝手に入った”Copilotを本当に削除できるようになった — ただし落とし穴も

## 要約
MicrosoftがWindows Insider向けビルドで、管理者が組織内のPCから「Microsoft Copilot」アプリを削除できるポリシー（RemoveMicrosoftCopilotApp）を追加。ただし削除には複数の条件があり、すべての環境で即座に使えるわけではありません。

## この記事を読むべき理由
国内の企業・学校で配布されたPCや、プリインストールされたAI機能の制御に悩むIT管理者、日本のユーザーのプライバシーや運用方針を守りたい担当者にとって、今後の運用方針や導入可否判断に直結する情報です。

## 詳細解説
- 対象ビルドと対象エディション  
  Windows InsiderのDev/Betaチャネル向けビルド 26220.7535（KB5072046）で有効。対応するOSはWindows 11 Pro / Enterprise / EDU。

- 追加されたポリシー  
  RemoveMicrosoftCopilotAppというポリシーにより、管理者はユーザー環境から「Microsoft Copilot」アプリをアンインストール可能。ただし実行できるのは条件を満たしたデバイスのみ。

- 削除の条件（重要）  
  1) デバイスに「Microsoft 365 Copilot」と「Microsoft Copilot」の両方がインストールされていること。  
  2) Microsoft Copilotアプリがユーザー自身によってインストールされたものでないこと（管理側での削除対象）。  
  3) 過去28日間にMicrosoft Copilotアプリが起動されていないこと。  
  注：Microsoft Copilot（無償のプリインストール版）とMicrosoft 365 Copilot（有料のサブスク版）は別物で、本ポリシーは前者の削除を対象とします。

- 実運用上のハードル  
  Copilotは既定で「ログオン時に自動起動」が有効。さらにショートカット（Windows+C、Alt+Spaceなど）で簡単に起動してしまうため、「過去28日間未起動」という条件を満たすのが難しい場合があります。

- 管理ツールと操作場所  
  Group Policy Editorで設定可能：User Configuration > Administrative Templates > Windows AI > Remove Microsoft Copilot App。Insiderで試した後、正式リリースで配布されるのを待つのが現実的です。なおユーザー側はMicrosoft Store等から再インストール可能。

## 実践ポイント
- IT管理者向けチェックリスト  
  - まず環境が対象のエディションか確認（Pro/Enterprise/EDU）。  
  - 該当ビルドが社内で利用可能か、または正式リリース待ちかを評価。Insiderで検証するなら社内テスト端末で実施する。  
  - 削除条件（特に「過去28日間未起動」）を満たすため、該当端末で自動起動を無効化し、利用者へ不要起動を控える周知を行う。  
  - Group Policyで Remove Microsoft Copilot App を適用する前に、対象端末にMicrosoft 365 Copilotとの兼ね合いがないか確認する（有料機能を誤って阻害しない）。

- 現場でできる対策（ユーザー向け）  
  - Copilotを使わないなら自動起動をオフ、不要なショートカット操作を避けるよう案内。  
  - 削除後に必要になったらMicrosoft Storeから再インストール可能であることを周知しておく。

日本の組織ではプリインストールや一括配布が多く、運用ポリシーとユーザー教育が鍵になります。今回の改良は管理者権限での制御を進める一歩ですが、条件と運用負荷を踏まえた計画が必要です。
