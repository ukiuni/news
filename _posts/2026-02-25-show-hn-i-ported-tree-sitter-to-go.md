---
layout: post
title: "Show HN: I ported Tree-sitter to Go - Tree-sitterをGoに移植しました"
date: 2026-02-25T19:34:54.384Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/odvcencio/gotreesitter"
source_title: "GitHub - odvcencio/gotreesitter: Pure Go tree-sitter runtime"
source_id: 47155597
excerpt: "純Go化でC依存を廃し、WASM対応かつ超高速なインクリメンタル解析を実現"
image: "https://opengraph.githubassets.com/d0823a0b082987fef9e0c4b7abf834e0a7a9ba314b7f3e1683ece3d27a7dab6b/odvcencio/gotreesitter"
---

# Show HN: I ported Tree-sitter to Go - Tree-sitterをGoに移植しました
エディタの心臓を純Goで再実装 — Tree-sitterがC依存を捨てて高速化した理由と使いどころ

## 要約
Tree-sitterのランタイムを「純Go」で再実装したプロジェクト gotreesitter は、CGo不要でクロスコンパイルやWASMに強く、特にインクリメンタル編集が圧倒的に高速です。

## この記事を読むべき理由
エディタ／言語サーバー／静的解析ツールを作る日本の開発者にとって、Cツールチェーン不要で導入しやすく、CIや配布が楽になる実務的メリットがあります。軽量で高速なパーサーはエディタ体験やCIパフォーマンスに直結します。

## 詳細解説
- コア方針：gotreesitterはtree-sitterのパーステーブル形式をそのまま使うが、実行系は完全にGoで再実装（CGoゼロ）。そのため任意プラットフォームでgo build/go getが動作し、WASMビルドも現実的に。
- パフォーマンス：ベンチマークではフルパースが約1.33ms（C版2.06ms、約1.5x高速）、インクリメンタル単一バイト編集は約1.38μs（C版124μs、約90x高速）、無変更の再解析は8.6ns（C版121μs、約14,000x）と報告。インクリメンタル経路でサブツリーを積極的に再利用する設計が効いています。
- 機能互換：既存のtree-sitter文法（パーステーブル）を流用可能。S式クエリ、カーソルストリーミング、構造量指定子、各種述語（#eq? 等）やハイライター、タグ抽出（symbol tagging）をサポート。
- 言語サポート：205の文法が同梱（204が「full」品質）。一部（例：norg）は外部スキャナ未移植で部分的にしか解析できない点に注意。
- アーキテクチャ：テーブル駆動LR(1)＋GLR、アリーナアロケータ（GC負荷低減）、DFAレキサ、外部スキャナVM、クエリエンジン、ハイライタ／タグガー等をGoで実装。文法はts2goツールでバイナリ化して読み込む仕組み。
- 配布オプション：文法バイナリを埋め込むか外部ファイル化（-tags grammar_blobs_external＋環境変数）してバイナリサイズと起動挙動を制御可。

短いサンプル（クイックスタート）:

```go
package main

import (
	"fmt"
	"github.com/odvcencio/gotreesitter"
	"github.com/odvcencio/gotreesitter/grammars"
)

func main() {
	src := []byte("package main\nfunc main() {}\n")
	lang := grammars.GoLanguage()
	parser := gotreesitter.NewParser(lang)
	tree := parser.Parse(src)
	fmt.Println(tree.RootNode().Type())
}
```

## 実践ポイント
- まず試す：go get github.com/odvcencio/gotreesitter で導入し、grammars.DetectLanguage("foo.go") → NewParser → ParseIncremental の流れを試す。
- エディタ統合：VS Code拡張やLSPでインクリメンタルパース／ハイライトを任せれば、入力遅延の改善が期待できる。
- CIと配布：Cツールチェーンを用意せずにクロスコンパイル可能なので、コンテナやCIイメージの簡素化に有効。
- バイナリサイズ制御：全言語埋め込みが不要なら -tags grammar_blobs_external と GOTREESITTER_GRAMMAR_BLOB_DIR を使って外部バイナリ化。
- 拡張：独自文法を追加するには grammars/languages.manifest を編集し ts2go を実行する手順に従う。
