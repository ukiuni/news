---
layout: post
title: "Some notes on starting to use Django - Djangoを使い始めるためのメモ"
date: 2026-01-29T07:12:40.553Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://jvns.ca/blog/2026/01/27/some-notes-on-starting-to-use-django/"
source_title: "Some notes on starting to use Django"
source_id: 1222508342
excerpt: "少人数開発や個人プロジェクトで高速・安全に成果を出すDjango入門実践メモ"
---

# Some notes on starting to use Django - Djangoを使い始めるためのメモ
20年選手の「枯れた」フレームワークで、少ない労力で素早く作れる理由 — 初心者が知っておくべき実践メモ

## 要約
Djangoは「明示的で分かりやすい構造」「管理画面やORMなどの標準機能」「自動マイグレーション」が揃った、少人数・個人プロジェクトに向く堅実なWebフレームワークだという感想と実用メモ。

## この記事を読むべき理由
日本のスタートアップや個人開発、社内ツール作成では「素早く安全に作って運用する」ことが重要。Djangoはその要件を満たしやすく、短時間で形にできる利点があるため、これから使い始める人に役立つ実践的なポイントを端的に示します。

## 詳細解説
- 構造が明示的：Railsの「魔法」に比べ、Djangoは主要ファイルが明快（urls.py, models.py, views.py, admin.py, tests.py）。久しぶりに開いても何を変更すれば良いか追いやすい。
- ビルトイン管理画面：ほんの少しの設定でCRUD用の管理UIが手に入る。非開発者によるデータ編集や確認がやりやすい。

```python
# Python
@admin.register(Zine)
class ZineAdmin(admin.ModelAdmin):
    list_display = ["name", "publication_date", "free", "slug", "image_preview"]
    search_fields = ["name", "slug"]
    readonly_fields = ["image_preview"]
    ordering = ["-publication_date"]
```

- ORMの扱いやすさ：DjangoのORMはJOINを`__`で表現でき、複雑な結合を短く書けるため可読性が高い。
```python
# Python
Zine.objects.exclude(product__order__email_hash=email_hash)
```
- 自動マイグレーション：models.pyを変えるとDjangoがマイグレーションファイルを生成してくれるため、試行錯誤しながらモデルを進化させやすい。
- 小規模運用でのSQLite採用：Postgres運用に抵抗がある場合、少ない書き込み量ならSQLiteで手軽に本番運用でき、VACUUM INTOでファイルバックアップが取れる。
- バッテリー同梱：CSRF、CSP、メール送信など基本機能が標準で揃っており、設定だけで切り替え可能。

```python
# Python (dev settings)
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "emails"
```

```python
# Python (production settings)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.example.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "xxxx"
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_API_KEY')
```

- 注意点：設定はグローバル変数で管理するため、変数名のタイプミスに注意。IDEのサポートが効きにくい箇所がある。

## 実践ポイント
- 最初は公式チュートリアル→models/views/admin/testsの基本5ファイルを理解する。
- 管理画面を有効活用して開発初期は手作業でデータを入れて試す。
- 変更はmodels.py→makemigrations→migrateで管理し、自動生成されたマイグレーションを確認する習慣をつける。
- 小規模サイトや内部ツールはSQLite運用を検討（書き込み頻度を見極めること）。
- dev/prodで設定を分け、メールなど外部サービスは環境変数で管理する。
- 日本語リソースやコミュニティも増えているので、公式ドキュメントと併せて日本語記事を参照すると学習が速い。
