---
layout: post
title: "Porting Go's strings package to C - GoのstringsパッケージをCに移植する"
date: 2026-04-07T01:24:08.151Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://antonz.org/porting-go-strings/"
source_title: "Porting Go's strings package to C"
source_id: 47627595
excerpt: "GoのstringsをCに移植し、アロケータ設計とゼロコピーで性能と所有権問題を実証"
image: "https://antonz.org/porting-go-strings/cover.png"
---

# Porting Go's strings package to C - GoのstringsパッケージをCに移植する
Go標準の文字列/バイト処理をCで再現して見えた「性能・所有権・割当て」のリアル

## 要約
Goのstrings/bytesパッケージを段階的にCへ移植した事例。ビット演算やUTF-8、ゼロコピー処理、明示的なアロケータ設計、ベンチマークでの評価と最適化までの道筋が示される。

## この記事を読むべき理由
Goの便利な標準ライブラリ設計をCに持ち込みたい人、あるいは組み込みやレガシー環境で「Go的」なAPIを低レイヤで再現したい日本のエンジニアにとって、実装上のトレードオフと実践的テクニックが学べるから。

## 詳細解説
- 取り掛かりは依存の少ない純関数群（math/bits, unicode/utf8）から。言語間の微妙な差（例：Goはシフトの優先度が高いがCは低い）を意識して括弧で解決するなどの小技が必要。
  
  ```go
  // Go: shift has higher precedence
  var x uint32 = 1 << 2 + 3 // (1 << 2) + 3 == 7
  ```
  ```c
  /* C: shift has lower precedence */
  uint32_t x = 1 << (2 + 3); /* 1 << (2 + 3) == 32 */
  ```

- bytesパッケージではZero-copyの再解釈が重要。Goの[]byte→string変換をCで模す際、メモリを複製せずに参照構造体で扱う実装が採られている（文字列長比較＋memcmpで等価判定）。
- 単純なループ（IndexByte等）はCのforループ＋境界チェックマクロで忠実に再現。だがメモリを返す関数（Repeat等）はC側で「誰がfreeするか」を明確にする必要があるため、アロケータ導入がキモとなる。
- アロケータ設計：Alloc/Realloc/Freeを関数ポインタで持つ構造体を渡す方式。これにより呼び出し側でmalloc、arena、トラッキング等を切り替え可能になり、隠れた割当てを排する設計が得られる。

  ```c
  /* シンプルなアロケータインターフェイス（例） */
  typedef struct {
    void *self;
    so_Result (*Alloc)(void *self, so_int size, so_int align);
    so_Result (*Realloc)(void *self, void *ptr, so_int oldSize, so_int newSize, so_int align);
    void (*Free)(void *self, void *ptr, so_int size, so_int align);
  } mem_Allocator;
  ```

- Buffer/Builderのような可変バッファは構造体にアロケータを持たせる。メソッドは明示的関数（strings_Builder_WriteString 等）となり冗長だが、自動翻訳ツールで軽減できると示唆。
- ベンチマーク基盤もCで移植し、ns/op・MB/s・B/op・allocs/opを記録。さらにTrackerアロケータで割当て統計を取得し、最適化（検索アルゴリズムやビルダ増長戦略）に反映した。

## 実践ポイント
- 移植は依存の少ない純関数から始める（bits, utf8 → bytes → strings）。
- 言語間の演算子優先度差は括弧で明示する習慣を付ける。
- メモリ割当てはアロケータを第一級に扱う：APIにallocatorパラメータを渡し、呼び出し側が所有権を管理できる設計にする。
- ゼロコピー変換（[]byte→string）は安全性（不変性）を担保できればパフォーマンス上有効。
- ベンチマークとトラッキングアロケータで実測し、ホットパス（検索やバッファ増長）を最適化する。
- 日本の現場では、組込み/ゲーム/既存Cコードとの連携や軽量ランタイムが重要なケースが多く、今回の設計思想（明示的所有権・アロケータ・ベンチ駆動最適化）は直接参考になる。

実装を始める際は、小さく移植→測定→最適化を繰り返すのが近道。
