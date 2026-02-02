---
layout: post
title: "Common webhook security mistakes (raw body, replay attacks, timing attacks) - Webhook セキュリティのよくある誤り（生のボディ、リプレイ攻撃、タイミング攻撃）"
date: 2026-02-02T17:03:19.154Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/JosephDoUrden/webhook-hmac-kit"
source_title: "GitHub - JosephDoUrden/webhook-hmac-kit: Stripe-style webhook signing without the Stripe lock-in."
source_id: 411049747
excerpt: "Webhookの生ボディ署名やタイミング比較、ノンス運用で起きる致命的ミスと実践対策を詳述"
image: "https://opengraph.githubassets.com/159605ce23f867b8640d2d4e09b0c66bc26028474c240edda5de0ad2af4786f9/JosephDoUrden/webhook-hmac-kit"
---

# Common webhook security mistakes (raw body, replay attacks, timing attacks) - Webhook セキュリティのよくある誤り（生のボディ、リプレイ攻撃、タイミング攻撃）

必読：Webhookの署名と検証で陥りがちな落とし穴を一挙解説 — 実運用で使える対策付き

## 要約
WebhookはHMACで「生のボディ」を署名し、タイムスタンプ＋ノンスでリプレイ防止を行うべき。署名比較やJSON再シリアライズなどの誤りが実運用で致命的になる。

## この記事を読むべき理由
日本のSaaS連携、決済連携、Salesforce/Workato等のインテグレーションでもWebhookは多用されます。誤実装は不正受信や二重処理、情報漏洩につながるため、基礎と実践的対策を押さえておくべきです。

## 詳細解説
- 署名方式  
  HMAC-SHA256で署名し、検証側も同じ生データ（「exact bytes」）で計算する。ライブラリは「v1:{timestamp}:{nonce}:{payload}」のような正規化文字列を用いる。
  例: v1:1700000000:nonce_abc123:{"event":"payment.completed","amount":4999}

- 生のボディが重要な理由  
  JSONをparse→stringifyすると空白やキー順の差でバイト列が変わり、署名が一致しなくなる。必ず"verify first, parse second"（検証→解析）。

- タイミング攻撃対策  
  単純な === 比較は時間差で秘密が漏れるリスクがある。常に crypto.timingSafeEqual のような定数時間比較を使う。

- リプレイ攻撃対策  
  タイムスタンプ許容幅（例: 300秒）＋ノンス（UUID）で同一ノンスの再利用を拒否する。ノンスはRedis等でTTL付きキーとして保存し、重複を検出する。

- エラー設計とHTTPステータス  
  署名不正→401、タイムスタンプ外→400、ノンス重複→409 のように分けてハンドリングすると運用で原因特定しやすい。

- なぜJWTじゃないか  
  JWTは認証向けであり、HTTPペイロードの「生のバイト」を直接安全に署名する用途にはHMACがシンプルで適切。

- 運用上の注意  
  シークレットはログに出さない、HTTPS必須、ペイロードサイズ制限、キー回転を統合レイヤで扱う。

受信の簡単な実装例（Express）:
```typescript
import express from 'express'
import { verifyWebhook, WebhookError } from 'webhook-hmac-kit'

const app = express()

app.post('/webhook', express.raw({ type: 'application/json' }), async (req, res) => {
  try {
    await verifyWebhook({
      secret: process.env.WEBHOOK_SECRET!,
      payload: req.body.toString('utf-8'),
      signature: req.headers['x-webhook-signature'] as string,
      timestamp: Number(req.headers['x-webhook-timestamp']),
      nonce: req.headers['x-webhook-nonce'] as string,
    })
    const event = JSON.parse(req.body.toString('utf-8')) // 検証後にパース
    res.sendStatus(200)
  } catch (err) {
    if (err instanceof WebhookError) {
      res.status(401).json({ error: err.code })
    } else {
      res.sendStatus(500)
    }
  }
})
```

送信（署名）例:
```javascript
import { signWebhook } from 'webhook-hmac-kit'
import crypto from 'node:crypto'

const payload = JSON.stringify({ event: 'record.updated', id: '001xx000003DGbX' })
const timestamp = Math.floor(Date.now() / 1000)
const nonce = crypto.randomUUID()
const { signature } = signWebhook({ secret: 'whsec_your_secret', payload, timestamp, nonce })
// 署名・timestamp・nonce をヘッダで送る
```

## 実践ポイント
- 受信側は必ず「生のボディ」で検証してからJSONをパースする。  
- 署名は常に定数時間比較を使う（crypto.timingSafeEqual等）。  
- タイムスタンプ許容幅を設定し、ノンスをTTL付きで保存して重複を拒否する。  
- シークレットをログに出さない、HTTPSを必須化、ペイロードサイズ制限を設ける。  
- 簡単なテストベクトルで署名/検証が一致することをCIで確認する。

短く言えば：生のバイト列を大事に、比較は安全に、時間とノンスでリプレイを防ぐ。これだけ守ればWebhook周りの落とし穴の多くを排除できます。
