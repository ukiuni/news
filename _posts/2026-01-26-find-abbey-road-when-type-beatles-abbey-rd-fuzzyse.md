---
layout: post
title: "Find 'Abbey Road when type 'Beatles abbey rd': Fuzzy/Semantic search in Postgres - 「beatles abbey rd」で『Abbey Road』を見つける：Postgresで作るファジー＆意味検索"
date: 2026-01-26T19:23:08.802Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://rendiment.io/postgresql/2026/01/21/pgtrgm-pgvector-music.html"
source_title: "Finding ‘Abbey Road’ When Users Type ‘beatles abbey rd’ - Fuzzy and Semantic Search in PostgreSQL | Rendiment"
source_id: 46709461
excerpt: "Postgresでpg_trgmとpgvector併用し誤字に強い音楽検索を実装"
image: "https://rendiment.io/assets/img/gallery/record-store-small.jpg"
---

# Find 'Abbey Road when type 'Beatles abbey rd': Fuzzy/Semantic search in Postgres - 「beatles abbey rd」で『Abbey Road』を見つける：Postgresで作るファジー＆意味検索
「beatles abbey rd」と入力しても本当に狙ったアルバムが返ってくる検索を、PostgreSQLだけで実装する実践ガイド

## 要約
pg_trgm（トライグラムによるファジー一致）と pgvector（埋め込みベクトルによる意味検索）を組み合わせ、ノイズだらけのユーザー入力を高精度にマッチさせる手法を具体例（Spotifyデータセット）で示す。

## この記事を読むべき理由
検索はユーザー体験の要。日本語を含む実運用でも誤字・省略・言い換えに強い設計が必須。Postgresのみで高速・実用的に実現する方法が学べる。

## 詳細解説
- 問題点：データは整っていても、入力は「abbey rd」「dark side moon」「beatles final album」などバラバラ。単純な = では全滅。
- 2つのアプローチ：
  - pg_trgm（トライグラム）  
    - 文字列を3文字ごとのシーケンスに分割して重なりを測る。typo・省略・語順違いに強い。  
    - インデックス：GIN + gin_trgm_ops。検索では similarity() やインデックスを使う場合は % 演算子。  
    - 例（SQL）:

```sql
-- GIN index for trigram
CREATE INDEX idx_album_name_trgm ON album_catalog USING gin (album_normalized gin_trgm_ops);

-- similarity query (index-friendly)
SET pg_trgm.similarity_threshold = 0.3;
SELECT album_name, artists, similarity('abbey rd', album_normalized) AS score
FROM album_catalog
WHERE album_normalized % 'abbey rd'
ORDER BY score DESC
LIMIT 5;
```

  - pgvector（埋め込みベクトル）  
    - 文章の意味を数値ベクトルに変換（sentence-transformers 等）。単語が一致しなくても概念的に近ければ高スコア。  
    - インデックス：IVFFlat（vector_cosine_ops）、lists はクラスタ数（例：sqrt(rows) や rows/1000）。類似度は cosine を距離に変換して扱う（Postgres の <=> 演算子）。  
    - 概要のコード（Python）:

```python
# Python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-mpnet-base-v2')  # 英語向け例
emb = model.encode("Beatles final studio album").tolist()
# UPDATE album_catalog SET album_embedding = %s WHERE id = %s
```

- 正規化（Normalization）が鍵：カタログとクエリ両方を同じルールで正規化（小文字化、RemasterやDeluxe表記の除去、略語展開、句読点除去、余分な語の削除）することでpg_trgmの精度が大幅に向上。サンプルの正規化関数は英語向けだが、考え方は共通。
- ハイブリッド戦略：まず高速なpg_trgmで候補を取る（閾値で判定）、不確かな場合は埋め込み検索でフォールバック。これが実運用での良好なトレードオフ。

## 日本市場との関連
- 日本語は空白で単語が区切れないため、pg_trgmのトライグラムは一定の効果があるが、語彙分割（形態素解析：MeCab/Sudachi）やNFKC正規化、カタカナ・全角半角の統一などを組み合わせると精度向上。  
- 埋め込みは日本語対応モデル（multilingual や日本語専用 sentence-transformers）を選ぶと意味検索が有効に働く。業務システムで社内固有語が多い場合は専用データで微調整（fine-tune）を検討。

## 実践ポイント
1. データ準備：カタログに album_normalized（正規化文字列）と album_embedding（vector）を用意する。  
2. 正規化ルールを明確に：記号、表記揺れ、略語、リマスター表記の除去を必須化。日本語は形態素解析＋正規化。  
3. インデックス：
   - pg_trgm: GIN + gin_trgm_ops
   - pgvector: IVFFlat + vector_cosine_ops（lists はテーブルサイズに応じて調整）  
4. 閾値設計：pg_trgm の similarity_threshold を実データでチューニング（記事は 0.3 を目安）。埋め込みは cosine ベースで 0.6 前後を出発点に。  
5. ハイブリッド実装：まず pg_trgm（高速）→ スコア低ければ pgvector（精度重視）でフォールバック。  
6. 日本語対応：形態素解析器でトークン化、マルチリンガル/日本語対応の埋め込みモデルを選ぶ。  
7. コスト管理：埋め込み生成は高コスト（時間・計算）。バッチで事前生成してDBに保存する。

この手順で、ユーザーが「beatles abbey rd」「ビートルズ アビー ロード」「ビートルズ最後のアルバム」といったバラバラな入力を投げても、高確率で期待するアルバムを返せる検索がPostgres上で実現できる。
