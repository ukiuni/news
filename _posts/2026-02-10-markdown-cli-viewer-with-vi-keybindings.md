---
layout: post
title: "Markdown CLI viewer with VI keybindings - VI風キーバインドのMarkdown CLIビューア"
date: 2026-02-10T18:54:32.978Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/taf2/mdvi"
source_title: "GitHub - taf2/mdvi: cli based Markdown viewer"
source_id: 46963865
excerpt: "Vim風操作と高速レンダリングで端末上のMarkdown閲覧を劇的に快適化するmdvi"
image: "https://opengraph.githubassets.com/02ee755e9394c15a52b46521713f78cd149cdf3325791ff9b5d084bb55ce96e0/taf2/mdvi"
---

# Markdown CLI viewer with VI keybindings - VI風キーバインドのMarkdown CLIビューア
魅了タイトル: ターミナルでVim感覚の高品質Markdown閲覧を――mdviでドキュメントが読みやすくなる理由

## 要約
Rust製のフルスクリーン端末Markdownビューア「mdvi」は、Vimライクな操作感と高品質レンダリング、ライブリロードを備えた軽量ツールです。大きなドキュメントやリモート環境での読み物に最適。

## この記事を読むべき理由
ローカルやサーバ上でMarkdownを読む機会が多い日本のエンジニア／ドキュメント担当にとって、GUIを起動せずに高速で読みやすい表示と直感的なキーバインドを得られる実用的な選択肢だからです。

## 詳細解説
- コア技術: Rustで実装。端末制御は crossterm、TUIは ratatui、Markdownパースは pulldown-cmark を利用し、単一バイナリで高性能かつ配布が容易。
- 表示機能: 見出し、リスト／タスクリスト、引用、コードブロック／インラインコード、リンク、表、脚注、強調／取り消し線など主要Markdown要素を高品質にレンダリング。
- 操作性: Vim風キー（j/k, g/G, Ctrl‑f/b など）に加え、矢印・PageUp/Down・Home/Endなど標準キーもサポート。検索（/）、次/前検索（n/N）、ヘルプトグル（?）、リロード（r）、特定行から開始（--line）など実用的な機能を持つ。
- 開発・配布: cargoでビルド可能。Homebrewタップも用意されており、macOSやLinux（Homebrew対応）で簡単に導入できる。Rust製のため大ファイルでも高速。

## 実践ポイント
- インストール（例: Homebrew / ソース）
```bash
# Homebrew
brew tap taf2/tap
brew install mdvi

# ソースから
cargo install --path .
```
- すぐ試す: mdvi README.md、特定行から開く: mdvi --line 120 docs/spec.md
- CIログやテスト失敗の出力行を指定してローカルで素早く確認するワークフローに組み込むと便利。
- less や bat の代替として、リモートサーバ上やターミナル中心の開発環境でのドキュメント閲覧に導入を検討する価値あり。
