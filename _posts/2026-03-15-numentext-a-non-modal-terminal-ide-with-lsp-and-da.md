---
layout: post
title: "NumenText: a non-modal terminal IDE with LSP and DAP, inspired by Borland C++ - NumenText：Borland C++に着想を得た非モーダルなターミナルIDE"
date: 2026-03-15T00:28:00.705Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/numentech-co/numentext"
source_title: "GitHub - numentech-co/numentext: Terminal-based IDE written in Go, inspired by Borland C++ and Turbo C · GitHub"
source_id: 382446251
excerpt: "非モーダルな軽量ターミナルIDEでLSP/DAP連携し即デバッグ可能"
image: "https://opengraph.githubassets.com/6cea28482bbe089cc0ce8ad86c720c2ca6b068aa8e05b5cc6185a276270036a5/numentech-co/numentext"
---

# NumenText: a non-modal terminal IDE with LSP and DAP, inspired by Borland C++ - NumenText：Borland C++に着想を得た非モーダルなターミナルIDE
魅力的タイトル: 端末で動く「昔懐かしくもモダン」なIDE——NumenTextでサクッとデバッグとLSPを使う方法

## 要約
NumenTextはGoで書かれたシングルバイナリのターミナルIDEで、モーダル操作（vim）を学ばずに使えるメニュー駆動・非モーダル設計。LSP/DAP連携で補完・定義ジャンプ・ブレークポイント付きデバッグが可能。

## この記事を読むべき理由
ターミナルで開発する日本のエンジニアや学習中の人にとって、軽量かつ設定がシンプルなIDEは、リモートサーバやWSL上での開発、組込みや学習環境に最適。NumenTextは「学習コストが低い端末IDE」という選択肢を提示します。

## 詳細解説
- 設計思想：小さな高速Goバイナリに留め、言語固有の解析はLSP/DAPに委譲。Borland/Turbo C風のメニュー駆動UIでモーダル（vim）を強いない。
- 主要機能：
  - マルチタブ編集＋シンタックスハイライト（Chromaで20以上の言語対応）
  - 統合端末（PTY）とコマンドブロックモード
  - LSPクライアント（自動検出：gopls, pyright, clangd, rust-analyzer, typescript-language-server）で補完・定義ジャンプ・ホバー・診断
  - DAPクライアント（dlv, debugpy, lldb-vscode）でブレークポイント、step over/in/out
  - ビルド＆実行（F5実行、F9ビルド）を言語別に用意（C/C++/Go/Rust/Python/JS/TS/Java等）
  - ファイルツリー、検索/置換、コマンドパレット（Ctrl+Shift+P）、クイックオープン（Ctrl+P）
  - パネルのリサイズ、Vi/Helix風キー操作モード切替、設定は~/.numentext/config.jsonに永続
- アーキテクチャ（概略）：main.go → app wiring、editor/terminal/lsp/dap/ui/runner/filetree/config と分割。UIはtviewベースの設計方針やスタイル規約あり。
- 技術的に押さえるべき点：
  - LSP/DAPは外部サーバに依存するため、各言語のサーバを別途インストールする必要あり。
  - シングルバイナリだがビルドにはGo 1.25以上が必須。
  - モーダル操作を好まない人向けに標準で馴染みのあるCtrlショートカットが用意。

## 実践ポイント
- 試し方（ビルドして動かす）:
```bash
git clone https://github.com/numentech-co/numentext.git
cd numentext
go build -o numentext .
./numentext
```
- LSP/DAP準備：使用言語に対応するLSP（例: gopls, pyright, clangd）とDAP（dlv, debugpy, lldb-vscode）をインストールしてPATHに置く。
- 便利ショートカット：F5（実行）、F9（ビルド）、Ctrl+P（ファイル検索）、Ctrl+Shift+P（コマンドパレット）、F12（定義へ）、F11（ホバー）。
- 日本での使いどころ：リモートサーバや教育現場、軽量な開発環境、コンテナ内でのデバッグ入門に向く。WSL上でセットアップすればWindows環境でも使える。
- 貢献やカスタマイズ：設定は~/.numentext/config.jsonに保存。Goで拡張しやすい設計なので、言語サーバの自動検出追加やUI調整でコントリビュートしやすい。

（ソースはApache-2.0ライセンス、詳細はリポジトリのREADMEを参照）
