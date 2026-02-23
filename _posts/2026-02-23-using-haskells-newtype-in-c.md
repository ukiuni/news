---
layout: post
title: "Using Haskell's 'newtype' in C - CでHaskellの'newtype'を使う"
date: 2026-02-23T19:22:17.038Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.nelhage.com/2010/10/using-haskells-newtype-in-c/"
source_title: "Using Haskell&#39;s &#39;newtype&#39; in C - Made of Bugs"
source_id: 398369259
excerpt: "newtype風ラッパで物理/仮想アドレス誤用を検出する簡単C技"
---

# Using Haskell's 'newtype' in C - CでHaskellの'newtype'を使う
Cで型のミスを防ぐ小技：物理/仮想アドレスの取り違えをコンパイラに検出させる方法

## 要約
Cのtypedefでは区別できない「同じ表現を持つ別意味の型」を、singleton structと小さなユーティリティでラップすることでコンパイラにチェックさせられる手法の紹介。JOSやLinuxカーネルで使われる実例に基づく。

## この記事を読むべき理由
低レイヤー開発（OS、ドライバ、組み込み）では同じビット表現でも用途が違う値を誤用すると致命的なバグになります。日本の組込み/OS開発者や安全性を重視する現場で、手軽に型安全性を高められる実践テクニックです。

## 詳細解説
- 問題点：typedef uint32_t physaddr_t; のような別名はコンパイラに区別されず、物理アドレスと仮想アドレスを取り違えるバグを見逃す。
- 解決策：単一フィールドのstructでラップする（Haskellのnewtypeに類似）。これにより型が別物になり、誤った型を渡すとコンパイル時に検出される。

例（単純版）:
```c
c
typedef struct { uint32_t val; } physaddr_t;
typedef struct { uint32_t val; } virtaddr_t;
```

便利マクロ例（NEWTYPEとアクセサ）:
```c
c
#define NEWTYPE(tag, repr) \
typedef struct { repr val; } tag; \
static inline tag make_##tag(repr v) { return (tag){.val = v}; } \
static inline repr tag##_val(tag v) { return v.val; }

NEWTYPE(physaddr, uint32_t);
NEWTYPE(virtaddr, uint32_t);
```

実用例（KADDR/PADDRの改訂）:
```c
c
#define PADDR(kva) ({ \
  if (virtaddr_val(kva) < KERNBASE) panic("..."); \
  make_physaddr(virtaddr_val(kva) - KERNBASE); \
})

#define KADDR(pa) ({ \
  uint32_t ppn = physaddr_val(pa) >> PTXSHIFT; \
  if (ppn >= npage) panic("..."); \
  make_virtaddr(physaddr_val(pa) + KERNBASE); \
})
```

- 性能・表現：ほとんどのコンパイラで最適化され、実行コード・メモリ表現は素の型と同等。i386の戻り値扱いなどABI上の差異で返り値で多少のコストがある場合があるが、amd64では問題にならないことが多い。
- 実運用：開発時は型チェックを有効にし、リリースでは NDEBUG を使って typedef に切り替える運用も可能（必要なら）。

原典は JOS の実装例や Linux カーネルの page 型（pte_t 等）を踏襲している点もポイント。

## 実践ポイント
- まずは危険領域（物理/仮想アドレス、ユニットの違う測定値、エンコード済み文字列 等）を洗い出す。
- NEWTYPEマクロ＋make_/val アクセサをヘッダで定義して、変換は局所化する（ユーティリティ関数を作る）。
- パフォーマンスが心配ならベンチかコンパイラ出力を確認。問題あれば NDEBUG で typedef に戻す運用を検討。
- カーネルや組込みコードを書くチームでは、こうした型ラッピングをコーディング規約に組み込むとエラー削減効果が高い。
