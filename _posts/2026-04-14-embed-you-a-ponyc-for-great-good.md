---
layout: post
title: "Embed You a ponyc for Great Good - ponycを埋め込んで大いなる善を"
date: 2026-04-14T16:02:48.268Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.ponylang.io/blog/2026/04/embed-you-a-ponyc-for-great-good/"
source_title: "Embed You a ponyc for Great Good - Pony"
source_id: 1424160544
excerpt: "libponyc-standaloneでコンパイラを自己完結化し配布・検証負担を激減"
---

# Embed You a ponyc for Great Good - ponycを埋め込んで大いなる善を

コンパイラを丸ごと一つのバイナリにして、ツール作りと配布を劇的に楽にする方法

## 要約
Ponyのコンパイラ本体はライブラリ化されており、libponyc-standaloneという「静的にまとめた .a」によって、依存関係を気にせず自己完結型のツールを作れるようになった、という話です。Pony側のラッパー（pony-ast）がASTやコンパイルパイプラインへ便利なAPIを提供します。

## この記事を読むべき理由
依存関係や環境差分で悩むことが多い日本の現場（オンプレ／組み込み／CI）にとって、コンパイラを自己完結バイナリ化する発想は配布・検証・クロスビルドの負担を大きく減らします。言語サーバやリンター、ドキュメント生成器を自前で作る際の設計指針にもなります。

## 詳細解説
- libponyc と ponyc:
  - ponyc は日常的に使うコマンドライン側の薄いラッパー（Cで約149行）で、本体は libponyc というライブラリです。
- libponyc-standalone の狙い:
  - LLVM、ランタイム、補助ライブラリを全部まとめて単一の静的ライブラリ（.a）に梱包。リンクすれば共有ライブラリを別途配る必要がなく、環境依存の「動くのは自分のマシンだけ」問題を避けられます。
  - APIはCで公開されるため、C/Rust/Go/Ponyなど任意の言語でラッパーを作れます。
- Pony側の「きれいな」ラッパー（pony-ast）:
  - ponycリポジトリ内 tools/lib/... にある Pony ラッパーは、Compiler.compile(source_dir, [pony_path], limit=PassFinaliser) のようなAPIを提供します。
  - 成功時は Program を、失敗時は Array[Error] を返す。Error はファイル位置やメッセージを持つ構造体で、ただの文字列ではありません。
  - limit パラメータで「どこまでパイプラインを走らせるか」（parse / typecheck / finalize / codegen 等）を指定でき、言語サーバは typecheck で止める、ドキュメント生成は codegen を省く、といった使い分けが可能です。
  - Program はパッケージ→モジュール→AST とツリー構造で辿れます。
- なぜまだ標準ライブラリに入っていないか:
  - 現状は tools 配下で実験中。API が発展途上なので、安定した形にまとまってから標準ライブラリへ移行する方針です。
- 使い道の実例:
  - pony-lsp（言語サーバ）、pony-lint（リンター）、pony-doc（ドキュメント生成）。それぞれ wrapper を異なる形で使い、LSPはアクターで並列にコンパイル、リンターはASTを歩き回り、ドキュメントは型付き宣言を読む、という具合です。

## 実践ポイント
- まずは repo の tools/lib/ponylang/pony_compiler を覗き、Compiler.compile の使い方を確認する。
- ラッパー言語は既存技術に合わせて選択（C/Rust/Go/Pony）。C API なので相互運用は容易。
- 静的リンクは配布が楽だがバイナリ肥大やライセンス面に注意。用途に応じて静的／動的を選ぶ。
- API はまだ変わる可能性があるため、ツール開発時はリリースやブランチを明示的に固定して運用する。
- 日本の組み込み・CI・オフライン環境では特に有用。Raspberry PiやRISC‑Vなどクロスコンパイル環境での自己完結バイナリは配布コストを下げる。

---
