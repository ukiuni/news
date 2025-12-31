---
layout: post
title: "A super fast website using Cloudflare workers - Cloudflare Workersで作る超高速サイト"
date: 2025-12-31T14:38:17.753Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://crazyfast.website"
source_title: "A super fast website using Cloudflare workers"
source_id: 46410676
excerpt: "Cloudflare Workersで初回30ms・再訪4msを実現する超高速サイト構築法"
---

# A super fast website using Cloudflare workers - Cloudflare Workersで作る超高速サイト
地球最速を目指すウェブの作り方：エッジで動く“本物の”JavaScriptがもたらす体感速度

## 要約
Cloudflare Workersを使い、200以上のエッジロケーションで実行される“リアルな”JavaScript＋サービスワーカーのCache-first戦略により、初回約30ms、再訪約4msという体感速度を実現した実例の紹介。

## この記事を読むべき理由
日本でもユーザーはモバイル・遅い回線での体験を重視します。エッジでロジックを走らせてレスポンスを極小化する手法は、ページ体感速度・Lighthouseスコア改善・コンバージョン向上に直結します。国内PoP（例：東京）を使えば同様の恩恵が得られます。

## 詳細解説
- エッジ実行（Cloudflare Workers）  
  単なるキャッシュ済みHTMLではなく、エッジでJavaScriptが実行される点が肝。ユーザーのリクエストは地理的に最も近い200+のPoPで処理されるため、往復遅延が小さい。

- キャッシュ戦略：Service Worker + Cache-first  
  初回はエッジで実行して生成したレスポンスをキャッシュし、再訪ではブラウザ内のService Worker／ブラウザキャッシュがネットワークアクセスをスキップさせる。これにより再訪は ~4ms 程度まで短縮される。

- アセット最適化  
  - Brotli圧縮で合計サイズを ~2.5KB にまで削減（多くの画像より小さい）。  
  - CSS/JSをインライン化して外部リクエストを排除。DNS/TCP/TLSハンドシェイクを省く。  
  - システムフォント使用でFOIT（フォント遅延）やレイアウトシフトを回避。  

- キャッシュ制御  
  Immutableキャッシュ（Cache-Control: max-age=31536000, immutable）を利用し、改変されないアセットは長期キャッシュ化。エッジ側で必要に応じて更新を管理する。

- 結果指標  
  Lighthouse 100/100/100/100 を達成した例として提示されている。主な理由は低いTTFB、ゼロ外部リクエスト、安定したレイアウト。

## 実践ポイント
すぐ実践できるチェックリスト：
1. Cloudflare Workersを有効化し、主要なルートをWorkerでハンドルする。  
2. Worker内でキャッシュ（caches.default）を使い「生成→キャッシュ→返却」を行う。簡易例：

```javascript
// javascript
addEventListener("fetch", event => {
  event.respondWith(handle(event.request));
});

async function handle(req) {
  const cache = caches.default;
  const cached = await cache.match(req);
  if (cached) return cached;

  const res = await fetch(req);
  const clone = res.clone();
  // 1時間だけエッジにキャッシュする例
  clone.headers.append("Cache-Control", "public, max-age=3600, immutable");
  event.waitUntil(cache.put(req, clone));
  return res;
}
```

3. クリティカルCSS/JSをインライン化して外部リクエストを排除。  
4. 画像は必要最小限にし、Brotli圧縮を適用。テキスト系アセットはさらに小さく。  
5. システムフォントを活用してFOITやCLSを減らす。必要ならfont-display: optional を検討。  
6. Service WorkerでCache-first戦略を実装し、再訪時はネットワークをスキップ。  
7. パフォーマンス検証は Lighthouse と WebPageTest（東京ロケーション）で比較。実測 RTT を観測してPoPの恩恵を確認する。  

実運用上の注意：
- 長期キャッシュを使う場合はバージョニング戦略を必ず実装すること（破壊的変更対策）。  
- エッジでの処理はCold startやWorkersのCPU/実行時間制限を考慮する。

## 引用元
- タイトル: A super fast website using Cloudflare workers  
- URL: https://crazyfast.website
