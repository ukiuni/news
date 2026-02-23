---
layout: post
title: "Pipelined Relational Query Language, Pronounced \"Prequel\" - パイプライン型リレーショナルクエリ言語（発音：プリクエル）"
date: 2026-02-23T15:03:45.151Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://prql-lang.org/"
source_title: "PRQL"
source_id: 47099980
excerpt: "PRQLでSQLが読みやすく高速に変換、VS CodeやJupyterで即活用可能"
image: "https://prql-lang.org/static/img/favicon-32x32.png"
---

# Pipelined Relational Query Language, Pronounced "Prequel" - パイプライン型リレーショナルクエリ言語（発音：プリクエル）
SQLのイライラを解消する新しい選択肢「PRQL」で、誰でも読みやすく速く書けるデータ変換へ

## 要約
PRQLは「パイプライン化された」宣言的クエリ言語で、読みやすく短い構文から各種SQL方言にコンパイルされる。データ探索や分析パイプラインを直感的に書けるのが特徴。

## この記事を読むべき理由
日本でもデータ分析やBIツール、DuckDB／ClickHouse／Postgresなどを使う現場が増えています。既存のSQL資産を壊さずに、可読性・保守性を高められる選択肢としてPRQLは即戦力になります。VS Code拡張やJupyter連携もあり、既存の開発フローに導入しやすい点も実務向けです。

## 詳細解説
- 基本概念：PRQLは「線形パイプライン」の各ステップが前の結果を受け継ぐ。from → filter → derive → group → aggregate → sort → take といった変換を縦に並べることで読みやすくする設計。
- 直感的な構文：日付リテラル、範囲（..）、読める数値（10_000）、f-strings（文字列補間）やs-strings（生SQL埋め込み）など、現代的な構文を備える。
- 拡張性と互換性：PRQLはSQLにコンパイルするため、Postgres、MSSQL、ClickHouseなど複数の方言をターゲットにできる。必要なら生のSQLを埋め込める（エスケープハッチ）。
- ツールと実装：コンパイラはRustで書かれ、Apache-2.0ライセンスでオープンソース。prqlc CLI、pyprql（Jupyter/Pandas連携）、VS Code拡張、DuckDB/ClickHouseのサポートがある。言語バインディング（Python/JS/Rなど）も充実。
- 開発体験：パイプライン設計は大規模クエリの可読性向上、インテリセンスや型チェック（進行中）による早期バグ検出、列系譜（column lineage）サポートの期待がある。
- 実例（簡潔）：

```prql
from employees
filter age >= 30
derive { full = f"{last_name}, {first_name}" }
group department (
  aggregate { avg_salary = avg salary, total = sum salary }
)
sort {-total}
take 5
```

上記は概念的に次のようなSQLに変換される（方言により差分あり）:

```sql
SELECT department, AVG(salary) AS avg_salary, SUM(salary) AS total
FROM employees
WHERE age >= 30
GROUP BY department
ORDER BY total DESC
LIMIT 5;
```

## 実践ポイント
- まずは Playground（ブラウザ）で手を動かす。PRQLを入力すると即座にSQLに変換される。  
- ローカルで試すなら prqlc をインストール（brew / cargo / winget）し、VS Code拡張でライブ変換を使うと習得が早い。  
- JupyterやPandas環境では pyprql を使えば既存のデータフローに組み込める（DuckDBと相性が良い）。  
- 既存の複雑なSQLを段階的にPRQLに書き換え、可読性とメンテ性を評価して導入を検討する。  

以上。興味があれば公式ドキュメントとPlaygroundで具体例を試してみてください。
