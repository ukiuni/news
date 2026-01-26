---
layout: post
title: "Admiran: a pure, lazy, functional programming language and self-hosting compiler - Admiran：純粋で遅延評価の関数型言語とセルフホスティングコンパイラ"
date: 2026-01-26T22:44:48.125Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/taolson/Admiran"
source_title: "GitHub - taolson/Admiran: Admiran is a pure, lazy, functional language and self-hosting compiler based upon Miranda"
source_id: 416734606
excerpt: "Miranda流の純粋遅延評価とセルフホストコンパイラで型推論やGC実装を学べる言語Admiran"
image: "https://opengraph.githubassets.com/df6bde836bf1a948e666edea228358cf850301eaa558261a06cfd52281fc461b/taolson/Admiran"
---

# Admiran: a pure, lazy, functional programming language and self-hosting compiler - Admiran：純粋で遅延評価の関数型言語とセルフホスティングコンパイラ
自作コンパイラで学ぶ「遅延評価」と「型推論」──Miranda流を現代に再構築した小さな実験言語

## 要約
AdmiranはMirandaに基づく、純粋で遅延評価の関数型言語とそのセルフホスト型コンパイラ。x86-64向けにアセンブリを出力し、Hindley–Milner型推論や小さなGCなどコンパイラ実装の学習に最適な実験プロジェクトです。

## この記事を読むべき理由
- 関数型言語やコンパイラ実装を学びたい入門者〜中級者にとって、実際のセルフホスト実装（ソース＋ツール群）が手元で動かせる稀有な教材だから。  
- 日本の開発環境（macOS / Linux）で動き、手を動かして理解できる点が実務や学習に直結します。

## 詳細解説
- 言語設計: Mirandaの拡張サブセットとして設計。純粋関数型・遅延評価を採用し、モナド風のIO、ラムダ、ケース式、ユーザー定義の中置演算子、アンボックス型（unboxed）など実用的な機能を追加しています。
- 型システム: Hindley–Milner型推論で静的型付けを行うが、Haskellのような型クラスや高階種類（higher-kinded types）は持たず、型クラス相当の辞書は明示的に渡す設計です。
- 実装と性能: コンパイラ本体は約6.7k SLOC、標準ライブラリ約3.3k SLOC。出力はx86-64アセンブリで、元のMiranda実装より20〜50倍高速という実測が報告されています。実行にはCコンパイラが必要で、Mac/Linux（Apple siliconはRosetta 2経由）で動作します。
- ライブラリとデータ構造: リスト／タプルは組み込み。AVLベースのmap/set/bag、可変／不変ベクタ、parser combinator、ストリーム（融合対応）、フィンガーツリーによる両端キュー、ヒープ、ジッパーなど充実した実装が付属します。
- ガベージコレクタとランタイム: 小さなCランタイムをリンクし、2段階コンパクティングGCを実装。軽量ランタイム設計が学べます。
- ビルド／ブートストラップ: amc（Admiranコンパイラ）はAdmiranで書かれており、あらかじめ用意されたブートコンパイラで4段階のブートストラップを行います（config.amの設定→makeで自動化）。.x2ファイルは最適化後のASTのキャッシュで再ビルドを高速化します。
- 設計の制約: 型クラスや高階種類の欠如、Mirandaの一部機能非対応（num型の省略など）という設計トレードオフがあり、学習教材としての単純さと実装容易性を優先しています。

## 実践ポイント
- まずリポジトリをクローンし、examples/のサンプル（primes.amなど）を試す。Makefileで一括ビルドまたは個別に amc モジュール名 を使う。  
- compiler/config.am を自分の環境（hostOS, admiranLibPath）に合わせて編集してから make してブートストラップを実行する。成功メッセージが出れば bin/amc が生成されます。  
- dumpX2.am を使って .x2（最適化済AST）を覗くと、インラインや最適化の挙動が学べる。  
- コンパイラ／ランタイムのソースを読むことで、Hindley–Milner型推論、最適化パス、GC、コード生成（x86-64）の生の実装が学べるため、大学の講義ノートや独学材料として有用。  
- 小規模な機能追加（例：新しいライブラリ関数）でブートストラップを何度か回し、セルフホスティングの挙動を体験すると理解が深まる。

興味があれば公式リポジトリ（GitHub: taolson/Admiran）を覗いて、READMEとexamplesから始めてください。
