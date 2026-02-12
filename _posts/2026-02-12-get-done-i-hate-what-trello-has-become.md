---
layout: post
title: "Get **** done. I hate what Trello has become - 仕事を前に進めろ。Trelloが変わってしまったことが嫌いだ"
date: 2026-02-12T16:30:25.123Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/karsten_biedermann/get-done-i-hate-what-trello-has-become-5a05"
source_title: "Get **** done. I hate what Trello has become - DEV Community"
source_id: 3244484
excerpt: "肥大化したTrelloを捨て、2週間で試せる最小限ボード活用法"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fr92limgmfwppx8aj0nqf.png"
---

# Get **** done. I hate what Trello has become - 仕事を前に進めろ。Trelloが変わってしまったことが嫌いだ

シンプルさで仕事が進む──「余計なもの」をそぎ落としたタスクボードの提案

## 要約
著者は肥大化したTrello型の「生産性ツール」への不満から、余計な機能を排したシンプルなボード（Frello）を作った。技術的には Next.js/React と Supabase（DB＋認証）で構築され、企業向けの課金やダッシュボードを排した設計が特徴。

## この記事を読むべき理由
日本でもJira/Trelloのようなツールがチーム文化や予算の重荷になりがち。ツールが「可視化＝進捗」と誤解されると、実作業が停滞します。小〜中規模チームや個人で成果を出したい人ほど、こうした“戻し”の発想は刺さります。

## 詳細解説
- 問題点：多くの現行ツールは「レポーティング」と「エンタープライズ機能」に最適化され、UI/UXが複雑化。結果として管理作業が増え、本来の作業が減る。  
- 設計思想：必要なのは「枠（スペース）」と「抑制（ノーと言うこと）」。機能を増やすのではなく、選択肢を絞ることで思考と実行を促す。  
- 実装面：作者は Next.js/React をフロントに、Supabase をデータベース兼認証に採用。素早く立ち上げられ、リアルタイム性や認証まわりを外部に頼れる点が利点。  
- プロダクト決定事項：オンボーディングツアー無し、機能チェックリスト無し、隠れたアップセル無し。エンタープライズ対応や席単位課金は念頭にないため、スケールやガバナンスを重視する組織には向かない。

## 実践ポイント
- 今すぐ試す：プロジェクト1つを「単一ボード」に集約して2週間運用してみる。  
- 設定を削る：必須フィールド、複雑な自動化、ダッシュボードを一旦オフ。必要なら段階的に追加。  
- 評価基準を変える：「見える化」ではなく「完了率／サイクルタイム」でツールの有効性を測る。  
- 小さく作る選択肢：社内向けの最小限ツールを作るなら、Next.js + Supabase は短期間でプロトタイプを作るのに向く。  

シンプルな道具は、手を止めずに仕事を進めさせてくれます。まずは「減らす」ことから始めてみてください。
