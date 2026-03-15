---
layout: post
title: "A Preview of Coalton 2.0 - Coalton 0.2 のプレビュー"
date: 2026-03-15T00:27:27.149Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://coalton-lang.github.io/20260312-coalton0p2/"
source_title: "A Preview of Coalton 0.2 | The Coalton Programming Language"
source_id: 1716548690
excerpt: "Coalton 2.0は固定引数・キーワード・短ラムダで型エラーを明瞭化し高速化"
---

# A Preview of Coalton 2.0 - Coalton 0.2 のプレビュー
Common Lisp の力を引き出す新Coalton：固定引数・キーワード引数・短ラムダで「書きやすく」「速く」「型も親切に」

## 要約
Coalton の次期リリースでは「固定引数関数」を中心に、キーワード引数・複数値戻り・リテラル/内包表記・短ラムダなどの文法改良を導入し、型エラーの明瞭化と実行効率の改善を狙います。数式処理では $ \sqrt{2+\sqrt{3}} = \sqrt{2}(\sqrt{3}+1)/2 $ のような代数的事実を厳密に扱える機能も強化されます。

## この記事を読むべき理由
API設計やFFI、実運用でのパフォーマンス・可読性に直結する変更です。Common Lisp 環境で型安全かつ実用的な関数型コードを書きたい日本の開発者や、Lisp 系ツールチェーンに関心がある人は要注目です。

## 詳細解説
- 固定引数関数（fixed arity）  
  これまでの自動カリー（Haskell風）をやめ、関数には厳密な入力個数が定義されます。部分適用は明示的に行う設計に変わり、呼び出し時の引数不足は即座にエラーになります。これにより、API設計の自然さ、不要なクロージャ割当の削減、タイプエラーの局所化が得られます。
  例（概念）：
  ```lisp
  ;; 固定引数
  (define (f x y z) (+ x (* y z)))  ; 型: A * A * A -> A

  ;; 明示的にカリー化する場合
  (define f-curried (fn (x) (fn (y) (fn (z) (f x y z)))))
  ```
- キーワード引数  
  固定引数の導入によりキーワード引数が自然に追加され、オプション群を構造体でごちゃごちゃ書く必要が減ります。標準ライブラリ例ではファイル開閉で `(open path &key (direction Input) (if-exists EError))` のように使えます。
- 複数値戻り（multiple values）  
  タプル「戻り値のアンボックス化」実装を整理し、関数が複数値を直接返す設計に。一方で複数値は明示的に受け取る必要があります（let の新構文など）。
  ```lisp
  (declare split-at (UFix * String -> String * String))
  (define (split-at n str)
    (values (substring str 0 n) (substring str n (length str))))
  ```
- Unit と Void の役割整理  
  引数ゼロ・戻り値ゼロを型構文レベルで表現するため、従来の Unit の慣習が整理され、Voidは「ゼロ個」を表す記法になります。
- コレクション／連想のリテラルと内包表記  
  ブラケットでのオーバーロード可能なリテラルを導入（例 `[1 2 3]`、空集合 `[]`、連想は `["k" => v]`、空連想は `[=>]`）。FromCollection/FromAssociation 型クラスにより任意のコレクション実装にマッピングされます。内包表記（comprehensions）もサポートされ、生成ロジックを簡潔に記述できます。
  ```lisp
  (define dictionary [name => i for i in (up-to 10) with name = (number-name i)])
  ```
- 短ラムダ構文（short lambda）  
  短い匿名関数を簡潔に書ける `\x.x` 風の構文を導入。ネスト可、カリー化との組合せで可読性向上。
  例: `\x.\y.(f x y)`  
- その他  
  スコープ化された型変数、実数代数数（real algebraic numbers）や xmath による厳密数式処理、コンパイル改善やエラーメッセージの強化などが含まれます。

## 実践ポイント
- 既存コードの移行では型シグネチャ（引数数）を見直す必要あり。自動カリー依存箇所は明示的にカリー化するかAPIを修正する。  
- オプション引数はキーワード引数へ移行すると可読性・保守性が向上する。  
- 複数値戻りを使う場合は受け取り側を必ず明示する（新しい let 構文を活用）。  
- リテラルと内包表記を使えばデータ生成コードが大幅に簡潔に。FromCollection/FromAssociation の実装を用意すれば既存コレクションにも適用可能。  
- 短ラムダ `\…` は一時関数や高階関数の可読性向上に有効。  
- Common Lisp と強く結びついた実装なので、Lisp の既存資産や FFI を活かすユースケース（組み込み系、解析系、既存レガシーの延命）に向く。

導入を試すなら、まず固定引数に合わせて型注釈を確認し、キーワード引数・リテラル・短ラムダを段階的に取り入れて挙動とコンパイルエラーの改善を体感してください。
