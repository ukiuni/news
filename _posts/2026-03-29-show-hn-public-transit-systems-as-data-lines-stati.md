---
layout: post
title: "Show HN: Public transit systems as data – lines, stations, railcars, and history - 公共交通システムをデータ化 — 路線・駅・車両・歴史"
date: 2026-03-29T11:10:43.299Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://publictransit.systems"
source_title: "Transit Systems | Public Transit Information Database"
source_id: 47561132
excerpt: "端末風UIとAPIで公共交通を横断公開、東京メトロ等の比較・可視化に使える実践データベース"
---

# Show HN: Public transit systems as data – lines, stations, railcars, and history - 公共交通システムをデータ化 — 路線・駅・車両・歴史

都市の交通を“データの地図”にするサイト。開発者・研究者がすぐ使える実践的データベース

## 要約
世界の公共交通システム（駅・路線・車両・履歴）を端末風UIとAPIで公開するプロジェクト。東京メトロを含む主要9システムのメタ情報や比較・検索機能を備える。

## この記事を読むべき理由
日本では既に膨大な交通データが存在するが、それを横断的に扱える公開データベースは貴重。交通アプリ、輸送解析、デジタルツイン、学術研究、自治体の意思決定支援に直接役立つため、エンジニアやプロダクト担当は知っておくべき。

## 詳細解説
- インターフェース：ターミナル風のUIでシステム一覧や検索（⌘K）を直感的に操作。開発者向けにCLI風のクエリ例も提示。  
- 含まれるデータ：駅数、路線数、総延長、日次利用者などの基本メトリクスに加え、路線・駅・車両・歴史情報を構造化して格納。グローバル統計（例：Total Stations 1,570、Total Lines 89、Track Length 1,506 mi）を表示。  
- 収録システム例：Light RailLink、BART、Beijing Metro、CTA、NYC Subway、Sound Transit、Tokyo Metro、WMATA 等。Tokyo Metro はデータに含まれ、世界最大級の乗降数が参照可能。  
- 開発者向け機能：比較ツール（システムのサイドバイサイド分析）、グローバル検索、公開API、ドキュメント、GitHubでのコントリビュート案内。データソースと履歴記録も明記されている点が信頼性向上に貢献。

## 実践ポイント
- サイトで⌘Kを押してまず検索し、東京メトロや近隣都市のデータを確認する。  
- APIとドキュメントを参照してデータを取得し、Mapbox/Leafletで可視化してみる。  
- 比較ツールで都市間ベンチマーク（路線密度・駅当たり利用者など）を出し、企画や解析に活用。  
- 欠落・誤りを見つけたらGitHubで貢献して、日本固有の改善（停留所名の表記揺れや運行履歴）を反映させる。
