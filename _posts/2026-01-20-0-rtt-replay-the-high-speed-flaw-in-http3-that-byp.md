---
layout: post
title: "0-RTT Replay: The High-Speed Flaw in HTTP/3 That Bypasses Idempotency - HTTP/3の0-RTT再送攻撃：冪等性をすり抜ける高速の落とし穴"
date: 2026-01-20T12:37:52.736Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://instatunnel.my/blog/0-rtt-replay-the-high-speed-flaw-in-http3-that-bypasses-idempotency"
source_title: "0-RTT Replay Attacks: The Hidden Risk in HTTP/3 | InstaTunnel Blog"
source_id: 422134739
excerpt: "HTTP/3の0-RTTで支払い等がリプレイされ二重決済が発生する危険と実務対策を解説"
image: "https://i.ibb.co/9HZzF2Cv/0-RTT-Replay-The-High-Speed-Flaw-in-HTTP3-That-Bypasses-Idempotency.png"
---

# 0-RTT Replay: The High-Speed Flaw in HTTP/3 That Bypasses Idempotency - HTTP/3の0-RTT再送攻撃：冪等性をすり抜ける高速の落とし穴
HTTP/3の「瞬間接続（0-RTT）」は高速だが、リプレイ攻撃で非冪等な操作が二重実行されるリスクがある

## 要約
HTTP/3（QUIC）の0-RTTは復帰クライアントがハンドシェイク完了前にデータを送れるため高速化に寄与するが、同じパケットを捕獲・再送する「リプレイ攻撃」で非冪等操作（支払い、注文など）が重複実行される危険がある。

## この記事を読むべき理由
日本のウェブサービス／FinTech運営者やAPI開発者にとって、0-RTTはユーザー体験を改善する一方で金銭的・信頼の損失につながる実務上の脆弱性です。対策を知らないと、復旧コストや規模の大きな損害に直結します。

## 詳細解説
- なぜ0-RTTがあるか  
  従来のTCP+TLSでは接続確立に複数ラウンドトリップが必要。QUICはトランスポートと暗号を統合し、初回は1-RTT、再接続で0-RTT（セッションチケットを使った早期データ）を実現して遅延を削減する。

- 何が危ないのか（リプレイの仕組み）  
  0-RTTは過去のセッションから導出したPSKを使うため、サーバーがそのデータが「いま生きている正当なクライアントから来たものか」を確認する前にリクエストを処理してしまう可能性がある。攻撃者はパケットをキャプチャして後で同じパケットを送り直すだけで、暗号を破らなくてもサーバーに同一操作を実行させられる。

- なぜ暗号化が防げないのか  
  パケット内容を復号する必要はなく、サーバー側が有効な早期データとして受け入れてしまえば作用が重複する。

- 冪等性（idempotency）との関係  
  GET等は安全だが、POST/PATCH/DELETEなどは非冪等。0-RTTによるリプレイで決済や注文が二重に実行される実例（送金API、購入ボタンなど）が現実的に起き得る。

- 抑止・緩和策（レイヤ別）
  1. プロトコルレベル — RFC 8470 の Early-Data ヘッダと 425 Too Early  
     ・ロードバランサ／CDNは0-RTTをオリジンへ渡す際に Early-Data: 1 を付与し、オリジンはこれを見て「まだ処理しない」か評価する。安全でない処理は 425 を返して 1-RTT を待たせる。  
  2. 辞書（Strike Register）／Bloom Filter  
     ・受信したセッションチケットや初期パケットの識別子を記録し、短時間での再利用を拒否する。分散環境では状態同期が難しく、Bloom Filterでメモリ効率よくチェックするのが実用的。  
  3. アプリレベルの冪等化 — Idempotency Key  
     ・クライアントが state-changing リクエストに UUID 等の Idempotency-Key を付与し、サーバーはそのキーごとに結果をキャッシュして重複を防ぐ（Stripe方式）。

- 実装例（運用上のポイント）
  ・CloudflareはデフォルトでGETのみ慎重に0-RTTを扱い、Early-Dataを付ける。  
  ・Nginxは ssl_early_data で0-RTTを有効化できるが、バックエンド側で Early-Data をチェックして 425 を返すなどの対処が必要。  
  ・分散システムではStrike Registerの共有やFalse Positiveを許容したBloom Filter設計が鍵。

## 実践ポイント
- 原則：GETのみ0-RTTを許可、POST/PUT/DELETEは1-RTTにフォールバックさせる。  
- エッジ構成：CDN/ロードバランサで Early-Data ヘッダを付与・伝搬させる。オリジンは必ずこのヘッダを確認すること。  
- アプリ設計：状態変更APIは必須で Idempotency-Key を受け入れ、キーごとに処理結果を保存して再送を無害化する。  
- 再利用防止：可能ならStrike RegisterやBloom Filterで短期再送を検出。分散環境では確率的手法を組み合わせる。  
- レスポンス戦略：安全が確認できない早期データは 425 Too Early を返し、クライアントに再試行させる。  
- テストと監視：リプレイをシミュレートする侵入テスト、二重課金検知のロギング・アラートを整備する。

短い実装例（Nginx / Node.js）：

```nginx
server {
    listen 443 quic reuseport;
    ssl_protocols TLSv1.3;
    ssl_early_data on;
    location /api/secure {
        if ($ssl_early_data = "1") {
            add_header X-Handshake-Status "Early";
            proxy_pass http://backend;
        }
        proxy_pass http://backend;
    }
}
```

```javascript
// javascript
app.post('/api/transfer', (req, res) => {
  if (req.headers['early-data'] === '1') {
    return res.status(425).send('Too Early');
  }
  const idempotency = req.headers['idempotency-key'];
  if (idempotency && cache.has(idempotency)) {
    return res.json(cache.get(idempotency));
  }
  const result = processTransfer(req.body);
  if (idempotency) cache.set(idempotency, result, { ttl: 24*3600 });
  res.json(result);
});
```

まとめ：0-RTTはUX向上に有効だが、金融や注文系のAPIでは慎重に扱うこと。RFC 8470準拠＋アプリ側の冪等化で「速度」と「安全性」のバランスを取ろう。
