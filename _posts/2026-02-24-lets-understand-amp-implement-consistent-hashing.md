---
layout: post
title: "Let's understand & implement consistent hashing. - 一貫性ハッシュを理解して実装しよう"
date: 2026-02-24T07:13:09.301Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://sushantdhiman.dev/lets-implement-consistent-hashing/"
source_title: "Let&#x27;s Implement Consistent Hashing From Scratch in Golang"
source_id: 399130212
excerpt: "ノード増減での大規模データ移動を防ぐ一貫性ハッシュの概念とGo実装を実践的に解説"
image: "https://sushantdhiman.dev/content/images/2026/02/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2fa77e92d8-0806-4e86-ad27-cfd4f5ff0557_2215x1805-jpeg.jpg"
---

# Let's understand & implement consistent hashing. - 一貫性ハッシュを理解して実装しよう
クリックせずにはいられないタイトル: 小さな変更で大混乱を防ぐ――分散システムの“鍵”を握る一貫性ハッシュ入門

## 要約
一貫性ハッシュは、ノードの増減によるデータ再配置を最小化するキー分配手法で、キャッシュやシャーディングで高い可用性とスケーラビリティを実現します。本稿では概念と、Goでのシンプルな実装例をわかりやすく解説します。

## この記事を読むべき理由
- 日本のクラウド／マイクロサービス運用でも、ノードのスケールや故障は頻発するため、再配置コストを下げる技術は即戦力になる。  
- Redisクラスタや分散キャッシュ、データベースシャード設計を検討しているエンジニアにとって基本かつ実践的な知識だから。

## 詳細解説
- 基本概念：ノード（サーバ）とキーを同じハッシュ空間（円環）にマッピングし、キーはその位置から時計回りで最初に出会うノードに割り当てる。これによりノード追加・削除時に影響を受けるキーは局所化される。  
- ハッシュ関数：均等な分布と速度を両立するために Murmur3 のような非暗号学的ハッシュがよく使われる（実装例では murmur3.Sum32）。  
- 実装要点：
  - 円環を表すのは「ソート済みハッシュ配列 + ハッシュ→ノードのマップ」。  
  - ノード追加はノードIDをハッシュ化して配列に挿入、ソート。  
  - キー割当はキーのハッシュ値に対して、配列内でより大きい最初の要素を探す（二分探索でも可）。見つからなければ先頭にラップアラウンド。  
  - ノード削除時は、そのノードの持つキーを次のノードに移す（最小限の移動で済む）。  
- 注意点（現場で役立つ改善案）：
  - 仮想ノード（virtual nodes）で分散を滑らかにする：物理ノードごとに複数のハッシュポイントを作る。  
  - 同期・並行処理：読み書きロックや原子操作で競合を防ぐ。  
  - モニタリング：ノードごとのキー数分布を監視し、不均衡が続く場合は仮想ノード数やハッシュ選定を調整する。

サンプル（抜粋・簡略化したGo実装）:

```go
package main

import (
	"errors"
	"fmt"
	"sort"
	"sync"

	"github.com/spaolacci/murmur3"
)

type Node struct {
	ID   string
	Keys map[string]string
}

type ConsistentHashRing struct {
	mu     sync.RWMutex
	nodes  map[uint32]*Node
	hashes []uint32
}

func NewConsistentHashRing() *ConsistentHashRing {
	return &ConsistentHashRing{nodes: make(map[uint32]*Node)}
}

func hashFunction(key string) uint32 {
	return murmur3.Sum32([]byte(key))
}

func (chr *ConsistentHashRing) AddNode(id string) {
	chr.mu.Lock()
	defer chr.mu.Unlock()
	h := hashFunction(id)
	chr.nodes[h] = &Node{ID: id, Keys: make(map[string]string)}
	chr.hashes = append(chr.hashes, h)
	sort.Slice(chr.hashes, func(i, j int) bool { return chr.hashes[i] < chr.hashes[j] })
}

func (chr *ConsistentHashRing) getNextNodeIndex(h uint32) int {
	// linear scan shown; replace with binary search for large rings
	for i, hh := range chr.hashes {
		if hh > h {
			return i
		}
	}
	return 0
}

func (chr *ConsistentHashRing) GetNode(key string) *Node {
	chr.mu.RLock()
	defer chr.mu.RUnlock()
	if len(chr.hashes) == 0 {
		return nil
	}
	h := hashFunction(key)
	idx := chr.getNextNodeIndex(h)
	return chr.nodes[chr.hashes[idx]]
}

func (chr *ConsistentHashRing) StoreKey(key, val string) {
	if n := chr.GetNode(key); n != nil {
		n.Keys[key] = val
	}
}

func (chr *ConsistentHashRing) RetrieveKey(key string) (string, error) {
	if n := chr.GetNode(key); n != nil {
		if v, ok := n.Keys[key]; ok {
			return v, nil
		}
		return "", errors.New("key not found")
	}
	return "", errors.New("no node")
}
```

## 実践ポイント
- まずは小さなテストクラスターで実装して、ノード増減時のキー移動率を計測する。  
- 実運用では仮想ノードを導入してノード間の偏りを解消する。  
- ハッシュ関数は用途に応じて選ぶ（速度重視なら Murmur3、セキュリティを要する場合は別途検討）。  
- RedisやMemcachedを採用する際は、プロダクション構成（クラスタ/サイドカー）と一貫性ハッシュの設計を合わせて検討する。

以上を押さえれば、一貫性ハッシュはキャッシュの耐障害性やスケーラビリティ改善にすぐ役立ちます。
