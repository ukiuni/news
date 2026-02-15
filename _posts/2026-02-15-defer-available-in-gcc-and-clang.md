---
layout: post
title: "Defer available in gcc and clang - gcc と clang で defer が使えるようになった"
date: 2026-02-15T21:27:12.037Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://gustedt.wordpress.com/2026/02/15/defer-available-in-gcc-and-clang/"
source_title: "Defer available in gcc and clang &#8211; Jens Gustedt&#039;s Blog"
source_id: 1000965826
excerpt: "clang‑22で正式対応、gcc9以上でフォールバック可能なCのdeferで後始末を簡潔に実現"
image: "https://gustedt.wordpress.com/wp-content/uploads/2025/09/raven.png"
---

# Defer available in gcc and clang - gcc と clang で defer が使えるようになった
もう戻り処理で迷わない：Cに「defer」構文が実用レベルで到来（clang-22 と gcc フォールバック対応）

## 要約
C言語における後始末処理のための構文「defer」が、TS 25755 として仕様化が進み、clang-22 で実装が利用可能になり、gcc 9 以降でも簡易フォールバックで使えるようになりました。

## この記事を読むべき理由
リソース解放やミューテックスの解放忘れ、複雑な早期リターンによるスパゲッティ処理を減らせます。日本の開発現場（組込み、サーバ、Android NDK 等）で使うコンパイラのサポート状況を把握しておくと安全で保守しやすいコードに移行できます。

## 詳細解説
- 標準化動向: JeanHeyd Meneide 編集の技術仕様 TS 25755 が進行中で、これに沿った defer の定義が策定されています。
- コンパイラ対応: clang-22 から標準的に利用可能。gcc 側はネスト関数を用いるフォールバック実装で gcc-9 以降でも動かせるコードがある（ただし古い clang は block 拡張と互換性がないためフォールバック不可）。
- セキュリティ/実行面: gcc のネスト関数フォールバックはトランポリン等を生成せず、最適化無しでも実行時の安全性に配慮されています（著者の検証による）。
- 実装上の注意: gcc フォールバックはローカルスコープ（中括弧）内で使う必要がある。stddefer.h があればそれを優先して include するのが望ましい。コンパイル環境によっては -fdefer-ts 等のオプションが必要な場合あり。
- 互換性: ビルドターゲット次第ではサポート不足なツールチェインがあるため、CI でのテストとフォールバック検出ロジックが必要。

簡単なフォールバック例（要約）:
```c
#include <stdlib.h>

#if __has_include(<stddefer.h>)
# include <stddefer.h>
#elif __GNUC__ > 8
/* 簡易フォールバック（実際は複数マクロで生成） */
#define defer _Defer
/* ...フォールバック実装のマクロ群... */
#else
# error "defer が利用できません"
#endif
```

## 実践ポイント
- まず自分のビルド環境で clang-22 以上または gcc-9 以上での挙動を確認する。
- stddefer.h が使える環境ならそれを優先し、無ければフォールバックマクロを用意して条件付き include する。
- 大きなスタック配列や malloc の後始末、ミューテックスの unlock など、失敗パスや早期 return が多い箇所から導入する。
- 組込みや古いディストリでの互換性をCIで確認し、中括弧スコープ内で使うルールをチームで統一する。
- Android NDK 等で clang が使われているケースでは早期採用の恩恵が大きい。

実務ではまず小さなユーティリティ関数やクリティカルセクションの後始末から試し、静的解析とテストで挙動を確認すると移行が安全です。
