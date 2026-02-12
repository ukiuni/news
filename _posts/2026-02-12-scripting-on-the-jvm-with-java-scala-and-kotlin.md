---
layout: post
title: "Scripting on the JVM with Java, Scala, and Kotlin - JVMでのスクリプティング（Java・Scala・Kotlin）"
date: 2026-02-12T11:13:00.716Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://mill-build.org/blog/19-scripting-on-the-jvm.html"
source_title: "Scripting on the JVM with Java, Scala, and Kotlin :: The Mill Build Tool"
source_id: 443611783
excerpt: "JBangやMillで手早く配布可能な、既存Java資産活用の実運用向けJVMスクリプト術"
---

# Scripting on the JVM with Java, Scala, and Kotlin - JVMでのスクリプティング（Java・Scala・Kotlin）
Javaで“ちゃんと”スクリプトを書く方法 — 簡潔で高速、そして現場で使えるJVMスクリプト術

## 要約
JVM言語は豊富なライブラリ、IDE支援、高速実行とコンパイル時チェックという強みがあり、JBangやMillのような軽量ツールを使えば小さなスクリプト用途でも十分実用的になる。

## この記事を読むべき理由
日本の企業・開発現場ではJava系の資産・運用慣習が強く残っています。既存のエコシステムを活かしつつ「手早く書けて配布しやすい」スクリプト環境を整える知見は、社内ツール・データ加工・CIジョブなどで即戦力になります。

## 詳細解説
- 利点
  - ライブラリ豊富: Maven Central上に高品質なライブラリが揃っており、ネットワーク/API処理やJSONパース、CLIパーサー（例: Jackson, Unirest, picocli）がそのまま使える。
  - IDE・ツール: IntelliJ等の補完やデバッガ、プロファイラがスクリプト開発でも有効。jstack等の運用ツールも使える。
  - 性能と並列化: JVMの単スレッド性能と簡単な並列化で重い処理も効率化可能。
  - 型チェック: コンパイル時に多くの呼び出しミスを防げるため、テストや運用での信頼性が上がる。

- 課題
  - ボイラープレートと冗長さ：普通のJavaは行数や構造が増えがちで、スピード感が出ない。
  - 実行環境の整備：JDKやMaven/Gradleのバージョン管理、CIや各端末への配布が面倒。
  - ビルド/実行の手間：従来のpom.xmlや長い mvn コマンドは小さなスクリプト向けではない。

- 解決策（実用的なアプローチ）
  - JBangやMillなどの軽量ツールを使うと、ファイル内ヘッダで依存を宣言してワンコマンド実行が可能に。例：
  
  ```java
  // JBang の例（ファイル先頭）
  //DEPS info.picocli:picocli:4.7.6
  //DEPS com.konghq:unirest-java:3.14.5
  //DEPS com.fasterxml.jackson.core:jackson-databind:2.17.2
  ```
  
  実行:
  ```bash
  jbang JsonApiClient.java --start "Functional_programming" --depth 2
  ```

  ```java
  // Mill の例（ファイル先頭）
  //| mvnDeps:
  //| - info.picocli:picocli:4.7.6
  //| - com.konghq:unirest-java:3.14.5
  //| - com.fasterxml.jackson.core:jackson-databind:2.17.2
  ```
  
  実行:
  ```bash
  ./mill JsonApiClient.java --start "Functional_programming" --depth 2
  ```

  - さらに、picocli等でCLI化すればシェルスクリプト代替として配布しやすい。

## 実践ポイント
- まずはJBangで試す：依存宣言だけで即実行できるので学習コストが低い。
- 社内配布はランタイム固定：SDKMANやdocker、CIでJDKバージョンを固定し再現性を確保する。
- 小さなツールは単一ファイル＋picocliで作る：配布とテストが楽になる。
- パフォーマンスが必要なら並列化（ExecutorとかForkJoin）を活用する。
- スクリプトが伸びてきたらMillやGradleに移行してビルドと依存を整理する。
