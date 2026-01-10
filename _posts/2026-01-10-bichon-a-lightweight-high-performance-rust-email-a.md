---
layout: post
title: "Bichon: A lightweight, high-performance Rust email archiver with WebUI - Bichon：軽量で高速なRust製メールアーカイバ（WebUI付き）"
date: 2026-01-10T20:06:07.866Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/rustmailer/bichon"
source_title: "GitHub - rustmailer/bichon: Bichon – A lightweight, high-performance Rust email archiver with WebUI"
source_id: 46569075
excerpt: "オンプレで速攻検索できるRust製メールアーカイバ、Bichonで大量メールを安全に圧縮保存・高速検索"
image: "https://opengraph.githubassets.com/e0c2a50cc3ea0bf1f65a419c5a055c2b0fb536396d52d2d48e518f4a3ec0faf6/rustmailer/bichon"
---

# Bichon: A lightweight, high-performance Rust email archiver with WebUI - Bichon：軽量で高速なRust製メールアーカイバ（WebUI付き）
魅力的なタイトル：小さく速い、でも本格派。Rust製メールアーカイバ「Bichon」でメール資産を手元に置く理由

## 要約
BichonはRustで書かれた軽量なメールアーカイブサーバーで、IMAPから同期してフルテキスト検索やWebUI・REST APIでの操作を可能にする。外部DB不要で高速・圧縮保存・複数アカウント統合検索が特徴。

## この記事を読むべき理由
- 大量メールの検索・長期保存が必要な開発者や運用担当にとって、手軽に立てられて速いアーカイバは即戦力になるため。  
- 日本の企業でも電子記録保存や監査対応、メールのエビデンス管理が求められる場面が増えており、オンプレで完結する選択肢は魅力的。

## 詳細解説
- 目的と設計  
  Bichonは「メールを送受信するクライアント」ではなく「メールをアーカイブして検索・管理するサーバー」。継続的にIMAPからデータを取り込み、ローカルにインデックス化して高速検索を提供する設計。外部データベースや検索サービスを必要とせず、単一バイナリで動く点が特徴。

- コア技術  
  バックエンド：Rust + Poem。検索・保存のコアにはTantivy（Rust製の全文検索エンジン）を使い、メール本文と添付含むフルテキスト検索を実現。軽量メタデータは Native_DB に保存。フロントは React + TypeScript でWebUIを提供する。

- 主な機能  
  - マルチアカウントIMAP同期（パスワード / OAuth2、トークン自動更新）  
  - フルテキスト検索（送信者・件名・本文・日付・サイズ・添付など）とファセット（タグ）による絞り込み  
  - 圧縮・重複除去によるストレージ効率化  
  - REST API + OpenAPI ドキュメント（アクセストークン認証）  
  - WebUI（多言語対応）・ダッシュボード・エクスポート（EML/添付）  
  - コマンドラインツール bichonctl による EML/MBOX インポート

- 運用上の注意点（バージョン差分）  
  - CORSの扱い（v0.1.4以降）：BICHON_CORS_ORIGINS を未設定だと全オリジン許可に変わった。設定する場合はワイルドカード不可で完全一致が必要（ポート含む）。ブラウザから使うなら正確なホスト/ポートを指定すること。  
  - 認証（v0.2.0以降）：アクセス・トークン認証が常に有効。初期の管理者ユーザーが同梱される（初期パスワードは必ず変更推奨）。  
  - ライセンス：AGPL-3.0。商用で改変やサービス提供を行う場合はライセンス影響を要確認。

## 実践ポイント
- まずはDockerで試す（推奨）：
```bash
# Pull
docker pull rustmailer/bichon:latest
# データディレクトリ作成
mkdir -p ./bichon-data
# 起動（例）
docker run -d --name bichon -p 15630:15630 -v $(pwd)/bichon-data:/data -e BICHON_LOG_LEVEL=info -e BICHON_ROOT_DIR=/data rustmailer/bichon:latest
```
- CORS設定に注意：ブラウザアクセスが必要なら環境変数に正確な origin を列挙する。例：
```text
-e BICHON_CORS_ORIGINS=http://192.168.1.16:15630,http://myserver.local:15630
```
- セキュリティ：初回ログイン後に管理者パスワードを必ず変更。AGPLの扱いも事前に法務確認を。  
- 既存メールの取り込み：EML/MBOXがあるなら bichonctl でインポートして即座に検索可能。  
- 運用監視：CORSやOAuth問題はデバッグログ（BICHON_LOG_LEVEL=debug）で詳細確認。大規模導入前に小スケールで同期・検索速度と圧縮率を検証する。  
- 日本の運用観点：社内のメール保存ポリシーや電子帳簿保存法などのコンプライアンス要件との整合性を確認の上で、オンプレ保存・監査ログ確保の選択肢として検討する。

Bichonは「素早く立てられて検索に強い」ことを重視したツール。まずはDockerでトライし、既存のメールアーカイブの検索性能や運用要件に合うかを検証してみると良い。公式リポジトリとWikiに導入手順やFAQが揃っているため、試用から本番導入まで段階的に進められる。
