---
layout: post
title: "Cert Authorities Check for DNSSEC From Today - 認証局が本日からDNSSECの検証を必須化"
date: 2026-03-16T17:53:44.154Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.grepular.com/Cert_Authorities_Check_for_DNSSEC_From_Today"
source_title: "Cert Authorities Check for DNSSEC From Today - grepular.com"
source_id: 47392510
excerpt: "DNSSECの不備で証明書発行が拒否される可能性—今すぐ署名とDSを確認"
image: "https://www.grepular.com/img/og-default.png?v=BQk80DfWRSqEt8E2"
---

# Cert Authorities Check for DNSSEC From Today - 認証局が本日からDNSSECの検証を必須化
今すぐ確認を：証明書発行の“落とし穴”を避けるためのDNSSECチェックガイド

## 要約
2026年3月15日付けで、ドメインにDNSSECが有効な場合、全ての認証局（CA）はDNSSEC検証を行った上でCAAやACMEのDNS応答を扱うことが必須になった。設定不備は証明書発行トラブルにつながる可能性がある。

## この記事を読むべき理由
日本でも多くの企業や個人が外部CAやACME（例: Let's Encrypt）を利用しているため、DNSSEC対応の有無が証明書取得の可否に直結する。事前確認でサービス停止や発行失敗を回避できる。

## 詳細解説
- 背景：DNSSECはDNS応答の改竄検出を提供する署名機構で、ドメイン所有性やポリシー（CAA）を信頼できる形で伝える。
- 変更点：CAはCAAレコードなどを照会する際、受け取ったDNS応答がDNSSECで正しく検証されたものかを確認しなければならない。ACMEプロトコルでDNSを使った認証を行う場合も同様に署名検証が必須となる。
- 技術的影響：DNSSECを有効にしているドメインでDNS署名が壊れている（DSレコードの未設定・不一致、ゾーン署名切れ、ミスな鍵ロールオーバ）と、CAは正当な応答を信頼できず証明書発行を拒否する可能性がある。
- 想定される対応：多くのCAは既に実装済みと考えられるが、違反や未対応が判明した場合は業界からの厳しい対応対象になり得る。

## 実践ポイント
- 自分のドメインでDNSSECが有効か確認：
```bash
dig +dnssec example.com DNSKEY
dig +dnssec example.com CAA
```
- レジストラ／DNSプロバイダがDNSSECをサポートしているか確認し、DSレコードを正しく登録する。多くは管理画面のワンクリック設定。
- 有効化前に検証ツールでチェック（DNSViz, Verisign Labs, dig +dnssec）。署名の有効期限やDSの不一致に注意。
- ACMEやCAを使う場合、CAAレコードが意図したCAを許可しているか確認。DNSSEC有効時はCAA応答の検証が必須になるため、CAA設定ミスが発行障害になる。
- 運用上の注意：鍵ロールオーバー手順を文書化し、DS更新を忘れない。CDNやマネージドDNSを使う場合はDNSSECの対応状況を事前確認。

以上を踏まえ、まずは自ドメインのDNSSECサポートと現在の署名状態を今すぐチェックすることを推奨する。
