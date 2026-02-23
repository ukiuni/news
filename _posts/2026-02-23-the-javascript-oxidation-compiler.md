---
layout: post
title: "The JavaScript Oxidation Compiler - JavaScript酸化コンパイラ"
date: 2026-02-23T04:16:42.759Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://oxc.rs/"
source_title: "The JavaScript Oxidation Compiler"
source_id: 47117459
excerpt: "Rust製の超高速JSツールチェーンOxcでCIと開発待ち時間を大幅短縮"
image: "https://oxc.rs/og.jpg"
---

# The JavaScript Oxidation Compiler - JavaScript酸化コンパイラ
驚異の高速ツールチェーンで「開発の待ち時間」を一気に短縮する新世代JSツール

## 要約
Rustで実装された高速なJavaScript/TypeScriptツール群（lint/format/parse/transform/minify/resolver）。既存のエコシステム互換を保ちつつ、ESLint/Prettier等より圧倒的に高速をうたうのが特徴。

## この記事を読むべき理由
日本の開発現場でもモノレポやCI時間短縮、TypeScript増加によるビルド負荷が課題。Oxcは「そのまま置き換えやすく」「高速」で、開発速度とコスト削減に直結する可能性があるため注目に値する。

## 詳細解説
- コア思想：Rustで書かれた単一エコシステム（Oxlint/Oxfmt/oxc-parser/oxc-transform/oxc-resolver/oxc-minify）で高速処理を実現。
- Linter（Oxlint）
  - ESLint互換、650以上のルール。
  - Type-aware linting（tsgo）で型情報を活かした検出が可能。
  - 公称50〜100倍高速（ESLint比）。
- Formatter（Oxfmt、Alpha）
  - Prettier互換、Tailwindクラスソート対応。
  - Biomeより3倍、Prettierより35倍高速と報告。
- Parser（oxc-parser）
  - .js/.jsx/.ts/.tsx対応、Test262 stage4全テスト通過。
  - ベンチマーク例：Oxc 26.3ms vs SWC 84.1ms vs Biome 130.1ms（M3 Maxでのtypescript.js）。
- Transformer（oxc-transform）
  - TypeScript/JSXの構文低減やDTS出力、React Fast Refresh対応など。
- Resolver（oxc-resolver）
  - Node互換のCJS/ESM解決、enhanced-resolveと挙動合わせつつ28倍高速。
- Minifier（oxc-minify、Alpha）
  - DCE、構文短縮、変数名マングリングなどを実装。
- OSSかつスポンサー運営：導入障壁が低くカスタマイズ性が高い点も強み。

## 実践ポイント
- まずはPlaygroundで小さなファイルを試し、パース/整形/リンティングの互換性を確認する。
- CIでは段階的移行を推奨：まずはフォーマッタ→リンタ→パーサ/トランスパイラの順で差し替える。
- ESLint/Prettierの既存設定が活かせるため、既存ルールを流用して比較ベンチを取る（CI時間短縮の効果測定）。
- TypeScriptを多用するプロジェクトは型情報を使ったOxlintの恩恵が大きい。
- 大規模リポジトリやMonorepo、GitHub ActionsやSelf-host CIでの導入は特に効果あり。まずはホットパス（ビルドやPRのチェック時間が長い箇所）で試すと採算が見えやすい。
