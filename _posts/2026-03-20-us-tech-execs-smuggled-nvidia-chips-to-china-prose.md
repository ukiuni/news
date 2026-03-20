---
layout: post
title: "U.S. tech execs smuggled Nvidia chips to China, prosecutors say - 米国のテック幹部がNvidiaチップを中国へ密輸と検察が主張"
date: 2026-03-20T10:24:19.027Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.cnbc.com/2026/03/19/us-tech-execs-smuggled-nvidia-chips-to-china-prosecutors-say.html"
source_title: "US charges Super Micro employees with smuggling Nvidia chips to China"
source_id: 378380050
excerpt: "米テック幹部がNvidia GPUを偽装輸出し中国へ密輸、国家安全と企業信用を揺るがす捜査"
image: "https://image.cnbcfm.com/api/v1/image/108071531-1733347456837-gettyimages-2187540914-SUPER_MICRO_COMPUTER.jpeg?v=1773964019&amp;w=1920&amp;h=1080"
---

# U.S. tech execs smuggled Nvidia chips to China, prosecutors say - 米国のテック幹部がNvidiaチップを中国へ密輸と検察が主張
Nvidia GPU密輸で露呈した「サプライチェーンとコンプライアンスの穴」

## 要約
米国検察は、米サーバーメーカー関係者らがNvidia製AI向けGPU搭載サーバーを偽装・迂回して中国へ転売したとして起訴。関係者は架空書類、再梱包、ダミー機の演出などで輸出規制をかいくぐったとされる。

## この記事を読むべき理由
AI開発で需要が高まる高性能GPUは国家安全保障に関わるため規制対象になっており、サプライチェーンの不正は企業の信用や株価、日本企業の部品調達・販売にも波及する可能性があるため。

## 詳細解説
- 何が起きたか：米司法当局は、Super Micro Computerの共同創業者ら3名（Yih‑Shyan “Wally” Liaw、Ruei‑Tsan “Steven” Chang、Ting‑Wei “Willy” Sun）に対し、Export Control Reform Act違反で起訴。被告らはNvidia GPU搭載サーバーを東南アジアの仲介会社経由で中国へ送ったとされる。  
- 手口：仲介会社が架空の使用先を書類で作成、別の物流業者が梱包をやりかえ、保税倉庫でダミー機を見せて本物は出荷済みとするなど、社内コンプライアンスや監査を欺く手法を多段で使用。監査人の立ち入りを制限・操作したとの指摘もある。  
- 規模：検察はこれらの取引で約25億ドル規模の売上が生じ、その内の一部（約5.1億ドル）が短期間で仲介→中国へ流れたと主張。これを受けて同社株は時間外で約12%下落。  
- 技術的背景：NvidiaのH200やBlackwell世代（B200など）といった高性能GPUは、大規模言語モデルや生成AIの学習に不可欠であり、米国はこうした先端チップの対中輸出に厳しい管理を課している。Nvidia側でも中国向け供給の管理や出荷条件に関する政治的・商業的合意が絡んでいる。  
- 法的・企業対応：当該従業員は休職・契約解除、数名は逮捕（うち1名は行方不明）と報道。企業レベルではコンプライアンス体制の信頼性が問われる事態に。

## 実践ポイント
- 企業（管理者向け）
  - 輸出管理（該非判定）と出荷トレースをシステム化し、第三者による抜き打ち監査を定期化する。  
  - サプライチェーンの中核業者に対するKYC（取引先実態確認）を強化する。  
- エンジニア／オペレーション向け
  - 出荷前後の資産管理（シリアル管理、ファームウェア差分確認）で「ダミー」置換を検出する仕組みを導入する。  
- 一般読者向け
  - AI関連ハードの供給は単なる製品流通ではなく政策・規制に直結することを理解する。ベンダーを選ぶ際はコンプライアンス体制の有無も重要な評価軸。  

短く言えば、AI時代のハードウェア流通は技術だけでなく法務・ガバナンスが勝敗を分ける。今回の事件は日本企業にも対岸の火事ではありません。
