---
layout: post
title: "Open Source security in spite of AI - AI時代でも揺るがないオープンソースのセキュリティ"
date: 2026-02-03T14:07:25.597Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://daniel.haxx.se/blog/2026/02/03/open-source-security-in-spite-of-ai/?utm_source=insidestack&amp;utm_medium=social"
source_title: "Open Source security in spite of AI | daniel.haxx.se"
source_id: 410310097
excerpt: "AI時代にSBOM・CI・fuzzでcurl等基盤OSSの供給網とレビューを強化する提案"
image: "https://daniel.haxx.se/blog/wp-content/uploads/2026/02/daniel-fosdem-2026.jpg"
---

# Open Source security in spite of AI - AI時代でも揺るがないオープンソースのセキュリティ
AIが加速する今、オープンソースの安全性をどう守るか — FOSDEM基調講演を受けて

## 要約
FOSDEM 2026でのDaniel Stenberg氏の基調講演は、AIツールが普及する中でもオープンソース（例：curl/libcurl）のセキュリティを維持する現実的な課題と対策を整理したものです。講演資料と録画が公開されています。

## この記事を読むべき理由
日本の企業・開発者も大量のオープンソースに依存しています。AIによる自動生成コードや新しい攻撃パターンの出現は、開発現場とサプライチェーン保護の考え方を変えます。本記事は初心者にも分かる形で、その影響と実践的対策をまとめます。

## 詳細解説
- AIの二面性  
  - 効率化：コード生成や脆弱性検出を支援し得る。  
  - リスク：生成コードの品質不保証、脆弱部品の混入、悪意あるコードの自動生成が容易に。

- オープンソース特有の課題  
  - ボランティア中心の保守体制は人手不足が常。AIが一時的に助けても、最終的なレビューと責任は人に残る。  
  - 依存関係の多層化（transitive deps）で脆弱性が見えにくい。curlのような基盤ライブラリは広範囲に影響する。

- 実践的な防御策（講演の要点に基づく概念）  
  - CI／CDに静的解析・依存性スキャン・SBOMを組み込む。  
  - フィジカルなテスト（fuzzing等）とヒューマンレビューの組合せを継続。  
  - 変更履歴・署名・リリースの厳格化でサプライチェーン攻撃に備える。  
  - コミュニティ運営と資金面の強化（スポンサー制度やバグバウンティ）で保守の持続性を確保。

## 実践ポイント
- まず自分のプロジェクトで使われている主要ライブラリ（curl等）をリスト化し、SBOMを作る。  
- CIに依存性スキャン（SCA）と静的解析を導入して、PRごとに自動チェックする。  
- 重要コンポーネントはfuzzテストや継続的なセキュリティレビューの対象にする。  
- 社内で「信頼できるリリース手順」と署名ルールを定める。  
- 使っているオープンソースプロジェクトに対して、貢献・金銭的支援・報告でエコシステムを守る。

（参考）FOSDEM講演の録画・スライドが公開されています。PDFスライドは59枚とのこと。
