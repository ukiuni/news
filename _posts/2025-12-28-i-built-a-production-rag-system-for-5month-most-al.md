---
layout: post
title: I Built a Production RAG System for $5/month (Most Alternatives Cost $100-200+)
date: 2025-12-28 04:17:09.687000+00:00
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: https://dev.to/dannwaneri/i-built-a-production-rag-system-for-5month-most-alternatives-cost-100-200-21hj
source_title: I Built a Production RAG System for $5/month (Most Alternatives Cost
  $100-200+) - DEV Community
source_id: 3122739
excerpt: Cloudflareエッジで埋め込み・検索を完結させ、RAGを月約$5で実運用する手法
---
# 月5ドルで実運用できるRAGを作った話 — 月100〜200ドルの常識を覆すエッジ設計

## 要約
Cloudflare Workers上で埋め込み生成＋ベクトル検索をエッジ側で完結させ、従来のRAG構成の月額$100–200を$5–10に抑えた実運用アーキテクチャの紹介。

## この記事を読むべき理由
日本のスタートアップやプロダクト開発で「AI検索を入れたいが費用がネック」という課題は共通です。低コストかつ低レイテンシでグローバル配信できる手法は、PoC〜本番導入までのハードルを劇的に下げます。

## 詳細解説
問題点（従来構成）
- 一般的なRAG: ユーザー → アプリサーバ → Embeddings API → ベクトルDB → ユーザー。各サービスの費用と往復遅延が積み上がる。  
- 例: Pineconeの最低プラン、OpenAI埋め込み費、EC2サーバ、監視で合計$130–190/月に到達するケース。

著者の発想
- すべてを「エッジ」に共置：ユーザー → Cloudflare Edge（埋め込み生成 + 検索 + 応答）→ ユーザー。往復を削減し、アイドルサーバを廃止してコストを削る。

技術スタックと要点
- Cloudflare Workers（TypeScript）上で動作。Workers AIで埋め込みを生成し、Cloudflare Vectorize（HNSW）で検索を実行。
- モデル: bge-small-en-v1.5（384次元）など軽量モデルを利用してオンエッジでの埋め込み生成を実現。
- メリット: 低遅延（世界300+都市のエッジ）、低コスト、シンプルな運用（単一のWorkerで認証・整形・検索を完結）。
- 制約: 大規模コレクションや高度なカスタムランキングには限界があり、モデルの表現力は大型APIモデルに劣る可能性がある。ベクトルDBやWorkersのストレージ/スループット制限、ベンダーロックインも考慮が必要。

簡易的な検索エンドポイント（イメージ）
```typescript
// typescript
async function searchIndex(query: string, topK: number, env: Env) {
  // 埋め込み生成（エッジで実行）
  const embedding = await env.AI.run("@cf/baai/bge-small-en-v1.5", { text: query });
  // ベクトル検索（Vectorize）
  const results = await env.VECTORIZE.query(embedding, { topK, returnVectors: false });
  // 結果整形
  return results.map(r => ({ id: r.id, score: r.score, snippet: r.metadata?.text }));
}
```

## 実践ポイント
- まずは小さめデータセットでPoCを作る（コスト効果と品質を確認）。  
- ドキュメントは適切にチャンク化して埋め込みを作る（文脈ウィンドウの最適化）。  
- topKやスコア閾値をチューニングして検索品質を確保。  
- セキュリティ／データ保護とリージョン要件（特に機密データ）を事前確認。日本の企業ではログや外部送信ポリシーに注意。  
- ハイブリッド運用も検討：小〜中規模はエッジ、大規模コレクションは専用ベクトルDB、といった構成でコストと性能を最適化。  
- Cloudflareの料金やVectorizeの制限を確認し、将来スケール時のコスト試算を行う。

