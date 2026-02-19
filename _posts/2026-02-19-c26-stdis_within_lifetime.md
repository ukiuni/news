---
layout: post
title: "C++26: std::is_within_lifetime - std::is_within_lifetime（オブジェクト寿命内判定）"
date: 2026-02-19T10:45:26.085Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.sandordargo.com/blog/2026/02/18/cpp26-std_is_within_lifetime"
source_title: "C++26: std::is_within_lifetime | Sandor Dargo's Blog"
source_id: 1207864299
excerpt: "C++26新機能: 寿命判定APIでconstexprのunion有効メンバを判定"
---

# C++26: std::is_within_lifetime - std::is_within_lifetime（オブジェクト寿命内判定）
constexprで「このオブジェクトは今生きているか？」を確実に調べる、新しい小さな武器

## 要約
C++26に追加されるconsteval関数 std::is_within_lifetime(const T* p) は、定数評価時にポインタが指すオブジェクトが現在その寿命内にあるかを安全に判定するための機能です。主な用途は共用体（union）のどのメンバーがアクティブかを確認することです。

## この記事を読むべき理由
constexpr/constevalを多用するモダンC++コードや、メモリ効率を重視する組み込み系・ライブラリ実装では「コンパイル時にオブジェクトの有無を正しく知る」ことが重要になります。本機能は未だランタイムでは代替が必要ですが、constexpr世界の未解決のバグ源を解消します。

## 詳細解説
- シグネチャと場所: <type_traits> に
  ```cpp
  consteval bool std::is_within_lifetime(const T* p);
  ```
  consteval専用で、実行時には使えません。

- 典型例（unionのアクティブメンバー確認）
  ```cpp
  union Storage { int i; double d; };

  constexpr bool check_active_member() {
      Storage s;
      s.i = 42; // i がアクティブ
      return std::is_within_lifetime(&s.i); // true
  }
  ```
  他方で &s.d は false になります（dはアクティブでない）。

- 設計上のポイント
  - ポインタを取る理由: 参照だと一時オブジェクトや寿命延長ルールが絡んで誤解を生みやすいため。ポインタは具体的なメモリ位置を明示します。
  - 汎化された名前: 主用途はunionだが、言語内の「寿命判定」というより根本的な問題を解くために一般的なAPIにしています。
  - consteval専用にした理由: コンパイラは定数評価時に詳細な寿命情報を追跡可能だが、ランタイムでは別手段（状態変数）を使うのが現実的。

- 動機となった問題例（OptBool）
  ```cpp
  struct OptBool {
      union { bool b; char c; };
      constexpr auto has_value() const -> bool {
          if consteval {
              return std::is_within_lifetime(&b);
          } else {
              return c != 2; // ランタイムではセントネルで判定
          }
      }
      constexpr bool value() const { return b; }
  };
  ```
  コンパイル時は UB を避けつつ正しく判定、ランタイムは最小オーバーヘッドで動作。

- 実装状況（執筆時点 2026/02）: 主要コンパイラでの実装はまだ進んでおらず、利用には待ちが必要。

## 実践ポイント
- constexpr/constevalで union を扱うライブラリ実装や省メモリ型（Optional< bool > 等）を作る場合、現在は「コンパイル時は std::is_within_lifetime、実行時はセントネル等」の併用が実用的。
- この関数は定数評価専用のため、ユニットテストでconstexpr評価を行うケース（コンパイルタイムの挙動検証）に活用できる。
- 実運用で使う前に、ターゲットコンパイラの C++26 サポート状況を確認すること（まだ未実装の可能性あり）。
