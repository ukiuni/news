---
layout: post
title: "Cl-kawa: Scheme on Java on Common Lisp - Common Lisp上のJava上のScheme（cl-kawa）"
date: 2026-02-25T06:50:04.726Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/atgreen/cl-kawa"
source_title: "GitHub - atgreen/cl-kawa: Scheme on Java on Common Lisp"
source_id: 47110384
excerpt: "cl-kawaでSBCL内にScheme・Java・Lispを境界ゼロで連携を試せる"
image: "https://opengraph.githubassets.com/f7a897d40ef31340fac14c8e94bbe77fafcb8d31174c114262f31f971868d3c5/atgreen/cl-kawa"
---

# Cl-kawa: Scheme on Java on Common Lisp - Common Lisp上のJava上のScheme（cl-kawa）
Lisp×Scheme×Javaが一つのプロセスで動く――境界ゼロの多言語インターオペ実験

## 要約
cl-kawaは、Kawa（Scheme→Javaバイトコード）とOpenLDK（Javaバイトコード→Common Lisp）を組み合わせ、SBCL上でScheme・Java・Common Lispを同一プロセス・同一ヒープで連携させる技術デモです。シリアライズやFFIを使わずに関数呼び出しや値交換が可能になります。

## この記事を読むべき理由
日本の組込み／研究／レガシー系でLispやJVMを触る開発者、あるいは多言語インターオペの教育・プロトタイピングに関心がある技術者にとって、新しい実験的アプローチとして興味深い選択肢になるからです。

## 詳細解説
- アーキテクチャ要点
  - KawaはSchemeコードをJavaバイトコードにコンパイルしてJVM上で動作させる実装。
  - OpenLDKはJavaバイトコードをCommon Lispコードにトランスパイルし、SBCLでネイティブにコンパイルする仕組み。
  - 両者が同一SBCLプロセス・ヒープを共有するため、プロセス境界やシリアライズなしに値や関数をやり取りできる。
- できること（主なAPI）
  - Common LispからScheme式（文字列／s式）の評価：kawa :eval
  - Scheme手続きの参照と呼び出し：kawa :lookup / kawa :funcall
  - Common Lisp関数をScheme側に登録：kawa :register
  - 値変換（gnu.math.IntNum → integer、java.lang.String → string、gnu.lists.Pair → cons 等）
- 必要環境と制約
  - SBCL、OpenLDK、Java 8（rt.jarが必要）、Kawa 3.1.1
  - 技術デモ目的であり、パフォーマンスや網羅的な型変換は保証されない。基本スカラーとリストのみ変換対象。
  - OpenLDKがrt.jarに依存するためJava 8を要求する点に注意。

## 実践ポイント
- 手早く試す手順（概略）
```bash
# 環境変数例（bash）
export JAVA_HOME=/path/to/java8/jre
export LDK_CLASSPATH=libs/kawa-3.1.1.jar
# SBCLでASDFシステムをロードして起動
sbcl --load hello.lisp
```
```lisp
;; SBCL内での例
(asdf:load-system :cl-kawa)
(kawa :startup :classpath "libs/kawa-3.1.1.jar")
(kawa :eval "(* 6 7)")        ; => 42
(kawa :register "cl-square" (lambda (x) (* x x)))
(kawa :eval '(cl-square 7))   ; => 49
```
- 活用アイデア
  - JVMライブラリをScheme経由でLispから試すプロトタイピング。
  - 言語処理系や教育用途で「多言語の呼び出しモデル」を学ぶ教材。
  - レガシーLisp資産とJVMエコシステムを結びつける実験的ブリッジ。
- 注意点
  - 本格運用前にパフォーマンスや型変換の限界を検証すること。
  - Java 8依存やサポート範囲が限定的である点を事前認識する。

以上は技術デモとして非常に示唆的なプロジェクトです。興味がある方はリポジトリをクローンして、環境を揃えて試してみてください。
