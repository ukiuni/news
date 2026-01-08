---
  layout: post
  title: "Implementing HNSW (Hierarchical Navigable Small World) Vector Search in PHP - PHPで実装するHNSW（階層型ナビゲーブル・スモールワールド）ベクトル検索"
  date: 2026-01-01T16:58:54.652Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://centamori.com/index.php?slug=hierarchical-navigable-small-world-hnsw-php&lang=en"
  source_title: "Implementing HNSW (Hierarchical Navigable Small World) Vector Search in PHP"
  source_id: 46454968
  excerpt: "PHPで10万〜百万件をミリ秒で検索するHNSW実装ガイド（具体例付き）"
---

# Implementing HNSW (Hierarchical Navigable Small World) Vector Search in PHP - PHPで実装するHNSW（階層型ナビゲーブル・スモールワールド）ベクトル検索
PHPでミリ秒レベルの近傍探索を実現する――10万〜百万件規模のベクトルから“針”を素早く見つける技術ガイド

## 要約
HNSWは、データを「高速道路→幹線→路地」という階層的グラフに配置し、全探索の$O(N)$を大幅に削減して事実上亜線形な探索を実現するアルゴリズム。この記事はPHPでの実装方針と重要パラメータ（$M, ef$）、探索・挿入アルゴリズムの要点を解説する。

## この記事を読むべき理由
- 日本の多くのWebサービスや社内システムで根強いPHP環境でも、最新のベクトル検索（RAGや推薦）を自前で組み込める。
- 数十万〜百万規模のコーパスを低遅延で検索したい場合、HNSWは現実的かつ実装可能な選択肢になる。

## 詳細解説
- 基本概念  
  HNSWはノード（ベクトル）を複数のレイヤに配置する。上位レイヤほどノード数が少なく、長距離接続（“高速道路”）を担う。探索は最上位の近傍から始めて徐々に下位レイヤへ「ズームイン」していく。これにより探索回数は理論的に$O(\log N)$に近づく。

- 探索の流れ（サマリ）  
  1. ヘッダのエントリポイントから開始。  
  2. 各レイヤで貪欲に近いノードへ移動し、もはや改善できない地点まで進む。  
  3. レイヤ1まで下り、最後にレイヤ0（全ノードが存在）で$ef$サイズの候補リストを使って精密探索を行う。  
  レイヤ0の探索は優先度付きキュー（SplPriorityQueue等）を用い、有望なノードから展開していく。候補リストのサイズを$ef$と呼び、$ef$を大きくすると精度が上がるが遅くなる。

- 重要パラメータ  
  - $M$: 1ノードあたりの最大接続数。大きいほどグラフが密になり検索精度は向上するがメモリと構築時間が増える（典型値は8〜32）。  
  - $ef$: 検索時の候補キューサイズ（探索幅）。精度と速度のトレードオフを制御。構築時に使う$efConstruction$も別に存在する。  
  - 距離指標: コサイン類似度や内積が一般的（元記事はCosine Similarityを使用）。

- 挿入（インデックス構築）  
  新しい点の最大レベルは確率的に決める（指数分布に相当）。挿入時は既存のグラフを辿って近傍を見つけ、$M$以内に収まるよう接続を調整する。接続が溢れた場合は類似度の低い辺を切る。

- なぜ速いか  
  上位レイヤで候補領域を素早く絞り、下位で局所的に精密探索するため、総比較回数が大幅に減る。百万点で数千比較→ミリ秒応答が現実的。

- 実装上の注意（PHP向け）  
  - SplPriorityQueueや配列の扱い方で実行速度が変わる。ベクトルは浮動小数点配列を効率的に保持する（Packed arraysやC拡張の検討も）  
  - 永続化（ノード構造・接続）はメモリ、ファイル、DBいずれかの設計に依存。大量データならバイナリファイルや専用DBを検討。  
  - 並列・非同期でのバッチ挿入や再構築戦略を用意する。

- 実装例（探索の核となる降下ループ、PHP風）  
```php
<?php
// PHP
$entryPoint = $this->readHeader();
$currObj = $entryPoint;
$currDist = Math::cosineSimilarity($queryVector, $this->getVector($currObj));

for ($lc = $maxLevel; $lc >= 1; $lc--) {
    while (true) {
        $changed = false;
        $node = $this->readNode($currObj);
        $neighbors = $node['connections'][$lc] ?? [];
        foreach ($neighbors as $nid) {
            $dist = Math::cosineSimilarity($queryVector, $this->getVector($nid));
            if ($dist > $currDist) {
                $currDist = $dist;
                $currObj = $nid;
                $changed = true;
            }
        }
        if (!$changed) break;
    }
}
// ここからレイヤ0の$efを使った精密探索へ
```

## 実践ポイント
- まずは小さなコーパスでチューニング：$M=8$、$ef=100$程度から始め、精度と速度をベンチマークする。  
- PHPネイティブでの実装が重い場合は、Vektorのような既存実装や外部サービス（Qdrant/Pinecone）との併用を検討。  
- 挿入は逐次実行よりバッチ化が有利。リアルタイム挿入が必要ならメモリ設計を厳密に。  
- 距離計算（コサイン等）はホットスポットになるため最適化（SIMD、拡張モジュール、事前正規化）を検討。  
- メトリクス：検索遅延、召喚率（recall）とスループットを常にモニタリングする。

