---
layout: post
title: "Show HN: Open-source certificate from GitHub activity - GitHubアクティビティから作るオープンソース証明書"
date: 2026-01-22T05:35:58.631Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://certificate.brendonmatos.com"
source_title: "Generate your certificate"
source_id: 46668780
excerpt: "GitHubユーザー名だけで公開活動を可視化し、面接向けの証明書を即生成"
image: "https://ui.nuxt.com/assets/templates/nuxt/starter-light.png"
---

# Show HN: Open-source certificate from GitHub activity - GitHubアクティビティから作るオープンソース証明書

あなたのGitHub貢献を“見える化”して飾れる証明書に — 面接やポートフォリオで差がつく一枚。

## 要約
GitHubユーザー名を入力するだけで、その公開アクティビティを基にパーソナルな貢献証明書を生成・ダウンロードできるオープンソースのツールです。

## この記事を読むべき理由
日本でもOSS貢献は採用や評価で重視されます。手軽に“見せられる証拠”を作れるこのツールは、ポートフォリオ強化やコミュニティでの可視化に即効性があります。

## 詳細解説
- 概要：サイトにGitHubのユーザー名を入れると、そのユーザーの公開アクティビティ（コミットやPRなど）を集計して証明書を生成します。タイトルからオープンソースで公開されていることが明示されています。
- 技術面（想定）：GitHub APIまたは公開データを取得して集計・レンダリングし、PDFや画像で出力する構成が想定されます。表示・印刷向けのテンプレートが用意され、カスタマイズ可能な実装である可能性が高いです。
- 注意点：公開アクティビティのみが反映されるため、プライベートリポジトリの貢献は表示されません。API制限や認証が必要な場合は利用フローにトークンや認可が絡むことがあります。

## 実践ポイント
- まずはサイト（https://certificate.brendonmatos.com）でユーザー名を入力して証明書を生成してみる。
- 履歴書・LinkedIn・ポートフォリオに画像やPDFを添えて「可視化された貢献」として提示する。
- オープンソース版のソースを確認してデザインや項目を自社ブランディングに合わせてカスタマイズする（採用資料や社内評価用に便利）。
- プライベート貢献を含めたい場合は、ツールのドキュメントで認証手段やスコープの扱いを確認する。
