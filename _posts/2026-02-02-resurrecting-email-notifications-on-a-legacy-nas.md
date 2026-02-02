---
layout: post
title: "Resurrecting Email Notifications on a Legacy NAS - レガシーNASでメール通知を復活させる"
date: 2026-02-02T14:04:22.532Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://rhardih.io/2026/02/resurrecting-email-notifications-on-a-legacy-nas/"
source_title: "Resurrecting Email Notifications on a Legacy NAS &#8211; Zoned Out"
source_id: 832959499
excerpt: "10年物QNAPの通知をPi+Postfixで即復旧、古いTLSと証明書不足を回避"
---

# Resurrecting Email Notifications on a Legacy NAS - レガシーNASでメール通知を復活させる
10年選手のQNAPが通知を失った理由と、ラズパイで即効復旧させた実践ガイド

## 要約
古いQNAP NASが外部SMTPに接続できなくなった原因は「信頼済みルート証明書の欠如」と「古いssmtpのTLS制約」。解決策はNASのSMTPをローカルの軽量リレー（Raspberry Pi + Postfix）に向けて、Pi側で最新TLSとAPIキーで転送する方法。

## この記事を読むべき理由
古いNASや組込み機器でメール通知が急に止まる事例は日本の家庭や中小IT運用でも頻出。メーカーの公式サポート切れ機器でも最小限の投資で通知を復活させる技術的指針が得られます。

## 詳細解説
問題の分解
- まず疑うべきはTLS周り：NAS内のOpenSSLが古くても、証明書チェーンの検証用ルートが未導入だと接続が失敗します。
- 実際に openssl s_client で smtp.resend.com:465 に接続すると「Verify return code: 20 (unable to get local issuer certificate)」となり、ISRG Root X1（Let's Encrypt）を信頼していないのが判明。
- ルート証明書を /etc/ssl/certs に追加するとTLSハンドシェイク自体はOKになったが、送信プログラム ssmtp が STARTTLS 後に接続を完了できず失敗していた。ssmtp は古いライブラリや実装制約で最新SMTP/TLS要件に追従できない場合がある。

解決方針
- NAS側に大改修を加えず、同一LAN内に「翻訳役」を置く：Raspberry Pi上でPostfixをSMTPリレーとして稼働させ、NASは平文（または未認証）のローカルSMTPでPiに投げ、PiがResend等外部SMTPへ最新TLS＋APIキーで中継する。
- メリット：NASの設定を最小変更に留め、安全な外部転送（認証・暗号化）をPi側で集中管理。

重要な技術ポイント（抜粋）
- ルート証明書の追加手順（NAS上での例）
```bash
# opensslで接続確認
openssl s_client -connect smtp.resend.com:465 -tls1_2

# 公式から取得（NAS側で直接取得できない場合は手元で取得して転送）
curl -k -o ISRG_Root_X1.pem https://letsencrypt.org/certs/isrgrootx1.pem

# ハッシュ名を作ってリンク（Debian系の証明書ストア形式）
openssl x509 -hash -noout -in ISRG_Root_X1.pem
ln -s ISRG_Root_X1.pem 4042bcee.0
```
- ssmtpの簡易設定例（NAS側）
```ini
# /etc/ssmtp/ssmtp.conf
root=[email protected]
mailhub=smtp.resend.com:587
AuthUser=resend
AuthPass=re_xxxxx
UseSTARTTLS=YES
```
- Postfix（Pi側）最小構成の要点（抜粋）
```ini
# /etc/postfix/main.cf (抜粋)
inet_interfaces = all
inet_protocols = ipv4
mynetworks = 127.0.0.0/8 192.168.0.0/24
mydestination = 
local_transport = error:local delivery disabled

# Relay to Resend with implicit TLS
relayhost = [smtp.resend.com]:465
smtp_tls_wrappermode = yes
smtp_tls_security_level = encrypt

# SASL for relay auth
smtp_sasl_auth_enable = yes
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_sasl_security_options = noanonymous
```
- 必須の検証と落とし穴
  - swaksでローカルテストする際、IPv6優先で接続失敗することがある（-4でIPv4指定）。
  - Resendなどは送信元（From）が検証済みドメインであることを要求する（550 Invalid `from` field）。
  - /etc/postfix/sasl_passwd を作成後は postmap でハッシュ化し、権限を厳格に設定すること。
  - ファイアウォールやNASのSMTP設定（認証・暗号化を無効にしてローカルのみ許可）を確認。

## 実践ポイント
- まず確認：NAS上で
```bash
openssl version
openssl s_client -connect smtp.example.com:465 -tls1_2
```
で証明書チェーンエラーが出るか確認する。
- ルート証明書が欠けていれば取得してNASの信頼ストアに追加する（上記手順）。
- ssmtp や組込み送信クライアントがTLSを通せない場合は潔くローカルリレーを立てる（Raspberry Pi + Postfixが簡単）。
- Postfix側設定：relayhostに外部SMTP（ポート465）を指定、smtp_tls_wrappermode=yes、SASLでAPIキーを渡す。sasl_passwdは postmap して権限を600に。
- テストは swaks -4 を利用し、Fromは外部サービスで許可されたドメインにする。
- 運用上はPiをLAN内限定にし、NASからの接続元IPを制限すると安全。

この手順なら、サポート切れのNASでも低コストで通知機能を取り戻せます。必要ならNAS機種ごとのコマンドやPostfixの完全なplaybookを短くまとめて提示しますか？
