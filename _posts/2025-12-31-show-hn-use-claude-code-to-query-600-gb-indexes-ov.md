---
layout: post
title: "Show HN: Use Claude Code to Query 600 GB Indexes over Hacker News, ArXiv, etc. - Claude Codeで600GBの索引をクエリする"
date: 2025-12-31T09:37:33.177Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://exopriors.com/scry"
source_title: "Show HN: Use Claude Code to Query 600 GB Indexes over Hacker News, ArXiv, etc."
source_id: 46442245
excerpt: "Claude Codeで600GB超、6000万文書をSQLと埋め込みで対話的に高速探索"
---

# Show HN: Use Claude Code to Query 600 GB Indexes over Hacker News, ArXiv, etc. - Claude Codeで600GBの索引をクエリする
AIにSQLとベクトル代数を与えて「知の索引」を自在に探索する――研究・議論コーパスを対話的に掘るためのAlignment Scry

## 要約
ExoPriorsの「Alignment Scry」は、arXiv/Hacker News/ LessWrong 等を含む約60Mドキュメント・22M埋め込み・600GB超の索引に対して、SQL＋ベクトル演算で検索・分析できる実験的プラットフォーム。Claude（Code/Web）から直接APIを叩いて、語彙検索＋意味検索を組み合わせた高精度探索が可能になる。

## この記事を読むべき理由
- AI安全や先端研究の文献・議論を短時間で横断検索できるツールは、日本の研究者・プロダクト開発者・政策担当者にとって情報収集の効率化に直結する。  
- 単なる全文検索では拾えない意味的類似や時系列変化の分析が、ベクトル演算とSQLで手軽にできる点が実務的に有用。

## 詳細解説
- データ規模と中身  
  - 約60Mドキュメント、22Mのベクトル埋め込み、600GB超の索引。ソースは arXiv、Hacker News、LessWrong、community-archive 等。  
- インターフェースと主な機能  
  - SQLライクなAPI：自由にSELECT/ JOIN / AGGREGATEが使える。  
  - ベクトル操作：サーバ側に保存した概念埋め込みを参照して類似度ソート。pgvectorの距離演算子（例: <=>）を利用。  
  - ハイブリッド検索：BM25（lexical）で候補を取り、埋め込みで再ランクするパターンを推奨。  
- ベクトル代数（概念的に）  
  - セントロイド（平均）で作者やトピックの「代表ベクトル」を作れる：  
    $$\mathrm{centroid}=\frac{1}{N}\sum_{i=1}^{N}v_i$$  
  - 概念ミキシング例（重み付け・減算で味付け）：  
    $v = 0.6\cdot v_{\text{rigor}} - 0.3\cdot v_{\text{hype}}$  
  - 類似度はコサイン距離等で評価（小さいほど類似）。  
- 実行環境と統合  
  - Claude Code／Claude Web から直接APIを叩けるプロンプトが用意されており、手元でSQLを投げるように探索できる。Web側は「コード実行」「ネットワーク出力」を許可する設定が必要。  
- 検索APIの実践テクニック  
  - `alignment.search()` はBM25の上位100行が標準。完全性が必要なら `alignment.search_exhaustive()` をページングで使う。  
  - 大規模集計はタイムアウトしやすい：まず小さな候補セット（LIMIT 10–200）を作ってからJOIN/集計する。  
  - 速さが欲しければマテリアライズドビュー（例: `mv_hackernews_posts`, `mv_arxiv_papers`）を使う。  
- セキュリティと注意点  
  - 公開デモ用の読み取り鍵が埋め込まれているが、プロンプトインジェクション等のリスクは残る。Claudeに広い権限を与える際は注意して運用する。

簡単な実行例（curlでSQLを投げる例、実際のキーは環境に合わせて差し替えてください）:

```bash
bash
curl -X POST https://api.exopriors.com/v1/alignment/query \
  -H "Authorization: Bearer EXOPRIORS_PUBLIC_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sql":"SELECT * FROM alignment.search(\'mesa optimization\') LIMIT 10"}'
```

SQLで埋め込みを使った類似検索（概念）:

```sql
sql
WITH seed AS (
  SELECT embedding FROM alignment.embeddings WHERE uri LIKE '%risks-from-learned-optimization%'
)
SELECT e.uri, e.embedding <=> seed.embedding AS dist
FROM alignment.embeddings e, seed
WHERE e.created_at > '2023-01-01'
ORDER BY dist
LIMIT 25;
```

## 実践ポイント
- まずは無料コンソールで試す：小さいLIMITで探索し、スキーマやBM25の挙動を確認。  
- ハイブリッド運用：キーワードで候補を絞ってから埋め込みで精査する（lexical→semantic）。  
- 概念ハンドルを作成して辞書化：よく使う概念はサーバ側に名前付き埋め込みを保存して再利用する。  
- 日本語での活用：英語圏の議論が主体だが、日本の研究動向を追う際はarXivやHNの英語議論を横断検索し、要点抽出に使うと効率的。自前で日本語コーパスを埋め込み追加すれば日本語対応の強化が可能。  
- 大量検索は分割して実行：complete結果が必要なら `search_exhaustive()` をページングで回す設計にする。  
- セキュリティ：Claudeにネットワーク権を与える際は、プロンプトインジェクションやAPI権限の扱いを明確に。

