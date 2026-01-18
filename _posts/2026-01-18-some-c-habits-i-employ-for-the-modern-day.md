---
layout: post
title: "some C habits I employ for the modern day - 現代のCで実践する習慣"
date: 2026-01-18T17:06:26.877Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.unix.dog/~yosh/blog/c-habits-for-me.html"
source_title: "some C habits I employ for the modern day | ~yosh"
source_id: 1435824206
excerpt: "C23前提で安全性と可読性を高めるC習慣—長さ付き文字列やResult型でバグ削減"
image: "https://unix.dog/~yosh/img/renard_lftanthology.png"
---

# some C habits I employ for the modern day - 現代のCで実践する習慣
Cをもう一度好きになる：ミスを減らすモダンな小技10選

## 要約
C23を前提にした「安全さ」と「可読性」を両立する小さな習慣集。型エイリアス、長さ付き文字列、結果型、タプルマクロなど、実践で役立つテクニックをまとめる。

## この記事を読むべき理由
組み込みやシステム開発、ネイティブ拡張が多い日本の現場では、Cコードの堅牢性とメンテ性が生産性に直結します。レガシーコードと付き合いつつ、現代的な手法でバグを減らす具体案を短く確認できます。

## 詳細解説
- バージョンと前提  
  新規プロジェクトは可能ならC23を使う。C23は互換性や型に関する扱いで便利な点があり、GCC/clang/MSVCが対象なら恩恵が大きい。

- CHAR_BITの明示チェック  
  通常は1バイト＝8ビットを前提にする場面が多い。ターゲットが限定されるなら明示的にコンパイル時チェックを入れると誤用を防げる。
  ```c
  #if CHAR_BIT != 8
  #error "CHAR_BIT != 8"
  #endif
  ```

- 固定幅型のエイリアス  
  可読性とRust風の親しみやすさのため、短い型名を定義するのが便利。
  ```c
  typedef uint8_t  u8;
  typedef int32_t  i32;
  typedef uint64_t u64;
  typedef float    f32;
  typedef double   f64;
  typedef uintptr_t uptr;
  typedef ptrdiff_t isize;
  typedef size_t   usize;
  ```

- 長さ付き文字列（length+data）  
  ヌル終端文字列だけに頼らず、長さを保持する構造体を用意する。外部の“悪い関数”対策としてヌル終端は別途保持することができる。
  ```c
  typedef struct {
      u8 *data;   // includes null terminator when needed
      isize len;  // length excluding null terminator
  } String;
  ```

- 「解析（parse）して検証しない（validate）しない」哲学  
  可能な限り厳格な型をAPIに使い、信頼できる生成関数のみでその型を作らせる。Cでは不透明型（opaque type）や構造体の使い方で似た設計ができる。

- タプルマクロ（Tuple）と制約  
  C23では名前付きタグ型の互換性が改善されたが、無名型やポインタ型を含むとプリプロセッサで問題になる。小さいユーティリティ的なタプルはマクロで実装できるが、ポインタを含む場合は明示的な構造体を使うのが現実的。
  ```c
  #define Tuple2(T1, T2) \
  struct Tuple2_##T1##_##T2 { T1 a; T2 b; }
  ```

- 結果／サム型の模倣（Maybe/Result）  
  union と enum を組み合わせ、戻り値で成功/失敗を明示する設計が有効。呼び出し側は必ずokチェックをする習慣を付ける。
  ```c
  typedef enum { ERR_NONE, ERR_OOM, ERR_INV } ErrorCode;
  typedef struct { char *val; } SafeBuffer;
  typedef struct {
      bool ok;
      union { SafeBuffer *val; ErrorCode err; };
  } MaybeBuffer;
  ```

- 動的メモリ管理への姿勢  
  頻繁にヒープを扱うならアリーナや別言語（Rust/C#）への切替を検討。Cではアリーナを使うと管理が楽になる一方、用途によっては別技術の方が生産的。

- 標準ライブラリの取り扱い  
  string.hのうち危険なAPIは避け、mem系や自前の安全ラッパーを用意することが多い。外部APIは必ずドキュメント（man等）を確認する習慣が重要。

- 開発時の注意点  
  - コンパイル警告を厳密に（-Wall -Wextra）  
  - ASAN/UBSANで未定義動作を検出  
  - 単体テストと小さな例で契約（invariants）を検証

日本市場との関連性
- 組み込みや家電、産業機器が多い日本では「ポータビリティ」と「安全性」のトレードオフが常にある。CHAR_BITチェックやlen+dataは、ローカル環境での安全策として有効。ゲームModやライブラリバインディングを行う開発者にも直結する実践的な工夫が多い。

## 実践ポイント
- 新規はC23を選ぶ（ターゲットが限られる場合のみ例外）。  
- プロジェクト冒頭にCHAR_BITチェックを入れる。  
- 固定幅型の短いtypedefを用意して可読性を上げる。  
- 文字列は長さ付き構造体で扱い、外部APIに渡す際だけヌル終端を作る。  
- 公開APIはMaybe/Result風の構造体で失敗を明示し、必ず呼び出し側でokをチェックさせる。  
- 危険なstring.h関数はラップして安全なインターフェースを提供する。  
- 大規模な動的メモリが必要ならアリーナまたは別言語を検討。  
- 開発時は警告全有効化・ASAN/UBSANを常用する。

短い習慣群ですが、これらをベースにするとCでのバグや誤用がかなり減り、メンテもしやすくなります。興味があれば、個別のコード例やラッパー実装の雛形も用意できます。
