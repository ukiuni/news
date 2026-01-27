---
layout: post
title: "Simpler JVM Project Setup with Mill 1.1.0 - Mill 1.1.0で簡単になるJVMプロジェクトの立ち上げ"
date: 2026-01-27T13:10:09.650Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://mill-build.org/blog/17-simpler-jvm-mill-110.html"
source_title: "Simpler JVM Project Setup with Mill 1.1.0 :: The Mill Build Tool"
source_id: 416291061
excerpt: "Mill 1.1.0でYAMLとヘッダーのみでJVMツールを即構築"
---

# Simpler JVM Project Setup with Mill 1.1.0 - Mill 1.1.0で簡単になるJVMプロジェクトの立ち上げ
Millで1ファイル＋YAMLだけで始める、面倒なJava周りのセットアップを一気にラクにする方法

## 要約
Mill 1.1.0は「宣言的なbuild.mill.yaml」と「ソース内ヘッダーでの単一ファイルスクリプト」を導入し、初期設定の手間を大幅に削減してJVM（Java/Scala/Kotlin）での小さなツールやスクリプト作成を容易にします。

## この記事を読むべき理由
日本の企業や開発者にも馴染み深いJavaエコシステムで、ちょっとした社内ツールやプロトタイプを素早く共有・実行できる環境を手軽に作れるからです。複雑なpom.xmlや環境依存を避けたい場面で即効性があります。

## 詳細解説
- 宣言的設定（build.mill.yaml）
  - Mill 1.1.0はYAMLベースの宣言的設定をサポート。pom.xmlの冗長さを排し、依存やmainクラス、JVMバージョン、追加ソース/リソースなどを短く書けます。YAMLはSnakeYaml-Engine（YAML 1.2）でパースされ、よくあるYAMLの落とし穴に配慮されています。
  - 例（最小依存宣言）:
```yaml
yaml
build.mill.yaml
extends: JavaModule
mvnDeps:
  - org.jsoup:jsoup:1.7.2
```
- 単一ファイルスクリプト（ソース内ヘッダー）
  - Java/Scala/Kotlinのソースファイル先頭に特定のコメントヘッダーを置くだけで、そのファイルを依存付きで実行可能にします（ビルドファイル不要）。例:
```java
java
//| mvnDeps:
//| - org.jsoup:jsoup:1.7.2
import org.jsoup.Jsoup;
public class HtmlScraper { ... }
```
- ./millブートストラップ
  - プロジェクトに置く ./mill スクリプトが適切なMill本体とJVMを自動的にダウンロード／キャッシュ。ローカル環境やCIで「何もインストールしていない状態」から再現性のある実行が可能です。
- 機能と互換性
  - 宣言的設定は単純なユースケースに向く一方、従来のprogrammable build.millファイルは複雑なカスタムロジックに対応。両者を混在させられる点が柔軟です。
  - マルチモジュール、テスト、パッケージング、公開（Maven Central）など主要ワークフローをサポート。Kotlin/Scalaモジュール用のextendsも用意されています。

## 日本市場との関連性
- 大企業の既存Java資産を活かしつつ、短命なプロトタイプや運用ツールをPython/Nodeに頼らずにJVM上で迅速に作れるため、社内共通ツールの標準化や教育用途に向きます。
- CI環境（GitHub Actions、社内GitLab CI）での再現性が高く、日本の多数のプロジェクトで求められる「環境差の吸収」に有用です。
- OpenJDKやパッケージマネージャは国内外で広く使えるため、導入障壁は低いです。

## 実践ポイント
- まずは ./mill をプロジェクト直下に置き、簡単な build.mill.yaml を作って ./mill run で試す。
- 単発ツールはソースファイルにヘッダーを入れて ./mill HtmlScraper.java 引数 で実行してみる。
- 複雑な処理やカスタムタスクは既存の build.mill（プログラム型）に移行可能。宣言的は「素早く始める用」、プログラム型は「拡張用」と使い分ける。
- CIでは ./mill がダウンロードするので、DockerイメージやCIランナーにJDKを入れずに済むケースがあるが、JVMバージョン固定（jvmVersion）を設定して再現性を担保する。

短時間で試せて導入コストが低いので、まずは小さな社内ツールでTr yしてみると効果が見えやすいでしょう。
