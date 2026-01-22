---
layout: post
title: "Compiling Scheme to WebAssembly - SchemeをWebAssemblyへコンパイルする"
date: 2026-01-22T21:46:13.939Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://eli.thegreenplace.net/2026/compiling-scheme-to-webassembly/"
source_title: "Compiling Scheme to WebAssembly - Eli Bendersky's website"
source_id: 46663200
excerpt: "WebAssemblyのGCを使いSchemeをブラウザで動かす実践的コンパイラ実装紹介"
---

# Compiling Scheme to WebAssembly - SchemeをWebAssemblyへコンパイルする
Schemeがそのままブラウザ／WASMで動く！WASM GCを使った本格コンパイラ実装の舞台裏

## 要約
Eli Benderskyの「Bob」プロジェクトに、Schemeを直接WebAssembly（WASM）へ降ろすコンパイラが追加された。WASMのGC拡張を使い、高レベル言語のオブジェクト（ペア、シンボル、ブーリアン、整数など）を実行環境に馴染む形で表現している。

## この記事を読むべき理由
WASMはこれまで主に低レベルコードの配信先だったが、GCや参照型の導入で高級言語のランタイムをWASM上に直接置けるようになった。日本のWeb/エッジ開発や言語実装に関心あるエンジニアにとって、実戦的な設計例と実装ノウハウが得られる。

## 詳細解説
- 背景: BobはR5RS準拠のScheme実装スイート（Python、C++ VMなど）。今回の追加は「WasmCompiler」で、Schemeの式をWASMテキストへ降ろす。
- WASM GC利用: SchemeのオブジェクトをWASMの構造体(ref型を含む)で表現し、WASMランタイムにメモリ管理を任せる設計。
- 代表的な型表現（抜粋、要約）:

```wat
;; consのPAIR (car, cdrは任意オブジェクト参照)
(type $PAIR (struct (field (mut (ref null eq))) (field (mut (ref null eq)))))

;; BOOLはi32フィールドで真偽を保持
(type $BOOL (struct (field i32)))

;; SYMBOLは線形メモリ上のオフセットと長さで文字列を参照
(type $SYMBOL (struct (field i32) (field i32)))
```

- 数値表現: i31を使い「ボクシングなしの整数参照」を活用（1ビットフラグで参照と区別）。
- 文字列／シンボル: WASMは文字列型を持たないため、線形メモリにシンボル名を格納し(offset, length)で参照。これでシンボルのインターンも実現。
- 組み立て例: コンパイラは文字列をデータセクションへ吐き、該当オフセットで構造体を生成する。
- 組み込み関数(write等): ホストからは最低限のI/O（write_char, write_i32）だけをimportし、残りの値表示ロジックはWASMテキストで実装。WASM GC参照はホストからは不透明なので、このアプローチが現実的。

- ツール周り: テキスト→バイナリは bytecodealliance/wasm-tools 等、実行はNode.js（将来的にwasmtimeのPythonバインディングがGC未対応のため注意）。

## 実践ポイント
- ソースを追う: BobのWasmCompilerは約1000LOC（半分はWASMテキストの組み立て）。実装例として読む価値大。Eliのリポジトリを掘ること。
- 小さく試す: 簡単なScheme式（例: (write '(10 20 foo bar))）をコンパイルして、データセクション／struct.newの生成を確認する。
- WASM GCを学ぶ: ref、struct、i31、ref.testの使い方を実際のコードで追うと理解が早い。
- 実行環境: wasm-tools/wat2wasmでテキストをバイナリ化し、Nodeや対応ランタイムで動かしてみる。ホスト側I/Oは最小限に留める実装が互換性に有利。
- 応用案: 小さな言語ランタイムをWASMで作れば、ブラウザやエッジで安全に動かせる。日本のウェブサービスやエッジ処理での軽量言語導入に有用。

原著はEli Benderskyの記事（Compiling Scheme to WebAssembly）。実践的なWASM GCの使い方と設計決定が学べるので、言語実装やWASMランタイム応用に興味ある人は必読。
