---
layout: post
title: "Moving from WordPress to Jekyll (and static site generators in general) - WordPressからJekyllへ（および静的サイトジェネレータ一般）移行"
date: 2026-04-09T22:36:42.152Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.demandsphere.com/blog/rebuilding-demandsphere-with-jekyll-and-claude-code/"
source_title: "Moving from WordPress to Jekyll (and static site generators in general) | DemandSphere"
source_id: 47710007
excerpt: "WordPressからJekyllへ移行し、速度・安全・AI連携を短期で実現する実践チェックリスト"
image: "https://www.demandsphere.com/assets/og/blog-rebuilding-demandsphere-with-jekyll-and-claude-code.png"
---

# Moving from WordPress to Jekyll (and static site generators in general) - WordPressからJekyllへ（および静的サイトジェネレータ一般）移行
WordPress疲れを脱却！Jekyll移行で高速・安全・AI対応サイトを短期間で実現する方法

## 要約
WordPressで運用していたDemandSphereが、速度・セキュリティ・運用効率を理由にJekyll（SSG）へ移行。AIアシスト（Claude Code）やリポジトリ内の開発ツール群を活用して、コンテンツ移行・SEO・検索・スキーマ管理を効率化した事例です。

## この記事を読むべき理由
日本でもWordPressは依然多く使われていますが、表示速度・管理コスト・セキュリティやLLM連携を考えると静的化のメリットが大きいです。具体的な運用設計や移行チェックリストが学べ、実務ですぐ使える知見が得られます。

## 詳細解説
- なぜJekyllか：SSGはDBやアプリサーバを不要にし、HTMLテンプレート＋YAMLフロントマター＋Markdownで管理。MarkdownはLLMと相性が良く、AIツールとの連携がしやすい点も利点。
- 移行の核：WordPressのXMLエクスポートを起点に、Search Consoleデータで価値のあるページを選別。不要ページは削除してコンテンツ量を最適化。
- AI支援：Claude Codeを使い、ページごとの価値分析や大量変換・スクリプト生成を自動化。少人数でも短期間で移行を進められた。
- リポジトリ内Devツール群：ビルド外で動く監査ツール（サイト構造チェック、Lighthouse監査、Schema/AEO監査、OGプレビュー、類似コンテンツ分析など）を作成し、移行後の品質担保を自動化。
- 埋め込みによる類似分析：all-MiniLM-L6-v2でサイト全体をベクトル化し、重複やトピッククラスタ、内部リンク改善ポイントを抽出。
- クライアントサイド検索：ビルド時に/search.jsonを生成し、ブラウザ側で軽量なスコアリング検索を実装。外部検索サービス不要で数千ページ規模まで高速な応答を想定。
- SEOと運用面：全ページにJSON-LD（Organization/WebSite、Breadcrumb、FAQ、BlogPosting等）を自動生成。robotsやSitemap、環境ごとのメタ（ステージングはnoindex等）を整備。
- デプロイと運用：Cloudflare Pagesを利用し、ブランチ別に環境切替。ビルドスクリプトで本番・プレビューを振り分け、不要ツールを本番から除外。
- ハマりどころ：Content Security Policyの調整（外部ビコンや広告、地図ライブラリで苦戦）、faviconのルート配置とサイズ要件、画像最適化など細部の運用負荷。

## 実践ポイント
- 移行前に価値あるURLを洗い出す（GSCやログで流入/インデックス状況を確認）。
- WordPress XML → Markdown変換は自動化スクリプト＋人によるQAで。公開前にパーマリンクとリダイレクトを完璧に。
- フロントマター設計を決める（title, date, tags, faqsなど）。スキーマはテンプレートで自動生成。
- 小さな監査ツール（Lighthouse、OGプレビュー、スキーマチェッカー）をリポジトリに入れてCIで回す。
- 埋め込み（embeddings）で類似コンテンツを検出し、統合・差別化・内部リンク戦略を作る。
- search.json方式で簡易検索を実装するとコスト削減になる（数千ページまでは有効）。
- デプロイ環境はステージングと本番を分け、環境依存のメタやロボット制御を自動化する。
- CSP、favicon、画像サイズなど細かい点も事前チェックリストに入れておく。

この事例は、日本のサイト運用でも有益です。特に中〜大規模で更新頻度が高く、速度やAI連携を重視するプロジェクトに向いています。導入を検討する際はまずコンテンツ監査とフロントマター設計から始めてください。
