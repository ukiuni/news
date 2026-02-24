---
layout: post
title: "C Enum Sizes; or, How MSVC Ignores The Standard Once Again - Cのenumサイズ：MSVCがまた規格を無視する話"
date: 2026-02-24T02:03:56.802Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://ettolrach.com/blog/c_enum_msvc.html"
source_title: "C Enum Sizes; or, How MSVC Ignores The Standard Once Again | ettolrach"
source_id: 399403097
excerpt: "MSVCがenumを常に32ビット固定にしてABI破壊や値切捨てを招く危険性とは？"
---

# C Enum Sizes; or, How MSVC Ignores The Standard Once Again - Cのenumサイズ：MSVCがまた規格を無視する話
魅力的な日本語タイトル案：MSVCがenumのサイズを勝手に決めると何が壊れるのか？Windowsとクロスプラットフォーム開発者必読

## 要約
GCC/Clangは列挙子の値に応じてenumの基底型サイズを拡張するが、MSVCは最新版でもこの振る舞いやC23の基底型指定をサポートせず、32ビットに固定してしまうため予期せぬ値切捨てやABI不整合が起きる。

## この記事を読むべき理由
Windows上でMSVCを使う日本の開発者や、クロスコンパイル／FFI（例：Rust↔C）でライブラリを扱う人は、enumのサイズ差がバイナリ互換やランタイムバグにつながることを知っておくべきだから。

## 詳細解説
- C標準は「列挙体には基底型（underlying type）があり、明示しなければ符号付き/符号なしの整数型（charも含む）からコンパイラが選べる」としている（柔軟な実装を許容）。
- 多くの実装（GCC/Clang）は列挙子の最大値を見て32ビットを超える必要があれば64ビットに拡張する。例えば列挙子に $2^{32}$ を入れると64ビットの基底型が選ばれる。
- 一方でMSVCは（記事執筆時点のVisual Studio 2026, MSVC 14.50）列挙体を32ビットに固定し、C23で導入された基底型指定（enum X : int）のサポートも未整備。結果、巨大な列挙子が切り捨てられたり、期待した値が得られなかったりする。

例（簡潔版）：
```c
// c
enum Composer { Beethoven = 1, Tchaikovsky = 2, VaughanWilliams = 4294967296 /* = 2^32 */ };
```
GCC/Clangではenumが64ビットになり値が保持されるが、MSVCでは32ビットに固定されて値が0になったりする。

- なぜ起きるか：標準は柔軟だが、MSVCの実装選択が「常に32ビット」に寄せられているため。C23の仕様により明示的に基底型を指定できるが、コンパイラ側の実装が追いついていない。
- リスク：プリコンパイル済み（静的/共有）ライブラリやヘッダでenumを使っている場合、ビルド環境によってABIが変わり、誤動作・データ破壊を招く。

## 実践ポイント
- enumで大きな定数（$>2^{32}-1$）を使う場合はenum任せにせず、固定幅整数型を使う（例：int64_t / uint64_t）。  
- C23の基底型指定（enum E : long long）に頼らない。MSVCが未対応なら意味がない。  
- API/ABIを公開するライブラリではenumを公開型に使わず、明示的な整数型または構造体ラッパーを採用して互換性を担保する。  
- クロスコンパイルやFFI（Rustなど）では、対象コンパイラでのsizeof(enum)を確認し、bindgen等で適切なC型（c_int, c_ulongなど）を選ばせる。  
- CIにWindows/MSVCビルドを入れて実機で検証すること（単体テスト／sizeofチェックを自動化すると有効）。

短く言えば：enumのサイズはコンパイラ依存。Windows/MSVC環境では盲信せず、明示的な型設計で安全側に倒すこと。
