---
layout: post
title: "cl-kawa: A Turducken of Programming Languages - cl-kawa: プログラミング言語のタルダッケン"
date: 2026-02-22T04:02:13.927Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://atgreen.github.io/repl-yell/posts/cl-kawa/"
source_title: "cl-kawa: A Turducken of Programming Languages | REPL Yell!"
source_id: 976376448
excerpt: "SBCL上でOpenLDK+KawaがLisp/Java/Schemeを単一プロセスで共演する実験"
---

# cl-kawa: A Turducken of Programming Languages - cl-kawa: プログラミング言語のタルダッケン
1プロセスでCommon Lisp×Java×Schemeが共演する、言語実装好きにはたまらない実験的プロジェクト

## 要約
cl-kawaはSBCL上でOpenLDK（Lisp製のJVM）を動かし、その上でKawa Scheme（Scheme→JVMバイトコード）を実行することで、Common Lisp／Java／Schemeのランタイムを一つのプロセス・一つのヒープにネストさせた実験的実装です。

## この記事を読むべき理由
言語ランタイム、FFIやVMの内部に興味がある人／ツールチェーン設計を学びたい人にとって、実装レベルで「言語どうしを貼り合わせる」具体例とトリッキーな課題（クラス生成・例外制御・数値塔・リフレクション）を一度に学べます。日本の組込み／教育／レガシー系エンジニアにも示唆が多いです。

## 詳細解説
- レイヤ構成（タルダッケン比喩）  
  - 外層：Common Lisp（SBCL） — REPL、コンパイラ、CLOSなどを提供。  
  - 中層：Java（OpenLDK） — Common Lispで書かれたJVM実装。.class/.jarを読み、JavaバイトコードをCommon Lispへトランスパイルして実行。外部JVM不要。  
  - 内層：Kawa Scheme — SchemeをJVMバイトコードにコンパイルする実装。ここではOpenLDK上の仮想JVMで動く。

- 実行チェーン  
  Schemeソース → KawaがJVMバイトコード生成 → OpenLDKがバイトコードをCommon Lispコードに変換 → SBCLがネイティブへコンパイル、という流れが単一プロセス内で完結します。

- 相互運用（双方向）  
  - Common LispからSchemeを評価：kawa:evalでs式／文字列を評価し、結果をLisp値に変換。  
  - SchemeからCommon Lisp関数を呼ぶ：kawa:registerでLisp関数をKawaのProcedureとして登録可能。  
  - 例（要点）：Schemeで組み立てたjava.lang.Stringに対してJavaのtoUpperCaseを呼び、結果をLispでprintする一連の流れが動作します。

- 技術的に面白い挑戦点  
  - ランタイムでのクラス生成：KawaはREPLやラムダ毎にクラスを生成。OpenLDKはメモリ上のクラスバイト列を解析してCLOSクラスを作る必要あり。  
  - 例外ベースの制御（call/cc）：Kawaの継続は例外を投げる実装で、Java例外→Common Lisp条件へのマッピングが難所。  
  - 数値塔：Schemeの複雑な数値体系（任意精度や複素数など）が深いクラス階層を刺激する。  
  - リフレクションやUnsafeの利用：getDeclaredFields/Methodsやsun.misc.Unsafe相当の低レベル操作に対応する必要があった。

- 制約・注意点  
  - デモ目的でありプロダクション向けではない（型変換は基本型中心、性能は最適化優先ではない）。  
  - OpenLDKはブートストラップにJava 8のrt.jarを必要とする。  
  - ライセンスはMIT、ソースは github.com/atgreen/cl-kawa 。

## 実践ポイント
- 試す手順（簡易）:
```lisp
;; lisp
(asdf:load-system :cl-kawa)
(kawa:startup :classpath "libs/kawa-3.1.1.jar")
(kawa:eval '(+ 1 2))             ; => 3
(kawa:eval "(* 6 7)")            ; => 42
```
- 注意点：実行にはSBCLとJava 8のrt.jarが必要。パフォーマンスや型互換性は限定的なので実運用は非推奨。  
- 活用例：言語実装の学習、ランタイムのストレステスト、JVM依存を避けた実験的埋め込み、開発者向けデモや教育用プロジェクトとして最適。  
- 興味があればソースをクローンしてOpenLDKやKawaの内部実装（クラス生成・例外処理・値変換）を追うと多くの実践知が得られます。
