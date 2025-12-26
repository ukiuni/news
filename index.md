---
layout: home
title: HN Japan - 日本向けテックニュース
---

# HN Japan

Hacker Newsで話題の記事を、日本の読者向けに解説するサイトです。

## 最新記事

{% for post in site.posts limit:10 %}
- [{{ post.title }}]({{ post.url }}) - {{ post.date | date: "%Y年%m月%d日" }}
{% endfor %}
