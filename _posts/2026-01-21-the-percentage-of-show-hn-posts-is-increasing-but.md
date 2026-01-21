---
layout: post
title: "The percentage of Show HN posts is increasing, but their scores are decreasing - Show HN投稿の割合は増えているが、得点は下がっている"
date: 2026-01-21T10:02:19.424Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://snubi.net/posts/Show-HN/"
source_title: "The percentage of Show HN posts is increasing, but their scores are decreasing | snubi"
source_id: 46702099
excerpt: "LLM普及でShow HN投稿が急増するも平均スコアは大幅低下、差別化が勝敗を分ける"
image: "https://snubi.net/images/hero-kami.png"
---

# The percentage of Show HN posts is increasing, but their scores are decreasing - Show HN投稿の割合は増えているが、得点は下がっている
「Show HN」が増殖中。見かけは多いが、みんな本当に楽しんでいるのか？

## 要約
Hacker Newsの「Show HN」投稿割合は2012〜2022年の約2–3%から、LLMの普及を受けて2025年12月には12%以上に上昇した。一方で平均スコアは同期間で低下し、2025年12月時点でShow HNの平均は約9点、全体は約19.5点と二極化している。

## この記事を読むべき理由
日本のスタートアップや開発者コミュニティも海外のプロダクト発表やユーザー反応を参考にすることが多く、Show HNの動向は「プロダクトをどう発表するか」「LLMで作ったものの受け入れられ方」を考える上で示唆があるため。

## 詳細解説
- データソースと手法  
  著者はBigQueryのpublic Hacker NewsデータをCSVで抽出し、タイトルを小文字化して先頭が "show_hn: " のものをShow HNと判定しました（BigQueryのtypeフィールドには直接のshow_hn属性がないため）。元データは数百MB規模で、解析コードとCSVはGitHubに公開しています。  
  例：投稿割合は次の式で計算されています。  
  $$show\_hn\_ratio = \frac{show\_hn}{story} \times 100$$

- 主要な観察結果  
  1) 2012–2022年はShow HNが全ストーリーの約2–3%に留まっていた。  
  2) LLM（コード生成が可能なモデル）の登場以降、特にClaude CodeやCursor 1.0あたりからShow HN投稿が急増。2025年12月で12%以上に達した。  
  3) しかし同時にShow HNの平均スコアは低下傾向。かつては全体と同程度（15–18点）だったのが、2025年末には約9点と10点ほど低くなった。  
  4) 解析の制約として、投稿がLLMで生成されたかどうかは本文で明記されないことが多く判別困難、また著者自身はデータサイエンティストではない旨の注意書きがある。

- 考えられる理由（著者の推測含む）  
  ・LLMで手軽に「動くもの」を作れるため投稿数が増えた。  
  ・過剰供給によりユーザーがShow HNに飽きており、エンゲージメント（スコア）は下がった。  
  ・投稿の質にばらつきが大きくなった（テンプレ的・未完成プロダクトが増加）。  
  ・2022年の平均スコア上昇には新規ユーザーの増加など説明がつかない部分もある。

## 実践ポイント
- 投稿者向け（Show HNするなら）  
  - 「ただ動く」だけでは不十分。なぜ便利か、問題をどう解決するかを明確に伝える。  
  - デモ（GIF/短い動画）、インストール手順、主要な差別化ポイントを必ず用意する。  
  - LLMを使っている場合は透明性を保つと信頼度が上がる可能性がある。

- 分析／再現したい人向け  
  - 元データはBigQuery public datasetから抽出可能。著者のSQLとリポジトリを参照すると再現が容易。  
  - 解析時の注意点：タイトルだけでShow HNを判定しているため、表記ゆれや言語差に注意すること。大きなCSVを扱える環境を準備する。

- 日本市場での示唆  
  - 日本のプロダクト発表文化でも「手早く見せる」流れは同様に強まる可能性が高い。量が増える分、差別化（日本語での丁寧な説明やローカライズ）で目立てるチャンスがある。  
  - 企業や採用側は「LLMで素早くプロトタイプを出す能力」と「実用性・持続性を作る能力」を分けて評価する意識が必要。

参考：著者のクエリ例（BigQueryでstoryを抽出する一部）
```sql
SELECT
  `time`,
  `title`,
  `type`,
  `score`,
  `id`
FROM
  `bigquery-public-data.hacker_news.full`
WHERE
  `type` IN ('story') AND title IS NOT NULL;
```

元データとコード: https://github.com/plastic041/hackernews

（注）2026年のデータは記事では一部期間を除外しているため、最新傾向を確認する場合は定期的な再解析を推奨。
