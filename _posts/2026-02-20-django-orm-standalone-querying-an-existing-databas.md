---
layout: post
title: "Django ORM Standalone⁽¹⁾: Querying an existing database - 既存データベースを照会するDjango ORMのスタンドアローン利用"
date: 2026-02-20T13:41:57.338Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.paulox.net/2026/02/20/django-orm-standalone-database-inspectdb-query/"
source_title: "Django ORM Standalone⁽¹⁾: Querying an existing database"
source_id: 764438222
excerpt: "最小設定で既存SQLiteをDjango ORMで即探索・モデル化してデータ移行を素早く行う方法"
---

# Django ORM Standalone⁽¹⁾: Querying an existing database - 既存データベースを照会するDjango ORMのスタンドアローン利用
数行の設定で「既存DB」を覗く — Django ORMを最小構成で使ってレガシーDBを素早く探索する方法

## 要約
Djangoをフルプロジェクトにせず、最小の設定ファイルだけで既存データベース（例：ブラウザのSQLite）に接続し、inspectdbでモデルを生成してORMでクエリする手順を示す実用ガイド。

## この記事を読むべき理由
日本の企業・プロジェクトには古いDBや外部管理のDBが多く、短時間でスキーマを把握・探索・移行したい場面が頻出する。本手法は手軽にデータを調べたり移行スクリプトを作るのに最適。

## 詳細解説
手順は大きく分けて：最小のDjango設定作成 → DB接続確認 → inspectdbでモデル生成 → ORMでクエリ、の4ステップ。

1. 仮想環境を作りDjangoをインストール。
2. manage.py（最小）でDATABASESだけ設定し、SQLiteのパスを環境変数から読む例：

```python
# python
import os
from django.conf import settings
from django.core import management

settings.configure(
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.getenv("SQLITE_PATH"),
        }
    },
    INSTALLED_APPS=[]
)

if __name__ == "__main__":
    management.execute_from_command_line()
```

3. 環境変数を設定してDBシェルで接続確認：
```bash
export SQLITE_PATH=/path/to/places.sqlite
python manage.py dbshell
```

4. inspectdbで既存テーブルからモデル生成：
```bash
mkdir places
python manage.py inspectdb moz_places > places/models.py
```
生成モデルは自動注釈付きで、既存テーブルを変更しないように `managed = False` が付く。必要に応じて不要フィールド削除や primary_key の調整、ForeignKey の `on_delete` を手動で修正する。

5. モジュール化してORM利用：
- places/__init__.py を作り、INSTALLED_APPS に "places" を追加して再設定。
- shellでクエリ実行例：
```python
# python
Place.objects.count()
Place.objects.filter(url__startswith="https://www.djangoproject.com").count()
Place.objects.filter(title__contains="Django").values_list("title","description")
```

ポイント：マイグレーションやテーブル生成は行わない（managed=False）。ORMはあくまで読み取り・探索・データ移行のための「軽量アクセス層」として使う。

## 実践ポイント
- すぐ試すコマンド（まとめ）
  - pip install django
  - export SQLITE_PATH=/path/to/places.sqlite
  - python manage.py dbshell
  - python manage.py inspectdb moz_places > places/models.py
  - touch places/__init__.py; add "places" to INSTALLED_APPS
  - python manage.py shell → Place.objects...
- 注意点：inspectdb生成モデルは必ず手で整える（主キー、on_delete、不要フィールドの削除）。
- ユースケース：レガシーDB調査、未知スキーマのリバースエンジニアリング、データ監査／移行プロトタイプ、解析スクリプトの素早い作成。
- 日本の現場ではオンプレ・古いERP連携やブラウザ保存データ解析などに即応用可能。次はこれを拡張してデータ移行ワークフローに繋げると実務で効果的。
