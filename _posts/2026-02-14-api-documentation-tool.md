---
layout: post
title: "API Documentation Tool - API ドキュメントツール"
date: 2026-02-14T12:07:07.881Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/surhidamatya/api-baucha"
source_title: "GitHub - surhidamatya/api-baucha"
source_id: 441981114
excerpt: "Next.js×GoでOpenAPIを集約、社内APIドキュメントとコード生成を即提供"
image: "https://opengraph.githubassets.com/18f6b1c5679a965188f79ecf666c0e2e3f6c0cc8723f810d734f395f2e07a736/surhidamatya/api-baucha"
---

# API Documentation Tool - API ドキュメントツール
魅せるAPIドキュメントをこれ1つで：Next.js × Goで作るOpenAPI集約プラットフォーム

## 要約
API Bauchaは複数マイクロサービスのOpenAPI仕様を集約し、生成コードやエンドポイント詳細を提供するドキュメントプラットフォーム。バックエンドはGoで完成、フロントはNext.jsでほぼ実装済み（現状はビルド問題あり）。

## この記事を読むべき理由
日本のマイクロサービス運用やAPI-first開発で、サービスごとのOpenAPIを一本化して見える化・自動生成できるツールは生産性と品質向上に直結します。社内APIカタログや技術ドキュメント自動化を検討するチームは参考になります。

## 詳細解説
- アーキテクチャ  
  - フロント：Next.js 16 + React 19 + TypeScript 5.7、Tailwind CSS 4、Bun（パッケージ管理）  
  - バックエンド：Go 1.23（Ginフレームワーク）、JWT認証、構造化ログ、環境ベース設定  
  - 通信：REST API、OpenAPI 3.0仕様の集約を想定  
  - デプロイ：Docker / docker-compose（マルチステージビルド、非rootユーザ）

- 主要機能（バックエンド完成済）  
  - 複数マイクロサービスからのOpenAPI集約（並列処理：goroutine）  
  - スマートキャッシュ（スレッドセーフ、TTL = 1時間）  
  - JWTベース認証、CORS設定、ヘルスチェック、ログローテーション  
  - キャッシュ統計、キャッシュクリアAPI

- フロントの状況（85%）  
  - UIコンポーネント、ログイン、サイドバー、エンドポイント表示、コード生成（cURL/TypeScript/Go/Java）は実装済み  
  - 未実装：OpenAPIパーサ（frontend/lib/parsers/openapi-parser.ts）とドキュメントページの動的ルーティング（約1〜2時間の作業見積）

- 現在の注意点  
  - Next.js 16の静的生成周りでフロントビルドが失敗する問題あり。回避策としてバックエンド単体での起動を推奨。

## 実践ポイント
- 手早く試す（バックエンドのみ）
  - cd backend
  - go mod download
  - go build -o api-server ./cmd/api
  - ./api-server
  - 動作確認: curl http://localhost:8080/api/health

- 開発用API（例）
  - ログイン: POST /api/auth/login with {"username":"api@baucha.com","password":"@Test1234"}（開発用デフォルト。実運用ではJWT_SECRET等を必ず変更）
  - 集約OpenAPI取得: GET /api/openapi/specs
  - サービス一覧: GET /api/openapi/services
  - キャッシュ管理: GET /api/openapi/cache/stats, DELETE /api/openapi/cache

- フロント実装に貢献するなら
  - openapi-parserの実装（OpenAPI→ナビ構造変換）を優先
  - docs レイアウト・動的ページを追加すればフルスタックで動作可能

- 運用で気をつけること
  - デフォルトのJWT_SECRETやデフォルト資格情報は本番禁物。環境変数管理とCIでのシークレット注入を推奨。
  - キャッシュTTLやCORS設定は運用要件に応じてチューニングを。

プロジェクト：github.com/surhidamatya/api-baucha（MITライセンス、ソース中の著作権表記とLICENSEの保持が必要）
