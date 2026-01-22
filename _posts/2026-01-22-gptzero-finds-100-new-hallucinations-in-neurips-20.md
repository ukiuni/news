---
layout: post
title: "GPTZero finds 100 new hallucinations in NeurIPS 2025 accepted papers - GPTZero、NeurIPS 2025採択論文で100件の「虚偽引用」を検出"
date: 2026-01-22T16:07:32.487Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://gptzero.me/news/neurips/"
source_title: "GPTZero finds 100 new hallucinations in NeurIPS 2025 accepted papers"
source_id: 46720395
excerpt: "NeurIPS採択論文でGPTZeroが100件の偽引用を検出、査読崩壊の危機を浮き彫りに。"
image: "https://gptzero.me/news/content/images/2026/01/NeurIPS-logo.svg"
---

# GPTZero finds 100 new hallucinations in NeurIPS 2025 accepted papers - GPTZero、NeurIPS 2025採択論文で100件の「虚偽引用」を検出
魅力的タイトル: NeurIPS誌上の“偽の参考文献”100件発覚――AI時代の査読崩壊をどう防ぐか？

## 要約
GPTZeroがNeurIPS 2025で採択された4,841本の論文を走査し、少なくとも100件の「虚偽引用（hallucinated citations）」を確認。偽の著者・DOI・URL・arXiv IDなど、さまざまなパターンが見つかった。

## この記事を読むべき理由
NeurIPSは世界最高峰のAI会議の一つで、日本の研究者・企業も注目する研究発信源です。偽引用やAI生成テキストの流入は、研究の信頼性や採用・資金配分に直結するため、日本の研究者・開発者にも無関係ではありません。

## 詳細解説
- 検出結果の概要：GPTZeroのHallucination Checkで4,841本をスキャンし、100件超の確認済み虚偽引用が51本前後の採択論文に散在。以前にICLR査読中論文で50件を発見した報告もある。  
- 増加の背景：投稿数は2020→2025で約220%増（9,467→21,575件）と急増。生成AIの利用、いわゆる論文ミル、出版プレッシャーが査読パイプラインを圧迫。レビュー人数の増加は監視・専門性の乱れや不注意、場合によっては不正を生む。  
- 虚偽引用の典型パターン：存在しない論文タイトル、実在しない著者、誤った/捏造されたDOIやURL、間違ったarXiv IDや不完全なID、別論文にリンクする誤った参照。  
- AI生成テキストの判定：GPTZeroはテキストがAI混合（*）かAI生成（**）かを示すマーカーも付与。虚偽引用とAI生成テキストは同時に存在するケースが多い。  
- 影響：会議ポリシー上、虚偽引用は採択取り消しの対象となり得る。採択率（NeurIPS主要トラック約24.52%）を考えると、多数の競合を押しのけて掲載された論文に虚偽が含まれる問題は重大。

## 実践ポイント
- 研究者向け：自分の参考文献はDOI・arXiv ID・出版社ページで必ず検証し、コピペで済ませない。文献管理ツール（Zotero/EndNote/Mendeley）でメタデータを再確認する。  
- 査読者・編集者向け：自動チェックツール（例：hallucination detectors、リンク/DOI整合性チェッカー）を導入し、サンプルチェックを実施する。重要な引用は手動で確認。  
- 研究機関・会議運営者向け：提出時の引用整合性チェック、アーティファクト評価の義務化、レビュー研修で生成AIリスクを扱う。  
- 実務者（企業採用等）向け：論文を実装・転用する前に、引用と再現性を必ず検証し、研究を盲信しないプロセスを整備する。

（参考：GPTZeroの報告は公開スキャン結果に基づく解析であり、具体的な事例は偽著者・偽DOI・不整合なarXiv IDなどのパターンで確認されています。）
