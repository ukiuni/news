---
layout: post
title: "Show HN: Omni – Open-source workplace search and chat, built on Postgres - Omni — Postgres上に構築されたオープンソースの職場向け検索とチャット"
date: 2026-03-02T10:05:19.140Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/getomnico/omni"
source_title: "GitHub - getomnico/omni: Workplace AI Assistant and Search Platform"
source_id: 47215427
excerpt: "Postgresで完結する社内検索＋AIチャット基盤Omniの全貌"
image: "https://opengraph.githubassets.com/c79fdefe0afdd9ddb7cbed84f25a0dfeefc1275b2a7331e7cb0d8f84d82ca3ed/getomnico/omni"
---

# Show HN: Omni – Open-source workplace search and chat, built on Postgres - Omni — Postgres上に構築されたオープンソースの職場向け検索とチャット
Postgres一本で社内データを守りつつ「検索＋AIチャット」を自前で実現するオープンソース、Omniの全貌

## 要約
OmniはPostgresを中核にBM25全文検索とpgvectorベースの意味検索を統合し、社内アプリ（Google Workspace/Slack/Confluence/Jira等）を横断して検索／チャット／エージェント実行をセルフホストで提供するプラットフォームです。

## この記事を読むべき理由
日本企業はデータ保護やコンプライアンス（APPI）を重視します。Omniはデータを社外に出さず自社インフラで動かせるため、機密情報を扱う現場やオンプレ運用を検討するチームにとって実戦的な選択肢になります。

## 詳細解説
- アーキテクチャの核はPostgres：BM25による全文検索とpgvectorでの意味検索を同一DBで実装。Elasticsearchや専用ベクタDBが不要で、バックアップ・運用が単純化されます。  
- 多言語スタック：コアはRust（searcher/indexer/connector-manager）、Python（LLMオーケストレーション）、SvelteKit（フロント）で構成。  
- コネクタ設計：各データソース（Drive/Gmail/Slack/Confluence/Jira/ファイルシステム等）は独立した軽量コンテナで動作。言語/依存を分離でき、障害の局所化が容易。  
- AIエージェント：チャットUIからコネクタ検索やドキュメント読取、サンドボックス内でのPython/bash実行が可能。実行環境は隔離されたDockerネットワーク＋Landlockやリソース制約、ルート読み取り専用で安全性を高めています。  
- LLMは持ち込み可：Anthropic/OpenAI/GeminiやvLLMなど好みのモデルを接続可能。  
- デプロイ：単一サーバー向けにDocker Compose、プロダクション向けにTerraform（AWS/GCP）を用意。  
- 権限継承：接続先システムの権限を尊重し、ユーザーは元の許可範囲内のデータのみ閲覧可能。

## 日本市場との関連性
- 機密情報や個人情報の保護が重要な金融・製造・医療分野での導入メリットが大きい。  
- Slack/Google Workspace/Confluence/Jiraは日本でも広く使われており、既存環境への導入障壁が低い。  
- 自社LLM導入や国内クラウド（オンプレ含む）での運用を希望する企業に適合。

## 実践ポイント
- まずはリポジトリをクローンしてDocker Composeでローカル検証→Postgresバックアップ/リストア手順を確認。  
- 既存のGoogle Workspace/Slack API権限を準備し、コネクタ単位で接続テスト。  
- LLMはまずOpenAI等で試し、将来的にオンプレモデルへ切替える計画を立てる。  
- エージェントのコード実行機能は慎重に評価し、サンドボックス設定（ネットワーク/FS/CPU/メモリ制限）を強化する。  
- 運用面ではPostgresのインデックス（pgvector/BM25）とバックアップ・監視を重点的に設計する。

元リポジトリ（README）を参照して、まずは小規模環境で動かしてみることを推奨します。
