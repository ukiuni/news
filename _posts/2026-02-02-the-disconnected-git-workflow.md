---
layout: post
title: "The Disconnected Git Workflow - オフラインで回すGit送信ワークフロー"
date: 2026-02-02T10:34:15.254Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://ploum.net/2026-01-31-offline-git-send-email.html"
source_title: "The Disconnected Git Workflow"
source_id: 936270705
excerpt: "msmtpとgit-send-emailで複数アカウントを使いオフラインでパッチ送信を完結させる手順"
image: "https://ploum.net/files/bikepunk_logo_petit.png"
---

# The Disconnected Git Workflow - オフラインで回すGit送信ワークフロー
仕事でもOSSでも使える「メールでパッチ送信」術：GitHubのUIに頼らず、オフラインで複数アカウントを使ってgit-send-emailを回す方法

## 要約
git-send-email + msmtp（とそのキュー機能）を使えば、ローカルでコミット→メール送信→レビューをメールで完結させ、複数の差出人アドレス・オフライン送信を手堅く運用できます。

## この記事を読むべき理由
GitHubのプルリクやWeb UIに煩わされずにパッチを送りたい・複数メールアカウントやオフライン環境で作業する日本の開発者にとって、再現性が高くシンプルなワークフローを紹介します。

## 詳細解説
ポイントは msmtp を sendmail 代替として使い、msmtp のキュー機能でオフライン送信を実現する点。msmtpは複数アカウントを .msmtprc に定義でき、1つのアカウントに複数の from アドレス（正規表現も可）を割り当てられます。これを git の sendemail 機能と連携すると、各リポジトリごとに別の送信アドレスを使い分けられます。

主な設定と流れ：
- .msmtprc に複数アカウント（host/port/user/from/passwordeval 等）を定義
- グローバルな .gitconfig で sendmailCmd を msmtp（または msmtp-enqueue）へ設定し、envelopeSender = auto を有効化
- 各リポジトリで git config user.email / sendemail.from / sendemail.to を設定
- ローカルで作業後に git send-email HEAD^ などで送信（オフライン時はキューに溜める）
- オフラインで貯めたメールは msmtp-runqueue.sh で接続時に一括送信

例：.msmtprc（簡略）
```ini
# .msmtprc
account work
host smtp.company.com
port 465
user login@company.com
from ploum@company.com
tls_starttls off

account personal
host mail.provider.net
port 465
user ploum@mydomain.net
from ploum@mydomain.net
passwordeval "gpg --quiet --decrypt ~/mailpass.gpg"
```

例：グローバル .gitconfig の sendemail 設定
```ini
[sendemail]
    sendmailcmd = /usr/bin/msmtp --set-from-header=on
    envelopeSender = auto
```
（古い git では smtpserver / smtpserveroption を使う）

例：リポジトリごとの設定
```bash
git config user.email "Your Name <you-PROJECT@mydomain.net>"
git config sendemail.from "Your Name <you-PROJECT@mydomain.net>"
git config sendemail.to project-devel@mailing-list.com
```

間違ってコミットに誤った user.email を使った場合の修正：
```bash
git config user.email "Correct <you@domain>"
git commit --amend --reset-author
```

オフライン運用：msmtp に付属するスクリプト
- msmtp-enqueue.sh：メールを ~/.msmtpqueue に保存（オフラインでキュー）
- msmtp-listqueue.sh：キュー一覧表示
- msmtp-runqueue.sh：キューを実際に送信（オンライン時に実行）

.gitconfig をキュー用にすると：
```ini
[sendemail]
    sendmailcmd = /usr/libexec/msmtp/msmtpqueue/msmtp-enqueue.sh --set-from-header=on
    envelopeSender = auto
```

メールクライアント（例：neomutt）も sendmail を msmtp-enqueue に向ければ、返信も送信先アドレスに合わせてキューに入れられます。

## 実践ポイント
- まず .msmtprc に必要アカウントを登録。from はプロジェクト単位で使い分けるとスパム管理が楽。  
- グローバル .gitconfig の sendmailCmd と envelopeSender=auto を設定して git-send-email を msmtp と連携。  
- 各リポジトリで user.email / sendemail.from / sendemail.to を設定しておく。  
- オフライン作業時は msmtp-enqueue を使い、接続したら msmtp-runqueue.sh を走らせる習慣をつける。  
- 間違った author は git commit --amend --reset-author で簡単に直せる。

これでマウスやウェブUIに頼らない「シンプルでオフライン対応のパッチワークフロー」が手に入ります。
