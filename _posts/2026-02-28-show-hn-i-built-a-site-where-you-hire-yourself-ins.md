---
layout: post
title: "Show HN: I built a site where you hire yourself instead of applying for jobs - 求人に応募する代わりに自分を雇うサイトを作りました"
date: 2026-02-28T00:11:50.502Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://hired.wtf"
source_title: "Hire Yourself — Free Self-Employment Contract Generator | hired.wtf"
source_id: 47187450
excerpt: "自分を雇う契約で先延ばしを業務化し達成を強制する無料ジェネレータ"
image: "https://hired.wtf/api/og?name=You&amp;company=Your%20Company&amp;role=Your%20Next%20Role&amp;status=pending"
---

# Show HN: I built a site where you hire yourself instead of applying for jobs - 求人に応募する代わりに自分を雇うサイトを作りました
「自分を雇う」契約書で、先延ばしタスクを“業務”に変える――無料で即効使えるセルフ雇用ジェネレータ

## 要約
hired.wtfは「自分を雇う」ためのフォームで正式な契約書（と解除通知）を生成するサービス。やるべきことを職務に落とし込み、署名して公言することで自己コミットを強化するツールです。

## この記事を読むべき理由
日本でも副業やフリーランス、プロジェクト完遂のための自己管理が重要になっている今、単なる目標設定ではなく「契約」という心理的枠組みでコミットする手法はすぐ使える実践的なテクニックだからです。

## 詳細解説
- 仕組み：サイト上で役職名や成果、期限などに回答（抜粋では6問）。その入力を元に「雇用契約書」と「解雇（自己辞職）通知」が生成される。アカウント不要・無料でダウンロードできる点が特徴。  
- コンテンツの性質：職務名はユーモアを交えつつ具体的（例：Chief Novel Completion Officer、VP of Consistent Sleep）。成果は測定可能なマイルストーンで定義されている（例：90日で7時間睡眠を継続）。  
- 技術的に想定される実装：入力フォーム→テンプレートへ流し込み→PDF生成というシンプルな構成で、クライアント側でPDF生成ライブラリを使うかサーバでレンダリングしている可能性が高い。個人情報を最小にしている点も利用のハードルを下げています。  
- 設計思想：社会的契約（署名・公表）を利用した行動デザイン。自己効力感と外的監視（誰かに見せる／送る）を組み合わせて「やらざるを得ない」状況を作るのが肝。

## 実践ポイント
- 具体化：目標は定量化（何をいつまでに、どう評価するか）して契約に落とす。  
- 小さく始める：大目標を週次・日次マイルストーンに分解して契約化する。  
- 公言する：契約をSNS／Slack／仲間に共有して外的責任を作る。  
- 失敗ルールを決める：解雇通知や罰則（例：寄付、罰ゲーム）を明文化すると効果が上がる。  
- ツール連携：GitHub issue、カレンダー、タスク管理と紐づけて進捗を可視化する。  
- 注意点：法的拘束力は期待せず、個人情報や公開範囲は慎重に設定する。

作者は @thomaskanze。「Built in the jungle」の一言も含めたシンプルなアイデアが刺さるプロダクトです。興味があればまず一度、短期の小さな役割で試してみてください。
