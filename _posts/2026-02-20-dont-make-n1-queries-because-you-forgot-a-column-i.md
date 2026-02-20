---
layout: post
title: "Dont make N+1 queries because you forgot a column in a Raw Query - Raw Query でカラムを忘れて N+1 クエリを発生させないようにする"
date: 2026-02-20T19:30:31.251Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://youtu.be/WCqy6YZA6EI"
source_title: "Dont make N+1 queries because you forgot a column in a Raw Query #django - YouTube"
source_id: 402033590
excerpt: "Raw Queryで外部キーを忘れて起きるN+1地獄と即効回避法"
image: "https://i.ytimg.com/vi/WCqy6YZA6EI/maxresdefault.jpg"
---

# Dont make N+1 queries because you forgot a column in a Raw Query - Raw Query でカラムを忘れて N+1 クエリを発生させないようにする
魅力的タイトル: Raw SQLで「たった1列」を忘れて地獄のN+1にハマる前に読むべき対処法

## 要約
Raw Queryで必要なカラム（特に外部キーID）を抜かすと、後続の属性参照がオブジェクト単位の追加クエリを生み、結果的にN+1問題になる。対策は必要なIDを取得して一括フェッチするか、最初から結合して関連データを含めること。

## この記事を読むべき理由
Djangoでパフォーマンス異常（ページが遅い、DBクエリが激増する）に遭遇したとき、原因が「Raw SQLで1列を忘れた」だけ、というケースは意外と多い。日本のサービス運用でも簡単にスケール痛を招くため、初級者でもすぐ使える回避法を知っておくと便利です。

## 詳細解説
問題の典型パターン（省略版）：
```python
# python
posts = Post.objects.raw('SELECT id, title FROM app_post')
for p in posts:
    print(p.author.username)  # ここで author の取得がオブジェクト毎に走る -> N+1
```
raw() で author_id を取得していないと、Djangoは関連オブジェクト取得のために個別クエリを発行します。raw() は ORM の select_related / prefetch_related と同じ恩恵を自動的に受けない点に注意。

対処法の考え方：
- 必要な外部キー（author_idなど）を最初のクエリで取得する
- 取得したID群で関連テーブルを一括取得（in_bulk や filter(...__in=...)）
- あるいは最初からJOINして関連カラムを同時に取得し、自前でマッピングする
- 可能ならORMの select_related/prefetch_related を使って生の手仕事を減らす

## 実践ポイント
1. まずは問題の再現（N+1の確認）：
   - Django Debug Toolbar / logging でクエリ数をチェックする。

2. 簡単な修正（author_id を追加してまとめて取る）：
```python
# python
posts = list(Post.objects.raw('SELECT id, title, author_id FROM app_post'))
author_ids = {p.author_id for p in posts}
authors = User.objects.in_bulk(author_ids)
for p in posts:
    author = authors[p.author_id]
    print(author.username)  # N+1を回避
```

3. 別解：JOINして必要なカラムを一発で取る（クエリで完結）：
```python
# python
with connection.cursor() as c:
    c.execute('SELECT p.id, p.title, u.id AS user_id, u.username FROM app_post p JOIN auth_user u ON p.author_id = u.id')
    for row in c.fetchall():
        # row を辞書にして使えば追加クエリ不要
        ...
```

4. できるならORMを使う：
```python
# python
posts = Post.objects.select_related('author').all()
for p in posts:
    print(p.author.username)  # JOIN 1回で済む
```

要点まとめ：
- raw() を使うなら「あとでアクセスするカラム（特に外部キーID）」を抜かさない。
- 抜かしたら in_bulk / filter(...__in=...) で一括取得してマッピングする。
- Debug Toolbar 等でクエリ数を定期的に確認すること。

以上。
