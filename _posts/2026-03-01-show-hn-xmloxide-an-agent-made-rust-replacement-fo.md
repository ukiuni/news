---
layout: post
title: "Show HN: Xmloxide – an agent made rust replacement for libxml2 - Xmloxide — libxml2のRust製リプレイス"
date: 2026-03-01T01:35:18.051Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/jonwiggins/xmloxide"
source_title: "GitHub - jonwiggins/xmloxide: A pure Rust reimplementation of libxml2"
source_id: 47201816
excerpt: "libxml2互換で安全高速なRust製xmloxide—100%準拠で置換可"
image: "https://opengraph.githubassets.com/de006ed166f217de778be66c185d1404f611067dfbbd2fee0a4911dfc94b3e21/jonwiggins/xmloxide"
---

# Show HN: Xmloxide – an agent made rust replacement for libxml2 - Xmloxide — libxml2のRust製リプレイス

もうlibxml2に泣かない — Rustで書かれた「xmloxide」が安全性と速度を両立する次世代XML/HTMLライブラリ

## 要約
xmloxideはlibxml2を置き換えることを目指した純Rust再実装。メモリ安全（public APIにunsafeなし）、W3C準拠テスト100%合格、高性能なシリアライズとXPathを特徴とするライブラリ。

## この記事を読むべき理由
日本の多くの既存システム（組み込み、サーバ、ブラウザ周辺、ゲーム等）はC/C++製のlibxml2に依存している。libxml2のメンテ状況やセキュリティリスクを懸念するなら、xmloxideは実用的な“安全で高速な代替”になり得る。

## 詳細解説
- コア設計
  - ArenaベースのDOMツリーで高速シリアライズを実現。public APIにunsafeを含めない設計でメモリ安全。
  - ドキュメントごとに状態を持ち、グローバルステートなし（Send + Sync）。
  - C/C++向けの完全なFFIを提供（include/xmloxide.h）で既存Cコードへの置換を支援。

- 対応機能（libxml2相当または互換）
  - XML 1.0パーサ（エラー回復あり）、HTML 4.01パーサ（誤り耐性）、DOM/SAX2/XmlReader（プル）/Push（増分）API
  - XPath 1.0（完全な式パーサと評価器）、DTD/RelaxNG/XSDバリデーション、C14N、XInclude、XML Catalogs
  - xmllint互換CLIで既存ワークフローに入りやすい

- テストと互換性
  - W3C XML Conformance Test Suite：1727/1727（100%）
  - libxml2互換スイート：119/119（100%）
  - ユニットテスト785件、FFIテスト112件、ファジングターゲットあり

- パフォーマンス（要点）
  - 解析スループットはlibxml2とほぼ互角（多くの文書で3–4%差、SVGでは12%高速）
  - シリアライズは1.5–2.4×高速
  - XPathは1.1–2.7×高速
  - 主要最適化例：byteレベルの文字検査、バルクテキスト走査、ASCII高速経路、名前テストの高速化、ゼロコピー要素名分割等

- 制約
  - XML 1.1非対応、HTMLはHTML5ではなくHTML 4.01向け、XSLT/ Schematron非対応
  - PushParserは現在バッファリング方式（真のストリーミングとは異なる）

## 実践ポイント
- すぐ試す（Rust）
```rust
rust
use xmloxide::Document;
let doc = Document::parse_str("<root><child>Hello</child></root>").unwrap();
let root = doc.root_element().unwrap();
assert_eq!(doc.node_name(root), Some("root"));
```
- C/C++プロジェクトでの置換はFFIヘッダを利用：
```c
c
#include "xmloxide.h"
xmloxide_document *doc = xmloxide_parse_str("<root>Hello</root>");
```
- 実プロジェクト導入時の手順（推奨）
  1. 既存libxml2ベースのユニットテストをxmloxideで走らせ互換性を確認
  2. 大きなドキュメントはSAXストリーミングで検証（メモリ制約対策）
  3. C/C++埋め込みならinclude/xmloxide.hで段階的移行
  4. セキュリティ重視ならcargo-fuzzでファジング実行（nightlyが必要）

- 主要コマンド
  - ビルド／テスト：cargo build / cargo test
  - ベンチ（libxml2比較）：cargo bench --features bench-libxml2 --bench comparison_bench
  - Cライブラリ作成：make / make shared / make static

xmloxideは「既存のXMLワークロードをメモリ安全にしつつ、性能も維持・向上したい」場面で有力な選択肢。まずは既存テストを流して互換性を確かめるのが最短の一歩。
