---
layout: post
title: "I Built a Localhost Tunneling tool in TypeScript - Here's What Surprised Me - TypeScriptで作ったローカルホスト・トンネル：作ってわかった驚き4選"
date: 2026-01-21T10:04:57.231Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://softwareengineeringstandard.com/2026/01/20/i-built-a-localhost-tunnel-in-typescript-and-heres-what-surprised-me/"
source_title: "I Built a Localhost Tunneling tool in TypeScript - Here&#039;s What Surprised Me - SES"
source_id: 421387615
excerpt: "TypeScript製ローカルトンネルの開発で判明した運用・悪用対策と低レイヤ実装の教訓"
image: "https://softwareengineeringstandard.com/wp-content/uploads/2026/01/ALocalhostTunnelingToolInTypescript.png"
---

# I Built a Localhost Tunneling tool in TypeScript - Here's What Surprised Me - TypeScriptで作ったローカルホスト・トンネル：作ってわかった驚き4選
ngrok代替を目指して自作したら、技術以上に「運用」と「悪用対策」に学びがあった話

## 要約
TypeScriptでクライアント・サーバ両方を実装したローカルホスト用トンネリングツールを作ったら、想定外の悪用（フィッシング）、高レベルAPIの落とし穴、メッセージ設計の重要性、そしてNode.js特有のメモリ管理問題に直面した——という話。

## この記事を読むべき理由
ローカル開発を公開URLで検証する需要は日本でも高く、Webフックやクロスデバイステストで多くの現場が利用する。自前でトンネルを作る／運用する際に陥りやすい実務的な落とし穴と対処法（技術的＆運用的）が具体的に学べるため、エンジニアやプロダクト担当は必読。

## 詳細解説
1) 悪用問題：フィッシング業者がトンネルサービスを好む理由と対策  
- 問題点：匿名性の高い無料公開URLは、詐欺サイトのホスティングに狙われやすい。苦情が来ても実際の発信元IPが分からなければ追跡できない。  
- 対策（効果的だった2つ）  
  - X-Forwarded-Forヘッダを必ず付与して、オリジナルのクライアントIPを残す。  
  - ランダムサブドメインにクライアントIPを埋め込む（例：`xj38d-ip-111-111-111-111.tunnelmole.net`）。発信元が一目で分かるため匿名性が下がり、悪用が減る。  
- 運用面：トンネル用のドメインとメインサイトのドメインを分けておく（SEO／ドメイン評判保護）。

2) 高レベルHTTPクライアントの落とし穴（fetch/axios vs http）  
- 問題点：fetchやaxiosは便利だが、ヘッダの小文字化、ボディの自動処理、ソケットレベルの制御不能などで「透過的なプロキシ」に向かない。トンネルは受け取ったバイト列をそのまま転送すべき場面が多い。  
- 解決策：Node.jsの組み込み http.request を使い、ヘッダをそのまま渡し、Buffer単位でボディを転送する。低レイヤーを選ぶ代わりにコールバックやイベント処理が増えるが、正確性が担保される。

例：受信した転送リクエストを localhost に投げるハンドラ（概略）
```TypeScript
import http from 'http';

export default function forwardedRequest(msg, ws, options) {
  const { requestId, url, headers, method, body } = msg;
  const req = http.request({
    hostname: 'localhost',
    port: options.port,
    path: url,
    method,
    headers
  }, (res) => {
    let buf = Buffer.alloc(0);
    res.on('data', (chunk: Buffer) => { buf = Buffer.concat([buf, chunk]); });
    res.on('end', () => {
      ws.sendMessage({
        type: 'forwarded-response',
        requestId,
        statusCode: res.statusCode,
        headers: res.headers,
        body: buf.toString('base64')
      });
    });
  });

  req.on('error', () => { /* エラーハンドリング */ });

  if (body) req.write(Buffer.from(body, 'base64'));
  req.end();
}
```

3) WebSocketメッセージは必ず「型付きJSON」で設計する  
- WebSocketは単なるメッセージ送受信手段なので、自前でメッセージ仕様を作らないと泥沼になる。  
- 有効なパターン：すべてのメッセージをJSONで { type: string, ...payload } として送る。サーバ側で type をルーティングすることで拡張性と可読性が大幅に向上する。  
- 利点：コネクション初期化、転送リクエスト、転送レスポンス、エラー通知などを明確に扱える。

サーバ側の簡易ディスパッチ例：
```TypeScript
websocket.on('message', (text: string) => {
  try {
    const message = JSON.parse(text);
    const handler = messageHandlers[message.type];
    if (handler) handler(message, websocket);
    else console.error(`No handler for message type: ${message.type}`);
  } catch (e) {
    console.error('Invalid message', e);
  }
});
```

4) Node.jsは長時間稼働プロセス：メモリリークに注意  
- PHPのようなリクエストごと初期化型と違い、Nodeは状態を保持する。未解放のオブジェクト（使い終わったWebSocket参照やコネクション情報）を放置するとメモリ使用量が徐々に増えプロセスが落ちる。  
- 対策：WebSocketの close イベントでコネクション配列から除去する、タイムアウトやTTLを設ける、定期的な健診（heapdumpやプロファイラ）でリークを検出する。

## 実践ポイント
- 悪用対策の実装順（おすすめ）
  1. X-Forwarded-For を必須で付与する
  2. サブドメインに発信元IPを埋める（匿名性を下げる）
  3. トンネル用ドメインと公式サイトを分離する
- プロトコル設計：WebSocketメッセージは必ず型付きJSONで設計し、ハンドラマップで処理する（将来の拡張が楽になる）。
- トンネルの正確性を優先するなら fetch/axios は避け、Nodeの http.request を使ってヘッダ・ボディをそのまま転送する。
- 運用監視：接続数、メモリ使用、異常レスポンス率を監視。closeイベントで確実に掃除し、TTLや最大接続数で保護する。
- 日本市場向け注意点：企業ネットワークでの利用や個人情報を扱うWebhookの検証においては、発信元IPの明示と利用規約・報告窓口の整備が必須。通報対応フローを明確にしておくとCSIRT対応がスムーズ。

短くまとめると、「トンネルを作るのは技術的に面白いが、運用と悪用対策を同時に設計することがサービス成功の鍵」。開発者としては、低レイヤーの正確さ（http）と高レベルな設計（型付きメッセージ）、そして運用監視を三本柱にすると良い。
