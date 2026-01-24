---
layout: post
title: "RustyPP: A C++20 library and Clang tool to enforce Rust-like safety and mutability - RustyPP：C++20にRust風の安全性と可変性を導入"
date: 2026-01-24T19:34:53.339Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/I-A-S/RustyPP"
source_title: "GitHub - I-A-S/RustyPP: Rust-like Safety and Syntax for C++20"
source_id: 418543359
excerpt: "C++20でRust風の所有権と可変性を導入し、Clang検証でバグを抑止するライブラリ兼ツール"
image: "https://opengraph.githubassets.com/8ba4ca77a97827ffa0c56362e86321002d4dd48db48a8781fedb26f48d2e022f/I-A-S/RustyPP"
---

# RustyPP: A C++20 library and Clang tool to enforce Rust-like safety and mutability - RustyPP：C++20にRust風の安全性と可変性を導入
C++に「Rust的な所有権と明示的可変性」を持ち込み、バグをモデル段階で減らすヘッダオンリー＆Clangベースの検証ツール。

## 要約
Rustの設計哲学（明示的な可変性、Resultによるエラー伝播、所有権寄りの型）をC++20に持ち込むライブラリ＋Clang検証ツール。コード規律を自動化して「unsafeな生の型」を禁止できる。

## この記事を読むべき理由
C++で大規模・安全重視の開発をする日本のチーム（組み込み、自動車、金融、ミドル層サービスなど）にとって、人的ミスをコンパイル前に抑止する仕組みは即戦力になるため。

## 詳細解説
- コア思想：Mut<T>／Const<T>で可変性を明示し、生の型（int x; 等）をRustyValidatorで禁止。設計規律をツールで強制することで、暗黙のミューテーションやデータ競合を減らす。  
- 提供物：ヘッダ群（Include/rustypp）＋Clangベースの静的検証ツール（rustypp-validator）＋VS Code拡張（rustypp-vscode）。  
- 型と機能：Vec, String, Option, Result, Box, Arc といったRustライクな型が利用可能。Result<T,E>と RPP_TRY マクロでエラー伝播を簡潔に書ける。  
- 文法拡張（GCC/Clangのみ）：Statement expressions によりブロック式（let x = { ... };）を模倣。MSVCは未サポート（Windowsではclang-clを推奨）。  
- 検証の仕組み：rustypp-validator は compile_commands.json を参照してソースを解析、unsafe宣言を警告/エラー化する。CMakeで -DCMAKE_EXPORT_COMPILE_COMMANDS=ON や bear 等で生成。  
- 開発体験：VS Code拡張でリアルタイムに違反をハイライト。CIにvalidatorを組み込めばプルリクで規約違反を自動検出可能。

例（抜粋）：
```cpp
// C++
#include <rustypp/rustypp.hpp>
using namespace rpp;

auto safe_divide(f32 a, f32 b) -> Result<f32> {
  if (b == 0.0f) return fail("Division by zero");
  return a / b;
}

auto count() -> Result<void> {
  Mut<i32> counter = 0;
  Const<i32> limit = 10;
  f32 result = RPP_TRY(safe_divide(100.0f, 2.0f));
  Const<String> message = RPP_TRY({
    if (result > 50.0f) { fail("Result too large"); }
    RustyPP::Internal::make_unexpected("Success");
  });
}
```

## 実践ポイント
- 試す手順：Include/rustypp をプロジェクトの include にコピー -> #include <rustypp/rustypp.hpp> -> C++20 + GCC/Clang でビルド。  
- Validator導入：CMakeで compile_commands.json を出力 -> rustypp-validator をビルドしてプロジェクトに対して実行 -> CIに組み込む。  
- エディタ統合：rustypp-vscode を導入して開発中に即時フィードバックを得る。  
- 注意点：Statement expressions は GCC/Clang限定、MSVC非対応。既存コードの移行は段階的に（型ラッパーの導入→validatorルール厳格化）。  
- 採用判断：バグコストが高いプロジェクトやコード規律を明文化したいチームでは導入効果が大きい。

元リポジトリ: https://github.com/I-A-S/RustyPP
