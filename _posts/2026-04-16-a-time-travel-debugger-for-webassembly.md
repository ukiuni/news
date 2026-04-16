---
layout: post
title: "A time travel debugger for WebAssembly - WebAssembly向けタイムトラベルデバッガ"
date: 2026-04-16T15:19:22.165Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/friendlymatthew/gabagool/tree/main/gabagool-debug-adapter#gabagool-debug-adapter"
source_title: "gabagool/gabagool-debug-adapter at main · friendlymatthew/gabagool · GitHub"
source_id: 1005345582
excerpt: "WASMを命令単位で巻き戻して解析できるDAP準拠のタイムトラベルデバッガ。"
image: "https://opengraph.githubassets.com/da04febe9b3288b88953c07efba115e320111623e1b48cc6faab96d483f003be/friendlymatthew/gabagool"
---

# A time travel debugger for WebAssembly - WebAssembly向けタイムトラベルデバッガ
魅惑の「時間を戻してデバッグ」：WASMを一歩先で直感的に追える新ツール

## 要約
gabagool-debug-adapterは、WebAssemblyプログラムを時系列で前後に動かして調査できるDAPベースのデバッガです。現状は.wat（テキスト形式のWASM）をステップ実行でき、将来的にDWARF対応で元のソースに直接ステップすることを目指しています。

## この記事を読むべき理由
WASMは日本でもブラウザアプリ、ゲーム、サーバレスやエッジ処理で採用が増加中。従来のログやブレークポイントだけでは掴みづらいバグを「巻き戻して調べられる」ことで、開発効率とデバッグ精度が劇的に向上します。

## 詳細解説
- 仕組み：gabagoolはDebug Adapter Protocol（DAP）に準拠したサーバで、VS Codeと連携してWASM実行の「タイムトラベル（録画・再生／ステートスナップショット）」を提供します。現在は.watファイルの命令単位でステップ実行が可能。
- 対象：.wat（テキストWASM）を直接扱うため、wasm2watなどで変換して使います。リポジトリはRust/Cargoベース（Cargo.tomlあり）で、VS Code拡張と連携する構成です。
- 制限と将来性：現状は.wat限定。プロジェクトはDWARFシンボル対応を目標にしており、達成されればRustやC/C++など元ソースへの直ステップが可能になります。
- 使いどころ：非決定的バグ追跡、複雑な状態遷移の解析、ブラウザ外でのWASMユニットテストの深掘りなど。

## 実践ポイント
- 必須ツール：VS Code、Rust（cargo）、wasmツール（wabtのwasm2wat）を用意。
- ワンショットで試す：GitHub Codespacesでリポジトリを開き、コンテナがビルドされたらF5。
- ローカル手順（リポジトリルートで）:
```bash
# build と拡張ディレクトリへコピー（リポジトリ内スクリプト使用）
./gabagool-debug-adapter/local-install.sh

# VSCode拡張にシンボリックリンク（mac/linux）
ln -sfn "$(pwd)/gabagool-debug-adapter" ~/.vscode/extensions/gabagool-debug
```
- 実行：VS Codeをリロードして .wat ファイルを開き F5 → プログラムを選択 → タイムトラベルデバッグを開始。
- 補足：既存のWASMワークフローに組み込むには、ビルド時に.watを生成（wasm2wat）しておくとスムーズ。DWARF対応が来れば、Rust/C/C++の実ソースへ直接ステップできます。

この記事で紹介したツールは、WASMデバッグの考え方を変える可能性があります。まずはCodespacesやローカルで一度「巻き戻し」を体験してみてください。
