---
layout: post
title: "Benchmark: pgvector vs Pinecone vs Qdrant vs Weaviate - ベクトルデータベース性能比較"
date: 2026-04-08T18:10:50.976Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://vecstore.app/blog/vector-database-performance-compared"
source_title: "Vector Database Performance Compared: pgvector vs Pinecone vs Qdrant vs Weaviate - Vecstore"
source_id: 366839231
excerpt: "pgvector+Neonは1M規模で専用DB並の高速・低コスト、50M超は設計見直し必須"
image: "https://vecstore.app/og-default.png"
---

# Benchmark: pgvector vs Pinecone vs Qdrant vs Weaviate - ベクトルデータベース性能比較
Postgres一本で行ける？実運用で役立つ「速度・精度・コスト」比較ガイド

## 要約
1Mベクトル規模の実測では、pgvector（HNSW）が専用DBに匹敵する速度と高リコールを出し、NeonなどのサーバレスPostgresと組むとコスト・運用面で非常に有利になる。だが10M〜50Mを超えるとインデックスのメモリ要件で設計見直しが必要。

## この記事を読むべき理由
ベクトル検索をプロダクトに組み込む際、速度・精度・運用コストのトレードオフが最重要。日本のスタートアップやEC、SaaSで「既存のPostgresを活かすべきか」「専用ベクトルDBに移すべきか」を判断する材料になります。

## 詳細解説
- 比較対象
  - pgvector：Postgres拡張。別サービス不要でアプリDBと共存可能。HNSWサポートで性能が大幅改善。
  - Pinecone：マネージド（サーバレス/ポッド）。運用は楽だがチューニング自由度とコストに制約。
  - Qdrant：Rust製、自己ホスト可。フィルタ付き検索が得意。
  - Weaviate：ハイブリッド検索（キーワード＋ベクトル）をネイティブで提供。
  - Milvus：億単位スケール向けの人気OSS。
- レイテンシ（1M vectors, 1536d、概数 p50 / p95）
  - pgvector (HNSW): ~5ms / ~12ms
  - Qdrant: ~3ms / ~8ms
  - Weaviate: ~8ms / ~22ms
  - Pinecone (Serverless): ~12ms / ~48ms
  - Milvus: ~4ms / ~11ms
- リコール（精度、「精度優先」設定）
  - pgvector: ~98.5%（ef_search調整可）
  - Qdrant: ~99.2%
  - Weaviate: ~97.8%
  - Pinecone: ~95%（チューニング不可）
  - Milvus: ~99.0%
- コスト感（1M vectors, 1024d、概算/月）
  - pgvector on RDS: 約 $260
  - pgvector on Neon: 約 $30–150（サーバレスでバーストに強い）
  - Pinecone Serverless: 約 $50–80
  - Qdrant Cloud: 約 $65–102
  - Weaviate Cloud: 約 $45（最低プラン）
- スケーリングのポイント
  - HNSWはインデックスをメモリに載せる前提。数十Mでメモリ要件が急増（例：50M×768dで数百GB）。
  - pgvectorscale / StreamingDiskANN のようなディスクベース手法で大規模でも競争力が出る（Timescaleのベンチ：50MでPinecone比で大きな優位）。
- 実運用の知見（Vecstoreの経験）
  - Neon移行でレイテンシが200ms→80msに改善。検索自体はDB側で5–8ms、全体ボトルネックは埋め込み生成など別工程。

## 実践ポイント
- 小〜中規模（〜10M）：既にPostgresを使っているならpgvector + Neonがコスパと運用性で優先候補。
- フィルタ検索が重要：Qdrantが強み。自己ホストで最速の選択肢になることが多い。
- 運用ゼロが最重要：プロトタイプや運用リソースが無いならPinecone（ただしチューニング制約を理解）。
- 数十〜数百M〜億規模：Milvusやディスクベースのソリューション（pgvectorscale等）を検討。
- 何より重要：ベクトルDB選定に時間をかけすぎず、埋め込み品質・検索UXに注力すること（5msと15msの差はユーザにほぼ無関係）。

この記事を読んで、自分のサービスの「想定ベクトル数」「運用工数」「フィルタ要件」を整理すれば、適切な選択ができます。
