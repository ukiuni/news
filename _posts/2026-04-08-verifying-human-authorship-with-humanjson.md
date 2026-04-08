---
layout: post
title: "Verifying human authorship with human.json - human.jsonで人間による執筆を検証する"
date: 2026-04-08T18:13:51.360Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://joelchrono.xyz/blog/implementing-human-json/"
source_title: "Verifying human authorship with human.json"
source_id: 1278739761
excerpt: "human.jsonで人間執筆を可視化し、サイト間で信頼を相互担保する簡単導入ガイド"
image: "https://joelchrono.xyz/assets/img/banner.png"
---

# Verifying human authorship with human.json - human.jsonで人間による執筆を検証する
人が書いたことを「宣誓」する新しい仕組み——human.jsonを自サイトに導入して信頼を可視化しよう

## 要約
human.jsonはウェブサイト同士で「このサイトは人間が書いた」と相互に担保するための軽量プロトコル。拡張機能で表示でき、Jekyllなど静的サイトでも簡単に実装できる。

## この記事を読むべき理由
AI生成コンテンツが増える中で、誰が本当に“人”かを示す手段は信頼構築に直結する。日本の個人ブログやOSSプロジェクト、技術ドキュメントでも透明性を示す実用的な方法だから。

## 詳細解説
- 仕組み：ルートにhuman.jsonを置き、メタデータ（version, url, vouches配列）で「誰を担保するか」を列挙する。ブラウザ拡張はこのファイルを読み、担保関係をUIで示す。
- 実装（Jekyllの例）：編集しやすいYAML（_data/humans.yml）を使い、ビルド時にLiquidテンプレートでhuman.jsonを生成するアプローチが手軽。

例（Liquidテンプレートで生成するhuman.json）:
```liquid
---
layout: none
permalink: /human.json
---
{
  "version": "0.1.1",
  "url": "{{ site.url }}",
  "vouches": [
    {% for human in site.data.humans %}
    {
      "url": "{{ human.link }}",
      "vouched_at": "{{ human.date }}"
    }{% if forloop.last == false %},{% endif %}
    {% endfor %}
  ]
}
```

例（_data/humans.yml）:
```yaml
- link: "https://example.com"
  date: 2026-04-03
- link: "https://example2.com"
  date: 2026-04-03
```

headにリンクを追加して明示する:
```html
<link rel="human-json" href="/human.json">
```

注意点：JSONは人間に読みやすいとは限らないため、編集はYAML等で行いビルド時に生成するのが実用的。誰を「vouch」するかは運営方針次第で、生成画像や一部生成テキストの有無で線引きに迷う場合は透明な基準を公開するとよい。

## 実践ポイント
- 1) _data/humans.yml を作成して担保したいサイトを列挙する。  
- 2) Jekyllなどのビルドでhuman.jsonを生成するテンプレートを置く（上記例をコピペ可）。  
- 3) HTML headに<link rel="human-json" href="/human.json">を追加。  
- 4) 拡張機能で表示を確認し、担保基準をREADMEやサイト上で公開する。  
- 5) 継続的に見直し、担保の信頼性を保つ（変更履歴を残すのが望ましい）。
