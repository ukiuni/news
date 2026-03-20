---
layout: post
title: "Microsoft: KB5079473 breaks internet access to Windows 11 Teams, Edge, OneDrive, Copilot - Microsoft：KB5079473がWindows 11のTeams、Edge、OneDrive、Copilotでサインイン不能を引き起こす"
date: 2026-03-20T17:06:10.629Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.neowin.net/news/microsoft-kb5079473-breaks-internet-access-to-windows-11-teams-edge-onedrive-copilot/"
source_title: "Microsoft: KB5079473 breaks internet access to Windows 11 Teams, Edge, OneDrive, Copilot - Neowin"
source_id: 379083928
excerpt: "KB5079473でWindows11のTeams等が“接続あり”でもサインイン不可、接続維持で再起動"
---

# Microsoft: KB5079473 breaks internet access to Windows 11 Teams, Edge, OneDrive, Copilot - Microsoft：KB5079473がWindows 11のTeams、Edge、OneDrive、Copilotでサインイン不能を引き起こす
Patchで「ネット接続あり」なのにサインインできない？KB5079473が引き起こすWindows 11の厄介な不具合

## 要約
2026年3月10日配信のPatch Tuesday更新（KB5079473）適用後、MicrosoftアカウントでのサインインがTeams Free、OneDrive、Edge、Excel/Word、Copilotなどで失敗し「You'll need the Internet（接続が必要）」と表示される問題が報告・確認されている。Microsoftは特定のネットワーク接続状態が原因と説明し、対策を案内している。

## この記事を読むべき理由
国内のリモートワークや中小企業でもTeams/OneDrive/Edgeは日常的に使われており、ユーザーサインインが不能になると業務停止やファイル同期の遅延を招くため、原因・回避策を知っておく必要がある。

## 詳細解説
- 対象更新：Windows 11（24H2/25H2）向けKB5079473（2026年3月10日配信）。  
- 症状：Microsoftアカウント（MSA）でのアプリ内サインインが失敗し、実際には接続していても「インターネットに接続していない」といったエラーが出る。影響アプリはTeams Free、OneDrive、Microsoft Edge、Excel、Word、Microsoft 365 Copilotなど。  
- 原因（Microsoftの説明）：デバイスが「特定のネットワーク接続状態」に入ることで認証フローが失敗する挙動。Entra ID/Azure AD（企業向けAAD）での認証は影響を受けないとされる。  
- 文脈：同時期にMicrosoft 365の大規模障害や他のホットパッチ（例：KB5084897）もあり、アップデート運用への注意が高まっている。  
- 回避策（Microsoft公式の案内）：インターネット接続を維持したままデバイスを再起動すると接続状態が修復され、問題が解消される場合がある。逆にオフラインで再起動すると再発する可能性がある。問題は自然解消することもある。

## 実践ポイント
1. 影響が出たら「インターネット接続を維持したまま再起動」をまず実施。  
2. すぐに業務を続ける必要がある場合は、ブラウザ版（teams.microsoft.com / office.com）でのサインインを試す。  
3. 企業アカウント（AAD/Entra）を使っている環境は影響が出にくいが、ユーザー報告は随時確認すること。  
4. Windows Updateの履歴でKB5079473を確認し、必要ならアップデートの一時停止や「更新のアンインストール（設定 → Windows Update → 更新の履歴 → 更新プログラムをアンインストール）」を検討。ただし卸す際は影響範囲を確認してから。  
5. 今後のPatch運用：重要な端末は更新の自動適用を遅らせ、社内検証を行ってから適用する運用を検討する。  
6. Microsoftのサービス健康ページや公式アナウンスをこまめに確認する。

短く言えば、まずは「ネット接続ありで再起動」を試し、業務継続はブラウザ経由か企業ADで回避。アップデート運用の見直しも検討を。
