---
layout: post
title: "How we rebuilt Next.js with AI in one week - AIで1週間でNext.jsを再構築した方法"
date: 2026-02-24T22:39:13.952Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.cloudflare.com/vinext/"
source_title: "How we rebuilt Next.js with AI in one week"
source_id: 47142156
excerpt: "AIで1週間開発のvinext：ViteでNext.js互換化しビルド4倍速・配信57%削減"
image: "https://cf-assets.www.cloudflare.com/zkvhlag99gkb/720QQcrdICiSJXrr9VoixA/4934fffd05d1ca10cc661238b381308e/BLOG-3194_OG.png"
---

# How we rebuilt Next.js with AI in one week - AIで1週間でNext.jsを再構築した方法

AIと一人のエンジニアが作った「vinext」──ビルドが最大4倍速、クライアントバンドルは最大57%削減。Next.js互換APIをVite上に再実装し、Cloudflare Workersへワンコマンドでデプロイします。

## 要約
vinextはNext.jsのAPI互換をViteプラグインとして再実装した実験的プロジェクト。短期間・低コストで作られ、ビルド速度とバンドルサイズの改善を示していますが、まだ完全な互換性・被検証性は限定的です。

## この記事を読むべき理由
日本のフロントエンド開発者や運用担当者にとって、ビルド時間短縮と小さい配信サイズはCIコスト削減やデプロイ速度向上に直結します。特に大量ページを扱うECやメディア運用では注目すべきアプローチです。

## 詳細解説
- 背景問題：Next.jsはTurbopackなど独自ツールチェーンに依存し、Cloudflare・Netlify等のサーバレス環境へのデプロイで変換（OpenNext等）が必要になり脆弱性や保守コストが生じる。
- アプローチ：既存のNext出力を変換するのではなく、Next.jsのAPIサーフェス（ルーティング、SSR、React Server Components、サーバーアクション、ミドルウェア、キャッシュAPI等）をVite上にクリーンに再実装。既存のnext.config.jsやapp/, pages/構成をそのまま使える「ドロップイン互換」を目指す。
- デプロイ：vinext deploy で自動的にビルド→Worker設定生成→Cloudflare Workersへデプロイ。KVベースのISRハンドラなどを標準で提供し、Durable ObjectsやAIバインディングも開発環境でテスト可能に。
- ベンチマーク（概方向）：
  - ビルド時間：Next.js (Turbopack) を基準に vinext (Vite 7/Rollup) は約1.6倍速、Vite 8/Rolldownでは最大約4.4倍速を報告。
  - クライアントgz: Next.js 168.9KBに対し vinextは約73KB前後（〜56–57%削減）。
  - 注：ベンチは33ルートのテストアプリでの指標、一般化には注意が必要。
- 重要な制約と現状：
  - 実験的プロジェクトで、公開から一週間で作られた。APIカバレッジはNext.js 16の約94%まで到達。
  - 現時点でビルド時の静的事前レンダリング（generateStaticParams に基づく完全事前ビルド）は未対応。ただしISRはサポート。
  - 「Traffic-aware Pre-Rendering (TPR)」という新提案：デプロイ時にCloudflareのトラフィック解析から実際に訪問される上位ページだけを事前レンダリングし、残りはオンデマンドSSR＋ISRで処理することで大規模サイトのビルド時間を劇的に短縮。
- AIの役割：大規模言語モデルを用いて実装の大半を生成し、既存のNext.jsテスト群を移植して自動検証ループを確立。ガードレール（テスト・型チェック・lint）で品質を担保。

## 実践ポイント
- まずは試す：小さなNext.jsアプリで動作検証（ローカル→Workers）を行い、互換性と開発体験を確認する。
```bash
# インストール例
npm install vinext
# スクリプトを next -> vinext に置き換え
vinext dev
vinext build
vinext deploy
```
- 大規模サイトではTPRが有効か検証する（ホットなページだけ事前レンダリングしてビルド時間を削減）。
- 本番採用は慎重に：実験的で完全互換ではないため、依存機能（静的完全事前ビルドや特定プラグイン）を要する場合は検証を厳密に。
- 日本のホスティングやCDN環境での相性を確認：Cloudflare中心の設計だが、Vercel等への移植コストは小さいと報告あり。自社環境でのテストを推奨。
- 貢献・追跡：OSSで開発が進むため、日本の現場でのユースケース（大規模EC、官公庁サイト等）でフィードバックやPRを出す価値あり。
