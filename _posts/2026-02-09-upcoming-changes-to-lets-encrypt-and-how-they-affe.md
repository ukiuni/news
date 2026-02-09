---
layout: post
title: "Upcoming changes to Let's Encrypt and how they affect XMPP server operators - Let's Encryptの変更とXMPPサーバ運用への影響"
date: 2026-02-09T22:14:28.317Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.prosody.im/2026-letsencrypt-changes/"
source_title: "Upcoming changes to Let's Encrypt and how they affect XMPP server operators"
source_id: 46950780
excerpt: "Let’s Encryptがserver-only化、未対応XMPPで連合が切断される恐れ"
---

# Upcoming changes to Let's Encrypt and how they affect XMPP server operators - Let's Encryptの変更とXMPPサーバ運用への影響
XMPPの“連合”が突然つながらなくなるかも？Let’s Encryptの証明書仕様変更で今すぐ確認すべきこと

## 要約
2026年2月11日からLet’s Encryptが「サーバ認証のみ」の証明書をデフォルト発行します。多くのXMPPサーバ間接続（s2s）でTLSの役割解釈により接続失敗が起きる可能性がありますが、Prosodyは既に対策済みです。

## この記事を読むべき理由
日本でもLet’s Encryptを使うXMPPサーバは多く、連合（federation）先との接続障害が業務影響やコミュニティチャットの断絶を招く恐れがあります。今すぐ自サーバの互換性を確認しておく価値があります。

## 詳細解説
- 証明書の役割（Extended Key Usage, EKU）には「server authentication」と「client authentication」があり、従来のLet’s Encryptは両方を含んでいました。今後はデフォルトで「server authentication」のみになります（いわゆる server-only 証明書）。
- TLSの中では、「接続を開始した方」がTLS上の“クライアント”と見なされます。XMPPのs2sではサーバ同士の接続であっても、接続開始側がTLSライブラリの観点ではクライアント扱いになるため、証明書にclient authenticationが無いと検証失敗する実装が存在します（OpenSSLなど多くのライブラリがEKUチェックを行います）。
- Prosodyは以前からserver-only証明書を受け入れる代替検証を持っており、Let’s Encryptの新証明書でも問題ありません。しかし、他のサーバ実装はまだ未対応のものがあり、互換性のあるバージョンとしては ejabberd（25.08以降）やOpenfire の新しい実装が挙げられます。未対応だとs2s接続で「証明書が無効」と判断され接続が切れます。
- フォールバックとして古いdialback認証（DNSベース）を使って接続が続く場合がありますが、dialbackを無効化していると接続は完全に失敗します。ログには例として "Server-to-server connection failed: Could not authenticate to remote server" のようなエラーが出ます。

## 実践ポイント
- まずテスト：le-tlsserver.badxmpp.eu に XMPP ping（XEP-0199）を送る。iq応答があれば server-only を受け入れている。
- サーバソフトのバージョン確認と更新：ejabberdは25.08以上、Openfireやその他はベンダーの互換情報を確認してアップデートを行う。
- ログ監視：s2s関連の失敗ログをチェックし、該当エラーが出ていないか確認する。
- フェデレーション先と連絡：相手のサーバが未対応ならアップグレード依頼や一時的な対応策の調整を行う。
- dialbackは一時的な救済策に過ぎないため、可能な限りソフトウェアの更新で根本対応する。

（参考）検査用ホスト: le-tlsserver.badxmpp.eu — 成功すれば server-only 証明書を受け入れていることが確認できます。
