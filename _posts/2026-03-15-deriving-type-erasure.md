---
layout: post
title: "Deriving Type Erasure - 型消去の導出"
date: 2026-03-15T01:20:41.848Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://david.alvarezrosa.com/posts/deriving-type-erasure/"
source_title: "Deriving Type Erasure | David Álvarez Rosa | Personal Website"
source_id: 47321469
excerpt: "std::anyの仕組みを一歩ずつ実装し、型消去の設計と性能トレードオフを直感的に解説"
---

# Deriving Type Erasure - 型消去の導出
魅せる解説：std::anyの裏側を一歩ずつ「実装」して理解する

## 要約
C++で「型消去（type erasure）」を使うと、継承できない複数の具体型を1つの共通インターフェースで扱える。この記事は仮想関数＋テンプレートで最小限のAny（std::any相当）を作り、仕組みを分かりやすく示す。

## この記事を読むべき理由
ライブラリ設計やAPI公開で「異なる型を同列に扱いたい」場面は多く、日本の開発現場（組み込み、ゲーム、汎用ライブラリ制作など）でも有用。テンプレート過剰や実行時多態性の選択肢を理解することで、設計・性能トレードオフが明確になります。

## 詳細解説
- 継承ベースの多態性  
  仮想関数を持つ基底クラス（例：Shape）と派生クラス（Square/Circle）で area() を呼ぶ典型的な方法。利点はランタイムで共通型（Shape*）として扱えること。

- テンプレートによる多態性（コンパイル時）  
  関数テンプレート（例：printArea(const auto& shape)）は任意の型に対してコンパイル時にインスタンス化される。利点は高速なインライン化と型チェック、欠点は「共通の実行時型がない」こととテンプレートの伝播によるコード膨張とコンパイル時間増。

- 型消去（type erasure）のアイデア  
  各具体型に対して手作りのラッパー（SquareWrapper, CircleWrapper）を作り、共通の仮想インターフェースで包む。テンプレートを使えばラッパー生成を自動化でき、さらにその仕組みを隠蔽するクラス（AnyShape）を作れば利用者は具体実装を意識せずに扱える。

- 標準的な命名（Concept / Model）パターン  
  Anyクラスは内部に抽象概念 Concept（仮想メソッド群）とテンプレート化した Model<T>（Tにフォワードする実装）を持ち、unique_ptr<Concept> で具体モデルを保持する。これは std::any や std::function に使われる基本技法。小さいオブジェクトはヒープ割当を避けるために SBO（Small Buffer Optimization）を用いることが多い。

サンプル（簡略化版）：

```cpp
// C++
#include <memory>

class Any {
  struct Concept {
    virtual ~Concept() = default;
    virtual double f() const noexcept = 0;
  };
  template<typename T>
  struct Model : Concept {
    T obj_;
    Model(T obj) noexcept : obj_(std::move(obj)) {}
    double f() const noexcept override { return obj_.f(); }
  };
  std::unique_ptr<Concept> ptr_;
public:
  template<typename T>
  Any(T&& obj) : ptr_(std::make_unique<Model<std::decay_t<T>>>(std::forward<T>(obj))) {}
  double f() const noexcept { return ptr_->f(); }
};
```

## 実践ポイント
- 異種オブジェクトをランタイムでまとめたいときは型消去が有効。APIはシンプルに保てる。  
- パフォーマンス注意：単純実装はヒープ割当を伴う。高頻度パスはSBOやプールを検討する。  
- 代替案：型が限定できるなら std::variant、コンパイル時解決で良ければテンプレート（concepts）を選ぶ。  
- 実装練習：まずは上のAnyを自分で実装して、heap allocation の有無やバイナリサイズを比較してみると理解が深まる。  

以上を踏まえれば、std::anyやstd::functionの裏で何が動いているか、設計上の利点とコストが直感的に分かります。
