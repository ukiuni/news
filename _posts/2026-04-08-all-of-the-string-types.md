---
layout: post
title: "All of the String types - すべての文字列型"
date: 2026-04-08T05:59:59.912Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lambdalemon.gay/posts/string-types"
source_title: "LambdaLemon"
source_id: 1132513293
excerpt: "各言語の文字列型と日本語処理の落とし穴を比較し、安全で高速な選び方を実例で解説"
---

# All of the String types - すべての文字列型
文字列地獄から脱出！言語ごとの違いを短時間で理解して日本語対応で失敗しない選び方

## 要約
各言語が持つ「文字列型」の違い（可変/不変・エンコーディング・終端・メモリ所有権など）を整理し、日本語（マルチバイト）を扱う際の注意点と実務での選び方を示す。

## この記事を読むべき理由
日本語はマルチバイトや結合文字（合字、濁点など）を含むため、言語ごとの文字列表現の違いを知らないとバグやパフォーマンス問題、ファイル名/OS連携での不具合が起きやすい。特に日本の開発現場で多いC/C++、Java、Android、組み込み、RustやGoでの新規開発に直結する知識。

## 詳細解説
- 共通の観点：可変か不変か（growable）、null終端か、メモリの所有権、符号化（UTF‑8/16/32）──これらが使い勝手と安全性を決める。
- Rust: String（所有・可変・UTF‑8）、&str（参照・不変・UTF‑8）、Vec<char>（コードポイント配列、編集向け）。OS文字列はプラットフォーム依存（WindowsでUTF‑16風、Unixでバイト列）。
- C / C++: Cはchar*/null終端が基本でバイト列。wchar_tやchar16_t/32_tもあるがサイズとエンコーディングが環境依存。C++は std::basic_string<T> ベースで型ごとに扱える（std::string, std::u16string 等）。
- Go: string（不変・バイト列＋長さ・UTF‑8慣習）、[]byte（可変バイト列）、[]rune（コードポイント配列でUnicode対応）。
- Zig: 明示的に多数の配列型（非終端/終端、可変/不変）を提供。デフォルトはバイト列でUnicodeは明示的に扱う。
- Java / C#: stringは不変でUTF‑16ベース（charはUTF‑16コードユニット）。大量連結は StringBuilder を使う。
- Python: str はUnicodeの論理文字列（不変）。list[str] は可変の文字リスト。
- Swift: String は「人間が見て一文字」の概念（グラフェムクラスター）で、可変はコピーオンライト。Objective‑Cの NSString はUTF‑16基盤。
- Pascal / Haskell 等: 言語ごとに多様な歴史的型があるので注意。

重要ポイント：インデックス操作で「バイト位置」と「文字（グラフェム）」を混同すると日本語で破綻する。OSのファイル名やC連携ではUTF‑8/UTF‑16の違いに注意。

## 実践ポイント
- 日本語を扱うならまずUTF‑8を基準に考える（サーバ・多くのツール）だが、Windowsネイティブや古いAPIはUTF‑16に注意。
- 文字単位で編集するなら「コードポイント配列（rune/Vec<char>等）」か、さらに正確には「グラフェム対応ライブラリ」を使う（SwiftのCharacter相当）。
- 文字列連結が多い処理は可変バッファ／StringBuilder／ArrayList系を使って性能を確保。
- Cのchar*や外部バイト列を扱う際は終端・所有権・エンコーディングを明確にし、境界チェックを怠らない。
- テスト用に日本語（平仮名・漢字・合字・絵文字）を含むケースを必ず用意する。
- ファイル名やOS APIとやり取りする際は各言語のOsString/NSString 等の専用型を使う。

以上を押さえれば、言語ごとの「文字列地獄」から脱出して、日本語を安全かつ効率的に扱える。
