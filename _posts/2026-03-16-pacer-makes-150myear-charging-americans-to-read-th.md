---
layout: post
title: "PACER makes $150M/year charging Americans to read their own court records. Every bankruptcy court also publishes a free RSS feed with the same data. - PACERは年間1.5億ドルを課金している。破産裁判所は同じデータを無料RSSで公開している"
date: 2026-03-16T11:17:37.353Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://fedscoop.com/pacer-replacement-cost-free-law-project/"
source_title: "Free PACER advocates say $2 billion estimate is out of touch | FedScoop"
source_id: 381582031
excerpt: "PACERが年間1.5億ドル課金、実は破産裁判所の無料RSSで同データが読める"
image: "https://fedscoop.com/wp-content/uploads/sites/5/2017/08/GettyImages-524816639.jpg"
---

# PACER makes $150M/year charging Americans to read their own court records. Every bankruptcy court also publishes a free RSS feed with the same data. - PACERは年間1.5億ドルを課金している。破産裁判所は同じデータを無料RSSで公開している
開示に課金する司法システムを“無料化”できる？真のコストと日本への示唆

## 要約
米連邦裁判所の公開記録システムPACERはページ課金で巨額の収入を得ているが、非営利団体らは「無料版PACER」は数千万ドル規模で実現可能と主張している。しかも破産裁判所は同等データを無料RSSで既に公開している。

## この記事を読むべき理由
法的公開データの費用とアクセス性は、透明性・研究・リーガルテックの基盤。日本でも裁判情報の利活用やコスト最適化を考える際に示唆になる話題です。

## 詳細解説
- 現状：PACERは閲覧・ダウンロードにページ単位で課金（約$0.10/ページ）。年間収入は数千万〜1.5億ドル規模とされる。  
- 争点：司法当局は「新システム構築で数十億ドルかかる」と主張しているが、Free Law Projectなどの専門家はこれを過大評価と反論。  
- 技術的論拠：
  - 裁判記録の多くは静的PDFで、保存・配信コストは過去20年で劇的に低下（クラウド・オブジェクトストレージ、CDNの普及）。
  - 既存のe‑filingやケース管理システムを段階的にラップして移行すれば、構築は数千〜数百万ドル単位で済むと試算（例：18Fが税務裁判所向けに関わった事例）。
  - 破産裁判所が公開するRSSフィードは、ほぼ同等の事実データを無料配信しており、データ公開の代替手段として有効。
- 運用面：大規模一括刷新ではなく「増分展開（incremental rollout）」で運用費化すればリスクと初期費用を抑えられる。

## 実践ポイント
- まず確認：関心ある裁判所のRSSフィードや公開APIを探してみる（破産裁判所は特に有用）。  
- データ活用：研究・サービス開発は既存の無料フィード＋PDFを組み合わせれば低コストで可能。  
- 開発方針：新規システムは段階的に既存インフラを包む形で構築し、ストレージはクラウドオブジェクト＋CDNを使うとコスト効率が高い。  
- 市場／政策提言：日本でも裁判公開の利便性向上やオープン化議論が進めば、リーガルテックや学術応用が広がる。

以上を踏まえ、まずはPACER代替の技術的・運用的ハードルは想像より低い可能性が高く、既存の無料フィード活用から始めるのが現実的です。
