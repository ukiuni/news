---
layout: post
title: "Show HN: Stop paying for Dropbox/Google Drive, use your own S3 bucket instead - Dropbox/Google Driveに課金するのをやめて、自分のS3バケットを使う"
date: 2026-04-07T12:22:47.008Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://locker.dev"
source_title: "Locker | Open-Source File Storage Platform"
source_id: 47673394
excerpt: "自分のS3でDropboxを置換し、費用とベンダーロックインを断つオープンソースLocker"
---

# Show HN: Stop paying for Dropbox/Google Drive, use your own S3 bucket instead - Dropbox/Google Driveに課金するのをやめて、自分のS3バケットを使う
自分のS3でDropboxを卒業 — 週末で数TBを移行できる「Locker」でクラウド費用とベンダーロックインを断つ

## 要約
Lockerは自分でホストできるオープンソースのファイルストレージプラットフォームで、ローカル/ AWS S3 / Cloudflare R2 / Vercel Blob を切り替え可能。共有・検索・権限管理・API連携を備え、料金とデータ管理の自由を取り戻せます。

## この記事を読むべき理由
日本でもデータ主権やコスト最適化が注目されています。特にSaaSのストレージ費用やデータ流出リスクを抑えたい個人・スタートアップ・中小企業に有用な選択肢です。

## 詳細解説
- コア機能：アップロード、フォルダ管理、共有リンク（パスワード/有効期限/ダウンロード回数制限）、他者からのアップロードリンク、ワークスペースとロールベースの権限。
- ストレージプロバイダ非依存：環境変数（例：BLOB_STORAGE_PROVIDER）を変えるだけでローカル/ S3/ R2/ Vercel に切替。コード改変不要で既存のS3バケットを流用可能。
- 検索と操作性：画像・PDFのテキスト化で中身検索が可能。仮想bash風インターフェイスでls/cd/find/grep的操作ができるため、慣れた操作感でファイルを扱えます。
- セキュリティと自動化：メール/Google OAuth 認証、サーバー管理のセッション（暗号化クッキー）、APIキーとtRPCによる型安全なAPIで連携可能。
- 技術スタック：Next.js 16 (App Router)、PostgreSQL + Drizzle ORM、tRPC、BetterAuth、Tailwind、Turborepo、pnpm。ローカル開発はデフォルト設定で動作、プロダクションは任意のNode.js対応環境へ。
- コスト面の利点：既存のS3バケットを流用すればSaaS課金より大幅に安くなるケースがあり、Cloudflare R2ならアウトバウンド課金（egress）を抑えられます。

## 実践ポイント
- まず試す手順：リポジトリをクローン → pnpm install → PostgreSQL用意 → .envでBLOB_STORAGE_PROVIDERとストレージ設定を指定 → マイグレーション → サーバ起動。
- すぐ使える設定：既存のS3バケットを指定すれば既存データの移行コストと学習コストを抑えられる。R2は帯域が多い用途で有利。
- 運用注意点：バックアップ/監査ログ、アクセス権限設計、TLSやセッション管理を本番化前に確認すること。組織で使うなら認証連携（SSO）とAPIキー運用ルールを整備。
- 導入判断：小〜中規模チームやコスト最適化を優先するプロジェクトは検討候補。フルマネージドの安心感が欲しい場合は運用体制とのトレードオフを評価。

以上を踏まえ、まずローカルで立ち上げて既存S3を試すのが最短の検証方法です。
