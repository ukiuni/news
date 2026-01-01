---
  layout: post
  title: "Gene — a homoiconic, general-purpose language built around a generic “Gene” data type - Gene — 汎用ホモアイソニック言語「Gene」データ型を核にした言語"
  date: 2026-01-01T20:58:35.173Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/gene-lang/gene"
  source_title: "GitHub - gene-lang/gene"
  source_id: 473549789
  excerpt: "Geneは「型＋属性＋子要素」でコード＝データを実現し、DSLやローカルLLM実験に最適"
  image: "https://opengraph.githubassets.com/3b325d0cd171b2d116f02ba04b9418616e7dcf3181c5d1dc270eadbb2f18bd9c/gene-lang/gene"
---

# Gene — a homoiconic, general-purpose language built around a generic “Gene” data type - Gene — 汎用ホモアイソニック言語「Gene」データ型を核にした言語
魅力的タイトル: 「コードもデータもひとつに──Geneで始める『型＋属性＋子要素』の新しい言語設計」

## 要約
Geneは「Type + ^properties + children」という単一のデータ構造を核にしたホモアイソニック（コード＝データ）な汎用言語で、Nim実装のバイトコードVM、マクロ、クラス、疑似async、そしてローカルLLM連携を備えています。

## この記事を読むべき理由
日本の開発現場ではDSLや組み込みスクリプト、プライバシー重視のローカル推論環境への関心が高まっています。Geneは自己記述的なデータ設計とメタプログラミングの素地があり、DSL作成やアプリ内スクリプト、ローカルLLM連携の試作に向いているため、技術検証の価値があります。

## 詳細解説
- 中核データ構造（Gene）
  - 形式：(type ^prop1 value1 ^prop2 value2 child1 child2 ...)
  - 「type」が常に先頭にあり、^で始まるプロパティが任意のGene値を取れる。子要素は位置引数的に扱う。
  - これによりコード自身がデータとして完全に表現され、マクロやDSLが自然に書ける（ホモアイソニシティ）。

- 実装とVM
  - リポジトリはNimで書かれたバイトコードVM実装。スタックベースでcomputed-gotoディスパッチを採用。
  - コンパイラは中間表現GIRを出力し、バイトコード生成とキャッシュ機能あり（build/*.gir）。
  - NaN-boxed 8バイト値等でパフォーマンス最適化を図る。

- 言語機能
  - S式類似の表面構文だが、Gene独自のtype/properties/childrenが特徴。
  - マクロ（未評価引数を扱える）によりコンパイル時変換が可能。
  - 基本的なクラスシステム（class, new, ネストクラス）、疑似async/await（futureベース）。
  - CLIツールチェイン（run / eval / repl / parse / compile）を提供。

- ローカルLLM連携
  - genex/llm 名前空間で llama.cpp 経由のGGUFモデルを呼び出せる。ネイティブライブラリをビルドしてリンクする方式で、プライバシー重視のオフライン推論が可能。
  - モックバックエンドも用意されており、環境がなくても挙動確認ができる。

- 現状の制約
  - パターンマッチの高度機能は実験的、モジュール/パッケージ管理は未完。
  - クラス周り（コンストラクタや継承の全機能）はまだ拡張中。

- パフォーマンス
  - 最適化済みVMでのベンチマーク例：fib(24)で約3.8M関数呼び出し/秒（macOS ARM64, 2025測定）。

## 実践ポイント
- まず触ってみる（環境：Nim/nimble）
  - クローン、ビルド:
    ```bash
    git clone https://github.com/gcao/gene
    cd gene
    nimble build
    ```
  - REPLや examples/ を起動してホモアイソニック設計を体感する。

- LLMを試す（ローカル推論の検証）
  - サブモジュール取得とネイティブビルド:
    ```bash
    git submodule update --init --recursive tools/llama.cpp
    tools/build_llama_runtime.sh
    nimble build
    ```
  - GENE_LLM_MODEL を指して実機モデルで検証、なければモックバックエンドで確認可。

- マクロとDSL設計の実験
  - Geneのtype/props/childrenを使い、簡単なDSL（設定言語、UI定義、ビルドルールなど）を試作してみると思想が見えやすい。
  - GIRやdocs/ を読み、コンパイラ・VMのフロー（解析→GIR→バイトコード）を追うと拡張ポイントが分かる。

- 採用検討の観点
  - 小〜中規模プロジェクトでの組み込みスクリプトや社内DSL・プライバシー重視のローカル推論実験に向く。
  - ただしモジュール管理やクラス機能の成熟度は今後の確認が必要。

## 引用元
- タイトル: Gene — a homoiconic, general-purpose language built around a generic “Gene” data type
- URL: https://github.com/gene-lang/gene
