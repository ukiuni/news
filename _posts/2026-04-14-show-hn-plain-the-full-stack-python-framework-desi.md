---
layout: post
title: "Show HN: Plain – The full-stack Python framework designed for humans and agents - Plain — 人間とエージェントのために設計されたフルスタックPythonフレームワーク"
date: 2026-04-14T22:05:57.956Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/dropseed/plain"
source_title: "GitHub - dropseed/plain: A web framework for building products with Python. · GitHub"
source_id: 47768750
excerpt: "型付きモデルとエージェント連携で高速開発するDjango派生のフルスタックPythonフレームワーク"
image: "https://repository-images.githubusercontent.com/617269166/2711cb6a-6a5f-4df5-a40e-c4f442315afc"
---

# Show HN: Plain – The full-stack Python framework designed for humans and agents - Plain — 人間とエージェントのために設計されたフルスタックPythonフレームワーク

AI時代の実用派フレームワーク：Plainで「人にもエージェントにも優しい」Web開発を始めよう

## 要約
PlainはDjangoを起点に再設計されたフルスタックPythonフレームワークで、型付きモデル・明示的な設計・エージェント連携（Claudeなど）を念頭に置いたツール群を提供します。

## この記事を読むべき理由
日本でもPostgresやJinja2、Tailwindを使うプロジェクトは多く、Plainは既存知識で素早く試せる上、開発者体験（CLI、自動ドキュメント、ガードレール、テスト支援）が充実しているため、プロダクト開発の効率化やAI支援ワークフロー導入の第一歩になります。

## 詳細解説
- コア思想：明示的で型付き。人に読みやすく、LLMやエージェントが扱いやすいコードを目指す。Python 3.13+／Postgresベース。
- 構成：単一フレームワークだが機能ごとに約30のfirst-partyパッケージ（plain.postgres, plain.auth, plain.htmx, plain.tailwindなど）で分離。
- ORMとモデル例（型注釈で宣言）:
```python
from plain import postgres
from plain.postgres import types

@postgres.register_model
class User(postgres.Model):
    email: str = types.EmailField()
    display_name: str = types.CharField(max_length=100)
    is_admin: bool = types.BooleanField(default=False)
```
- ビューとルータ（クラスベース、明示的ルーティング）:
```python
from plain.views import DetailView
from .models import User

class UserDetail(DetailView):
    template_name = "users/detail.html"
    def get_object(self):
        return User.query.get(pk=self.url_kwargs["pk"])
```
- CLIとエージェント支援：plain docs（LLM向けAPIサーフェス出力可）、plain fix、plain testなど。プロジェクト内に「rules」（ガードレール）や「skills」（/plain-install 等の自動化ワークフロー）を置き、エージェントが安全に作業できる設計。
- 開発ツールチェーン：uv（パッケージ管理）、ruff/ty（静的チェック）、esbuild/oxc（JS）などモダンな選定。

## 実践ポイント
- まずは公式スターターを試す（Python 3.13+ と Postgres 環境を用意）。
- plain devでローカル起動、plain docs --apiでAPIシグネチャを確認してLLM連携を検討。
- 既存のDjango経験者はmigration方針やmodels/viewsの移植を小さな機能単位で検証する。
- CIにplain check/plain testを組み込み、rulesでエージェント実行時の安全策を整備する。

興味があれば公式リポジトリ（GitHub: dropseed/plain）とドキュメントを参照して、まずはミニプロジェクトを一つ立ち上げてみることを推奨します。
