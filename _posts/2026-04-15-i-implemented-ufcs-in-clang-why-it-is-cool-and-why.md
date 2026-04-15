---
layout: post
title: "I implemented UFCS in clang. Why it is cool, and why it will never come to C++ - ClangにUFCSを実装しました。なぜ魅力的で、なぜC++には来ないのか"
date: 2026-04-15T21:05:29.653Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/ZXShady/zxshady.github.io/blob/main/ufcs.md"
source_title: "zxshady.github.io/ufcs.md at main · ZXShady/zxshady.github.io · GitHub"
source_id: 360801895
excerpt: "ClangにUFCSを実装し、可読性・コンパイル時間改善の利点とC++標準化が困難な理由を実証"
image: "https://opengraph.githubassets.com/ff87c3b7a095e57b5732bcb8016bb10f573500ab97e7bfe43aff67002cb2afc2/ZXShady/zxshady.github.io"
---

# I implemented UFCS in clang. Why it is cool, and why it will never come to C++ - ClangにUFCSを実装しました。なぜ魅力的で、なぜC++には来ないのか

使いたくなる！C++に“拡張メソッド”を持ち込んだら日常のコードがこう変わる

## 要約
UFCS（Uniform Function Call Syntax）は「object.f(args)」と「f(object, args)」を相互に使えるようにする提案で、可読性・汎用性・ヘッダ肥大の解決に強力に働く一方、名前解決やオーバーロード解決といったC++の核心部分に深く触れるため標準化は困難、という話です。

## この記事を読むべき理由
C++のテンプレート／ライブラリ設計やコンパイル時間問題に悩む日本のエンジニアにとって、UFCSがもたらす設計上の利点と現実的な障壁は日常の生産性改善やライブラリ設計の指針になります。

## 詳細解説
- UFCSとは：  
  普通はメンバ関数と自由関数（free function）が別の書き方を要求するが、UFCSは「x.f(a)」が存在しなければ「f(x,a)」へフォールバックする仕組み。

- メリット（簡易化して列挙）：  
  - ジェネリックプログラミングが楽に：テンプレート内で「メンバか自由関数か」を気にせず書ける。  
  - IDEの補完が強化される：ライブラリ関数もオブジェクト側の候補として見えるようになる。  
  - 小さく速いヘッダ：依存をクラスに押し込まず、基本APIは軽くして高レイヤを自由関数で提供できる（ヘッダ肥大とコンパイル時間の低減）。  
  - 重複削減：std::string と std::string_view のような似たインターフェースを重複して実装する必要が減る。  
  - enum や組み込み型にも「メソッド風」呼び出しが可能に。

- 問題点（導入が難しい理由）：  
  - 名前解決の複雑化：ADL（引数依存名前解決）を広げると探索コストと意図しない衝突が増える。  
  - オーバーロードの曖昧さ：同名のメンバと自由関数が両方ある場合の決定規則が難しい。  
  - API帰属の混乱：x.f()が型に属する暗黙の印象を与え、可読性や保守性の問題に。  
  - ポインタ／-> の綴りミスや演算子オーバーロードとの混同リスク。  
  - 結果としてC++の既存ルール（lookup, overload）が壊れかねない。

- 技術的解決案（概略）：  
  著者は問題の多くが「フォールバックでADLを幅広く使う」設計に起因すると指摘。解決の方針は「探索範囲を狭める／明示的に制御可能にする」ことで、無差別な名前衝突や性能劣化を抑えることが考えられる。

- 短いコード例（今のC++とUFCSイメージ）：
```cpp
// C++（現状）
class Foo {};
void do_thing(Foo f, int i);
Foo f;
do_thing(f, 42);    // 自由関数
// UFCS があれば
f.do_thing(42);     // メンバ風に呼べる
```

## 実践ポイント
- 今日からできること：非メンバ関数＋ADLをうまく使う、ヘッダ依存を減らすために高レイヤ機能は分離しておく。  
- ライブラリ設計上の指針：クラスは最小限のコア操作のみに留め、派生的なユーティリティは名前空間の自由関数として提供するとメンテ性が上がる。  
- 興味がある人は著者のClangフォークで実装を試せる（原文参照）。UFCSの恩恵と問題点を自分のプロジェクトで想定検証してみてください。
