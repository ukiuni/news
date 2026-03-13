---
layout: post
title: "XML is a cheap DSL - XMLは安上がりなDSL"
date: 2026-03-13T21:36:23.915Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://unplannedobsolescence.com/blog/xml-cheap-dsl/"
source_title: "XML is a cheap DSL"
source_id: 1239049001
excerpt: "IRS事例から学ぶ、XMLをDSL化して税計算の監査性と拡張性を高める方法"
---

# XML is a cheap DSL - XMLは安上がりなDSL
誰も教えてくれなかった「XMLが現代のDSLで強い」理由 — 税計算で見せた実戦的メリット

## 要約
IRSのTax Withholding Estimator（TWE）で使われる「Fact Dictionary」は、複雑な税ロジックを宣言的に定義するためにXMLをDSLとして採用しており、可読性・検証性・実行順序の問題回避で有益だった、という主張。

## この記事を読むべき理由
日本でも税制・社会保障・規制対応のロジックは同様に複雑化しており、可監査で拡張しやすいDSL設計の選択肢は自治体システムや会計SaaSに直接役立つから。

## 詳細解説
- 背景：TWEはオープンソースで公開された税推定ツール。計算ロジックを「Fact（事実）」としてXMLで宣言し、Fact Graphというロジックエンジンが依存関係を解き実行する。
- 宣言的モデルの利点：命令型（例：JavaScriptでの順次計算）だと入力待ちや実行順序、途中値の欠落が問題になる。宣言的なグラフは依存関係だけを定義し、エンジンが最適に評価するため、途中計算の監査・再現が可能になる。
- XMLが適する理由：DSLとしてのXMLはタグ名で演算子や型を直接表現でき、ネストした式や意味を直感的に読める。JSONだと各ノードに「kind/type」を明記する必要が増え、構造が冗長になりやすい。
- 実例（概念）：
```xml
xml
<Fact path="/totalOwed">
  <Derived>
    <Subtract>
      <Minuend><Dependency path="/totalTax"/></Minuend>
      <Subtrahends><Dependency path="/totalPayments"/></Subtrahends>
    </Subtract>
  </Derived>
</Fact>
```
- 監査性：Fact Graphは「どの入力が最終値に影響したか」を辿れるため、大規模な税法ロジックの検証や第三者によるレビューに強い。

## 実践ポイント
- 複雑なドメインロジック（税・保険・規制ルールなど）は宣言的DSLで定義すると保守性と監査性が上がる。
- DSLを選ぶ際、表現力と可読性を重視するならXMLは依然有力。特に「タグで意味を表す」設計が合う場面で有効。
- 実装はFact（derived/writable）を明確に分離し、依存パスを小さく保つ（テストしやすくするため）。
- コレクション処理や集約は専用ノード（例：CollectionSum）で抽象化し、実装詳細を隠蔽する。
- オープンソース実例（IRSのFact Graph）を読み、構造設計とテスト・監査の考え方を学ぶ。ただしTWEの事実データは推定用で申告に使わないこと。


