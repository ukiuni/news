---
layout: post
title: "Warning: Facebook Ads for Free Windows 11 Upgrade Will Infect PCs With Malware - 警告：Facebook広告の「無料Windows 11アップグレード」がPCをマルウェア化する"
date: 2026-03-01T01:34:29.175Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://uk.pcmag.com/security/163315/warning-facebook-ads-for-free-windows-11-upgrade-will-infect-pcs-with-malware"
source_title: "Warning: Facebook Ads for Free Windows 11 Upgrade Will Infect PCs With Malware"
source_id: 393991489
excerpt: "Facebook広告の偽Windows11更新で偽インストーラーがパスワードや暗号資産を窃取"
image: "https://sm.pcmag.com/t/pcmag_uk/news/w/warning-fa/warning-facebook-ads-for-free-windows-11-upgrade-will-infect_2gkk.1200.jpg"
---

# Warning: Facebook Ads for Free Windows 11 Upgrade Will Infect PCs With Malware - 警告：Facebook広告の「無料Windows 11アップグレード」がPCをマルウェア化する
Facebookの「無料Win11アップデート」広告に要注意 — クリックでパスワードや暗号資産まで奪われる危険

## 要約
Facebook広告で「無料／簡単にWindows 11へアップグレード」と誘導する偽サイトが出回り、偽インストーラー（ms-update32.exe など）を落としてパスワードやブラウザセッション、暗号資産ウォレット情報を窃取する攻撃が確認されています。公式の更新は必ずシステム設定のWindows Updateから行ってください。

## この記事を読むべき理由
日本でも古いWindows 10機が多数残るため、アップグレード案内に誘われやすく、業務PC・個人PCともに被害のリスクが高いです。ソーシャル広告経由の攻撃手口を知っておくことは即実践できる防御になります。

## 詳細解説
- 攻撃手口：Facebook広告でMicrosoftロゴや「Win 11 Pro」などの表記を用い、見た目が公式に見える偽サイトへ誘導。URLは ms-25h2-download[.]pro などの類似ドメイン。  
- すり替え：サイトはボットや研究者の検出を行い、検出されると通常のページへリダイレクトして痕跡を隠します。実ユーザーと判断されると 75MB 程度の実行ファイル（ms-update32.exe）がダウンロードされますが、これは偽インストーラーでマルウェアを実行します。  
- 被害内容：保存パスワード、ブラウザのログインセッション、暗号資産ウォレット情報などを窃取するモジュールが含まれる可能性。ダウンロードは攻撃者管理のGitHubページ等にホストされているケースも確認されています。  
- 検出と対策状況：Chromeなど一部ブラウザが偽サイトを悪質サイトとして警告していますが、広告経由での拡散が続いています。重要な点は「Windowsの更新はブラウザ広告から行わない」こと — MicrosoftはFacebook広告でアップデート配布を行いません。

## 実践ポイント
- 広告はクリックしない：SNS広告経由で配布されるOSアップデータは100%疑う。  
- 更新は必ず設定から：Windows Update（設定 > 更新とセキュリティ）からのみアップデートを実行。  
- URLを確認：microsoft.com 以外の類似ドメインは偽サイト。実行ファイルはダウンロードしない。  
- セキュリティ対策：信頼できるアンチウイルスを有効化し、ブラウザのフィッシング保護やSmartScreenをオンに。  
- 万一クリック／実行したら：ネットワーク切断、フルスキャン、パスワードの変更（特にブラウザ保存分）、暗号資産ウォレットの秘密鍵をオフラインで再確認・移行。  
- 報告と共有：怪しい広告はFacebookに報告し、社内や家族にも周知する。

安全な習慣（公式更新経路の利用、定期バックアップ、2段階認証の導入）が最も有効です。
