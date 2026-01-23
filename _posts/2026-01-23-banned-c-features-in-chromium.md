---
layout: post
title: "Banned C++ Features in Chromium - Chromiumで禁止されているC++機能"
date: 2026-01-23T22:18:53.355Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://chromium.googlesource.com/chromium/src/+/main/styleguide/c++/c++-features.md"
source_title: "Modern C++ use in Chromium"
source_id: 46737447
excerpt: "Chromiumが禁止するC++機能と実務で使える代替策を一目で解説"
---

# Banned C++ Features in Chromium - Chromiumで禁止されているC++機能
Chromiumが“使わせない”C++機能――理由と現場で役立つ代替テクニック

## 要約
Chromiumは安全性・移植性・ビルド安定性を優先し、標準やAbseilの一部機能をプロジェクト内で禁止または保留にしています。禁止理由と代替、第三者ライブラリ利用時のルールを明確に定義しています。

## この記事を読むべき理由
日本の開発現場でもモダンC++を採り入れる流れが強まる中、Chromiumの判断基準は大規模プロダクト設計や企業ポリシー策定の参考になります。特に組み込み・レガシーツールチェーンやセキュリティ要件が厳しい案件では有益です。

## 詳細解説
- 方針の背景：新しいC++規格は3年ごとに来るが、Chromiumはツールチェーンや互換性の確認が済むまで「初期サポート→TBD→許可/禁止」のプロセスで採用を決める。議論は cxx@chromium.org で行い、2年経ったTBDは明示的に扱われます。  
- 第三者ライブラリ：内部実装で禁止機能を使うことは許されるが、Chromium側が呼ぶ公開インタフェースで禁止型を直接使うのは原則禁止（ただし変換して即座に許可済み型へ変える等の例外あり）。セキュリティやコンパイラ未対応が理由なら要相談。  
- 代表的な禁止例（抜粋）：
  - C++11: std::function, std::shared_ptr, std::weak_ptr, std::bind, <regex>, 例外ライブラリ（exceptions）など。
  - C++17: std::filesystem, std::any, parallel algorithms, UTF‑8文字リテラル（char8_t関連）など。
  - C++20: Modulesやchar8_t、一部ライブラリ（std::bit_cast、std::span、std::bind_front等）は禁止。だが概念(concepts)、レンジ、三者比較演算子などは許可。
  - C++20/23で保留（TBD）になっているのはコルーチン、std::format、std::expected、mdspanなど将来の議論対象。
  - Abseilでも多数のコンポーネントを禁止またはTBD扱い（Any, Optional, Span, StatusOr 等）。  
- 理由の例：例外はChromiumビルドで無効、shared_ptrはRefCountポリシーと衝突、<chrono>や<regex>は既存実装と重複、いくつかは標準ライブラリ実装（libc++）の未完成が原因。

## 実践ポイント
- まず公式リストを参照し、禁止機能を使わない設計にする。  
- Chromium内の代替を使う：base::Bind / base::Once/RepeatingCallback、base::RandomBitGenerator、base/strings/string_number_conversions.h、abslの安全な代替（ascii.h 等）。  
- サードパーティを使う場合はインタフェースで禁止型を露出しない、必要なら変換レイヤーを挟む。  
- 新機能を提案する際は短い提案文と議論リンクを cxx@chromium.org に送る。TBDは2年で結論化される点を意識。  
- 日本の現場では、古いコンパイラサポートや社内コーディング規約を踏まえ、Chromiumの基準を社内スタイル策定の参考にすると良い。

以上を抑えれば、Chromium流の安全偏重ポリシーをプロジェクト設計に活かせます。
