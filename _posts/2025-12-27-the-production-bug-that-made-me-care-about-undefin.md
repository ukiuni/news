---
layout: post
title: "The production bug that made me care about undefined behavior"
date: 2025-12-27T18:41:03.731Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://gaultier.github.io/blog/the_production_bug_that_made_me_care_about_undefined_behavior.html"
source_title: "The production bug that made me care about undefined behavior"
source_id: 438007156
excerpt: "決済本番で発生した未初期化が原因の「両方true」不具合と具体的対策"
---

# 決済APIで起きた「両方true」事件 — 未初期化が現場を壊す話

## 要約
決済サービスの本番コードで、あるレスポンス構造体の未初期化メンバが原因で「error と succeeded が同時に true」になる現象が発生した。C++の初期化ルールの落とし穴と実務での対処法を解説する。

## この記事を読むべき理由
大規模な金融系やレガシーC++コードを扱う現場では、未初期化（undefined behavior）は小さなコードで大きな障害を招く。日本の決済・金融システムや高信頼性が求められるプロダクトに働くエンジニアは、原因把握と対策を今すぐ取り入れるべきだから。

## 詳細解説
問題のコード（簡略化）は次のような構成でした。

```cpp
// cpp
struct Response {
    bool error;
    bool succeeded;
    std::string data;
};

void handle() {
    Response response;     // ← ここが問題
    try {
        // DB操作など（response は触らない）
        response.succeeded = true;
    } catch(...) {
        response.error = true;
    }
    response.write();
}
```

ポイントは C と C++ の初期化ルールの違いです。C では自動変数のメンバは未初期化のままですが、C++ でも型によって挙動が分かれます。ここでは std::string の存在により Response は「非POD（非平坦）型」になり、暗黙のデフォルトコンストラクタが生成され呼ばれます。しかしそのデフォルト構築は組み込み型（bool など）を初期化しないため、`error` が不定値のまま読み出され得ます。つまり

- try ブロックで succeeded を true にセットした場合でも、
- error は初期化されていないため「運次第で true に見える」ことがあり得る

これが「両方 true」になる原因です。コンパイラ生成のコンストラクタが呼ばれても、組み込み型はゼロ初期化されない――この点が多くのエンジニアを混乱させます。

また、発見が難しい理由としては
- 実行環境や最適化で未初期化領域のビットパターンが変わるため再現性が低い
- 普通のデバッグ・ログでは見逃しやすい
が挙げられます。

検出・解析に有効な手段は次章で述べます。

## 実践ポイント
すぐ導入できる対策を列挙します。

- 明示的に初期化する（最も簡単で確実）
  - ローカル変数化時にブレース初期化を使う:
    ```cpp
    // cpp
    Response response{}; // bool は false に、std::string は空文字に
    ```
  - 構造体定義でデフォルト値を与える:
    ```cpp
    // cpp
    struct Response {
        bool error = false;
        bool succeeded = false;
        std::string data;
    };
    ```
- コンストラクタを明示する（RAIIで必ず初期値を与える）
- CI に静的解析とサニタイザを入れる
  - 静的解析: clang-tidy, cppcheck, clang static analyzer
  - コンパイル時警告: -Wall -Wextra -Wuninitialized を有効化
  - ランタイム検出: MemorySanitizer (-fsanitize=memory) や UndefinedBehaviorSanitizer (-fsanitize=undefined) をテストビルド／CIで実行
- テストと fuzz/プロパティテストで境界ケースを検出する
- コードレビューのチェックリストに「全メンバ初期化」「自動変数の初期化」を追加する
- レガシーコードでは段階的にデフォルト初期化を導入して不具合を減らす

なぜこれが重要か：金融や決済のようなドメインでは、未初期化が原因で稀に誤ったレスポンスやトランザクション不整合を生み、監査や法令対応の問題につながる。単純な初期化で回避できるリスクを放置しないことが重要です。

