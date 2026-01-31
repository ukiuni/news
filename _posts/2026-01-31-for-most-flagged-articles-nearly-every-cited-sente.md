---
layout: post
title: "For most flagged articles, nearly every cited sentence failed verification - 多くの検出済み記事では、引用されたほとんどの文が検証に失敗した"
date: 2026-01-31T22:29:54.179Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://wikiedu.org/blog/2026/01/29/generative-ai-and-wikipedia-editing-what-we-learned-in-2025/"
source_title: "Generative AI and Wikipedia editing: What we learned in 2025 &#8211; Wiki Education"
source_id: 46840924
excerpt: "生成AIで増えたWikipedia記事、引用のほぼ全てが検証に失敗し信頼が揺らぐ実態"
image: "https://wikiedu.org/wp-content/uploads/2026/01/GenAI-blog-post-2026-feature-image.png"
---

# For most flagged articles, nearly every cited sentence failed verification - 多くの検出済み記事では、引用されたほとんどの文が検証に失敗した

生成AIが作る「もっともらしい」Wikipedia記事は、見た目ほど信用できない――検証不能な文だらけの実態

## 要約
Wiki Educationの調査で、ChatGPT以降に増えた生成AI系の編集は「引用先が実在しても該当箇所に情報がない」ケースが多く、検出された記事の多くでほぼすべての引用文が検証に失敗した。

## この記事を読むべき理由
日本でも大学の課題やコミュニティ編集でWikipediaが使われる機会が増えています。生成AIをツールに使う前に起きうる誤情報リスクと、現場での対処法を知っておくことは重要です。

## 詳細解説
- 対象と手法：Wiki Educationは自分たちが関与した2022年以降の新規記事3,078件を、生成AI検出ツールPangramで解析。ChatGPT登場以降に検出が増加した。  
- 主な発見：178記事がAIフラグ。偽の出典は7％に過ぎず、多くは「本当にあるソースに対して、該当する記述がそのソース内に存在しない」＝引用不一致（failed verification）だった。検出された記事では、引用された各文が検証不能というケースが多数あった。  
- 影響と対応：Wiki Educationはダッシュボード経由でほぼリアルタイムに検出→編集の一時撤回（サンドボックスへ戻す、スタブ化、削除提案など）を行い、スタッフや講師が差し戻しや修正を実施。結果的に介入でメインスペースへのAI生成文投稿率は想定より低く抑えられた。  
- 検出の限界：Pangramは本文プローズに強いが、書誌リストや箇条書き、マークアップ混在のサンドボックスでは誤検出が出やすい。  
- 有用な使い方：生成AIは「記事の穴を見つける」「関連ソース探索のヒント」「アウトライン作成」「文法チェック」など下調べや編集支援には有効。ただし出力をそのまま貼ると検証不能な情報になる危険が高い。

## 実践ポイント
- 生成AIの出力は「下書きのネタ」として使い、必ず元ソースを自力で確認する。  
- 各主張は該当ソースの該当箇所（ページ番号や段落）で裏取りし、引用が一致するか確認する。  
- 大学や企業で課題運用する場合は「サンドボックス運用」「検出ツールの導入」「教員による検証ルール」を組み込む。  
- 日本語Wikipediaや日本語資料では、英語向け検出器の精度差に注意。ローカルでの検証を重視する。  
- 最終ルール：「生成AIの出力をコピペしてWikipedia本文に載せない」――検証不能な情報を増やさないための最低限の原則。
