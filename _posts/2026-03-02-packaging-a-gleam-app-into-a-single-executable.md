---
layout: post
title: "Packaging a Gleam app into a single executable - Gleamアプリを単一実行ファイルにパッケージする"
date: 2026-03-02T19:56:12.855Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.dhzdhd.dev/blog/gleam-executable"
source_title: "Portfolio"
source_id: 1398021591
excerpt: "GleamアプリをErlang/Javascript両ルートで単一実行ファイル化する実践比較ガイド"
image: "https://github.com/dhzdhd/Portfolio-v3/blob/master/static/favicon.png?raw=true"
---

# Packaging a Gleam app into a single executable - Gleamアプリを単一実行ファイルにパッケージする
Gleamで作ったアプリを“配布できる一つの実行ファイル”にする方法を、手早く比較・実践できる形で整理します。

## 要約
GleamはErlang/JavaScriptへコンパイルできる軽快な関数型言語だが、実行ファイル化は標準サポートがない。本稿はErlang側とJavaScript側それぞれの実行ファイル化ルート（Gleescript、Burrito、Deno、Node SEA、Bun、Nexe等）を比較し、手順と利点・注意点を示します。

## この記事を読むべき理由
Gleamは国内でも関心が高まりつつあり、社内配布やツール化で「ランタイム不要の単一ファイル」が欲しくなる場面が増えます。実環境（Linux/Windows/Mac）で動かすための現実的な選択肢と実践手順を把握できます。

## 詳細解説
基本：プロジェクト作成後、ターゲットを指定してビルドする
```bash
# プロジェクト作成
gleam new <project_name>

# ビルド（どちらかを選ぶ）
gleam build --target=erlang
gleam build --target=javascript
```

Erlangターゲット
- Gleescript（escript ベース）
  - 概要：escriptを作成してErlang VM上で実行する方法。
  - 長所：作り方がシンプル。小さめのバイナリ。
  - 短所：実行には対象マシンにErlang VM が必要。
  - 手順（最小例）：
    ```bash
    gleam add gleescript
    gleam build --target=erlang
    gleam run -m gleescript
    ./your_project
    ```
- Burrito（BEAMを丸ごと同梱）
  - 概要：ERTS（Erlangランタイム）を同梱してself-containedにするツール。
  - 長所：ホストにErlang不要で配布可能。
  - 短所：Gleamとの組合せ事例が少なく調整が必要な場合あり。

JavaScriptターゲット
- Deno compile（bundler＋deno compile）
  - 概要：生成されたJSをバンドル（esbuild等）してから、Denoで実行ファイル化する。Denoランタイムを軽量に同梱。
  - 長所：手順が比較的単純でマルチプラットフォーム対応。
  - 短所：実行ファイルは大きめ。Denoの権限設定が必要な場合あり。
  - 手順（例）：
    ```bash
    gleam build --target=javascript

    # esbuildで束ねる（例）
    esbuild build/dev/javascript/<project>/<project>.mjs \
      --platform=node --bundle --minify-whitespace --minify-syntax \
      --outfile=bundle.cjs --format=cjs --footer:js="main();"

    deno compile --target=<target_arch> --output <executable_name> bundle.cjs
    ```
- Node SEA（Single Executable Applications、実験的）
  - 概要：Node v23+ の実験機能でNodeバイナリにアプリを注入して単一実行ファイル化。
  - 長所：ランタイム不要で配布可能。
  - 短所：CJS限定、手順が複雑で失敗しやすい（記事著者はセグフォルトに遭遇）。
- Bun build --compile
  - 概要：BunがJSファイルを束ねてランタイム込みで実行ファイルを作る。バンドル不要で高速。
  - 長所：最も簡単・高速。実用的。
  - 短所：実行ファイルサイズが大きくなる（100MB超が普通）。
  - 手順：
    ```bash
    gleam build --target=javascript
    bun build --compile --outfile=bundle build/dev/javascript/<project>/<project>.mjs --footer="main();"
    ```
- Nexe
  - 概要：Nodeアプリを単一exe化するツール。Gleamとの組合せは比較的試しやすいが設定は必要。

サイズと配布上のトレードオフ
- Bun/Denoはランタイム同梱で大きくなるが、配布・実行の簡便さは高い。
- Gleescriptは小さいがターゲットにErlangが必要。
- BurritoやNexeは「ホストにランタイム不要」な配布に向くが設定や互換性確認が必要。

## 実践ポイント
- まず目的を決める：配布の簡単さ重視→Bun / Deno。バイナリサイズ重視でホストにVMを許容→Gleescript。
- JSターゲットは必ずバンドルしてから実行ファイル化する（esbuild等が定番）。
- Denoでは実行権限（ファイル/ネットワークなど）を起動時に設定する必要あり。
- クロスプラットフォーム配布は各OSで実機テストを必ず行う。
- 本番用途でサイズや起動時間が問題なら、Burritoや工夫したescript＋ERTS同梱の検討を（手間は増える）。

以上を元に、まずはローカルで Bun か Deno の手順を試して得られる「体験」を確認するのが近道です。
