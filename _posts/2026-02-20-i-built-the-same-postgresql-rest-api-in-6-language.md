---
layout: post
title: "I built the same PostgreSQL REST API in 6 languages — here's how the database libraries compare - 同じPostgreSQL REST APIを6言語で実装して比較してみた"
date: 2026-02-20T16:20:36.011Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://davideme.com/articles/crud-postgres/"
source_title: "TypeScript and Kotlin Are the Safest Way to Talk to PostgreSQL. Where Does Your Language Land? - Davide Mendolia"
source_id: 436906019
excerpt: "6言語で同じPostgreSQL APIを実装、Prismaが型とマイグレーションで最も安全と判明"
---

# I built the same PostgreSQL REST API in 6 languages — here's how the database libraries compare - 同じPostgreSQL REST APIを6言語で実装して比較してみた
思わず試したくなる「言語別・データベース安全性ガイド」：TypeScriptとKotlinがなぜ“安全”と呼ばれるのか？

## 要約
TypeScript（Prisma）、Kotlin（Exposed）など6言語で同一のPostgreSQL CRUD APIを実装し、「どの段階で安全性が担保されるか」を比較。TypeScriptは単一のスキーマから型付きクライアントとマイグレーションを生成し、最も「整合性が高い」スタックだった。

## この記事を読むべき理由
言語やORM/ライブラリの選択が、開発速度だけでなく「実行前にバグを捕まえられるか」「本番DBとコードがずれるリスク」に直結します。日本のチームでも採用判断・CIポリシー設計にすぐ役立つ知見です。

## 詳細解説
- 比較対象：TypeScript(Prisma)、Python(SQLAlchemy)、Java(Hibernate/Spring Data)、C#(EF Core)、Go(pgx+sqlc)、Kotlin(Exposed)。同一スキーマ・OpenAPIで実装。
- 明確な対立軸：Implicit（フレームワークがSQLを隠蔽） vs Explicit（SQL構造を明示）
  - Implicit例：Spring Dataのメソッド名、LINQ、PrismaのJSON API。可読で簡単だが「どのSQLが走るか」を一見で確かめにくい。
  - Explicit例：Goの生SQL+sqlc、Kotlinの型安全DSL、PythonのSQL形のAPI。SQL構造がコードに反映され、意図が明確。
- 「安全性」を測る3チェック（Queries ↔ Table/Entity ↔ Migration）
  1. クエリがテーブル定義に合っているか（コンパイル/生成時に検出されるか）
     - Build/compile-timeで検出：Go(sqlc)、Kotlin、C#、TypeScript(Prisma)
     - Boot-timeで検出：Java（Spring Data、起動時に検出）
     - Runtimeのみ：Python（実行時エラー）
  2. テーブル定義とエンティティが別れていないか（ソースが一元か）
     - 一元管理：TypeScript(Prisma)、Kotlin(Exposed)、Go(sqlcの生成物)、Python(SQLAlchemyのモデル)
     - 別定義でドリフト発生リスク：Java、C#
  3. 定義とマイグレーションが同期されるか（自動生成か）
     - 自動生成で同期：TypeScript(Prisma)、C#(EF Core)
     - 半自動〜手動：Python(Alembic要編集)、Java/Go/Kotlinは手動
- 結論的評価：TypeScript（Prisma）は3チェックすべてを満たす「単一の真実（single source of truth）」を提供。Kotlinはクエリ安全性が強く良好だが、マイグレーション同期は手動でリスクあり。
- 実務での機能差
  - Soft delete：Java/C#はグローバルフィルタで自動、他はクエリ毎に記述（忘れやすさの差）。
  - タイムスタンプ：TypeScript/Javaはアプリ側で管理、他はDBトリガー依存（可視性と移植性のトレードオフ）。
- 補足：コンパイル時の安全性は構造的エラーのみ検出。ビジネスロジックの欠落（例：deleted_at のWHERE漏れ）は別対策（テスト・コードレビュー）で補う必要あり。

## 実践ポイント
- 単一ソース重視ならPrisma(TypeScript)が強力。IDEでフィールドミスを捕まえ、マイグレーションも生成できる。
- 型安全なSQL（sqlcやKotlinのDSL）は意図が明確。複雑なクエリや性能調整が多いなら有利。
- グローバルなsoft-deleteやquery-filterは便利だが「魔法」を理解しておく（除外や復元が必要な場面を想定）。
- マイグレーションの同期はCIで必須チェックにする（schema driftを防ぐ）。
- 単体テスト・統合テストで論理ミス（WHERE漏れ、N+1等）をカバーするプロセスを導入する。

短く言えば：どの言語も一長一短。構造エラーを事前に防ぎたいならTypeScript/Prisma、SQLの可視性と制御を重視するならGo/sqlcやKotlinのDSLが現場向きです。
