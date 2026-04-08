---
layout: post
title: "Sharing CodePen 2.0 demos on DEV - CodePen 2.0デモをDEVに共有する方法"
date: 2026-04-08T22:20:42.258Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/alvaromontoro/sharing-codepen-20-demos-on-dev-273"
source_title: "Sharing CodePen 2.0 demos on DEV - DEV Community"
source_id: 3462809
excerpt: "data属性でクラシックURLを作りCodePen 2.0をDEVに即埋め込み"
image: "https://media2.dev.to/dynamic/image/width=1200,height=627,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fv6os61zdhth7fjm1wrql.png"
---

# Sharing CodePen 2.0 demos on DEV - CodePen 2.0デモをDEVに共有する方法
CodePen 2.0の新URLでもDEVにデモを埋め込む“簡単ワークアラウンド”

## 要約
CodePen 2.0が導入した新しいURL形式はDEVの標準埋め込み判定で弾かれるが、Embedモーダルのdata属性（ユーザー名とハッシュ）を使って古い形式のURLを作れば問題なく埋め込める。

## この記事を読むべき理由
フロントエンドのサンプル共有は学習・採用・技術発信で重要。DEVに英語圏向けデモを貼る機会がある日本の開発者/技術書き手に即効で使える実践テクニックです。

## 詳細解説
問題点
- CodePen 2.0の共有URLは /editor/:user/pen/:editor_pen_id/:slug_hash のような新形式になり、DEV（Forem）のCodePenタグがこれを無効なURLとして拒否する。  

回避策（原理）
- Embedモーダルで生成されるHTMLには data-user と data-slug-hash が含まれる。これらを取り出して、従来のクラシックURL形式 https://codepen.io/[USER]/pen/[SLUG_HASH] を作れば、DEVの {% codepen %} タグで受け入れられる（表示はプレビューのみ）。

具体的手順
1. CodePenエディタ右上の「Share」→「Embed」を選択。  
2. 「HTML (recommended)」のコードを表示。  
3. そのHTML内から data-user と data-slug-hash の値をコピー。  
4. 次の形式でクラシックURLを作成し、DEV記事内で埋め込む。

例
```html
{% codepen https://codepen.io/alvaromontoro/pen/MYjBBrm %}
```

注記
- この方法はプレビュー表示のみ（ソース全開示はされない）。  
- DEV側（Forem）は対応パッチを入れる予定なので、将来的には不要になる可能性あり。

## 実践ポイント
- CodePenで共有する際はまずEmbedモーダルのHTMLを確認する癖をつける。  
- data-user と data-slug-hash をメモしてクラシックURLを作れば、すぐにDEV記事でデモを見せられる。  
- Qiita等日本のプラットフォームでは通常影響しないが、英語圏向け投稿や国際的なポートフォリオで役立つ。
