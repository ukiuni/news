---
layout: post
title: "Native FreeBSD Kerberos/LDAP with FreeIPA/IDM - FreeBSDでネイティブにKerberos/LDAPをFreeIPA/IDMと統合する方法"
date: 2026-02-18T12:23:31.714Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://vermaden.wordpress.com/2026/02/18/native-freebsd-kerberos-ldap-with-freeipa-idm/"
source_title: "Native FreeBSD Kerberos/LDAP with FreeIPA/IDM | 𝚟𝚎𝚛𝚖𝚊𝚍𝚎𝚗"
source_id: 47059520
excerpt: "FreeBSD15でsssd不要、MIT Kerberos+nslcdでFreeIPA参加手順"
image: "https://vermaden.wordpress.com/wp-content/uploads/2025/11/freebsd-logo.png"
---

# Native FreeBSD Kerberos/LDAP with FreeIPA/IDM - FreeBSDでネイティブにKerberos/LDAPをFreeIPA/IDMと統合する方法
FreeBSD 15のMIT Kerberos移行で実現した、軽量かつ堅牢なFreeIPA/IdM連携の最短手順

## 要約
FreeBSD 15で Heimdal から MIT Kerberos に移行したことで、重厚な sssd を使わずに nss-pam-ldapd(nslcd) + MIT Kerberos で FreeIPA/IdM ドメインにネイティブ参加できる手順を紹介します。従来の複雑なビルド/依存関係を避け、SSH・コンソール認証・ホームディレクトリ自動作成までカバーします。

## この記事を読むべき理由
日本でもLinux中心のIdM/FreeIPA環境にFreeBSDサーバを組み込みたい場面が増えています。本手法はパッケージ中心で再現性が高く、運用負荷を下げられるため、教育機関・ISP・社内サーバ運用者に有益です（元記事は Christian Hofstede‑Kuhn の作業がベース）。

## 詳細解説
- 背景：FreeBSD 15 で Heimdal → MIT Kerberos へ移行したことが本手法の肝。MIT Kerberos を利用できることで GSSAPI（Kerberos）認証が安定して動作します。以前は sssd に多くの依存があり、アップグレードやビルドが面倒でした。
- アーキテクチャ：MIT Kerberos（システム側の Kerberos 実装） + nss-pam-ldapd（nslcd）で LDAP のユーザ情報取得、PAM での Kerberos 認証を組み合わせる。nslcd は軽量で LGPL ライセンス。
- 主な手順（要点）：
  1. pkg repo を quarterly → latest に切替（最新パッケージ利用）。
  2. 必要パッケージを導入：
     ```bash
     # bash
     pkg install -y nss-pam-ldapd pam_mkhomedir sudo doas
     ```
  3. FreeIPA 側でホスト追加と keytab 取得（ipa host-add / ipa-getkeytab）、取得した keytab を FreeBSD の /etc/krb5.keytab に配置し権限を設定。
     ```bash
     # bash
     fetch -o /etc/krb5.keytab http://rhidm.lab.org/ipa/config/fbsd15.keytab
     chmod 640 /etc/krb5.keytab
     ```
  4. /etc/krb5.conf にレルム/KDC を設定、/usr/local/etc/nslcd.conf に LDAP 接続と SASL GSSAPI を設定（sasl_mech GSSAPI）。
  5. nslcd を有効化・起動し、/etc/nsswitch.conf を passwd/group に ldap を追加。
  6. sshd で GSSAPI を有効化（GSSAPIAuthentication yes 等）し再起動。kinit でチケットを取得して SSH ログインを確認。
  7. ホームディレクトリ自動作成は pam_mkhomedir を sshd PAM に追加（session optional pam_mkhomedir.so mode=0700）。
  8. コンソールログインで Kerberos 認証を使いたい場合は /etc/pam.d/system 内の pam_krb5.so エントリを有効化。
  9. nslcd が keytab を読み取れるように sshd ユーザを nslcd グループに追加する等、権限調整を忘れずに。

- 注意点：
  - nss-pam-ldapd は LGPL ライセンス。組織ポリシーに注意。
  - DNS が正しく設定されていない場合は /etc/hosts で FreeIPA サーバ/ホスト名解決を行う。

## 実践ポイント
- まずは検証環境で FreeBSD 15 を用意して手順を再現する（パッケージ版で簡単に確認可能）。
- FreeIPA 側でホストを追加→keytab 発行→FreeBSD に配置、/etc/krb5.conf と nslcd.conf を最小設定で動かすのが近道。
- SSH での動作確認は kinit → ssh -l を順に実行。ホーム作成や sudo/doas での権限確認も忘れずに。
- 本番投入前にメンテナンス手順（keytab 更新、Kerberos/LDAP サーバ障害時のフェールオーバー）を用意する。

元記事（参考）： https://vermaden.wordpress.com/2026/02/18/native-freebsd-kerberos-ldap-with-freeipa-idm/ (原著は Christian Hofstede‑Kuhn の手法がベース)
