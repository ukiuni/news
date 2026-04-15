---
layout: post
title: "Understanding Clojure's Persistent Vectors, pt. 1 - Clojureの永続ベクター入門（前編）"
date: 2026-04-15T03:38:32.693Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://hypirion.com/musings/understanding-persistent-vector-pt-1"
source_title: "Understanding Clojure's Persistent Vectors, pt. 1"
source_id: 47721076
excerpt: "32分岐の浅い木とパスコピーでClojure永続ベクターがほぼO(1)で高速動作する仕組み"
---

# Understanding Clojure's Persistent Vectors, pt. 1 - Clojureの永続ベクター入門（前編）
魅力的なタイトル: 浅い木で高速化する秘密 — Clojure永続ベクターが「ほぼO(1)」で動く仕組み

## 要約
ClojureのPersistent Vectorは「パスコピー」と高い分岐数（ブランチングファクタ）で、更新・末尾追加・削除をほぼ定数時間で実現する不変データ構造です。

## この記事を読むべき理由
不変データ構造は並行処理やバグ低減に強く、JVM上のサービスやフロントエンド的な状態管理でも有用。設計の肝を理解すれば、実運用での選択や最適化（transientやtail）判断に役立ちます。

## 詳細解説
- 基本アイデア  
  ベクターを浅い多分岐木で表現し、葉に要素を並べる。更新や挿入は「パスコピー」で根から対象葉までのノードだけを複製して新しい木を作るため、他のバージョンと内部構造を共有できる。

- 更新（assoc）  
  指定インデックスへは木を下りつつその経路のノードをコピーし、葉で値を差し替えて新しいベクターを返す。変更は局所的なのでコストは木の深さに依存。

- 末尾追加（conj）の3ケース  
  1) 右端の葉に空きがある：assocと同様にパスコピーして差し込む。  
  2) 目的の子ポインタがnull：不足ノードを生成してリンクする（部分的に新ノードを作る）。  
  3) ルートが満杯（ルートオーバーフロー）：新しいルートを作り旧ルートをその子にしてツリーを深くする。n分岐ならサイズが$n^k$の境目でオーバーフローする。

- ポップ（pop）の3ケース  
  1) 右端葉に複数要素：パスコピーして末尾を削除。  
  2) 葉が空になる：空ノードはnullにして親へ伝播させる（ノード削除が上方向へ波及）。  
  3) ルートが単一子になる：ルートをその子で置き換えて木を浅くする。

- なぜ「ほぼO(1)」か  
  理論上は$O(\log n)$だが、Clojureは1ノードあたりの分岐数を32にしているため木の深さは非常に浅い。例えば10億要素未満なら深さは最大6程度で、実用上定数時間に近い振る舞いをします（$O(\log_{32} n)$）。

$$\text{depth} \approx \lceil \log_{32} n \rceil$$

簡単なClojure例:
```clojure
(def v [0 1 2 3 4])
(def v2 (conj v 5))      ; 末尾追加（部分的に共有）
(def v3 (assoc v 2 :x))  ; インデックス2を置換（パスコピー）
(def v4 (pop v))         ; 末尾削除（必要ならノード削除／ルート調整）
```

## 実践ポイント
- 小・中規模の不変コレクション管理ならClojureベクターは高速で安全。並行処理やイベント駆動系に向く。  
- ホットループで大量追加する場合はtransientを使って一時的に可変にしてから永続化する（パフォーマンス改善）。  
- 大量データでの深さ・メモリ特性を想定し、必要ならtail最適化や部分共有の理解を深める。  
- JVMエコシステム（マイクロサービス、データ処理）で不変構造を採用する判断材料に：共有コストとコピー範囲が限定される点を評価する。

元記事：Jean Niklas L'orange「Understanding Clojure's Persistent Vectors, pt. 1」
