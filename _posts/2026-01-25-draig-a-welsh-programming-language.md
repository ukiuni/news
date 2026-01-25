---
layout: post
title: "Draig, a Welsh Programming Language - Draig（ウェールズ語のプログラミング言語）"
date: 2026-01-25T03:05:58.791Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://raku.land/zef:l10n/L10N::CY"
source_title: "Draig, a Welsh Programming Language"
source_id: 46721421
excerpt: "母語でプログラミング可能にするRaku派生「Draig」の導入と実例"
---

# Draig, a Welsh Programming Language - Draig（ウェールズ語のプログラミング言語）
魅力タイトル: コードを母語で書く──ウェールズ語Raku「Draig」が示すローカライズの未来

## 要約
ウェールズ語ローカライズ版のRaku（L10N::CY）は、キーワードや実行ツールを母語化してコードをウェールズ語で書けるようにする実験的プロジェクトです。付属の実行バイナリ draig や `use L10N::CY` 宣言で簡単に切り替えできます。

## この記事を読むべき理由
英語以外の言語でプログラミング環境を提供する取り組みは、教育や地域言語保存、非英語話者の敷居を下げる可能性があります。日本でもローカライズや多言語サポートの意義を考える際、実践例として参考になります。

## 詳細解説
- L10N::CY は Raku 言語のウェールズ語ローカライズを担う配布物（distribution）。ウェールズ語化されたキーワードや標準出力表現を提供します。
- インストール後は draig という実行ラッパーが使え、これを通すだけでウェールズ語環境が自動で有効になります。プログラム内で局所的に有効にしたい場合は `use L10N::CY;` を使います。
- 実行例（端末で）:
```bash
$ export RAKUDO_RAKUAST=1
$ draig -e 'dywedyd "Helo Byd"'
Helo Byd
```
- 技術的に、言語ローカライズはキーワード、エラーメッセージ、標準ライブラリの表記などを翻訳・マッピングする必要があり、コンパイラ／パーサー周りの調整やツールチェーン（デバッガ、IDE統合など）対応が課題になります。
- ライセンスは Artistic License 2.0。プロジェクトや実装の詳細は Raku Localization Team とリンク先の解説記事（例：Creating a new programming language - Draig）を参照できます。

## 実践ポイント
- まずは VS Code の統合ターミナルで上記コマンドを試し、draig が出力するメッセージやキーワードを確認してみてください。
- 教育用途なら、母語での入門教材やワークショップを試作してみると効果を測れます。
- 日本語や地域言語へのローカライズを検討する際は、キーワード設計、ツールの互換性、チームの合意（混在する英語コードとの扱い）を事前に決めると導入がスムーズです。
