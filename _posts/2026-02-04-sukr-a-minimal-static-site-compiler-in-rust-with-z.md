---
layout: post
title: "Sukr: A minimal static site compiler in Rust with zero-JS output - Sukr：ゼロJS出力の最小限静的サイトコンパイラ"
date: 2026-02-04T15:58:18.171Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://sukr.io"
source_title: "sukr | Sukr Documentation"
source_id: 1158973545
excerpt: "ビルド時にKaTeX/Mermaid埋め込みのRust製ゼロJS静的サイト生成ツールです"
---

# Sukr: A minimal static site compiler in Rust with zero-JS output - Sukr：ゼロJS出力の最小限静的サイトコンパイラ
ゼロJSで軽量・高速、しかもビルド時にKaTeXやMermaidを処理する「sukr」を試してみたくなる理由

## 要約
sukrはRust製のミニマルな静的サイトコンパイラで、クライアント側にJavaScriptを残さずMarkdownから高性能なHTMLを生成する。コードハイライトはtree-sitter、数式はKaTeX、図はMermaidをビルド時にインライン化するのが特徴。

## この記事を読むべき理由
日本のサイトでも「表示速度」「SEO」「プライバシー（広告・解析の削減）」が重視されており、クライアントJSを減らすアプローチは実運用で価値が高い。国内の技術ブログやドキュメント、オープンソースのサイトに向く実践的な選択肢です。

## 詳細解説
- ゼロJS出力：sukrはクライアントでの重いランタイムを排除し、純粋な静的HTMLを生成。初回表示が速く、モバイル回線でも有利。
- Tree-sitterハイライト：正規表現ではなく構文解析器を使った正確なシンタックスハイライトを提供。言語内挿入（例：Nix→Bash、HTML→JS/CSS）にも対応。
- ビルド時KaTeX：LaTeX数式をサーバ側でKaTeXに変換し、300KB級のクライアントJSバンドルを不要にする。
- Mermaid→SVG：Mermaidをビルド時にSVGへ変換してインライン化。読み込み遅延が不要で瞬時に図が表示される。
- テンプレート：Teraテンプレートをランタイムで読み込めるため、再コンパイルなしでテンプレート修正が可能。
- モノレポ対応：設定ファイルを切り替えて複数サイトをビルドできるため、ドキュメント群や複数プロダクトに適する。
- 実装言語：Rustで書かれており、高速かつ依存を最小化したビルドが期待できる。

## 実践ポイント
- インストールと簡単な初期構成
```bash
cargo install sukr
mkdir -p content templates static
echo 'title = "My Site"' > site.toml
echo 'author = "Me"' >> site.toml
echo 'base_url = "https://example.com"' >> site.toml
sukr # ビルド実行
```
- 数式や図を使う場合はMarkdown内に通常通り記述すれば、ビルド時にKaTeX/Mermaidが静的に埋め込まれる。
- 日本語コンテンツ：UTF-8で問題なく動作。テンプレートでmetaやlang属性を適切に設定してSEOを最適化する。
- デプロイ：生成物は静的HTMLなのでGitHub Pages、Netlify、Vercel、CDNにそのまま置ける。JSを削ぎ落としたサイトは帯域と読み込み時間の節約になる。
- 移行検討：既存のJS重視なサイト（動的ウィジェットが多いもの）は段階的な切り替えを推奨。ドキュメントやブログなど静的コンテンツから導入すると効果が分かりやすい。

元記事のドキュメントは公式サイト（https://sukr.io）で詳細を参照してください。
