---
layout: post
title: "TLS handshake step-by-step — interactive HTTPS breakdown - TLSハンドシェイクをステップバイステップで解説（インタラクティブなHTTPS分解）"
date: 2026-02-22T19:31:33.417Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://toolkit.whysonil.dev/how-it-works/https"
source_title: "How HTTPS Works - TLS 1.3 Handshake Explained | Toolkit"
source_id: 399165595
excerpt: "TLS1.3の鍵交換を図解で詳解、ECDHE/HKDFや証明書検証まで丁寧解説"
image: "https://toolkit.whysonil.dev/og-image.png"
---

# TLS handshake step-by-step — interactive HTTPS breakdown - TLSハンドシェイクをステップバイステップで解説（インタラクティブなHTTPS分解）
ブラウザとサーバーが「鍵」をすり合わせる瞬間を図解で理解する — TLS 1.3 を初心者向けにやさしく解説

## 要約
TLS 1.3 のハンドシェイクは、TCPの接続確立（SYN/SYN-ACK/ACK）に続き、ClientHello→ServerHello→証明書→ECDHEで共有秘密を作り、HKDFでセッション鍵を導出し、Finishedメッセージで相互検証して暗号化されたHTTP通信を開始する流れ。

## この記事を読むべき理由
TLSはウェブの「鍵」であり、個人情報や決済を守る基盤。日本のサービス運営者やフロントエンド/インフラ担当はTLSの仕組みを理解して正しい設定・検証ができると、セキュリティとユーザー信頼を同時に高められる。

## 詳細解説
- TCPハンドシェイク（ポート443）
  - クライアントがSYNを送信 → サーバがSYN-ACKで応答 → クライアントがACKで完了。これで信頼性のあるパイプができる。
- Client Hello
  - ブラウザが対応TLSバージョン、暗号スイートの候補、SNI（接続先ドメイン）、ランダム値を送る。
- Server Hello
  - サーバが一つの暗号スイート（例: TLS_AES_256_GCM_SHA384）を選び、自身のランダム値を返す。
- 証明書（X.509）
  - サーバは公開鍵と身元情報をCA署名付きで提示。ブラウザは信頼できるCAか、有効期限、ドメイン一致を検証する（例: Let's Encryptチェーンの検証）。
- 鍵交換（ECDHE）
  - クライアントとサーバがE​CDHE（例: X25519）で公開値を交換し、共有秘密をそれぞれ独立に計算。これによりフォワードシークレシーが確保される。
- 鍵導出（HKDF）
  - 共有秘密＋Client/ServerランダムからHKDFで対称鍵（client_write_key / server_write_key 等）とIVを生成。対称暗号（AES-GCMやChaCha20-Poly1305）で高速暗号化を行う。
- Finished メッセージ
  - ハンドシェイク全体のハッシュを鍵でMAC/暗号化したFinishedを相互に送受信し、改竄がないことを確認。
- 完了後はHTTP/2やHTTP/3をTLSで保護した通信へ。TLS1.3は往復回数が少なく高速化（記事抜粋で約20msの手順時間例）。

重要な点：TLS1.3は古いRSA鍵交換を廃止し、より安全なE​CDHE中心の流れになっている。証明書チェーン検証、OCSP/CRL、署名アルゴリズム（SHA256など）のチェックが必須。

## 実践ポイント
- サーバ側でTLS 1.3を有効化し、X25519（ECDHE）とAES-GCM/ChaCha20-Poly1305を優先する。
- 証明書はLet's Encryptなどで自動更新を導入（更新忘れでサービス停止を防ぐ）。
- SSL/TLS設定を外部ツール（SSL Labs）で定期診断し、古いプロトコル（TLS1.0/1.1）や脆弱な暗号を無効化する。
- OCSPステープリング、HSTS、HTTP/3（QUIC）対応を検討し、レイテンシと安全性を改善する。
- 日本のサービスでは個人情報保護（改正個人情報保護法）やIPAのガイドラインを踏まえ、通信の暗号化を事業要件に組み込む。

以上を押さえれば、TLSハンドシェイクの「何が起きているか」を理解した上で安全なHTTPS運用に役立てられる。
