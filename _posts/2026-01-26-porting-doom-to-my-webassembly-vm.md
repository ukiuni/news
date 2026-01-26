---
layout: post
title: "Porting DOOM to my WebAssembly VM - DOOMを自作WebAssembly VMへ移植"
date: 2026-01-26T17:23:31.815Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://irreducible.io/blog/porting-doom-to-wasm/"
source_title: "Irreducible"
source_id: 1683383371
excerpt: "自作Wasm VMへDOOMを移植、最小libcとホストコール設計で動かす手法"
---

# Porting DOOM to my WebAssembly VM - DOOMを自作WebAssembly VMへ移植
思わず試したくなる！自作Wasm VMでDOOMを動かした話 — 小さなVMを本物の大作で「実戦テスト」する方法

## 要約
自作のWebAssembly VM（最初はCでプロトタイプ、後にRustへ移植）がWasm Core 2.0のテストを通過したので、大規模な実運用テストとしてDOOM（doomgenericフォーク）をWasm上で動かすために必要だった設計と実装を紹介します。

## この記事を読むべき理由
Wasmはブラウザ外でも急速に普及しており、組み込みやサーバー、エッジでのネイティブ代替として注目されています。日本のエンジニアが「既存C資産をWasmに持ち込む」際に直面する実務的な選択肢と実装ノウハウが学べます。

## 詳細解説
- 背景：著者は最初にCで最小限のWasm VMを作り、後にRustで全面書き直しを実施。Rust化で開発速度と構造変更の安心感が向上し、最終的にWasm Core 2.0（SIMD除く）テストをパス。
- ポリシーと設計方針：VMは仕様のセマンティクスを直接反映する形で実装。最適化は最小限（相対ジャンプの事前計算などのみ）。unsafeを多用するが、Rust移行後はセグフォールト無し。
- DOOM移植での主要課題：
  1. コンパイラターゲット：LLVMバックエンドを持つコンパイラ（emcc/clang/zig cc等）で wasm32 を出力。
  2. ホストとのIO設計：Wasmはサンドボックスなのでファイルやウィンドウ、キーボードはインポート関数（ホストコール）で提供する必要がある。
- 選択肢と著者の判断：
  - Emscripten：ブラウザ前提のバンドル(JS)を生成するため、ブラウザ外の自作VMには不向き。
  - WASI（wasi-sdk）：標準的で利点多し。ただしWASIはコンポーネントモデル上に定義され、エンジン側で対応が必要。今回のVMは未対応のため採用見送り。
  - 生のClang＋独自インターフェース：ホスト側（Rust製のembedder）で必要なホストコールを定義し、ゲスト側は最小限のlibcを実装して対応。著者はこれを採用。
- doomgeneric側の要件：プラットフォーム依存で6つの関数（初期化、フレーム描画、スリープ、タイム取得、キー取得、ウィンドウタイトル設定）を実装すれば動く設計。
- ゲスト側libc：DOOM実行に必要な約43個のC標準関数（fopen/fread/fwrite/printf/malloc等）を段階的に宣言・実装してリンクエラー→ランタイムテストで補完。
- ホストコール群（module名 "semblance"）例：
  - プロセス系：exit, panic
  - IO系：fopen, fread, fwrite, ftell, fseek, fflush, fclose
  - GFX系：init_window, set_window_title, render（生ピクセルバッファを書き込む）
  - タイマー系：get_ticks_ms, sleep_ms
  - 入力系：read_key（キーボードイベントを返す構造体）
- エントリポイント設計：通常の_start→main の流れを変え、_start（初期化）と_tick（1フレーム分を進める）を分離。ウィンドウイベントループはホスト側（embedder）が管理し、ゲストは_tickでゲームロジックを進める設計。
- メモリ管理：DOOM側は独自のゾーンアロケータを持つが、libc側にはWasm向けのwal­locを導入（calloc/reallocサポートを追加したフォーク）して互換性を確保。

## 実践ポイント
- まず方針を決める：WASIを採るか独自ホストインターフェースにするかを用途で選ぶ（ブラウザ外・軽量エンジンなら独自インターフェースが学びが大きい）。
- 必要最低限のlibc APIを洗い出す：コンパイル→未定義シンボルで足りない関数を順次実装するやり方が現実的。
- ホストコール設計は最小粒度で：ファイル・レンダリング・タイマー・入力の4カテゴリを用意すればゲーム系の移植はほぼカバー可能。
- エントリを分ける：UIループをホストに持たせるために _start / _tick の分離は有効（イベント駆動の互換性が高い）。
- テスト：まずWasm Coreのテストスイートを通すこと。大規模アプリ（DOOMなど）を動かす前に仕様準拠を確認するとデバッグ工数が激減する。

この試みは「Wasmを単なるブラウザ外ランタイムとして使う」具体例であり、組み込みやエッジで既存C資産を活かす際の実践的な設計テンプレートになります。興味があれば、実装リポジトリの構成やホスト呼び出しの実装例（Rust側）、libcの抜粋実装などについて続編で深掘りできます。
