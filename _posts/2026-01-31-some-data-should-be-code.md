---
layout: post
title: "Some Data Should Be Code - データの一部はコードであるべき"
date: 2026-01-31T05:43:55.378Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://borretti.me/article/some-data-should-be-code"
source_title: "Some Data Should Be Code"
source_id: 1649313405
excerpt: "YAMLやMakefileの地獄から脱出、コード化で保守とテストを劇的に簡素化"
image: "https://borretti.me/assets/card/some-data-should-be-code.webp"
---

# Some Data Should Be Code - データの一部はコードであるべき
YAML/Makefileの地獄から抜け出す：データを「コード」に昇格させて開発を楽にする

## 要約
Makefileや大量のYAMLは「データ」だが、繰り返しや条件分岐が必要になると維持が辛くなる。こうしたケースはコード（プログラム）で生成・管理したほうが可読性・再利用性・安全性が高まる、という主張。

## この記事を読むべき理由
日本でもCIのYAMLやCloudFormation、手作業のMakefileは日常的な痛み。小規模プロジェクトやインフラの反復作業を楽にしたいエンジニアや運用者に、実践的な代替案を示す内容。

## 詳細解説
- 問題点：Makefileや手書きのYAMLは一見シンプルだが、ルールが繰り返されると抽象化が難しく、保守コストが増す。例：年・月ごとに同じ処理を定義するルールが多数並ぶ場合。
- 本質：これらのファイルは「宣言的データ」であり、本来はコード（制御構造・型・モジュール）で生成する方が有利。コード化すればループ、条件分岐、関数抽象、型チェックが使える。
- 既存ソリューション：AWS CDK や Pulumi、doit のように「コードで定義してデータを出力する」アプローチが実用例。CDKはCloudFormation YAMLをコードから生成し、抽象化や型安全を提供する。
- メリット：繰り返しの削減、テストの容易さ（生成ロジックのユニットテスト化）、差分レビューの単純化、複雑な依存関係の動的表現。

簡単な比較例 — 繰り返しルールを手書きするMakefile（イメージ）:
```makefile
# makefile
a.png: a.csv plot.py
	python plot.py $< $@
b.png: b.csv plot.py
	python plot.py $< $@
```
同じ処理をPythonで生成するイメージ:
```python
# python
from buildgraph import BuildGraph
g = BuildGraph()
for y in range(2019, 2026):
    for m in range(1,13):
        path = f"ledger/{y}-{m:02d}.toml"
        g.rule(targets=[path], deps=["inputs/checkbook.csv"], fn=lambda p=path,y=y,m=m: import_from_checkbook(p,y,m))
```

## 実践ポイント
- 繰り返しや条件分岐が増える定義は「まずコードへ移行」してみる。  
- 小さな実験から：doit や CDK、Pulumi を試し、既存のYAML/Makefileを生成させるワークフローを作成。  
- 生成ロジックはユニットテスト化して信頼性を確保。差分はCIでチェックする。  
- 既存チームへ導入する場合は段階的に（まずは非クリティカルな定義から）。

元記事は、データ形式で済ませがちな設計を見直し「データの一部はコードにすべきだ」と説いている。日本の現場でも即実践できる考え方。
