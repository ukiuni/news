---
layout: post
title: "Index, Count, Offset, Size - インデックス、カウント、オフセット、サイズ"
date: 2026-02-21T15:22:24.162Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://tigerbeetle.com/blog/2026-02-16-index-count-offset-size/"
source_title: "Index, Count, Offset, Size"
source_id: 400090873
excerpt: "命名規則でオフバイワンを即検出、バイトと要素を明確化して致命的バグを激減させる方法"
image: "https://tigerbeetle.com/blog/2026-02-16-index-count-offset-size/banner.webp"
---

# Index, Count, Offset, Size - インデックス、カウント、オフセット、サイズ
配列バグを一瞬で見抜く「命名法」の習慣 — 小さなルールでオフバイワン地獄を減らす

## 要約
TigerBeetle の提案は非常にシンプル：要素数は always "count"、要素を指すのは "index"、バイト単位は "size"、バイト位置は "offset" と命名し、$index < count$ の不変条件を守ることでインデックス系バグを目に見えるようにする、というものです。

## この記事を読むべき理由
配列・バッファ操作は初級者から熟練者まで頻繁にミスする領域です。命名の一貫性だけでオフバイワンや単位取り違えによる致命的バグを早期発見でき、特に低レイヤの金融系や組込み・OS周りで有効です。日本のプロダクトでもメンテ性向上とバグ削減に直結します。

## 詳細解説
- 基本ルール
  - "count" = 要素の数（配列の長さ = 要素単位）
  - "index" = 特定の要素を指す整数。常に $index < count$ を満たす。
  - "size" = バイト単位の大きさ。定義上 $$size = \mathrm{sizeof}(T)\times count$$
  - "offset" = バイト単位での位置（index のバイト版）
- 意図
  - 命名に _index / _count / _size / _offset を必ず付けることで、異なる単位（要素 vs バイト）や役割を混同しにくくする。
  - 例えば source, source_words, source_index のようにサフィックスで揃える（「big endian naming」）と、対応箇所が視覚的に揃いミスが見つけやすくなる。
- 実装上の補助
  - 型・assert・境界チェックで命名と合わせて防御層を作る（例：assert で $index < count$、byte-length の一致など）。
  - ambiguous な length は避ける（言語によって意味が異なるため）。代わりに明確な count/size を使う。

簡単な命名例（Zig風、説明用）
```zig
const node_offset = ptrToInt(node) - ptrToInt(pool.buffer.ptr); // bytes
const node_index  = node_offset / node_size;                    // elements
assert(node_index < pool.count);
```

## 実践ポイント
- コードベースでまず変数名ポリシーを決める：必ず _index/_count/_size/_offset を使う。
- バイトと要素で混同しそうな箇所にコメントと assert を入れる。
- データ構造の操作は「index側」と「byte側」で変数名を揃え、左右で同じサフィックス長にする（例：source_index / target_index）。
- CI に境界チェックテストを加え、命名ルールが守られているかコードレビューでチェックする。

短いルールを積み重ねるだけで、オフバイワン等の地味で致命的なバグを大幅に減らせます。
