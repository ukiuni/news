---
layout: post
title: "What Claude Code chooses - Claude Codeは何を選ぶか"
date: 2026-02-27T12:48:17.969Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://amplifying.ai/research/claude-code-picks"
source_title: "What Claude Code Actually Chooses — Amplifying"
source_id: 47169757
excerpt: "AIは「買う」より「作る」を推し、JS寄りツール偏向と運用・セキュリティリスクを露呈"
image: "https://amplifying.ai/research/claude-code-picks/opengraph-image.png?267f044bb5256d31"
---

# What Claude Code chooses - Claude Codeは何を選ぶか
AIが「ツールを薦める」とき、意外と「作る」選択をする — Claude Codeの実測ベンチマークから見える現場の潮流

## 要約
AmplifyingがClaude Code（複数バージョン）を2,430回の実リポジトリ問合せで検証した結果、AIは「買う」より「作る（Custom/DIY）」を多用し、選ぶツール群はJSエコシステム寄りに偏ることが分かった。

## この記事を読むべき理由
日本の開発チームやプロダクトオーナーは、AIが提示する設計・ツール候補をそのまま採用しがち。AIの推奨傾向を知れば、技術選定の偏りやセキュリティ・運用リスクを事前に把握できる。

## 詳細解説
- データ概要：2,430レスポンス、3モデル（Sonnet 4.5 / Opus 4.5 / Opus 4.6）、20カテゴリ、抽出率85.3%、モデル間同意は90%（18/20カテゴリ）。
- 大きな発見：12/20カテゴリで「Custom/DIY」が最多。合計252件のDIY選択。例：機能フラグはenv＋割合ロールアウトの構成ファイルで実装、Python認証はJWT＋bcryptを自前で生成、キャッシュはインメモリTTLラッパー。
- ツールの「寡占」傾向：一度ツールを選ぶと決め打ちが強い。上位の既定ツール例：GitHub Actions（約94%）、Stripe（約91%）、shadcn/ui（約90%）、Vercel（JSで100%）、Tailwind、Zustand、Sentry、Resend、Vitest、PostgreSQLなど。
- 世代差（Recency Gradient）：新しいモデルほど新鋭ツールを選ぶ傾向。例：Opus 4.6はDrizzleをJS ORMで100%選択、Prismaは古いモデル寄り。Celeryは古いモデルで強く、新モデルではFastAPI BackgroundTasksやDIYに置き換わる。
- デプロイ分断：JSフロントはVercel一択、PythonバックエンドはRailwayが多数派（約82%）。従来のクラウド（AWS/GCP/Azure）は主要選択肢にならない。
- 見落とし・偏り：ReduxやExpress、Jest、npmなど市場で広い採用がある技術が主要推奨から外れるケースが多い。AIの推薦は「市場採用」ではなく「訓練データやモデルの好み」に依存。

## 実践ポイント
- AI提案は「参考」に留める：特に認証・決済などセキュリティ重要領域は自動生成コードを鵜呑みにしない（レビューと脆弱性検査を必須化）。
- 組織の制約を明確化：クラウドプロバイダや運用方針（AWS必須など）はプロンプトへ明示して偏らない提案を得る。
- 社内ベンチを作る：自社コードベースでAI推奨ツール比較を定期的に走らせ、採用・非採用の理由をデータ化する。
- 日本市場への示唆：日本企業では既存AWS投資やオンプレ運用が多いが、AIは軽量プラットフォーム（Railway/Vercel等）を好むため、運用・コスト面のギャップを評価して採用判断を行う。
- 新ツールの採用前に小さなPoCを回す：モデルが推す「新鋭」ツールは短期的には有効だが長期メンテ性とエコシステムを確認する。

（出典：Amplifying — Claude Code picks 実測データより、データ収集：2026年2月）
