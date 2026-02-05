---
layout: post
title: "(Un)portable defer in C - Cにおける（非）ポータブルなdefer"
date: 2026-02-05T17:08:13.838Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://antonz.org/defer-in-c/"
source_title: "(Un)portable defer in C"
source_id: 1214140681
excerpt: "コンパイラ別に使えるdefer実装と導入の最適解を事例付きで提示"
image: "https://antonz.org/defer-in-c/cover.png"
---

# (Un)portable defer in C - Cにおける（非）ポータブルなdefer
Cで「defer」を実装するならどれが現実的か？コンパイラ別の利点と落とし穴を短く整理

## 要約
deferはリソース解放を安全にする便利機能だがC標準には未導入。GCC/Clang向けの属性やブロック、MSVCの__finally、setjmp/longjmpトリック、スタック型実装など多数の実装があり、用途や対応コンパイラで最適解が変わる。

## この記事を読むべき理由
Cで安全にリソース管理をしたい初級〜中級エンジニア向けに、「どの実装を採るべきか」をコンパイラ互換性・早期リターン対応・実装複雑性の観点で明快に示す。

## 詳細解説
- 背景: ZigやGoなど近年の言語でdeferが重宝される一方、Cの標準化は遅れており（N2895は見送り、N3734は検討中）、実運用では各所で独自実装が使われる。
- GCC（C23相当）: [[gnu::cleanup]]属性＋ネスト関数で理想的な挙動を実現。ただしネスト関数はGCC固有でClangでは非対応。__COUNTER__を使うので唯一無二の識別子が簡単に作れる。
- C11/GCC: ネスト関数を避けたC11互換版は可能だがやはりGCC依存。
- Clang/GCC互換: Clangはblocks拡張を使えるため、cleanup属性＋blocksで両方対応の実装がある。ビルド時に -fblocks が必要で、deferしたブロックの後にセミコロンが必要など文法ルールに注意。
- MSVC: cleanup属性なし。__try / __finally を使えば類似の動作だがスコープ単位の細かい利用は難しい。
- longjmp系: 破壊的で推奨されない（可読性・安全性の観点でNG）。
- STC（forループトリック）: 全コンパイラで動くが、break/returnでdeferがスキップされる欠点あり。
- スタック方式（defers + returnd）: 関数単位でdeferスタックを用意し早期リターンでも実行される。本質的にポータブルだが関数先頭での宣言と専用のreturnマクロが必要。
- 簡易版（GCC/Clang）: deferred呼び出しをstructとcleanupで表現する方式は実用的でシンプル。個人的に現実運用で最も扱いやすい妥協案。

簡易実装（概念例）:
```c
// c
struct _defer_ctx { void (*fn)(void*); void *arg; };
static inline void _defer_cleanup(struct _defer_ctx *ctx){ if(ctx->fn) ctx->fn(ctx->arg); }

#define _DEFER_NAME(a,b) a##b
#define defer(fn, ptr) \
  struct _defer_ctx _DEFER_NAME(_defer_var_, __COUNTER__) \
  __attribute__((cleanup(_defer_cleanup))) = {(void(*)(void*))(fn),(void*)(ptr)}
```

## 実践ポイント
- POSIX/LinuxやWASM向け（GCC/Clang利用）なら「簡易版（cleanup属性＋struct）」がおすすめ：シンプルで早く導入できる。Clangでblocks版を使うなら -fblocks を付ける。
- Windows/MSVC専用なら __try/__finally を活用するか、ポータブル性を優先してスタック方式（defers）を採用する。
- longjmpトリックやループハックは可読性・安全性で避ける。
- 早期リターンや例外的終了（クラッシュ）で必ず実行したいなら、スタック方式かcleanup属性ベースを検討する。
- 開発チームのビルド環境（GCC/Clang/MSVC）をまず確認して、互換性優先か導入容易さ優先かを決めること。
