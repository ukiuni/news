---
layout: post
title: "We moved Railway's frontend off Next.js. Builds went from 10+ mins to under two - RailwayのフロントエンドをNext.jsから移行。ビルド時間が10分超→2分未満に"
date: 2026-04-08T08:04:48.461Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.railway.com/p/moving-railways-frontend-off-nextjs"
source_title: "Moving Railway&#x27;s Frontend Off Next.js"
source_id: 47685945
excerpt: "Vite＋TanStackに移行し、ビルドが10分超→2分未満に劇的短縮"
image: "https://res.cloudinary.com/railway/image/upload/v1775567332/blog/Moving-OG_aclrsn.png"
---

# We moved Railway's frontend off Next.js. Builds went from 10+ mins to under two - RailwayのフロントエンドをNext.jsから移行。ビルド時間が10分超→2分未満に

ビルド地獄を脱出したいですか？RailwayがNext.jsを捨て、Vite＋TanStackで開発ループを劇的に高速化した実録。

## 要約
Next.jsが抱えるビルド遅延と「サーバー寄り」設計がボトルネックになり、RailwayはフロントエンドをVite＋TanStack Routerへ移行。ビルド時間は10分超から2分未満に短縮され、開発の即時フィードバックが復活した。

## この記事を読むべき理由
- 反復開発の速度がプロダクト競争力に直結する今、ビルド改善はコスト削減以上の意味を持つ。  
- 日本のSaaS/スタートアップで似た課題を抱えるチームは、実用的な移行手順とトレードオフが学べる。

## 詳細解説
- 問題点：Railwayはダッシュボードやキャンバスがクライアント重視で、WebSocket多用のリアルタイムUI。Next.jsのPages Routerでは共有レイアウトが工夫の上乗せになり、ビルドは「finalizing page optimization」で長時間停滞。結果的に1回のビルドが10分超え、開発速度に重大な税がかかっていた。  
- 選定理由（Vite + TanStack Start）：クライアントファースト設計、即時HMR・ほぼゼロの起動時間、型付きルーティング（ルート／クエリの推論と補完）、パスレスレイアウトによる組み立てやすさ、必要箇所のみSSRという明示的なモデル。開発者の体験が良い点も決め手。  
- 移行戦略（2 PRでゼロダウンタイム）：  
  1) Next.js依存の除去（next/image/next/head/next/router をブラウザ標準やフレームワーク非依存版へ差し替え）。  
  2) フレームワーク切替：ページからコンポーネントを抽出し、ルートをファイルツリーから生成。Nitroをサーバー層に導入し、リダイレクト（500+）、セキュリティヘッダ、キャッシュ設定を一元化。Nodeポリフィルをブラウザネイティブに置換。結果、日曜早朝マージで即時運用、ダウンタイムなし。  
- インフラと配信：Railway自身のプレビューDeploy/ヘルスチェック/ゼロダウンタイム機能を活用。Fastlyでエッジ配信、マーケページはキャッシュ、動的はISRを適用。Viteのアセットモデル（コンテンツハッシュ単位のチャンク化）により、変更範囲のみ差分ダウンロードとなる。  
- トレードオフ：next/image等の組込み最適化を手放し、Fastly + <img>で補填。next-seo等エコシステムツールは自家実装に移行。TanStack Startは新しく荒削りだが、方向性とメンテの反応性に信頼を置いた。

## 実践ポイント
- 自分のアプリが「クライアント主導」か「サーバー主導」かを見極める。クライアント中心ならVite/TanStackは有力候補。  
- 移行は段階的に：まずフレームワーク依存を削る（画像・ヘッド・ルーターAPIの抽象化）、次にフレームワークを差し替える。  
- インフラ側はエッジキャッシュとコンテンツハッシュ化を活用し、差分配信を目指す（ユーザーの再DLを最小化）。  
- SSRは必要箇所だけに限定。不要な画面をSSR化しないことでサーバー負荷と開発複雑性を減らす。  
- 小さく試す：ローカルでTanStack Start＋Viteの開発ループを体感してから移行計画を立てる。

以上を踏まえれば、ビルド時間とフィードバックループの改善は単なる快適さではなく、開発速度とプロダクト価値を直接押し上げる施策になる。
