---
layout: post
title: "Devirtualization and Static Polymorphism - 仮想呼び出しの除去と静的多相性"
date: 2026-02-25T22:41:48.812Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://david.alvarezrosa.com/posts/devirtualization-and-static-polymorphism/"
source_title: "Devirtualization and Static Polymorphism | David Álvarez Rosa | Personal Website"
source_id: 396565852
excerpt: "ゲームや組込み向けに仮想呼び出しをLTOやCRTPでほぼゼロ化する手法を解説"
---

# Devirtualization and Static Polymorphism - 仮想呼び出しの除去と静的多相性
仮想関数をやめて、コンパイル時に解決する「ゼロコスト多相性」を手に入れる方法

## 要約
仮想関数（virtual dispatch）は設計はきれいだが実行時コストがある。コンパイラのdevirtualizationやC++の静的多相（CRTP / C++23のdeducing this）を使えば、ホットパスでそのコストをほぼゼロにできる。

## この記事を読むべき理由
パフォーマンスが重要な日本の領域（ゲーム、組み込み、金融、リアルタイム処理）では、設計上の“きれいさ”がボトルネックになることがある。実装の落とし穴と具体的な回避手段を知ることで、遅延やキャッシュ効率の問題を解消できる。

## 詳細解説
- 仮想呼び出しの仕組み  
  基底クラスの仮想メソッドは各クラスのvtable（関数ポインタテーブル）と各オブジェクトのvptrを使って実行時にディスパッチされる。これが原因でオブジェクトサイズ増、間接呼び出し（インライン不可）、分岐予測ミス増、キャッシュ効率低下が発生する。

- Devirtualization（脱仮想化）  
  コンパイラは場合によっては仮想呼び出し先を確定でき、直接呼び出しやインラインに置き換える（devirtualize）。ただし翻訳単位ごとの独立コンパイルだと制約がある。-flto（リンク時最適化）や-fwhole-program、そしてメソッドに対するfinal指定はコンパイラに「この実装しかあり得ない」ことを伝え、脱仮想化を助ける。

- Static polymorphism（静的多相）  
  コンパイル時に解決する手法としてCRTP（Curiously Recurring Template Pattern）がある。基底をテンプレート化し、派生側を型パラメータとして渡すことで仮想関数なしに多相を実現し、コンパイラが完全にインライン化できる。C++23のdeducing thisを使えば、クラス全体をテンプレート化せずにメンバー関数単位で同様の静的解決が可能になる。

- トレードオフ  
  静的多相は「型ごとに別の型」が生成されるため、異なる派生型を同一コンテナで扱うときや動的交換可能性が必要な設計には向かない。またテンプレートによるコード膨張や可読性低下の可能性がある。

- 簡単な例（CRTP）
```cpp
// cpp
template<typename Derived>
struct Base {
  int foo() { return 77 + static_cast<Derived*>(this)->bar(); }
};

struct Derived : Base<Derived> {
  int bar() { return 88; }
};
```

- C++23 deducing this の例
```cpp
// cpp
struct Base {
  auto foo(this auto&& self) { return 77 + self.bar(); }
};

struct Derived : Base {
  int bar() { return 88; }
};
```

## 実践ポイント
- まずプロファイルを取る：仮想呼び出しが本当にホットか確認する。  
- コンパイラに任せる前提で：-O3 + -flto を試す。大規模プロジェクトはLTOで脱仮想化が効くことが多い。  
- 局所的対策：変更困難な箇所は final を付けて脱仮想化を助ける。  
- ホットパスは静的多相で最適化：性能が重要な小さなAPIはCRTPやdeducing thisで書き換える。  
- 設計のバランス：動的ポリモーフィズムが必要な箇所は維持。静的化による可読性や拡張性の低下と性能向上を天秤にかける。

以上。短時間で効果が出やすいのはプロファイル→LTO→final→必要ならCRTPという順序。
