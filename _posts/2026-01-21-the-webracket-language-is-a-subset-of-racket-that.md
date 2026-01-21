---
layout: post
title: "The WebRacket language is a subset of Racket that compiles to WebAssembly - WebRacketはWebAssemblyへコンパイルするRacketのサブセット"
date: 2026-01-21T20:52:54.600Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/soegaard/webracket"
source_title: "GitHub - soegaard/webracket: The WebRacket language is a subset of Racket that compiles to WebAssembly"
source_id: 46662247
excerpt: "WebRacketでRacketをwasm化し、ブラウザで脱JavaScriptな開発を実現"
image: "https://opengraph.githubassets.com/ec422fc97e4686510c6546b7cbcb1e0e1065ed49a1f6c3c3480845873bcdb794/soegaard/webracket"
---

# The WebRacket language is a subset of Racket that compiles to WebAssembly - WebRacketはWebAssemblyへコンパイルするRacketのサブセット
Racketをブラウザで動かす！WebRacketで「脱JavaScript」のWeb開発をはじめよう

## 要約
WebRacketはRacketの実用的なサブセットをWebAssembly（wasm）へコンパイルし、ブラウザやNode上でRacketコードを動かせるプロジェクトです。JavaScriptとのFFIでDOMやCanvas、MathJaxなどのブラウザAPIと連携できます。

## この記事を読むべき理由
日本のWeb開発者やRacket愛好家が、既存のJavaScript依存から離れて関数型言語でブラウザアプリを作る選択肢を手に入れられるため。教育用途やプロトタイピング、既存のRacket資産の再利用にも有効です。

## 詳細解説
- 基本方針：Racketの完全移植ではなく、「実用的なサブセット」を直接スタイル（direct-style）でwasmにコンパイル。将来的に完全なRacket対応を目指すが段階的に実装中。
- 実行環境：生成したwasmはブラウザ（Chrome/Firefox/Safariで動作を目標）かNodeで実行可能。ブラウザ向けにhtmlを生成し、raco-static-webで簡単にローカル確認ができる。
- FFIとバインディング：JavaScript FFIでブラウザAPIと接続。既存でMath、DOM、Canvas、MathJax、XTermJS、JSXGraphのバインディングが用意され、外部JSライブラリを利用可能。
- 言語サブセット（主な点）：
  - 数値：flonum（浮動小数）とfixnumのみ。複素数やbignumは未対応（優先度は高め）。
  - ハッシュテーブル：可変テーブルはサポート（弱参照の弱さは無視して強保持）。
  - 構造体や適用可能構造体、構造プロパティ等、多くを実装。Prefab構造体は未対応。
  - 正規表現：モジュール/リンクレットのサポートが進めば実装予定。
  - ポート：ブラウザ向けに文字列／バイト列ポートのみ対応（ファイルポートは要望次第）。
  - 制御構造：末尾呼び出し・複数値・上方向例外をサポート。call/ccや継続マークは未対応（実装は難度高）。
  - 並行性：現状はシングルスレッド。
- コンパイラ内部：Racketのexpanderを使い、NanoPassフレームワークで複数パス（α変換、クロージャ変換、anormal化など）を経てWebAssembly S式を生成。wasm-toolsでバイナリ化。
- 付属例：MathJaxエディタ、Matrix風デジタルレイン、MiniScheme REPL、pictのポート、Space Invaders、xtermjsデモなど、ブラウザ連携を示す実例が多数。
- 必要ツール：wasm-tools（Bytecode Alliance）、Node.js（--experimental-wasm-exnref対応）、Racket 9.0以上、raco-static-web。

## 実践ポイント
- まず試す：リポジトリをクローンし、wasm-tools・Node・Racket9・raco-static-webを揃えてexamples/を `raco static-web` で開くだけで各デモを確認できます。
- 小さく始める：MathJaxやxtermjsのサンプルを改変して、FFI経由でDOMや外部ライブラリに触れてみると学習効率が高い。
- 貢献の余地：モジュール／リンクレット、複素数・bignum、継続や正規表現の実装、FFIバインディング拡充などコントリビュート機会が豊富。
- 日本市場での利用想定：教育（Scheme/Racket入門をブラウザで提供）、数学表記を多用する学術系ダッシュボード、ターミナルエミュ（xtermjs）を活用した開発ツールのWeb移植などが現実的用途。

興味があるなら、examples/を開いて小さなUIや計算デモを作るところから始めてみてください。
