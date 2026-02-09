---
layout: post
title: "Thoughts on Generating C - Cを生成することについての6つの考察"
date: 2026-02-09T14:26:31.464Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://wingolog.org/archives/2026/02/09/six-thoughts-on-generating-c"
source_title: "six thoughts on generating c — wingolog"
source_id: 46945235
excerpt: "型・ポインタ・ABI・未整列対策で生成Cの安全性と高速性を実現する実践的ガイド。"
---

# Thoughts on Generating C - Cを生成することについての6つの考察
生成したCコードで「安全」と「速さ」を両立するための実践テクニック

## 要約
コンパイラやトランスパイラが出力先にCを選ぶときに役立つ、実務的な6つの考え方を端的にまとめたメモ。型・ポインタ・ABI・未整列アクセスなどに対する具体的対処法を示す。

## この記事を読むべき理由
組込み、ネイティブ実行、WebAssemblyのAOTなどで「生成C」を使うケースは日本でも多い。ツールチェーンの力を活かしつつ、バグや性能落ちを避ける実践知がすぐに役立つ。

## 詳細解説
1. static inline関数でデータ抽象を残す  
   マクロではなくalways-inlineのstatic inline関数を使うと、抽象化のコストが完全に消える。例：メモリ範囲チェックやポインタ算術を関数化しても最適化で消える。
   ```c
   #include <stdint.h>
   #define static_inline static inline __attribute__((always_inline))

   struct memory { uintptr_t base; uint64_t size; };
   struct access { uint32_t addr; uint32_t len; };

   static_inline void* write_ptr(struct memory m, struct access a) {
       // BOUNDS_CHECK(m, a);
       char *base = __builtin_assume_aligned((char*)m.base, 4096);
       return (void*)(base + a.addr);
   }
   ```

2. 暗黙の整数変換を避ける  
   uint8_t→intなどのCの既定の昇格ルールでバグになりやすい。static inlineの変換関数（u8_to_u32 等）を作り、コンパイル時に -Wconversion を有効にして明示的に扱う。

3. ポインタや整数に「意図」を付ける（単一メンバ構造体）  
   rawなuintptr_tやsize_tだけで表すと混同する。単一メンバstructで型を分割すると、コンパイラの型チェックを活かせる。
   ```c
   typedef struct { uintptr_t v; } anyref;
   typedef struct { anyref p; } eqref;
   typedef struct { eqref p; } structref;

   typedef struct { structref p; double field_0; } type_0;
   typedef struct { structref p; } type_0ref; // 値渡し用の参照型
   static_inline void type_0_set_field_0(type_0ref obj, double val) { /* ... */ }
   ```

4. 未整列アクセスは memcpy を恐れず使う  
   生成コードで未整列ロード/ストアが必要な場合、ポインタキャストより memcpy(&dst, src, sizeof(...)) を使うと移植性が高く、コンパイラが最適化してくれることが多い。

5. ABIとmusttail対策：手動レジスタ割当て  
   tail call や多数の引数/戻り値を扱う際、Cコンパイラが期待通りにレジスタを割り当てないことがある。最初のN個をレジスタで渡し、それ以外は事前確保したグローバル変数に保存→calleeがロードする形で安定させると良い。複数戻り値も同様にグローバルスロットで扱える。

6. 長所と短所を理解する  
   長所：GCC/Clangの最適化や既存ランタイムを利用できるため生産性と性能のトレードオフが良好。短所：スタック制御の欠如、精密なスタック走査（GC）やゼロコスト例外実装の難しさ、ソースレベルのデバッグ（DWARF埋め込みの難しさ）などは妥協点になる。Rust出力の利点（寿命チェック等）もあるが、ツールチェーン面や尾呼び出しの扱いを総合すると一長一短。

## 実践ポイント
- 小さめの抽象は必ず static inline __attribute__((always_inline)) にする。  
- 型変換は全てヘルパー関数に集約し、-Wconversion を有効化する。  
- 意図を示す単一メンバstructでポインタ／オフセットをラップする。  
- 未整列アクセスは memcpy を使ってコンパイラに最適化させる。  
- tail call／多値戻りはレジスタ優先＋グローバルスロットで手動に管理する。  
- 生成Cが型チェックを通ることを検証するテストを必ず入れる（型チェックで多くのバグが潰せる）。

以上を守れば、「生成C」で得られる利点を最大化し、難所を最小化できる。
