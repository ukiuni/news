---
layout: post
title: "Understanding the Go Compiler: The Linker - Goコンパイラを理解する：リンカ"
date: 2026-02-14T06:43:22.082Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://internals-for-interns.com/posts/the-go-linker/"
source_title: "The Linker | Internals for Interns"
source_id: 46936671
excerpt: "Goリンカの4大処理でバイナリが動く仕組みと最適化術を実務視点で解説"
image: "https://internals-for-interns.com/images/go-header.png"
---

# Understanding the Go Compiler: The Linker - Goコンパイラを理解する：リンカ
魅力的なタイトル: 「なぜGoのバイナリは“そのまま動く”のか？リンカが担う4つの仕事を初心者にもやさしく解説」

## 要約
リンカはパッケージごとに作られたオブジェクトファイル群を結合して、実際に実行可能なバイナリを作る。主な仕事はシンボル解決・再配置・未使用コード削除・メモリ配置と実行ファイル生成の4つ。

## この記事を読むべき理由
Goは静的リンキングを好むため、日本の開発現場（コンテナ運用、サーバレス、配布可能なバイナリ配布）で特に重要。リンカの挙動を知れば、バイナリサイズ最適化、デバッグ、cgoやプラグイン利用時の落とし穴回避に役立ちます。

## 詳細解説
- 全体像  
  コンパイラは各パッケージを個別の.o（または.a）に変換します。リンカはそれらを読み込み、プログラム全体の「どのシンボルがどこにあるか」を把握して結合します。

- 主要タスク（概念的説明）  
  1. シンボル解決：各オブジェクトの参照（例：fmt.Println）を定義側と結びつける。  
  2. 再配置（Relocation）：他パッケージへの呼び出しなどに使われた「仮のアドレス」を、最終的なメモリアドレスに書き換える。  
  3. デッドコード削除：main.mainから到達できないシンボルは除去し、静的リンクでもサイズを小さくする。  
  4. レイアウトと実行ファイル生成：.text/.rodata/.data/.bssなどのセクションを決め、OSごとの形式（ELF/Mach-O/PE）でファイル化する。エントリポイントはランタイム初期化コード（main.mainではない）になる。  

- 内部処理の流れ（簡潔）  
  1) ローダーが全シンボルを索引化し依存をたどる。  
  2) 到達可能性解析で必要なシンボルのみマーク。  
  3) セクションごとにアドレスを割当て（アラインメント等を考慮）。  
  4) 再配置レコードをもとにバイナリ内の参照をパッチ。  
  5) セグメント化してOS向けの実行ファイルを書き出す。  

- 実例（要点）  
  mainが別パッケージgreeterのHelloを呼ぶ場合、greeter.oに定義、main.oに参照（リロケーション）が入り、リンカが結合・パッチして最終バイナリを作る。コンパイラのインライン最適化が働くと、そもそもリンカの対象にならないこともある（//go:noinlineで挙動確認可）。

- 静的 vs 動的 / ビルドモード  
  デフォルトは静的リンク。cgoや共有ライブラリ利用時は動的リンクになり、インタプリタや.dyn セクションが追加される。-buildmodeで c-archive / c-shared / plugin 等に切替可。

## 実践ポイント
- 手元で確認するコマンド  
  - シンボル確認: go tool nm <binary>  
  - セクション確認: readelf -S / otool -l / dumpbin など（OS依存）  
- サイズ最適化: go build -ldflags="-s -w"（デバッグ情報削除）、不要な依存を減らす、デッドコード削除を意識する。  
- インラインの影響を見る: go build -gcflags="-m" でインラインや最適化のレポートを確認。強制的に呼び出しを残したい場合は //go:noinline を使う。  
- cgoやプラグイン利用時の注意: 動的リンクやエクスポートルールが変わるのでリンカの出力形式と依存を必ず確認する。  
- デプロイ性重視なら静的バイナリ：日本のクラウド/コンテナ環境では移植性が高く便利。ただしサイズとライセンス（システムライブラリ連携）に注意。

参考（実例コード）
```go
package main

import "example/greeter"

func main() {
    greeter.Hello()
}
```

```go
package greeter

import "fmt"

//go:noinline
func Hello() { fmt.Println("Hello") }
```

以上を押さえれば、Goのリンカが「なぜバイナリを一つにまとめ、必要な部分だけ残すのか」が実務レベルで理解できます。
