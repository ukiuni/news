---
layout: post
title: "The Curated, Automated Open Source Portfolio: How It’s Going - キュレートされた自動化オープンソースポートフォリオ：進捗報告"
date: 2026-04-07T19:24:07.391Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/adiatiayu/the-curated-automated-open-source-portfolio-how-its-going-5f98"
source_title: "The Curated, Automated Open Source Portfolio: How It’s Going - DEV Community"
source_id: 3439601
excerpt: "スマホ＋AIで見えないOSS貢献を自動可視化し採用や評価で差をつける方法"
image: "https://media2.dev.to/dynamic/image/width=1200,height=627,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Ftzonqo7qexn3uxoybf8t.png"
---

# The Curated, Automated Open Source Portfolio: How It’s Going - キュレートされた自動化オープンソースポートフォリオ：進捗報告

スマホとAIで作る「見えない貢献」を可視化するOSSポートフォリオ

## 要約
スマホ＋AIで自動生成するオープンソース貢献ポートフォリオが進化し、レビューや共著コミットなど“見えない”作業を正確に集計・可視化するテンプレートとして公開された。

## この記事を読むべき理由
日本でもOSS活動が採用や評価に効く時代。日々のレビューや助言、共同コミットといったGitHubの「見えない」貢献を自動で集計・見せられれば、履歴書や社内評価で説得力が増します。特に副業・転職志向のエンジニアやコミュニティ運営者に有益です。

## 詳細解説
- コア機能：マージされたPR、Issue、PRレビューを定期的に取得してログ化。Node.jsスクリプト＋GitHub Actionsで自動更新する設計。  
- 「見えない仕事」の捕捉：  
  - Co-authored commits（共著コミット）を検出し、PRがレビュー／共著／マージといった複数のカテゴリにまたがって登録できるようにデータモデルを改修。  
  - 長い議論やレビューで生まれた価値は「collaboration」カテゴリで扱い、単純なコミット数だけで測れない貢献を扱う。  
- 可視化：棒グラフでコード／レビュー／コラボレーション比率を表示し、どの役割を担っているかを一目で示す。  
- パーソナリティ判定：活動データから「Community Mentor」や「Project Architect」などのコラボレーション・プロフィールを生成し、自分の貢献スタイルを表現。  
- 配布形態：  
  - テンプレート版（core）：誰でも使えるシンプル版。Markdown出力もあり、静的サイト化せずGitHub上で共有可能。  
  - パーソナル版（workshop）：著者が実験する拡張機能（記事フェッチ、リーダーシップページ、作業中ビュー等）。  
- カスタマイズ：色やアイコンの設定だけでブランド調整が可能。静的HTMLでGitHub Pagesにホストできる。  
- セットアップ概要：リポジトリをテンプレートで複製 → ローカルでnpm ci → scripts/config/config.jsのハンドル／開始年を更新 → GitHub Actions有効化で自動生成。

## 実践ポイント
- まずはテンプレートを「Use this template」で複製して試す。config.jsに自分のGitHubハンドルと開始年を設定。  
- GitHub Actionsを有効にして自動更新を動かすとメンテ不要で履歴が貯まる。  
- Markdown出力を履歴書や職務経歴書に貼る（日本の採用担当はリンクで成果を確認したがる）。  
- 日本語READMEや貢献説明を追加して、社内評価や面接で説明しやすくする。  
- コミュニティ役割（メンター、レビュアーなど）を明示すれば、採用や社内評価での差別化になる。

使い方はシンプルなので、まず自分のリポジトリで試して「見えない」貢献を可視化してみてください。
