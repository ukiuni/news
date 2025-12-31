---
layout: post
title: "How I authenticate a product identity from the browser using asymmetric JWT - ブラウザから製品IDを認証する方法（非対称JWT）"
date: 2025-12-31T04:38:22.192Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://sushantdhiman.substack.com/p/i-never-knew-jwt-could-be-used-this"
source_title: "How I authenticate a product identity from the browser using asymmetric JWT"
source_id: 475908338
excerpt: "APIキー漏洩を防ぎ顧客側署名を公開鍵で検証する、ブラウザ発のプロダクト認証法"
---

# How I authenticate a product identity from the browser using asymmetric JWT - ブラウザから製品IDを認証する方法（非対称JWT）

APIキーが漏れる前に止める──「共有秘密」を捨てた逆転の発想でブラウザ発のプロダクト認証を実現する方法

## 要約
APIキーや従来のJWTでは対応できない、ブラウザ発の「プロダクト（プロジェクト）アイデンティティ」認証課題に対して、顧客側がJWTを非対称で署名しサービス側が検証する「Reverse JWT」パターンを提案。秘密鍵は顧客のサーバに置き、公開鍵で検証することでブラウザにシークレットを置かない。

## この記事を読むべき理由
ブラウザから直接統合ポータルを開くような埋め込み型SaaSやSDKを提供する場面は日本のスタートアップや企業内製チームでも増加中。この記事のパターンは「ユーザー認証が不要なプロダクト単位の認証」を安全に実装する現実的な選択肢を示す。

## 詳細解説
問題設定
- シナリオ: Connectiveのような統合インフラで、ユーザーのログイン無しに「あるプロジェクト（製品）であること」をブラウザ経由で証明したい。
- 制約: 認証要求はブラウザから始まる／ブラウザに秘密を置けない／ユーザーアカウントは関与しない。

従来手法の限界
- APIキー：ブラウザで参照されるためDevTools等で容易に漏洩する。
- 典型的なJWT：サーバが発行者としてユーザー認証に依存する想定のため、ユーザーレスなプロダクト証明には適合しない。

Reverse JWT（非対称署名）パターン
1. プロジェクト作成時にRSA（またはEC）鍵ペアを生成。
2. 顧客は秘密鍵を自社バックエンドで安全に保管（HSM推奨）。
3. Connective等のプラットフォームは公開鍵を保存。
4. 顧客バックエンドがプロジェクト用JWTに署名してブラウザに渡す。
5. ブラウザはそのJWTをプラットフォームに送信。プラットフォームは公開鍵で検証してプロジェクトを認証。

利点
- ブラウザにシークレットを置かない（漏洩リスク低減）。
- JWTの検証は公開鍵のみで完結するためサーバ側の検証が安全。
- ユーザーレスの「プロダクトアイデンティティ」問題に最適。

考慮すべきセキュリティ/運用事項
- 短寿命のトークン（exp）と一度きりのnonce/jtiでリプレイ防止。
- kidによる公開鍵の管理とキーローテーション・失効処理。
- TLS必須、CORS制御、署名アルゴリズム（RS256/ES256）の明示。
- 顧客側で秘密鍵を安全に保護すること（HSMや環境変数の扱い）。
- 署名要求の認可（誰でも署名トークンを受け付けないように初期バインディングの検証）。

代替案
- mTLS（クライアント証明書）: ブラウザから直接は難しいが企業間通信なら強力。
- OAuth2 クライアント認証: サーバ間での認証には向くがブラウザ経由ユースケースとは噛み合わない。
- WebAuthn等: ユーザー主体の認証向けで、プロダクト単位には不適合。

## 実践ポイント
- 鍵管理: 各プロジェクトに鍵ペアを割り当て、公開鍵はプラットフォームDBでkid管理。
- トークン設計: 必要最小限のクレーム（iss, aud, exp, jti, proj_id）を入れ、expは短め（例 1–5分）。
- 検証: アルゴリズム固定検証（algチェック）、kid不一致は拒否。
- 運用: ログとアラートを整備し、公開鍵の入れ替えや秘密鍵漏洩に備える。
- ライブラリ: 標準のJWTライブラリ（Node/Go/Python等）でRS/ES系の検証を利用する。

簡単な概念コード（署名＝顧客バックエンド、検証＝プラットフォーム）
```javascript
// JavaScript (概念)
const jwt = require('jsonwebtoken');

// 顧客バックエンド: 署名（秘密鍵保持）
const token = jwt.sign({ proj_id: 'proj-123' }, CUSTOMER_PRIVATE_KEY, {
  algorithm: 'RS256',
  expiresIn: '2m',
  header: { kid: 'key-1' }
});

// ブラウザ経由でプラットフォームへ送信...

// プラットフォーム: 検証（公開鍵で検証）
try {
  const payload = jwt.verify(token, CUSTOMER_PUBLIC_KEY, { algorithms: ['RS256'], audience: 'connective' });
  // proj_id を信頼して処理を進める
} catch (err) {
  // 検証失敗処理
}
```

## 引用元
- タイトル: How I authenticate a product identity from the browser using asymmetric JWT
- URL: https://sushantdhiman.substack.com/p/i-never-knew-jwt-could-be-used-this
