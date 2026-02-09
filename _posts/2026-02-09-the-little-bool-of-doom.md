---
layout: post
title: "The little bool of doom - 「破滅の小さな bool」"
date: 2026-02-09T14:24:53.617Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.svgames.pl/article/the-little-bool-of-doom"
source_title: "The little bool of doom – suve's ramblings"
source_id: 1327366970
excerpt: "古いDOOMコードがC23移行で爆発、memset初期化が実行時バグを誘発—原因と対処を解説"
---

# The little bool of doom - 「破滅の小さな bool」
DOOMの古いコードが、C23と_gcc_の進化で思わぬ“爆破”を起こした理由 — ビルドエラーから実行時バグまで、初心者にもわかる技術解説

## 要約
GCCのデフォルトC標準がC23に変わったため、プロジェクト内で独自定義していたenumベースのboolean型が言語キーワードと衝突してビルドエラーに。さらに_bool_（C99/_Bool）に切り替えると、memset(-1)で初期化された古いコードが意図しない振る舞いを示し、ランタイムエラーを誘発した。

## この記事を読むべき理由
- 最近のコンパイラやC標準の変化が、古いCコードにどんな影響を与えるかが実例で学べる。  
- 特に組み込みやレガシーコードを扱う日本の開発者にとって、ビルド設定・型の扱い・初期化の落とし穴は実務上重要。

## 詳細解説
1. 問題の発端  
   - chocolate-doom のコードは boolean を enum { false, true } で定義していた。  
   - GCC 15系でデフォルトが -std=gnu23 に変わり、C23では bool/true/false がキーワードになったためコンパイルエラーに。

2. ビルド面の対処案  
   - (A) ビルドフラグで古いC標準を指定する（例: -std=gnu17）  
   - (B) ソースを直して標準の bool を使う（条件付きで __STDC_VERSION__ を参照）  
   - (C) enum 値を別名に変える（例: False/True）  
   著者は (B) を提案し一時的patchを作成したが、最終的に upstream はプロジェクトをC99扱いにする選択をした。

3. 実行時バグの核心（ここが肝）  
   - 元コードは boolean 配列を memset(..., -1, ...) で初期化していた。enum型（4バイト）では全ビット1は非ゼロとして“真”扱いになり特定の比較が期待通りに動いた。  
   - しかし _Bool（C99の真のブール型、実体は1バイト）にするとメモリ上は0xFF（255）となり、コンパイラが異なる命令（8ビット目だけ参照するなど）を生成することで、同じ条件式が片方では成立し片方でも成立してしまうといった不整合が発生。  
   - 根本は「memsetで-1して生データを書き込む」ことがブール型の規格的取り扱い（0か1に正しく収める）を無視しており、未定義挙動または実装依存の副作用を招いた点。

4. アセンブリレベルの違い（要点のみ）  
   - enum(4バイト): 比較は32ビット単位で CMP/TEST eax,eax が使われる。  
   - _Bool(1バイト): 8ビットレジスタ（al）や TEST al,al が使われる。これが最適化やゼロ判定の振る舞い差を生む。

## 実践ポイント
- 古いコードをそのままビルドするときは、まず明示的に -std を指定して再現性を確保する（例: -std=gnu17）。  
- bool系を生メモリで初期化（memsetで -1 等）するのは危険。必ず代入で初期化するか、型を明示的な整数型にする。  
- 標準の bool を使うなら <stdbool.h> を include し、型サイズや振る舞いに依存するコード（memset等）は見直す。  
- 互換性確保のため、ソース側で条件付きコンパイルを行う例（参考）：

```c
// c
#include <inttypes.h>

#if defined(__cplusplus) || defined(__bool_true_false_are_defined) || (__STDC_VERSION__ >= 202311L)
// Use builtin bool for C++ and C23
#include <stdbool.h>
typedef bool boolean;
#else
// legacy: keep previous behaviour
typedef enum { false, true } boolean;
#endif
```

- プロジェクト単位で static_assert(sizeof(boolean) == X) のようなチェックを入れ、CIで新コンパイラ導入時に警告・失敗させることを推奨。

短く言うと：コンパイラや言語仕様の更新は「ビルドエラー」だけでなく「微妙な実行時バグ」も引き起こす。boolean の初期化や型サイズに依存した古い慣習は今すぐ見直しましょう。
