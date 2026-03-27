---
layout: post
title: "Installing a Let's Encrypt TLS Certificate on a Brother Printer with Certbot - CertbotでBrotherプリンターにLet's Encrypt TLS証明書を導入する"
date: 2026-03-27T15:50:17.936Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://owltec.ca/Other/Installing+a+Let%27s+Encrypt+TLS+certificate+on+a+Brother+printer+automatically+with+Certbot+(%26+Cloudflare)"
source_title: "Installing a Let's Encrypt TLS certificate on a Brother printer automatically with Certbot (&amp; Cloudflare) - OwlTec"
source_id: 47542644
excerpt: "CertbotとCloudflareでBrotherプリンターを自動TLS化する手順"
---

# Installing a Let's Encrypt TLS Certificate on a Brother Printer with Certbot - CertbotでBrotherプリンターにLet's Encrypt TLS証明書を導入する

魅力的なタイトル: 家の/社内のBrotherプリンターを本物のTLSで守る—Certbot＋Cloudflareで自動更新まで一括設定

## 要約
CertbotのCloudflareプラグインでDNS-01チャレンジを自動化し、Let's Encrypt証明書を取得してBrotherプリンターに適用、さらに更新を自動化する手順をわかりやすくまとめます。

## この記事を読むべき理由
多くの中小オフィスや自宅環境で使われるプリンターもTLS未導入だと盗聴や設定改ざんのリスクがあります。クラウド DNS（例: Cloudflare）を使えば、プリンター自身にACMEクライアントを入れられなくても安全に証明書を発行・更新できます。日本の現場でも実務で役立つ実践的な手順です。

## 詳細解説
ポイントは次の流れです：CloudflareのAPIでDNS-01チャレンジを自動化 → Certbotで証明書を取得 → 必要ならPKCS#12に変換 → Brotherプリンターへアップロード → 更新時は自動で同じ処理を実行。

主な技術要素
- DNS-01チャレンジ：プリンターが外部でACME応答できなくても、DNSレコードを操作してドメイン所有を証明可能。
- certbot-dns-cloudflare：Cloudflare APIを使ってTXTレコードを自動で追加/削除するプラグイン。
- 変換：多くのプリンター管理画面はPKCS#12（.p12/.pfx）形式を受け付けるため、取得した fullchain.pem / privkey.pem を openssl で .p12 に変換する必要がある場合が多い。
- 自動化：certbot の --deploy-hook / --post-hook で変換とプリンターへのアップロード（手動UIでも可）を連携して証明書更新も無停止で実現。

代表的なコマンド例（Cloudflare APIトークンを /etc/letsencrypt/cloudflare.ini に保存している前提）:

```bash
# Cloudflare用資格情報ファイル（例）
# /etc/letsencrypt/cloudflare.ini
dns_cloudflare_api_token = xxxxxxxx-your-token-xxxxxxxx
chmod 600 /etc/letsencrypt/cloudflare.ini
```

```bash
# Certbotで証明書取得（printer.example.com を自分のFQDNに置き換え）
sudo certbot certonly \
  --dns-cloudflare \
  --dns-cloudflare-credentials /etc/letsencrypt/cloudflare.ini \
  -d printer.example.com \
  --non-interactive --agree-tos -m admin@example.com
```

```bash
# PEMからPKCS#12へ変換（Brotherが.p12を要求する場合）
openssl pkcs12 -export \
  -in /etc/letsencrypt/live/printer.example.com/fullchain.pem \
  -inkey /etc/letsencrypt/live/printer.example.com/privkey.pem \
  -out /tmp/printer_cert.p12 \
  -name printer-cert -passout pass:yourpassword
```

アップロード方法はプリンター機種による：
- ブラウザ管理画面から手動アップロード（最も確実）
- 機種が対応すればAPIやcurlでPOSTアップロードを自動化（機種ドキュメントを確認）

更新自動化例：certbot renew の後に変換とアップロードを行うスクリプトを --deploy-hook に設定しておけば、更新時に自動で反映されます。

## 実践ポイント
- CloudflareはAPIトークンを「DNS編集のみに限定」して発行し、ファイル権限を600にする。
- プリンターFQDNは外部から到達できるDNS名を用意（内部LANのみなら内部CAや自己署名も検討）。
- まずは手動で証明書を取得→ブラウザでアップロードして動作確認、その後自動化する。
- openssl変換やアップロードスクリプトはテスト環境で繰り返し検証する（間違うとプリンターが一時的に応答しない可能性あり）。
- 証明書更新のログを監視し、失敗時にアラートが上がる仕組みを作る。

以上の流れを押さえれば、社内プリンターの通信をLet's Encryptで安全にし、証明書更新も自動化できます。必要なら、利用中のBrother機種向けの具体的なアップロード手順（機種名を教えてください）を補足します。
