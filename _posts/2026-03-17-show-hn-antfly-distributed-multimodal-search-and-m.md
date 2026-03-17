---
layout: post
title: "Show HN: Antfly: Distributed, Multimodal Search and Memory and Graphs in Go - Antfly：分散・マルチモーダル検索＋メモリ＋グラフ（Go製）"
date: 2026-03-17T16:54:10.114Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/antflydb/antfly"
source_title: "GitHub - antflydb/antfly · GitHub"
source_id: 47414291
excerpt: "Go製分散検索Antfly：BM25/ベクトル/画像音声対応でRAGとグラフ検索を統合"
image: "https://opengraph.githubassets.com/1d4c24a282094d6e60a6b83d75d4ac22aa1a481c73a0c984ca795c3a1fca99eb/antflydb/antfly"
---

# Show HN: Antfly: Distributed, Multimodal Search and Memory and Graphs in Go - Antfly：分散・マルチモーダル検索＋メモリ＋グラフ（Go製）
魅力的タイトル: いま注目のオープンソース「Antfly」で作る、高速・マルチモーダルな社内検索基盤

## 要約
AntflyはGo製の分散検索エンジンで、BM25やベクトル検索、グラフ探索、画像/音声/動画のマルチモーダル対応を一つのクエリで組み合わせられるプラットフォームです。組み込みのML推論（Termite）とRAGエージェントで検索→生成のフローを手軽に構築できます。

## この記事を読むべき理由
日本の企業でも「データが増えて検索が遅く、社内ナレッジやマルチメディアを横断的に検索したい」ニーズが増えています。Antflyはオンプレ／S3ストレージ対応やローカルモデル接続、Postgres拡張など実運用寄りの機能を備え、プライバシーやデータ滞在要件が厳しい日本市場で検討価値が高いです。

## 詳細解説
- アーキテクチャ：etcdのRaftを使ったマルチ・RAFT設計（メタデータ用RaftとシャードごとのストレージRaft）で、シャード分割・レプリケーション・ACID相当のシャード単位トランザクションを実現。障害試験はJepsen風の混乱注入テストとTLA+による仕様検証を行い堅牢性に配慮しています。  
- 検索機能：ハイブリッド検索を標準搭載（BM25＝全文検索、密ベクトル、Sparseベクトル(SPLADE) を同一クエリで融合）。リランキング用のクロスエンコーダとスコアベースのプルーニングで精度向上。  
- マルチモーダルとML推論：CLIP/CLAP系のモデルで画像・音声・動画もインデックス化。Termiteというサブモジュールが埋め込み・チャンク化・NER/OCR/転写・生成などを担い、スウォームモードで自動起動できます。  
- RAGとエージェント：検索結果を踏まえたRetrieval‑Augmented Generation（ストリーミング・マルチターン・ツール呼び出し対応）や、グラフ走査をツールとして使うエージェントが組み込まれています。  
- 実運用機能：ドキュメントTTL、自動シャード分割、S3/MinIO/R2対応、SIMD最適化（go-highwayでx86/ARM加速）、Kubernetesオペレータ、バックアップ／復元機能。  
- 開発者向け：Go/TypeScript/PythonのSDK、Reactコンポーネント、Postgres拡張(pgaf)で既存アプリやDBに簡単に組み込めます。  
- ライセンス：コアはElastic License 2.0（自己ホストや製品組込みは可だが「Antfly自体をマネージドサービスとして提供」は不可）。周辺コンポーネントはApache‑2.0。

クイックスタート例（ローカル1ノード）:
```go
go run ./cmd/antfly swarm
```
Dockerでの起動例:
```bash
docker run -p 8080:8080 ghcr.io/antflydb/antfly:omni
```
起動後、Antfarmダッシュボードが http://localhost:8080 に表示されます。

## 実践ポイント
- まずDockerで試し、Antfarmのプレイグラウンド（検索・RAG・グラフ）を触る。  
- 日本語コーパスではトークナイザーや埋め込みモデルの日本語対応を確認（ローカルモデルやOpenAI/Bedrock接続で比較）。  
- 既存DB連携ならpgafでPostgresに組み込み、段階的に検索を置き換える。  
- 運用ではS3保存・TTL・シャード設定を活用してコストと性能を調整。  
- ライセンス（ELv2）に注意し、自社でホスティングする前提で評価する。  
- ドキュメントとDiscordでコミュニティを参照：antfly.io/docs

参考：リポジトリ（README） https://github.com/antflydb/antfly

---
