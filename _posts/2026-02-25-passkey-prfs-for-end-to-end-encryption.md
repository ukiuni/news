---
layout: post
title: "Passkey PRFs for end-to-end encryption - パスキーPRFによるエンドツーエンド暗号化"
date: 2026-02-25T20:31:27.172Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://oblique.security/blog/passkey-prf/"
source_title: "Passkey PRFs for end-to-end encryption | Oblique"
source_id: 396552460
excerpt: "パスキーのPRFで端末間同期とE2EEバックアップ鍵を自動派生し安全に復元可能に"
image: "https://cdn.sanity.io/images/dlxnfmjc/production/08b44486a17414392f35f13ba7ad55b45ce8355a-2048x1075.jpg"
---

# Passkey PRFs for end-to-end encryption - パスキーPRFによるエンドツーエンド暗号化
パスキーで「思い出せない鍵」を解決する――E2EEバックアップと同期をシンプルにする新しい鍵派生法

## 要約
パスキー（OSやパスワードマネージャで同期される公開鍵認証）からWebAuthnのPRF拡張を使って擬似乱数を得て、そこから暗号鍵を派生してE2EEバックアップや端末間同期に利用する手法を解説します。

## この記事を読むべき理由
消失しやすいパスフレーズや長い鍵をユーザに覚えさせずに、パスキーを安全な鍵素材へ変換できるため、メッセージングやクラウド同期を提供する日本のサービス設計でユーザ体験とセキュリティを両立できます。

## 詳細解説
- 背景：従来のE2EEでは端末紛失で復元不能になる問題があり、パスワード依存はユーザ負担が大きい。パスキーはOSやパスワードマネージャで同期され、パスワードの代替として広がっています。
- PRF拡張（WebAuthn）：WebAuthnには署名以外に「prf」拡張があり、クライアントがサーバ提供のsaltと認証器の秘密値を組み合わせて決定論的な擬似乱数（PRF出力）を返します。任意のデータを直接署名するAPIがない環境でも鍵派生に使える点が利点です。
- 運用パターン：
  - saltは静的でも可（認証器ごとに異なるため衝突は起きない）、回転や複数saltを用いると鍵更新が容易。
  - PRF出力をそのままHKDFなどに入れて対称鍵（例：AES-GCM）や非対称鍵の種にできます。
  - 暗号化時にはIVやHKDF用のsaltを公開メタデータとして保存し、復号時に同じPRF出力を用いて鍵を再派生します。
- 制約と注意点：
  - ブラウザ/プラットフォームのPRFサポート状況を確認する必要あり。
  - PRF出力自体は機器固有の秘密値に依存するため、アカウント移行や複数端末での同期要件を設計に組み込むこと。
  - JavaScriptでの暗号処理（Web Crypto）とメタデータ管理（IV・HKDF saltの保存）を厳密に扱うこと。

簡潔な利用イメージ（登録／認証時にsaltを渡してPRFを得る）：
```javascript
// javascript
const salt = new TextEncoder().encode("site-static-salt").buffer;
const cred = await navigator.credentials.get({
  publicKey: {
    challenge, // サーバが発行
    rpId,
    extensions: { prf: { eval: { first: salt } } }
  }
});
const ext = cred.getClientExtensionResults();
const prfOutput = ext.prf.results.first; // これをHKDF等に投入
```

## 実践ポイント
- まずは対応ブラウザでPRFサポートを確認して小さなプロトタイプ（クライアントでPRF→HKDF→AES-GCM）を作る。
- salt戦略：サービス全体での静的saltで素早く導入、鍵ローテーションや端末間移行はユーザー単位のsaltや二重saltで対応。
- メタデータ管理：IVとHKDF saltは暗号文と一緒に安全に保存（公開メタデータとして扱う）。
- 応用例：メッセージバックアップ、パスキー同期を利用したSSH鍵種生成、監査用署名シードなど。
- 参考実装：Obliqueのデモリポジトリ（https://github.com/oblique-security/webauthn-prf-demo）をローカルで動かして挙動を確かめる。

短期的にはユーザ体験の改善、中長期では端末・OS間のシームレスなE2EE運用に役立つ技術です。
