---
layout: post
title: "C++ says \"We have try at home.\""
date: 2025-12-28T10:15:17.687Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://devblogs.microsoft.com/oldnewthing/20251222-00/?p=111890"
source_title: "C++ says \"We have try at home.\""
source_id: 46408984
excerpt: "C++でfinally相当をRAIIで安全に実装する方法と例外時の落とし穴を解説"
---

# C++はこう言う —「try…finally？ウチにあるよ」：RAIIで安全にスコープ脱出後の後片付けをする技術

## 要約
他言語の finally 相当は C++ では「デストラクタ（RAII）」で実現する。だが、例外処理中にデストラクタが例外を投げるとプログラムが即時終了するので注意が必要だ。

## この記事を読むべき理由
C++はサーバ、組込み、ゲームなど日本の主要なプロダクトでも広く使われており、スコープを抜けたときの後始末（リソース解放／ログ／後片付け）を安全に書く技術はバグや不具合を減らす即効性の高いスキルになります。

## 詳細解説
多くの言語（Java/C#/Python/JavaScript）は try { ... } finally { ... } 構文で「必ず実行される処理」を書けます。一方 C++ では同等の役割を「デストラクタ」に委ねます。ブロックを抜けるとそのブロック内で定義されたオブジェクトのデストラクタが実行されるため、リソース解放やクリーンアップ処理を確実に行えます（これが RAII: Resource Acquisition Is Initialization）。

実装例としては Windows の wil::scope_exit があり、渡したラムダをデストラクタで実行します:

```cpp
// C++
#include <wil/resource.h>

auto guard = wil::scope_exit([&] { always(); });
// ... 処理 ...
// ブロックを抜けるとラムダが呼ばれる
```

C++標準でも C++23 で std::scope_exit（<scope> ヘッダ）が利用可能です。unique_ptr のカスタムデリータや自前のスコープガードでも同じパターンを実現できます。

ただし重要な違いがひとつあります。try ブロックから例外が投げられてスタック巻き戻し（stack unwinding）が行われている最中に、その巻き戻しで呼ばれるデストラクタがさらに例外を投げると、C++は std::terminate を呼んで即時終了します（未処理の二重例外を避けるため）。JavaやC#では finally の例外が元の例外を上書きして継続する挙動なのに対し、C++は安全第一で即終了する設計です。

実務上はデストラクタや scope_exit に渡すラムダで例外を投げさせないこと、あるいは例外が発生してもログして無視する別関数（wil::scope_exit_log のような実装）を使うことが推奨されます。また MSVC には C 用の構造化例外処理（__try / __finally）がありますが、C++ の例外と混ぜると混乱を招きやすいので C++ コードでは使わないほうが安全です。

## 実践ポイント
- std::scope_exit（C++23）や wil::scope_exit を活用して明確にスコープ脱出時の処理を記述する。
- スコープガード内（デストラクタやラムダ）で例外を外に出さない：内部で try/catch してログ化する、あるいは noexcept を付ける。
- デストラクタは基本的に noexcept にする（暗黙的に noexcept(true) が望まれる）。
- 既存コードでリソース解放が分散している場合は RAII にリファクタリングして安全性と可読性を向上させる。
- Windows 固有の __try/__finally を C++ の例外処理と混同しない。相互作用に注意するか使わない選択をする。
- 単体テストで「例外が発生したときの挙動（アンワインド中の副作用含む）」を確認する。

