---
layout: post
title: "getopt: Go package for POSIX/GNU-style command line parsing - getopt: POSIX/GNUスタイルのコマンドライン解析用Goパッケージ"
date: 2026-03-03T08:49:24.475Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://pkg.go.dev/gitlab.com/natano/getopt"
source_title: "getopt package - gitlab.com/natano/getopt - Go Packages"
source_id: 1509094617
excerpt: "GoでPOSIX/GNU風CLIを簡潔に実装できるハンドラ型の高速なコマンドラインパーサ。"
---

# getopt: Go package for POSIX/GNU-style command line parsing - getopt: POSIX/GNUスタイルのコマンドライン解析用Goパッケージ
使い慣れたUnix風オプションをGoで手早く実装できる、柔軟なハンドラ型コマンドラインパーサ

## 要約
gitlab.com/natano/getoptは、POSIX/GNUスタイルの短縮・長いオプションをサポートするGo用パーサで、グローバル状態に依存せずハンドラ関数で逐次処理する設計が特徴です。型付き取得ヘルパーやオプションの順序依存ロジックを簡単に組めます。

## この記事を読むべき理由
Unix系ツール文化が強い日本の現場では、短縮オプションの組合せや短⇄長名の併置が当たり前。GoでCLIツールや内部ユーティリティを書く機会が多い開発者にとって、期待どおりの挙動を短時間で実装できる実用的な選択肢です。

## 詳細解説
- 基本設計  
  - Getopt(args []string, fn func(*Option) error) を使い、見つかった各オプションごとにハンドラを呼び出す。ハンドラ内で Option.Arg 系を呼ぶとそのオプションは引数を持つと解釈される。戻り値として残りの非オプション引数を返す。
  - グローバル状態を使わず、全て error インターフェースで返す点はGoらしい設計。

- サポートする構文（POSIX/GNU準拠）  
  - 短オプション: -a, -b arg, 複数結合 -abcd（最後のみ引数可）  
  - 長オプション: --long, --opt=val または --opt val（ただしオプションの実装次第）  
  - オプションの途中で "--" を置くと以降はオプション解析を停止。  
  - オプションと引数の混在（flags と args の intersperse）はサポートしない（POSIX準拠の挙動）。

- 型付き引数取得とAPIの利便性  
  - Arg, ArgInt/ArgIntVar, ArgFloat64, ArgTextVar（encoding.TextUnmarshaler対応）など多数のヘルパーを提供。ArgVar はポインタに値を代入してエラーだけ返すため1行で処理できる。  
  - Optional argument（省略可能引数）は同一トークンに結合して渡す必要があり、HasConjoinedArg() で判定できる。長オプションの結合引数が未消費だとエラーになる。

- 実用面の特徴  
  - オプションを事前定義しない（宣言的でない）ため、使い方説明（usage）は手書きが必要だが、オプション順や条件付きオプション（例：--format=mp3 のときにだけ有効な設定）など柔軟な振る舞いが実装しやすい。  
  - ライセンスは ISC、タグ付き v1.0.0（安定）で公開（公開日: 2026-03-02）。

- 代替案  
  - 標準の flag パッケージはPOSIX型ではない。pflag（github.com/spf13/pflag）は互換性あるドロップイン代替で、オプションと引数の混在もサポート（切替可）。

## 実践ポイント
- まずは最小のハンドラ型で試す（残り引数を受け取れる点を確認）:
```go
package main

import (
  "fmt"
  "os"
  "gitlab.com/natano/getopt"
)

func main() {
  args, err := getopt.Getopt(os.Args[1:], func(opt *getopt.Option) error {
    switch opt.Name() {
    case "-a", "--all":
      // フラグ処理
      return nil
    case "--bind":
      // TextUnmarshaler を使う型へ直接格納可能
      var addr string
      return opt.ArgVar(&addr)
    case "-v", "--verbose":
      if opt.HasConjoinedArg() {
        return opt.ArgIntVar(&someVerbosity)
      }
      someVerbosity++
      return nil
    }
    return opt.Unknown()
  })
  if err != nil { /* エラー処理 */ }
  fmt.Println("args:", args)
}
```
- 実務で選ぶ基準  
  - 短縮オプションの結合や長短併用、順序依存ロジックが必要ならこのパッケージが便利。簡易スクリプトや依存を増やしたくない場合は標準 flag で十分。
- 注意点  
  - Usage文字列は自前で用意する必要があること、オプションと引数の「混在」を期待する設計ではないこと、optional arg は同一トークンで渡す必要がある点に留意する。

以上を踏まえ、GoでUnixライクなCLIをきめ細かく制御したい場面ではnatano/getoptは即戦力になります。
