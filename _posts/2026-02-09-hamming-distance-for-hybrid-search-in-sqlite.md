---
layout: post
title: "Hamming Distance for Hybrid Search in SQLite - SQLiteでのハイブリッド検索のためのハミング距離"
date: 2026-02-09T07:49:30.391Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://notnotp.com/notes/hamming-distance-for-hybrid-search-in-sqlite/"
source_title: "Hamming Distance for Hybrid Search in SQLite"
source_id: 405539483
excerpt: "SQLiteのみで128B量子化埋め込みとハミング距離でBM25+意味検索を高速融合"
---

# Hamming Distance for Hybrid Search in SQLite - SQLiteでのハイブリッド検索のためのハミング距離
外部ベクタDB不要！SQLiteだけで「意味検索＋キーワード検索」を高速に組み合わせる方法

## 要約
SQLiteの拡張機能として「バイナリ埋め込み + ハミング距離」を導入すると、外部ベクタDBを使わずにハイブリッド検索（BM25＋意味検索）が実現でき、ストレージと速度の面で有利になる。

## この記事を読むべき理由
外部依存を避けたい日本企業やプロダクトで、コスト・運用負荷を下げつつ意味検索を導入したい開発者／プロダクト担当者にとって、実務で使える手法と実装イメージが得られます。

## 詳細解説
- バイナリ埋め込み：通常はfloat32ベース（例: 1024次元 → 約4KiB）だが、各次元を1ビットに量子化すると1024次元→128バイトに圧縮可能。類似度指標はコサイン→ハミング距離に変更。
- ハミング距離：2つのビット列で異なるビット数を数える指標。計算はXOR → popcount（1の数）で高速化でき、現代CPUはpopcount命令を持つ。
- SQLite拡張：動的ライブラリ（.so/.dylib）として関数登録すれば、SQLから`hamming_distance(blob1, blob2)`のように呼べる。コアは8バイトチャンクでXORし`__builtin_popcountll`で集計するのが高速・簡潔。

例：コア部分（要点のみ）
```c
#include <stdint.h>
#include <sqlite3ext.h>
SQLITE_EXTENSION_INIT1

static void hamming_distance(sqlite3_context *ctx, int argc, sqlite3_value **argv){
  const unsigned char *a = sqlite3_value_blob(argv[0]);
  const unsigned char *b = sqlite3_value_blob(argv[1]);
  int n = sqlite3_value_bytes(argv[0]);
  const uint64_t *va = (const uint64_t*)a, *vb = (const uint64_t*)b;
  int chunks = n / 8;
  uint64_t dist = 0;
  for(int i=0;i<chunks;i++) dist += __builtin_popcountll(va[i] ^ vb[i]);
  for(int i=chunks*8;i<n;i++) dist += __builtin_popcount(a[i] ^ b[i]);
  sqlite3_result_int64(ctx, dist);
}
```
- 実測（著者例）：128バイト埋め込みを1M行で走査、メモリDBでトップ10ソート込み約35ms（Apple M4）。ソートを外すと約28ms。O(n)スキャンだが十分実用的なケース多数。
- 制約：現状は関数ベースで、SQLiteにインデックスやトップK最適化を任せられない。真のtop-k化は仮想テーブル実装や外部インデックス（HNSW/IVF）を検討。

- ハイブリッド統合（RRF）：BM25の上位結果とハミング上位結果をRRFで合成。各リストの順位からスコアを足し合わせる手法で正規化不要。
$$
\text{score(doc)}=\frac{1}{k+\text{rank}_{bm25}+1}+\frac{1}{k+\text{rank}_{semantic}+1}
$$

簡潔なマージ関数（TypeScript風）
```ts
function mergeRRF(sem:number[], bm:number[], k=60){
  const scores = new Map<number,number>();
  sem.forEach((id,r)=>scores.set(id,(scores.get(id)||0)+1/(k+r+1)));
  bm.forEach((id,r)=>scores.set(id,(scores.get(id)||0)+1/(k+r+1)));
  return Array.from(scores.entries()).sort((a,b)=>b[1]-a[1]).map(([id])=>id);
}
```

## 実践ポイント
- まずは小〜中規模データ（〜数百万件）で試す：O(n)でも高速なら外部DB不要で運用開発コストを削減できる。
- 埋め込み生成はAPIでも良いが、社内データならローカルモデルでプライバシー確保が望ましい（日本の企業規模だと重要）。
- 精度とサイズのトレードオフを把握：バイナリ量子化は精度劣化するため、BM25とのハイブリッド化でカバーするのが実用的。
- 本番化するなら：仮想テーブルによるtop-k最適化、あるいは必要に応じてHNSWなどのベクトルインデックスを検討する。
- 実装手順：埋め込み→バイナリ量子化→SQLiteテーブルにBLOB格納→拡張をビルドして`hamming_distance()`を登録→BM25（FTS5）とRRFで統合。

以上を踏まえれば、外部ベクタDBに頼らない「SQLiteだけの現実的なハイブリッド検索」実装が手の届く範囲にあります。
