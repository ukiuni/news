---
layout: post
title: "TanStack Start Now Support React Server Components - TanStack StartがReact Server Componentsをサポート"
date: 2026-04-14T06:08:07.336Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://tanstack.com/blog/react-server-components"
source_title: "React Server Components Your Way | TanStack Blog"
source_id: 47761609
excerpt: "TanStack StartがRSCをFlight化し既存環境へ段階導入で高速化"
image: "https://tanstack.com/.netlify/images?url=%2Fblog-assets%2Freact-server-components%2Fheader.jpg&amp;w=1200&amp;h=630&amp;fit=cover&amp;fm=jpg&amp;q=80"
---

# TanStack Start Now Support React Server Components - TanStack StartがReact Server Componentsをサポート
RSCを「フレームワークに縛られず」自由に使える時代へ — TanStack Startの提案

## 要約
TanStack StartはReact Server Components（RSC）を「サーバーの専有物」ではなく、クライアントが取得・キャッシュ・レンダリングできる“Flightストリーム”として扱う設計を導入。既存のTanStackツール群（Query/Router）と自然に統合できます。

## この記事を読むべき理由
- 日本のWebサービスでも、コンテンツ重めページのパフォーマンス改善は重要。RSCを柔軟に取り入れることで配信負荷とブラウザのJS負荷を下げられます。  
- フレームワーク丸ごと乗り換えずに段階的導入できる点は、既存プロダクトに特に刺さります。

## 詳細解説
- 基本思想：RSCを「React Flightのストリーム」として扱い、サーバーはFlightストリーム（バイト列）を出し、クライアントやSSR側でそれをデコードしてReact要素に戻す。特殊プロトコルや黒箱化は避ける設計。
- 主要API（意図的に小さい）：
  - renderToReadableStream（サーバー側でReact要素→Flightストリーム）
  - createFromReadableStream（クライアント/SSRでストリーム→React要素）
  - createFromFetch（fetch結果から直接デコード）
- TanStack Queryとの相性：RSC出力を通常のasyncクエリとして扱えるため、queryKeyやstaleTimeなど既存のキャッシュ戦略がそのまま使える。静的コンテンツなら staleTime: Infinity を設定すればOK。
- Routerとの連携：ルートローダーがストリームを返し、ルータのキャッシュで即時復帰（バックボタンの応答性向上など）可能。
- CDN/ブラウザキャッシュ：GETサーバー関数はHTTPレスポンスなのでCDNに任せたキャッシュ戦略が立てやすい（例：Netlify向けヘッダ設定）。
- セキュリティ：暗黙のサーバーアクションは避け、明示的な RPC（createServerFn）を使う方針。シリアライズやバリデーションを明確にすることで攻撃面を小さくする。
- 適用スペクトラム：完全クライアントSPA〜ハイブリッド〜ほぼ静的まで、ルート／コンポーネント単位で柔軟に選べるのが特徴。

参考の簡易コード例（要点のみ）:

```tsx
// tsx
import { createServerFn } from '@tanstack/react-start'
import { createFromReadableStream, renderToReadableStream } from '@tanstack/react-start/rsc'

// サーバー関数（GETなど）
const getGreeting = createServerFn().handler(async () => {
  return renderToReadableStream(<h1>Hello from the server</h1>)
})

// クライアント側でQueryとして取得してレンダリング
function Greeting() {
  const query = useQuery({
    queryKey: ['greeting'],
    queryFn: async () => createFromReadableStream(await getGreeting()),
  })
  return <>{query.data}</>
}
```

実際の効果（tanstack.com移行例）：クライアント転送サイズやTotal Blocking Timeが大幅改善（例：Blogページで転送量が約1,101 KiB→785 KiB、TBT 1,200ms→260ms）。

## 実践ポイント
- まずは「コンテンツ重めで依存が多いページ」からRSCを導入する（ブログ、ドキュメント等）。  
- TanStack QueryでRSC出力をラップしてstaleTimeや背景リフェッチを活用する。  
- ルートローダーでRSCを返し、ルーターキャッシュでUXを向上させる（戻る操作の高速化）。  
- CDN側でGETレスポンスをキャッシュするヘッダを設定して配信コストを削減する。  
- サーバー関数はcreateServerFnで明示的に定義し、入力バリデーション／認証を忘れない。

短い導入の勝ち筋：既存のデータワークフロー（Query/Router/CDN）を壊さずにRSCを「ただの非同期データ」として扱うことで、段階的かつ安全にパフォーマンス改善が狙えます。
