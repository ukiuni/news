---
layout: post
title: "Writeup: Glue - unified toolchain for your schemas - Glue：スキーマのための統一ツールチェーン"
date: 2026-02-23T01:04:09.643Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://guywaldman.com/posts/introducing-glue"
source_title: "Introducing Glue: Unified toolchain for your schemas | Guy Waldman"
source_id: 400266201
excerpt: "単一IDLから多言語コード生成とVS Code連携で型管理を一元化するGlueを試してみませんか"
image: "https://guywaldman.com/og/posts/introducing-glue-banner.png"
---

# Writeup: Glue - unified toolchain for your schemas - Glue：スキーマのための統一ツールチェーン
1つの定義から型・API・コードを自動生成――Glueで「スキーマの混乱」を終わらせる

## 要約
Glueは単一のIDL（.glue）から多言語コード生成、検証、VS Code統合、ブラウザで動くプレイグラウンドを提供するオープンソースのツールチェーンです。OpenAPIやProtobufの断片化による「型の二重管理」を解消することを目指しています。

## この記事を読むべき理由
日本でもマイクロサービスやフロント／バックの分離、複数言語混在は当たり前。型やスキーマが散らばると保守コストやミス、サプライチェーンリスクが増えます。Glueは「型を一箇所で定義して生成する」ワークフローを提案し、開発効率と整合性を高めます。

## 詳細解説
- 背景問題：OpenAPI・Protobuf・Avroなどツール毎に仕様や出力が異なり、言語ごとに別ツールを使う必要がある。REST用に書いたスキーマをバイナリプロトコルや別言語で再利用するのが面倒。
- Glueの設計方針：
  - 最小で人間・LLMに優しいIDL（データモデル＝model、enum、interface/endpointを定義）。
  - 表示層（RESTやgRPCなど）から抽象化した型中心の定義。必要に応じてエスケープハッチで具体化可能。
  - 単一のCLIでコード生成と検証。VS Code拡張（シンタックス、LSP）とWebAssemblyベースのオンラインプレイグラウンドを提供。
- 機能例：optionalフィールド、デフォルト値、配列・Record（マップ）、エンドポイント定義とレスポンスの簡潔な記述など。OpenAPIの冗長さを避けつつ、HTTPエンドポイントも定義可能で、型だけほしいケースにも対応。
- 現状と展望：まずはIDL＋CLI＋VSCode＋playgroundを公開。今後エコシステム（コード生成プラグイン、UI表示、より多くのターゲット言語）を拡張する計画だが、採用感触次第で進化する段階。

例（Glue仕様の抜粋）:
```glue
model Apartment {
  /// The apartment number, e.g. "1A"
  number: int
  residents: Person[]
}

model Person {
  name: string
  age: int
  residence_end_date?: string
  is_employed: bool = false
}

endpoint "GET /building/{building_id}" GetBuilding {
  responses: {
    200: Building
    4XX: ApiError
    5XX: ApiError
  }
}
```

## 実践ポイント
- まずはブラウザ上のプレイグラウンド（https://gluelang.dev）で触ってみる。  
- VS Code拡張を入れて既存の型設計ワークフローに試験導入し、型定義→コード生成の差分を確認する。  
- Polyglotなコードベース（Go/Python/TypeScriptなど）で共有型を導入してみると、差し替えコストが見えます。  
- 現状は新規プロジェクトや型中心の設計に向くため、既存の大規模レガシーには段階的導入を推奨。GitHub（guywaldman/glue）でフィードバックを送ると今後の改善に反映されやすい。
