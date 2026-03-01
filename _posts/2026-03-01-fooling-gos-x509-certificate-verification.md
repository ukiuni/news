---
layout: post
title: "Fooling Go's X.509 Certificate Verification - GoのX.509証明書検証を騙す"
date: 2026-03-01T18:57:37.977Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://danielmangum.com/posts/fooling-go-x509-certificate-verification/"
source_title: "Fooling Go&#39;s X.509 Certificate Verification · Daniel Mangum"
source_id: 1637252347
excerpt: "たった2バイトの差でGoの証明書検証が失敗する原因と即効の実践対策"
image: "https://danielmangum.com/images/twitter-card.png"
---

# Fooling Go's X.509 Certificate Verification - GoのX.509証明書検証を騙す
Goの証明書検証が失敗する理由 — たった2バイトの罠

## 要約
見た目は同じ自己署名CA証明書でも、ASN.1の文字列型（PrintableString vs UTF8String）の違いでGoの検証が失敗する。OpenSSLでは通るが、Go標準ライブラリは証明書の生バイト列で照合しているため起きる不整合だ。

## この記事を読むべき理由
証明書検証はHTTPSや社内認証基盤で必須。日本の開発現場でも、見た目が同じ証明書でトラブルを招くケースは実務的に起こり得る。原因と対策を知れば無駄なデバッグ時間を避けられる。

## 詳細解説
- X.509はASN.1で定義され、DER（バイナリ）でエンコードされる。各フィールドは「タグ（型）」「長さ」「値」の順で並ぶ。
- 元記事で問題になったのはSubject/Issuerの文字列型：
  - PrintableString のタグは 0x13
  - UTF8String のタグは 0x0c
- 見た目（PEMをopensslで表示）では同一に見えても、DERバイト列を比較すると2バイトだけ異なっている。これがGoでの照合失敗の原因。
- Goのcrypto/x509パッケージはCertPoolの内部で byName map に cert.RawSubject（生のDERバイト列）をキーに格納し、leafの RawIssuer（生バイト列）と比較して親を探す。文字列型が異なると生バイトが一致せず候補にならない。
- 一方でOpenSSLはASN.1をパース後、文字列の正規化や型の許容範囲で比較しているため、この違いを吸収して検証に成功する。

確認に便利なコマンド例：
```bash
# DERで差分を見る
openssl x509 -in ca.crt.pem -outform der | xxd > ca.der.hex
openssl x509 -in ca.verifies.crt.pem -outform der | xxd > ca2.der.hex
diff ca.der.hex ca2.der.hex

# ASN.1型を確認
openssl asn1parse -in ca.crt.pem
openssl asn1parse -in leaf.crt.pem
```

## 実践ポイント
- トラブル対応
  - openssl asn1parseでSubject/Issuerの型（UTF8STRING / PRINTABLESTRING）を確認する。
  - DER差分（xxd + diff）でバイト差を見ると原因追跡が早い。
- 解決策（現場で取りうる対処）
  - 可能ならCAをUTF8Stringで再発行する（opensslの設定でUTF8を指定）。
  - 証明書発行ツールやテンプレートで文字列型を統一する（CNはUTF8に統一するのが安全）。
  - Go側で回避するなら、当該CA証明書を検証に使う前に、Issuer/Subjectの正規化を行ってRawを一致させるように変換する（ただし標準ライブラリの仕様を変える必要があるため実運用では再発行が現実的）。
- 開発運用の教訓
  - 「見た目が同じ」でもバイトレベルの違いでセキュリティ機能が動かなくなる。証明書は発行ポリシー（文字列エンコーディングを含む）を明文化して運用すること。

短くまとめると：ASN.1の文字列型の違い（たった2バイト）がGoの証明書チェーン検証を破綻させる。まずasn1parseで型を確認し、可能なら証明書をUTF8Stringで再発行して統一しよう。
