---
layout: post
title: "Show HN: Oxyde – Pydantic-native async ORM with a Rust core - Oxyde：PydanticネイティブなRustコア搭載の非同期ORM"
date: 2026-03-16T23:11:32.321Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/mr-fatalyst/oxyde"
source_title: "GitHub - mr-fatalyst/oxyde: Oxyde ORM is a type-safe, Pydantic-centric asynchronous ORM with a high-performance Rust core designed for clarity, speed, and reliability. · GitHub"
source_id: 47364260
excerpt: "Django風の使い勝手とPydantic型安全性を持つ、Rustコアで超高速な非同期ORM"
image: "https://opengraph.githubassets.com/4409a79b6e23ee1787877c87660319f4044552e77d03a2d7f995c88a3226c023/mr-fatalyst/oxyde"
---

# Show HN: Oxyde – Pydantic-native async ORM with a Rust core - Oxyde：PydanticネイティブなRustコア搭載の非同期ORM
魅力的タイトル: Django風の使い勝手×Pydanticの型安全性×Rustの高速性を両立した新世代ORM、まずは触ってみる価値あり

## 要約
Pydantic v2を中心に据えた型安全な非同期ORMで、SQL生成と実行をRustで処理することで高速化を図るプロジェクト。DjangoライクなAPIを持ちつつFastAPIなどと簡単に統合できる点が特徴。

## この記事を読むべき理由
日本でもFastAPIやasync/awaitを使う案件が増えており、型安全で高速なDBレイヤは生産性と信頼性を同時に高めます。既存のSQLAlchemy/Django ORMとは違う選択肢を求めるスタートアップやモダンなバックエンド開発者にとって注目の技術です。

## 詳細解説
- アーキテクチャ: Python側はPydanticモデル中心のAPIを提供し、SQLの生成・実行はRustコアで行う（高速化と安定性を狙い、ネイティブ実行を活用）。
- API感覚: Django風の Model.objects.filter() 系のクエリ構文を採用。明示的な振る舞いを優先し「魔法」は最小限。
- 型とバリデーション: Pydantic v2による完全な型ヒント・バリデーション・シリアライズを活用。
- 非同期ファースト: asyncioベースで設計され、FastAPI等のASGIアプリと自然に連携できる。
- DBサポート: PostgreSQL（12+）、SQLite（3.35+）、MySQL（8.0+）をサポート（RETURNING、UPSERT等の機能対応）。
- トランザクションとマイグレーション: transaction.atomic() や Django風の makemigrations / migrate CLI を提供。
- パフォーマンス: 公開ベンチマークでは主要Python ORMより高いスループットを示す（例：Postgresで約1,475 ops/sec vs SQLAlchemy 445、SQLiteでさらに差が広がる）。
- 注意点: 若いプロジェクトでAPIが進化中。導入は十分な検証を推奨。

## 実践ポイント
- インストールと初期化
```python
pip install oxyde
oxyde init
```
- モデル定義例
```python
from oxyde import Model, Field

class User(Model):
    id: int | None = Field(default=None, db_pk=True)
    name: str
    email: str = Field(db_unique=True)
    age: int | None = Field(default=None)
    class Meta:
        is_table = True
```
- マイグレーションと利用
```bash
oxyde makemigrations
oxyde migrate
```
- FastAPIでの利用例
```python
from fastapi import FastAPI
from oxyde import db
app = FastAPI(lifespan=db.lifespan(default="postgresql://user:pass@localhost/db"))
```
- すぐ試すコツ: ローカルはSQLiteで試作→パフォーマンス検証→本番はPostgresで運用。oxyde-adminで管理画面を自動生成可能。若いOSSのため、本番採用前にAPI安定性と運用要件を確認し、IssueやPRで貢献するのが安全。

（参考）公式ドキュメント: https://oxyde.fatalyst.dev/
