---
layout: post
title: "A single-file C allocator with explicit heaps and tuning knobs - 単一ファイルのCアロケータ：明示的ヒープとチューニング機能"
date: 2026-03-28T14:04:40.851Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/xtellect/spaces"
source_title: "GitHub - xtellect/spaces: A high-performance C allocator with explicit heap regions, fragmentation control, and runtime tuning. · GitHub"
source_id: 47520807
excerpt: "単一ファイルの高速CアロケータSpacesで明示的ヒープ管理とメモリ上限・共有を簡単導入"
image: "https://opengraph.githubassets.com/fb7e44b632e03c7f3df490db29b955ad4eba5bfea0da351dd3497e385e37f7fa/xtellect/spaces"
---

# A single-file C allocator with explicit heaps and tuning knobs - 単一ファイルのCアロケータ：明示的ヒープとチューニング機能
一行で導入できる「領域（heap）付きmalloc」。パーサーの一括破棄、メモリ上限の強制、プロセス間共有、実行時の割当ウォークまでできる高速Cアロケータ「Spaces」を試す理由。

## 要約
Spacesは単一ソースのLinux x86-64向けCアロケータで、領域（chunk）単位の明示的管理、割当の走査、メモリ天井設定、共有ヒープ、そして一般malloc互換の高速パスを備える。

## この記事を読むべき理由
日本のサーバ／バッチ処理・コンパイラ・キャッシュ設計で「部分ごとのメモリ予算管理」や「大量オブジェクトの一括破棄」が課題になっているなら、低手間で導入できる実用的ソリューションを手早く理解できる。

## 詳細解説
- コア概念：Spacesは「chunk（領域）」を作成してその中でmalloc相当の割当を行う。chunkごとに上限（ceiling）を設定でき、破棄はO(1)でchunk全体を解放可能。
- 実装の要点：
  - 64KB境界に整列したスラブを利用し、ptr & ~0xFFFFでメタデータを直接取得（ページマップや外部ツリー不要）。
  - 52のサイズクラス（8B〜8KB）＋固定サイズ用高速パス。スラブヘッダ読み込みで所有情報を1回で得る設計で高速化。
  - 同スレッドのmalloc/freeはロック無し。クロススレッドfreeはABA安全なTreiberスタックで実装。
  - 大きな割当 (>8KB) はmmap（巨大ページサポートあり）。4MB単位でセグメントをまとめて確保。
- 機能：
  - destroyable heaps（parse用アリーナ等）、live-allocationウォーク、per-chunk ceiling、shared chunks（System V shmでプロセス共有）、
    スレッド専有モード、自動エラーハンドラ差替え、細かなページサイズ／増分チューニング。
- 性能と制約：
  - 標準ベンチで上位に入るケースが多いが、極度のスレッドチェーン（数百スレッドがサイズを不規則に使う）ではL1ミスの影響あり。
  - x86-64 Linux向けの単一プリプロセス済み配布（他プラットフォームは追随予定）。
  - 最小割当8B、スラブあたり64KBの仮想フットプリントなどトレードオフあり。

## 実践ポイント
- すぐ試す（ビルド・リンク）
```bash
gcc -O3 -pthread -fPIC -c spaces.c
ar rc libspaces.a spaces.o && ranlib libspaces.a
gcc your_app.c -Wl,--whole-archive libspaces.a -Wl,--no-whole-archive -lpthread
```
- parser/ASTや一時オブジェクトにはchunkを使い、処理終わりに一発解放：
```c
// C
SpacesChunk parse_heap = spaces_chunk_create(0);
void *node = spaces_chunk_alloc(parse_heap, size, 0);
/* ... */
spaces_chunk_destroy(parse_heap); // 全部即破棄
```
- キャッシュ用途では ceiling を設定してOOMを防ぐ：
```c
spaces_chunk_set_ceiling(cache, 256 * 1024 * 1024); // 256MB 上限
```
- プロセス間共有は ftok を使った System V key で作成／アタッチする（容量設計に注意）。
- 運用上の注意：多スレッド短寿命・乱雑なサイズ割当が多いワークロード、また非 x86-64 環境では適用前に検証すること。

以上を踏まえ、部分的にメモリ管理の責任を「コード」から「allocator」に移したい場合、Spacesは即試す価値がある実用的選択肢である。
