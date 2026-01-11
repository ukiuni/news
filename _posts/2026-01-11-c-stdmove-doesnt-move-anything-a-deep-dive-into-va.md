---
layout: post
title: "C++ std::move doesn't move anything: A deep dive into Value Categories - C++ の std::move は何も移動しない：値カテゴリーの深掘り"
date: 2026-01-11T09:07:02.448Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://0xghost.dev/blog/std-move-deep-dive/"
source_title: "std::move doesn&#39;t move anything: A deep dive into Value Categories"
source_id: 46551602
excerpt: "std::moveは値カテゴリーの見せかけで、NRVOやnoexcept、constで性能を壊す落とし穴"
image: "https://0xghost.dev/og/std-move-deep-dive.png"
---

# C++ std::move doesn't move anything: A deep dive into Value Categories - C++ の std::move は何も移動しない：値カテゴリーの深掘り
魅力的なタイトル: 「std::move は“魔法”じゃない：気づかないうちにパフォーマンスを壊す3つの落とし穴」

## 要約
std::move はオブジェクトを移動しない――式の値カテゴリーを変えるだけで、実際の資源の「奪取」はムーブコンストラクタ／ムーブ代入が実行されたときに起きる。誤用すると NRVO や noexcept による最適化を阻害し、むしろコピーが発生して遅くなる。

## この記事を読むべき理由
日本のソフトウェア開発でも、ライブラリや大規模サービス、組み込み・ゲームなどで大量のコピーがパフォーマンスボトルネックになります。C++ のムーブ意味論を正しく理解すれば、無駄なコピーを避け、安定した高速化が図れます。

## 詳細解説
- std::move の正体  
  std::move は実体的なメモリ移動を行う関数ではなく、引数の式を「xvalue（expiring value）」に変換するためのキャストです。呼んだ瞬間にデータが移るわけではなく、ムーブ可能な式と見なされることで、コンパイラがムーブコンストラクタ／ムーブ代入を選ぶきっかけを作るだけです。

- 値カテゴリー（Value Categories）のおさらい  
  - lvalue：名前を持ちアドレスが取れる（通常の変数）。  
  - prvalue：一時オブジェクト（式の結果で名前を持たない）。  
  - xvalue：名前はあるが「これから破棄される」ものとして扱われる（std::move が作るもの）。  
  xvalue によってムーブが選ばれるが、ムーブが実行されるか、あるいは最適化でそもそもムーブもコピーも不要になるかは別問題です。

- NRVO（Named Return Value Optimization）と return std::move の落とし穴  
  関数からローカル変数を返すとき、コンパイラは NRVO によってその変数を呼び出し側の返却領域に直接構築でき、コピー/ムーブがゼロになります。しかし return std::move(local) のように明示的に std::move を付けると「名前で返している」条件が崩れ、NRVO が無効化されてムーブが発生する（= ゼロコストではなくなる）。移動よりゼロが速いので、return での std::move は基本的に不要で逆効果です。

- noexcept とコンテナの再配置  
  std::vector などは要素を新しいメモリへ移す際、ムーブコンストラクタが例外を投げる可能性があると安全のためにコピーを使います（強例外保証のため）。つまりムーブコンストラクタを noexcept にすることで、再配置時にコピーではなくムーブが使われ性能改善につながります。

- const オブジェクトからのムーブはコピーにフォールバックする  
  const なオブジェクトを std::move しても const 修飾は外れないため、ムーブコンストラクタ（非 const rvalue 参照を取るもの）にバインドできず、結果としてコピーコンストラクタが選ばれてしまいます。見た目はムーブ風でも実際はコピーが走るので注意。

- ムーブ後のオブジェクトの扱い  
  ムーブ後のオブジェクトは "valid but unspecified"（有効だが値は不定）です。破棄・代入・条件のないメソッドの呼び出しは安全ですが、中身を読み取って仕様に依存するような使い方は避けるべきです。

- 正しいムーブ実装（簡潔な例）  
  ムーブ演算子・ムーブコンストラクタは例外を投げないよう noexcept を付けるのが推奨です。最低限 Rule of Five を意識して実装します。

```cpp
class Buffer {
private:
    int *data;
    size_t sz;
public:
    Buffer(size_t n) : data(new int[n]), sz(n) {}
    ~Buffer() { delete[] data; }

    // コピー
    Buffer(const Buffer& o) : data(new int[o.sz]), sz(o.sz) {
        std::copy(o.data, o.data + sz, data);
    }

    // ムーブ（noexcept が肝）
    Buffer(Buffer&& o) noexcept : data(o.data), sz(o.sz) {
        o.data = nullptr;
        o.sz = 0;
    }

    Buffer& operator=(Buffer&& o) noexcept {
        if (this != &o) {
            delete[] data;
            data = o.data;
            sz = o.sz;
            o.data = nullptr;
            o.sz = 0;
        }
        return *this;
    }
};
```

## 実践ポイント
- return でローカル変数を返すときは基本的に std::move を付けない（return local; が最適）。  
- 自クラスのムーブコンストラクタ／ムーブ代入は可能な限り noexcept にする（特にコンテナ要素となる型）。  
- const オブジェクトに対して std::move を使わない（期待通りムーブされない）。  
- ムーブ後のオブジェクトには値を期待せず、再代入または破棄だけ行う。  
- 動作確認法：コンストラクタ／コピー／ムーブにログを入れてコピー回数・ムーブ回数を観察する。ビルド時に NRVO を確認したければ一時的に最適化を外す（例: -fno-elide-constructors）で挙動を検証する。  
- 静的解析／clang-tidy を活用する（noexcept 指摘やパフォーマンス指摘が出るツールがある）。  
- 大規模サービスや組み込み開発では、意図しないコピーがスループットやメモリ使用量に直結するため特に注意する。

短くまとめると：std::move は「ムーブしていいよ」と伝えるためのラベルであって実行ではない。言葉の裏側（値カテゴリー、noexcept、NRVO）を理解して使えば、安全に性能を改善できる。
