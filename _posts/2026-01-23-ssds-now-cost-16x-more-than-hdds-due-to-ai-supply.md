---
layout: post
title: "SSDs now cost 16x more than HDDs due to AI supply chain crisis - AI需要でSSDはHDDの16倍に：サプライチェーン危機が招くデータセンターの大転換"
date: 2026-01-23T05:24:35.998Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.tomshardware.com/pc-components/storage/ssds-now-cost-16x-more-than-hdds-hybrid-ssd-hdd-datacenter-deployments-are-now-significantly-cheaper-to-deploy-than-ssd-only-equivalents"
source_title: "SSDs now cost 16x more than HDDs due to AI supply chain crisis &mdash; hybrid SSD + HDD datacenter deployments are now significantly cheaper to deploy than SSD-only equivalents | Tom's Hardware"
source_id: 419911637
excerpt: "AI需要でSSDはHDDの16倍に高騰、TCOでハイブリッドが必須に"
image: "https://cdn.mos.cms.futurecdn.net/n4uucZP4dV7mmuFv43MWGE-2560-80.jpg"
---

# SSDs now cost 16x more than HDDs due to AI supply chain crisis - AI需要でSSDはHDDの16倍に：サプライチェーン危機が招くデータセンターの大転換
AIバブルで「容量はHDD、速度はSSD」のハイブリッド運用が現実的なコスト最適解に

## 要約
NANDフラッシュ不足とAI需要でSSD価格が急騰。容量あたりのコストはHDDの約16倍に達し、データセンターではSSDのみ運用よりSSD＋HDDのハイブリッド構成の方が大幅に安くつく状況になっています。

## この記事を読むべき理由
日本のクラウド事業者、オンプレを運用する企業、個人で大容量ストレージを扱う人にとって、ストレージ設計や購買判断が直ちにコストに直結するため。今後の調達戦略・アーキテクチャ選定に必須の情報です。

## 詳細解説
- 価格動向：VDURAの分析では、30TBクラスのエンタープライズTLC SSDが2025年Q2の約$3,062から2026年Q1にほぼ$11,000へと+257%に上昇。一方HDDは同期間で約+35%と相対的に安定しています。結果、容量比でのコスト比は6.2xから16.4xへ悪化しました。  
- 所有コスト比較：同等容量を3年運用した場合、SSD専用構成の総保有コストが約$25.20Mに対し、SSD/HDD混在ハイブリッドは約$5.99M（≒1/4）という試算も出ています。  
- 背景要因：AIデータセンター向け需要の急増でNAND供給が逼迫。メーカーは生産割当を争い、企業向けNAND価格の引き上げ・出荷枠の先取りが続いています。Kioxiaらは供給逼迫が2027年まで続く可能性を示唆。HDDもAI用途での需要増加によりバックオーダーが発生し、価格上昇が続いています。  
- 技術面の観点：NVMeやTLCなど性能指標は依然としてSSDが優位（ランダム/シーケンシャルI/Oやレイテンシ）。ただしコスト効率を考えると、キャッシュやホットデータはSSD、コールドデータはHDD/Tapeへ振り分ける階層化が合理的です。

## 実践ポイント
- アーキテクチャ：SSDはOS/キャッシュ/ホットデータ用、HDDは大容量アーカイブ用とするハイブリッド運用を検討する。  
- TCO評価：メーカー見積もりは数ヶ月で変わるため、3年〜5年のTCO試算を必ず行う。SSD専用と混在の比較を数値化すること。  
- 運用：データライフサイクル管理（Tiering）、圧縮・重複排除（dedupe）、オブジェクトストレージやコールドクラウドの活用で容量コストを下げる。  
- 調達戦略：長期契約・先物的な発注・分散調達で価格変動リスクを緩和する。日本企業は国内データセンターやクラウド事業者と交渉し、在庫確保の選択肢を検討する。  
- 個人向け：大量バックアップは高容量HDDやLTOテープを検討し、OS/作業ディスクは必要最小限のSSDに絞ると費用対効果が良い。

（参考）主要ポイント：30TB TLC SSD +257%、容量比コスト16.4x、ハイブリッドの3年TCOはSSD専用の約1/4。
