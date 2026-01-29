---
layout: post
title: "C++ Modules Are Here to Stay - C++ モジュールは定着する"
date: 2026-01-29T20:24:16.672Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://faresbakhit.github.io/e/cpp-modules/"
source_title: "C++ Modules are here to stay - Fares A. Bakhit"
source_id: 46741602
excerpt: "C++モジュールでビルドが劇的に速くなり設計も整う、実例付きで導入法"
---

# C++ Modules Are Here to Stay - C++ モジュールは定着する
C++ヘッダ地獄からの脱出――モジュールでビルドが速く、設計がきれいになる理由

## 要約
C++20のモジュールはヘッダ依存を減らしてコンパイル時間を劇的に短縮し、コードの公開／非公開境界を明確にする機能。段階的導入が可能で、実務・競技プログラミング両方に恩恵がある。

## この記事を読むべき理由
大規模プロジェクトや日常的なビルド待ちで時間を失っている日本の開発者にとって、モジュールは「速度」と「設計の保守性」を同時に改善する現実的な選択肢だから。

## 詳細解説
- 基本概念
  - Translation unit: 普通の .cpp ファイル。
  - Module unit: モジュールを宣言する翻訳単位（インターフェース単位と実装単位に分けられる）。
  - export 宣言: モジュール外に公開するクラスや関数を明示する。
- 使用例（簡略）
```cpp
// interface.cpp
export module dsa;
export int pow(int a, int b);
```
```cpp
// use.cpp
import dsa;
auto main() -> int { std::println("Hello world!"); }
```
- サブモジュールと「実態」  
  C++標準では厳密な階層的サブモジュール概念は薄く、dsa.rbtree のような名前は単なる識別子。実装の分割には「モジュールパーティション」を使い、同一モジュール内で共有するプライベート部を分離できる。
- 後方互換性
  既存のヘッダベースのライブラリはモジュール内で使える。段階的移行のための global module fragment（module;）が用意されている。
- ビルド性能
  著者のベンチマークでは、C++20 モジュールは既存のClangに対し大幅なビルド高速化（例: 8.6x）を示し、PCHよりもさらに高速化するケースがある。
- ツールサポート
  コンパイラは逐次対応中だが主要コンパイラは部分〜完全実装し、CMakeはモジュールをサポートしている（import std; は実験的）。

- 最小のCMake例
```cmake
cmake_minimum_required(VERSION 3.28)
project(dsa)
set(CMAKE_CXX_SCAN_FOR_MODULES ON)
set(CMAKE_CXX_STANDARD 23)
add_library(dsa)
target_sources(dsa PUBLIC FILE_SET dsa_public_modules TYPE CXX_MODULES FILES src/dsa.cpp)
add_executable(hello src/bin/hello.cpp)
target_link_libraries(hello PRIVATE dsa)
```

## 実践ポイント
1. 小さなライブラリで試す：既存ヘッダをモジュールインターフェースに置き換え、ビルド時間を計測する。  
2. モジュールパーティションで実装を分割：共有するプライベート構造体はパーティションに入れて外部に露出させない。  
3. CMake設定を追加：CMAKE_CXX_SCAN_FOR_MODULES を有効にして段階的に移行。import std; を使うなら CMAKE_EXPERIMENTAL_CXX_IMPORT_STD を検討。  
4. ツールチェーン確認：使うコンパイラ/clangd/CMakeのバージョンがモジュール対応か確認してから本格導入。  
5. まずは「速度改善の効果」を数値で確認：CIで差分ビルド時間を測り、導入の費用対効果を判断する。

短期間で体感できるメリットがあるため、まずは小さなモジュール化から試すことを強く推奨する。
