---
layout: post
title: "15 years later, Microsoft morged my diagram - 15年後、Microsoftが私の図をmorgedした"
date: 2026-02-18T06:55:51.580Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://nvie.com/posts/15-years-later/"
source_title: "15+ years later, Microsoft morged my diagram &raquo; nvie.com"
source_id: 47057829
excerpt: "MicrosoftがAIで有名なGit図を変質掲載、出典なしで議論に火"
---

# 15 years later, Microsoft morged my diagram - 15年後、Microsoftが私の図をmorgedした
Microsoftが“あの”Git図をAIで台無しにした――「continvoucly morged」が生んだドキュメント論争

## 要約
Vincent Driessenが2010年に公開した有名なGitブランチ図が、Microsoft Learnに似た図としてAI生成され無断で掲載され、クレジットや校閲の欠如が問題になっています。

## この記事を読むべき理由
日本の開発現場でもMicrosoftの公式ドキュメントや教材を参照する機会は多く、誤った図や出所不明の教材はワークフローに誤解を与えかねません。AI生成物と著作・品質管理の問題は今すぐ関心を持つべきテーマです。

## 詳細解説
- 元図の背景：DriessenはKeynoteで色や曲線、レイアウトまで練り上げたGitのブランチ図を2010年に公開し、ソースも共有して広く普及。  
- Microsoft側の問題点：同様の図がLearnに掲載されたが、AI生成の痕跡（矢印の欠損や誤向き、意味不明な文言「continvoucly morged」など）があり、出典表記やリンクがなかった。  
- 本質的な懸念：単に「類似」が問題なのではなく、プロセス不在で既存の有効な表現を劣化させて流通させること、さらに今後はもっと巧妙に変形されたAI生成物が出回り、出所や改変が見分けにくくなるリスク。  
- 著作権と慣習：作者がソース共有を許していたとしても、学習教材や公式ドキュメントでは出典と最低限のクレジット／校閲が必要。特に学習リソースでは誤情報の影響が大きい。

## 実践ポイント
- 公式ドキュメントを使う前に原典を確認し、出典が明記されているかチェックする。  
- 図や図表は可能なら原ファイル（SVG/Keynote等）を探して利用・再配布時にクレジットを付ける。  
- 組織内ドキュメントではAI生成画像の利用ポリシーと校閲プロセスを定める（出典／生成手順の記録）。  
- 不審な教材を見つけたら作者や配信元に問い合わせ、改善を促す。  
- 日本のチームではローカライズ版作成時に必ず技術担当がレビューする体制を作る。

短く言えば、AIで「作った」ことを理由に出典や品質管理を省くのは許されない――開発者コミュニティ全体で出所と品質を守る仕組みが必要です。
