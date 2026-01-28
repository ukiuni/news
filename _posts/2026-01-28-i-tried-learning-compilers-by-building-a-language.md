---
layout: post
title: "I tried learning compilers by building a language. It got out of hand. - 言語を作ってコンパイラを学んだら、収拾がつかなくなった"
date: 2026-01-28T05:07:18.552Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/theunnecessarythings/sr-lang"
source_title: "GitHub - theunnecessarythings/sr-lang: Personal experimental language."
source_id: 416868095
excerpt: "実践的な実験言語sr-langでコンパイラをMLIRまで作って学ぶ"
image: "https://opengraph.githubassets.com/1b0e51449d5cc127b59769fd70bac35fd07a8a6029ae3c6a09837f5f4916d099/theunnecessarythings/sr-lang"
---

# I tried learning compilers by building a language. It got out of hand. - 言語を作ってコンパイラを学んだら、収拾がつかなくなった

魅力的な日本語タイトル: コンパイラを“作りながら”学ぶ最短ルート──実験言語「sr-lang」で学びと遊びを同時に手に入れる

## 要約
作者が学習目的で作った実験的プログラミング言語 sr-lang は、パーサーから型システム、MLIR ベースのバックエンドまで実装を通じて学ぶための「実戦教材」。機能は豊富だがアルファ段階であり、学びや貢献に最適。

## この記事を読むべき理由
コンパイラの概念（構文解析・意味解析・中間表現・コード生成）を座学ではなく「実装を読む／触る」ことで直感的に理解したいエンジニアや学生にとって、sr-lang は実践的な教材かつ参加可能なオープンソースプロジェクトだからです。日本の組込み／ゲーム／AI 周りの低レイヤ開発者にも応用性があります。

## 詳細解説
- プロジェクトの哲学：学習優先で「本物の実装」を重視。洗練より探索と反復を許容する設計。
- 言語設計の要点：
  - 型推論（:=）や明示型（:）、コンパイル時定数（::）など宣言が柔軟。
  - 豊富なリテラル（整数の各表記、浮動小数点、raw/byte 文字列など）。
  - 演算（オーバーフロー考慮の演算子 +% / +| など）。
  - 関数/手続き（fn/proc、可変長引数、extern 宣言）、無名関数（|x|）やクロージャ。
  - 制御構造：if/else、while/for、ラベル付き break/continue、強力な match（パターンマッチ）。
  - エラー処理：ErrorUnion（Success!Error）、! 演算子での伝播、catch/orelse、defer/errdefer。
  - 集合型：構造体、列挙型、バリアント（和型）、配列・スライス・動的配列・マップ。
  - 低レベル：生ポインタ、明示的キャスト（通常/ビット/飽和/ラップ/チェック変換）。
  - メタプログラミング：comptime 実行、AST を扱う code ブロック、属性 @[]。
  - MLIR 統合：ソース内に mlir{...} を埋め込み中間表現を直接操作可能。
  - アセンブリ埋め込み、非同期（async/.await）、実行時/コンパイル時のリフレクション。
- ビルドと実行：
  - 実装は Zig で書かれ、バックエンドは LLVM/MLIR に依存。clang-20 を要求（opaque pointers 対応）。
  - Docker によるリリースビルドスクリプトが用意されており、環境構築の手間を軽減できる。
- 現状：アルファ段階で仕様変更や未整備箇所が多いが、それ自体が学習機会。examples/、tests/、std/ が読みやすい入門ポイント。

## 実践ポイント
- まず試す（バイナリが楽です）:
  - GitHub Releases からバイナリを落とすか、リポジトリをクローンしてローカルでビルド。
  - 例：  
    ```bash
    # bash
    ./bin/src --help
    ./bin/src run examples/hello.sr
    ```
- ソースを読む順序（初心者向け）:
  1. examples/ の簡単な .sr ファイルで言語感覚を掴む  
  2. src/ の AST 定義 → パーサ → 型検査 → MLIR 生成の流れを追う
  3. features.md と docs/ で設計意図を確認
- 貢献の始め方（Good First Issues）:
  - std/ の基本ユーティリティ（文字列操作、コレクション）を整備するのが入りやすい
  - テスト追加や簡単なバグ修正から始めると学びが大きい
- 日本市場での応用案：
  - 組込み向けのコンパイラ教学、大学のコンパイラ実習、GPU/Triton/Torch 統合を活かした ML 実験などに展開可能

興味があれば最初の一歩（リポジトリの examples/ を動かす）を案内します。どこから始めたいですか？
