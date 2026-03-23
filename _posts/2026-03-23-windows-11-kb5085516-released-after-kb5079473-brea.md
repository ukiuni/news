---
layout: post
title: "Windows 11 KB5085516 released after KB5079473 breaks Microsoft account sign-in in popular apps - KB5079473で人気アプリのMicrosoftサインインが壊れたためWindows 11にKB5085516を緊急配信"
date: 2026-03-23T02:14:38.375Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.windowslatest.com/2026/03/22/windows-11-kb5085516-released-after-kb5079473-breaks-internet-access-in-popular-apps-says-microsoft/"
source_title: "Windows 11 KB5085516 released after KB5079473 breaks Microsoft account sign-in in popular apps"
source_id: 417813804
excerpt: "KB5079473でTeamsなどがサインイン不能に、緊急KB5085516で即解決へ"
image: "https://www.windowslatest.com/wp-content/uploads/2026/03/Windows-11-KB5085516-update.jpg"
---

# Windows 11 KB5085516 released after KB5079473 breaks Microsoft account sign-in in popular apps - KB5079473で人気アプリのMicrosoftサインインが壊れたためWindows 11にKB5085516を緊急配信
TeamsやOfficeがログインできない人は要チェック：Microsoftが「サインイン不可」問題を修正する緊急パッチを公開

## 要約
3月配信のKB5079473で一部環境でMicrosoftアカウントのサインインやアプリのインターネット接続が障害となったため、Microsoftは緊急の「KB5085516」パッチをオプションで配布しました。該当する場合は早めに適用すると解決します。

## この記事を読むべき理由
企業でTeams、Office、OneDriveなどを日常的に使う日本のエンジニア／ビジネスユーザーは、サインイン不能が業務停止につながる可能性があります。影響範囲と対処法（更新の入手・適用方法）を短時間で確認できます。

## 詳細解説
- 問題の経緯：3月10日に配信されたKB5079473（Build 26200.8037）が一部ネットワーク条件でMicrosoftアカウントのサインインを妨げ、エラーコード0x800704cfや「インターネットに接続していない」表示を誘発。影響はTeams、Outlook、OneDrive、Word/Excel/PowerPoint、Microsoft Store、Feedback Hub、Copilotなど。
- 修正パッチ：KB5085516は「out-of-band（緊急）」アップデート。Windows 11 25H2はBuild 26200.8039、24H2はBuild 26100.8039に更新されます。自動強制配信ではなく、問題を抱える端末向けの任意インストール扱い。
- 適用時間と入手方法：Windows Updateから適用が推奨（ダウンロード約5分、適用5–7分程度）。Windows Updateで取得できない場合はMicrosoft Update Catalogの.msuファイルから手動インストール可能。
- 注意点：DNS変更・VPN・アプリ再インストール・wsresetなどでは直らないケースが報告されており、OS側の状態（特定のネットワーク接続状態）が原因になっている可能性。Microsoftは一部環境で自然復旧することもあると説明しています。

## 実践ポイント
- まずWindows Updateを確認し、KB5085516が表示されたら該当端末は適用する。  
- インストールできない／WUで取得できない場合はUpdate Catalogの.msuを使って手動適用。  
- 影響が出ていない端末は必須ではないが、業務利用端末やリモートワーク環境は適用を検討。  
- 管理者は配布前にテスト環境で適用確認し、展開手順を整備する（アンインストールやロールバックの手順も確認）。
