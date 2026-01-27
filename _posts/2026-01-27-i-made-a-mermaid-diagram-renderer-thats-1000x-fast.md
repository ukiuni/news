---
layout: post
title: "I made a Mermaid diagram renderer that's 1000x faster by not spawning Chrome for every render - Chromeを毎回起動しないで1000倍速にしたMermaidレンダラーを作った"
date: 2026-01-27T20:46:15.802Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/1jehuang/mermaid-rs-renderer"
source_title: "GitHub - 1jehuang/mermaid-rs-renderer: A fast native Rust Mermaid diagram renderer. No browser required. 500-1000x faster than mermaid-cli."
source_id: 415927251
excerpt: "Chromium起動不要でMermaid図を最大1000倍高速生成、CIで即時反映"
image: "https://opengraph.githubassets.com/0105676abdee0b077df527a8983210adebf789f1900dc7c833222c1096c3ed27/1jehuang/mermaid-rs-renderer"
---

# I made a Mermaid diagram renderer that's 1000x faster by not spawning Chrome for every render - Chromeを毎回起動しないで1000倍速にしたMermaidレンダラーを作った

Chromeを開かずにMermaid図をネイティブRustで高速レンダリングするツール「mmdr」。CIやドキュメント自動生成で待ち時間ゼロに近い体験を実現します。

## 要約
mmdrはMermaidのパース〜レイアウト〜SVGレンダリングをRustでネイティブ実装し、Chromiumを毎回起動するmermaid-cliに比べて500〜1000倍（ケースによって最大で1800x）高速化しています。

## この記事を読むべき理由
CIや静的サイト生成、リアルタイムプレビューでMermaid図を多用する日本の開発現場では、ブラウザ起動コストがボトルネックになりがちです。mmdrはその問題を根本から解消し、ビルド時間短縮や開発体験の改善に直結します。

## 詳細解説
- 問題点：mermaid-cliはレンダリングごとにヘッドレスChromiumをPuppeteer経由で起動するため、コールドスタートで約2秒以上、メモリも数百MB消費します。図を大量に生成するCIやドキュメント生成ではこれが致命的に遅い。
- 解決法：mmdrはMermaid文法のパーサ、内部IR、レイアウト（dagre_rust）、SVGレンダラをRustで実装。ブラウザやNode.js依存を排除し、ネイティブバイナリ/ライブラリとして動作します。
- ベンチマーク（代表値）：Flowchartレンダリングで mmdr ≒ 2.75ms、mermaid-cli ≒ 2,636ms → 約958x。ライブラリとして組み込めば更にプロセス生成オーバーヘッドが減り高速化。
- 機能：13種類のMermaid図をサポート（flowchart, sequence, class, state, er, pie, gantt, mindmap等）、ノード形状・エッジスタイル・class/style/テーマ設定・出力PNG/SVG対応。
- パイプライン比較：
  - mmdr: .mmd → parser.rs → ir.rs → layout.rs → render.rs → SVG → (resvg → PNG)
  - mermaid-cli: .mmd → mermaid-js → dagre → Browser DOM → Puppeteer → Chromium → Screenshot → PNG
- リソース差：コールドスタート ~3ms / メモリ ~15MB（mmdr） vs ~2000ms / 300+MB（mermaid-cli）。

## 実践ポイント
- CLIで試す（macOS/Linux Homebrew例）:
```bash
brew tap 1jehuang/mmdr && brew install mmdr
echo 'flowchart LR; A-->B-->C' | mmdr -e svg > diagram.svg
```
- CIで大量図生成するならmermaid-cliをmmdrに置き換えるだけで数分→数秒に短縮できます。
- 静的サイトジェネレータ（例：Zola）などに組み込む場合、依存を減らすために crate を default-features = false で使うと軽量化できます。
```toml
[dependencies]
mermaid-rs-renderer = { git = "https://github.com/1jehuang/mermaid-rs-renderer", default-features = false }
```
- Rustでタイミング情報を取りたいとき:
```rust
use mermaid_rs_renderer::{render_with_timing, RenderOptions};
let result = render_with_timing("flowchart LR; A-->B", RenderOptions::default()).unwrap();
println!("Rendered in {:.2}ms", result.total_ms());
```
- 注意点：非常に高速ですが、ノード数が増えるとレイアウト計算コストが支配的になり、速度差は小さくなる場合があります。大規模図でも100x以上の改善が期待できます。

mmdrはCIの高速化、ローカルでの即時プレビュー、軽量デプロイが欲しい開発チームにとって即戦力です。興味があればリポジトリのREADMEでインストールとサンプルを試してみてください。
