---
layout: post
title: "Rheo - Typesetting and static site engine based on Typst - Typstベースの組版＆静的サイトエンジン Rheo"
date: 2026-01-23T23:20:19.166Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/freecomputinglab/rheo"
source_title: "GitHub - freecomputinglab/rheo: Typesetting and static site engine based on Typst"
source_id: 1576283107
excerpt: "TypstベースのRheoで一度書いてPDF/HTML/EPUBを同時生成し即プレビュー可能"
image: "https://opengraph.githubassets.com/ac05db6ba298a81644135a07f2ecd893ef77a137467b51efede648c21332933c/freecomputinglab/rheo"
---

# Rheo - Typesetting and static site engine based on Typst - Typstベースの組版＆静的サイトエンジン Rheo
Typstで書いた原稿を「PDF・HTML・EPUB」で同時出力、開発サーバで即プレビューできる──Rheoでドキュメント制作が爆速に。

## 要約
TypstをベースにしたCLIツールRheoは、単一コマンドでTypstファイルをPDF/HTML/EPUBへ同時コンパイルし、ライブリロード付きの開発サーバや相対リンク調整、EPUB/PDFのマージ機能などを備えた静的サイト＆組版エンジンです。

## この記事を読むべき理由
日本のドキュメンテーション制作、技術ブログ、同人・電子出版の現場で「一度書いて複数フォーマット出力」を効率化できるツールだから。特にEPUB需要が高い日本市場では、章結合や書籍生成の自動化に有用です。

## 詳細解説
- コア技術：Typst（新世代の組版言語）を利用。RheoはRustで実装されたCLIで、Typstソースを同時にPDF/HTML/EPUBへ出力する。
- マルチフォーマット：デフォルトで3形式を同時生成。必要な形式だけ出力するフラグもあり（--pdf/--html/--epub）。
- 開発ワークフロー：watchモードでファイル変更を監視し、自動再コンパイル。--openで http://localhost:3000 の開発サーバを起動しブラウザ自動更新。
- 相対リンク処理：出力形式に応じてクロスドキュメントリンクを自動変換。存在しないリンクはコンパイル時に詳細エラーを返す。
- PDF/EPUB結合（spine）：rheo.tomlで複数ファイルを結合して1冊の本を作成可能。glob指定と辞書順ソートで目次順を制御。
- カスタマイズ：プロジェクトルートのstyle.cssをHTMLに注入して見た目を調整。rheo.tomlで細かい挙動を設定できる。
- インストール：Rust/Cargo経由が推奨。Nix flakesからの開発環境導入もサポート。ライセンスはApache-2.0かMITを選択可能。

## 実践ポイント
- インストール（Cargo推奨）
```bash
# Rustが必要
cargo install rheo
```
- 全出力を監視して起動
```bash
rheo watch examples/blog_site --open
```
- 特定フォーマットのみ出力
```bash
rheo compile my_project --pdf --html
```
- EPUB/PDFを結合する簡単なrheo.toml例
```toml
[pdf.spine]
title = "My Book"
vertebrae = ["cover.typ", "chapters/**/*.typ"]
merge = true
```
- カスタムスタイル：プロジェクト直下にstyle.cssを置くだけでHTMLに反映される
- 使いどころ：技術文書の多言語同時配布、学術資料の電子化、ブログをPDF同梱で配るワークフローに最適

短時間で複数フォーマットを手元で生成・確認したいなら、まずはcargoで入れてwatchモードを試してみてください。
