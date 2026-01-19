---
layout: post
title: "Nanolang: A tiny experimental language designed to be targeted by coding LLMs - Nanolang：コーディングLLMを狙った小さな実験言語"
date: 2026-01-19T23:09:57.785Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/jordanhubbard/nanolang"
source_title: "GitHub - jordanhubbard/nanolang: A tiny experimental language designed to be targeted by coding LLMs"
source_id: 46684958
excerpt: "NanolangはLLM向けに書きやすく設計された小型言語で、必須テストとCトランスパイルで実用的"
image: "https://repository-images.githubusercontent.com/1066847926/62062dd8-4653-4c88-91e4-f17493091431"
---

# Nanolang: A tiny experimental language designed to be targeted by coding LLMs - Nanolang：コーディングLLMを狙った小さな実験言語
小さく・明快でAIにも優しい言語――「NanoLang」でLLM時代の実用的なコード生成とテスト習慣を手に入れる

## 要約
NanoLangは「AI（特にコーディングLLM）が生成しやすい」ことを第一に設計された小さな静的型言語で、明確なプレフィックス構文・必須のシャドウテスト・Cへのトランスパイルを特徴とします。

## この記事を読むべき理由
日本の開発現場や教育現場で、AI支援のコーディングが当たり前になりつつある今、LLMと相性の良い言語設計やテスト文化の取り入れ方を学べる稀有な実験プロジェクトだからです。ラズパイやApple Siliconでの動作も公式サポートされ、組み込みや教育用途にも馴染みます。

## 詳細解説
- 言語設計の肝
  - プレフィックス記法（(+ a (* b c)) のように演算子優先順位を排する）で文法が曖昧にならず、LLMが誤解しにくい。  
  - 関数ごとに必ず shadow テストブロックを付けることで「テストが言語仕様の一部」になり、品質の担保を促進する。
- 型と性能
  - 静的型（型推論あり）、構造体・列挙体・ジェネリクス（Result<T,E>など）をサポート。  
  - コンパイラはNanocでソースをCへトランスパイルし、ネイティブ性能を確保する設計。
- モジュール／FFI
  - 自動依存管理（初回利用時にapt/Homebrew等でライブラリを入れる）とCとの容易なFFIで、既存エコシステムとの連携が取りやすい。
- 開発体験
  - 多数の実例（ゲーム、アルゴリズム、UI）とドキュメント（MEMORY.md：LLM向け学習パターン、spec.json：正式仕様）が整備され、LLMトレーニングやプロンプト設計に役立つ。
- 実行環境
  - Ubuntu、macOS（Apple Silicon）を公式サポート。WindowsはWSL2経由が推奨。Raspberry Pi等のARMもサポートされており、日本のIoT・教育用途に親和性が高い。

サンプル（Hello World）の構造例：
```nanolang
fn greet(name: string) -> string {
  return (+ "Hello, " name)
}
shadow greet {
  assert (str_equals (greet "World") "Hello, World")
}
fn main() -> int {
  (println (greet "World"))
  return 0
}
shadow main { assert true }
```

## 実践ポイント
- まず試す（5分〜）
  - リポジトリをクローンしてビルド： git clone https://github.com/jordanhubbard/nanolang.git && cd nanolang && make build
  - examples フォルダの hello.nano や snake_ncurses.nano を試して、言語感覚を掴む。
- LLMと組み合わせる
  - MEMORY.md と spec.json をプロンプト設計に使う：言語の「明確な規則」と「必須テスト」をプロンプトに含めると生成精度が向上する。
- 日本市場での活用案
  - ラズパイ教育キットでの言語入門（ARMサポート）や、ゲーム系サンプルを教材として利用。  
  - CIに「make test」を組み込み、shadowテストで自動品質チェックを回す文化を導入する。
- 注意点
  - 現状はネイティブWindows(.exe)未対応、WSL2を使うかクロスコンパイル対応を待つ。ライセンスはApache-2.0なので商用利用や取り込みも比較的自由。

興味が湧ったら、まずは examples と MEMORY.md を読み、簡単な関数を1つ書いてshadowテストを付けてみてください。LLMと人間の両方が読みやすいコードを書く練習になります。
