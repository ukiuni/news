---
layout: post
title: "Designated Initializers, the best feature of C++20 - C++20の「指定初期化子」、最強機能"
date: 2026-01-17T01:22:52.118Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://mropert.github.io/2026/01/15/designed_initializers/"
source_title: "Designated Initializers, the best feature of C++20 &middot; Mathieu Ropert"
source_id: 1416700973
excerpt: "C++20の指定初期化子でAPI設計が劇的に楽になりバグが減る理由と実践"
image: "https://mropert.github.io/assets/img/Me.jpg"
---

# Designated Initializers, the best feature of C++20 - C++20の「指定初期化子」、最強機能
C++20の地味だが強力な一手 —— 指定初期化子でAPI設計とバグ検出がグッと楽になる

## 要約
C++20の指定初期化子(designated initializers)は、構造体メンバーを名前で初期化でき、省略したメンバーは宣言時のデフォルトが使われる機能で、API設計やバグ防止に即効性のある改善をもたらす。

## この記事を読むべき理由
日本の大規模コードベースやゲーム／組み込み系のライブラリでは、引数の順序ミスやオプション増加によるオーバーロード地獄が現実問題です。指定初期化子はその多くをコンパイラで防げる実用的な技術で、現場で使える利点が大きいからです。

## 詳細解説
指定初期化子はC99由来の機能をC++に取り込んだもので、構造体の各メンバーを「名前で」初期化できます。たとえば：

```cpp
// cpp
Texture::Desc desc{
    .format = Texture::Format::R16G16B16A16_SFLOAT,
    .usage  = Texture::Usage::COLOR_ATTACHMENT | Texture::Usage::TRANSFER_SRC,
    .extent = device.get_extent(),
    .samples = 4
};
```

主な特徴と注意点：
- 名前付きなので「値の順序」を間違えても見落としにくい（可読性とコードレビューの助けになる）。
- 宣言側でデフォルト値を与えておけば、必要なメンバーだけを書くだけで済む（オプション多数のAPI設計に最適）。
- C99とは異なり、C++版は「宣言順と同じ順序」で指定することを要求する（順序が異なるとコンパイルエラー）。これはメンバーの構築順序に関するC++の安全性を守るための設計上の判断。
- braced-init-list をそのまま emplace_back に渡すなど「前方転送(forwarding)」ができない場面がある（以下のように一度オブジェクトで包めば回避可能）。

```cpp
// cpp
v.emplace_back(Texture::Desc{ .format = ..., .usage = ..., .extent = ..., .samples = 4 });
// または
v.push_back({ .format = ..., .usage = ..., .extent = ..., .samples = 4 });
```

従来の対策（strong typedef/NamedTypeやユーザーリテラル）と比べても、指定初期化子はコンパイラが直接サポートするため追加ライブラリ不要で扱いやすいのが利点です。

互換性面では、CヘッダにあるC99スタイルの順序入れ替え初期化がC++側に取り込まれるとエラーになることがある点や、extern "C" が文法をCに戻すわけではない点に注意が必要です。

## 実践ポイント
- 新API設計では「オプション集合」をstructにまとめ、利用者は指定初期化子で必要なものだけ指定するスタイルにする。
- 既存の多数オプション関数は、オーバーロードを増やすよりもオプション構造体を導入して推奨することでAPIの拡張性が上がる。
- デフォルト値は構造体宣言内で与えておく（0以外のデフォルトも可能）。変更時の互換性を考え、非trivialなメンバー追加には慎重になる。
- emplace_back等で使うときは、一度明示的に型で包むか push_back を使う（現状の言語仕様の制約）。
- Cと共存するコードでは、C側の指定初期化子がC++に取り込まれた時の順序エラーに注意する（ライブラリ境界をはっきりさせる）。

指定初期化子は小さな言語追加ながら、現場でのミスを減らしAPI設計をシンプルにする効果が大きく、日本の開発現場でも導入価値が高い機能です。
