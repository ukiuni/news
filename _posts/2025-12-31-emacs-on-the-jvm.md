---
layout: post
title: "Emacs on the JVM - JVM上のEmacs実装「Juicemacs」"
date: 2025-12-31T19:39:18.581Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/gudzpoz/Juicemacs"
source_title: "Emacs on the JVM"
source_id: 474231241
excerpt: "JuicemacsはGraalVMでELispをJIT化しポリグロット連携を試す実験的Emacs。"
---

# Emacs on the JVM - JVM上のEmacs実装「Juicemacs」
EmacsがJVMで目覚める — Juicemacsが挑む「JIT × マルチランタイム」実験

## 要約
JuicemacsはGraalVM/Truffle上で動く実験的なEmacs実装で、ELispのJIT化や並列化、Python/JavaScriptとのポリグロット連携を目指すWIPプロジェクトです。現状はREPLや一部のバイトコード・ASTインタプリタが動き、pdump互換の処理まで到達していますがUI周りは未実装です。

## この記事を読むべき理由
Emacs愛用者だけでなく、Java/GraalVMエコシステムやポリグロット実行基盤に関心のあるエンジニアにとって、JVM上で古典的Lisp環境を再構築する設計判断や性能トレードオフは実践的な学びになります。日本の企業でもGraalVMやJVMネイティブイメージの採用が増えている今、Juicemacsは興味深い実験台です。

## 詳細解説
- 目標と特徴
  - Speculative JIT：Truffleを利用してELispのJIT化を試みる。インタプリタ＋JITの統合によるホットパス最適化を狙う。
  - 透明な並列化：ELispコードの「並列化っぽさ」を目指す試みがあり、JVMのスレッドモデルを活用。
  - ポリグロット：Python/JavaScriptなどと相互運用可能にする方針。
  - GNU Emacs 30互換を目標に一部のバイトコード／AST実行をサポート。

- なぜJVMか
  - HotSpotの先進GC、スレッドモデル、Truffle（GraalVM）のJITフレームワークなど、既存のランタイム機能を流用できる点が利点。
  - 一方で起動遅延（Truffleだとさらにウォームアップが必要）やバイナリ肥大化などの課題がある。

- 実行と開発環境
  - 推奨JDK：JDK 25（GraalVM CE推奨）。
  - ビルド手順（概要）：リポジトリをクローン → elisp/emacs をビルドして生成ファイルを用意 → プロジェクトルートで gradle の :app:jvmCmd を使ってREPLを起動。
  - オプション：--dump=pdump や --dump-file でpdump出力、native image（:app:nativeCompile）で高速化。
  - デバッグ：--inspect=4242 によるChrome DevToolsプロトコル対応。

- テストと互換性
  - EmacsのERT（Emacs Lisp Regression Testing）の一部テストが動くが、多くは未実装のAPIで UnsupportedOperationException を投げる可能性あり。テスト実行に小さなワークアラウンドが必要。

- ドキュメントと参照
  - elisp/README、docs/Bytecode.org、docs/NativeComp.org 等で内部設計やバイトコード仕様の抜粋が公開されている。
  - 関連プロジェクト：remacs、rune、pimacs 等。

## 実践ポイント
- すぐ試す手順（短縮版）
  1. GraalVM（JDK 25相当）をインストール。
  2. リポジトリをクローンし、elisp/emacs をローカルでビルド。
  3. プロジェクトルートで sh -c "cd app && $(./gradlew -q :app:jvmCmd)" を実行してREPLを起動。
- 探るべき箇所
  - Truffle上のJIT最適化がELispワークロードでどう効くか（ウォームアップ効果、プロファイリング）。
  - native-imageを使った起動時間とpdump処理の差分。
  - ポリグロット連携の実用性（Javaライブラリ／Pythonコードとの相互運用）。
- 貢献の入口
  - docs/TODO.org やコード中の TODO / UnsupportedOperationException を検索して未実装箇所を見つけると貢献しやすい。
- 活用ケース
  - 教育・研究目的でJITや言語実装を学ぶ実験台として最適。企業ではまだ「実運用」向けではないが、GraalVM導入検討時の参考例になる。

