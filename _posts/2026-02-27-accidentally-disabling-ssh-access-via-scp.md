---
layout: post
title: "Accidentally disabling SSH access via scp - scpで誤ってSSHアクセスを無効化してしまう"
date: 2026-02-27T13:04:48.596Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://sny.sh/hypha/blog/scp"
source_title: "Accidentally disabling SSH access via scp"
source_id: 1417822406
excerpt: "scpでディレクトリを777で転送したらSSH鍵認証が無効化される原因と対処法を具体的に解説"
---

# Accidentally disabling SSH access via scp - scpで誤ってSSHアクセスを無効化してしまう
scpでホームディレクトリの権限が書き換わり、SSH鍵ログインが弾かれる“777の罠”

## 要約
scpでローカルのディレクトリ（パーミッション777）をサーバにコピーしたところ、サーバ側の既存ディレクトリのパーミッションが上書きされ、sshdが安全性のため鍵認証を拒否してログイン不能になった、という実例と原因の解説です。

## この記事を読むべき理由
初心者でもやりがちなファイル転送操作が予期せぬ形でSSHログインを壊す可能性があり、原因特定と対処を知っておくと実務でのトラブルを速やかに防げます。

## 詳細解説
症状：
- scpでファイルを転送した直後にSSH鍵ログインが失敗（Permission denied (publickey)）。
- authorized_keysは残っており、別手段（パスワードログインやWebDAV）でファイルを見ることはできた。

原因の核心：
- scpは転送元のファイル/ディレクトリの権限（mode）をターゲットに反映する挙動があり、転送元ディレクトリが777だと既存のターゲットディレクトリ権限を777にしてしまう。
- OpenSSHのsshdはホームディレクトリや鍵ファイルの所有権・モードが緩すぎると認証を拒否するため、ホームが777になると鍵認証が無効化される。
- ログには次のような行が出る：`sshd-session: Authentication refused: bad ownership or modes for directory /home/user`

再現例（要点のみ）：
```bash
# ローカル側
$ mkdir local_dir
$ chmod 777 local_dir
$ cd local_dir
$ touch a b c

# リモート側（事前に700にしておく）
$ ssh host mkdir remote_dir
$ ssh host chmod 700 remote_dir

# scpで転送すると remote_dir のモードが変わる
$ scp -r . host:remote_dir
$ ssh host ls -ld remote_dir
# drwxrwxrwx  ← 777になってしまう
```

対応状況：
- 著者はOpenSSHのバグトラッカーに報告し、短期間で修正が取り込まれ（次バージョン10.3に反映）、対処されました。

## 実践ポイント
- 転送前にローカルのディレクトリ/ファイル権限を確認する：`ls -ld`、`chmod`で777を避ける。
- ホームディレクトリは常に700または適切なモードに保つ：`chmod 700 ~`。
- scpで心配な場合はrsyncを使う（例：`rsync -av --no-perms` など）か、tarでまとめてSSH経由で展開する（権限調整を明示できる）。
- SSHログを確認して原因を特定する：`/var/log/auth.log` や `journalctl -u sshd` を見るとヒントが出る。
- システムのOpenSSHは可能なら最新版にアップデートする（該当バグはOpenSSH 10.3で修正済み）。

元記事のポイントを押さえつつ、まずは「転送前に権限を疑う」を習慣にすると、この手のトラブルを未然に防げます。
