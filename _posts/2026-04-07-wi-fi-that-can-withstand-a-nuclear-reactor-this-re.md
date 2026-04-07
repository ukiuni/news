---
layout: post
title: "Wi‑Fi That Can Withstand a Nuclear Reactor - 原子炉に耐えるWi‑Fi受信チップ"
date: 2026-04-07T15:20:03.369Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://spectrum.ieee.org/robotics-in-nuclear-industry"
source_title: "Radiation-Hardened Wi-Fi for Robotics in Nuclear Industry - IEEE Spectrum"
source_id: 47617103
excerpt: "原子炉解体現場で使える、500kGy耐性の無線受信器が実用に迫る"
image: "https://spectrum.ieee.org/media-library/image.jpg?id=65428641&width=1200&height=600&coordinates=0%2C241%2C0%2C259"
---

# Wi‑Fi That Can Withstand a Nuclear Reactor - 原子炉に耐えるWi‑Fi受信チップ
驚異の耐放射線設計で、配線レスロボットが原子炉解体の現場へ──未来の「放射線に強い無線」技術を解説

## 要約
研究チームが総線量500 kGyの放射線に耐える2.4 GHzのWi‑Fi受信器を開発。遠隔操作ロボットの無線化に向けた重要な一歩です。

## この記事を読むべき理由
Fukushimaなど原子力施設の廃炉・調査には人手では危険が伴い、ケーブルに頼らない信頼できる無線通信は日本の現場ニーズと直結します。技術的知見は組込み・ロバスト設計にも応用可能です。

## 詳細解説
- 背景：廃炉作業ではロボットが人を代替しますが、有線LANは絡まり・取り回しの問題があり無線化が望まれる。既存の宇宙用電子機器が耐える放射線量（例：100–300 Gy／数年）に対し、本研究は短期間で桁違いに高い総線量を目標にしています（試験値は $500\ \mathrm{kGy}=5\times10^{5}\ \mathrm{Gy}$）。
- 耐放射線の方針：
  - トランジスタ数を減らし回路の単純化を図る（故障点を減らす）。
  - MOSFETの幾何学を調整：ゲート長・幅を大きくして放射線での性能劣化を抑制。
  - PMOSの使用を最小化。PMOSは酸化膜と界面で正電荷が捕獲されやすくOFF化しやすいため、インダクタ等の酸化膜を持たない部品で代替。
  - NMOSは酸化膜内の正電荷と界面の負電荷が部分的に相殺され、比較的耐性があるため積極利用。
- 実験結果：受信器は照射前と同等の性能を示し、累積 $300\ \mathrm{kGy}$、$500\ \mathrm{kGy}$ 照射後もゲイン低下は約1.5 dBに留まるなど受信側としての実用性を確認。
- 今後の課題：送信側は高い電流が必要で破壊されやすく、従来プロセスでは300 kGyで失敗。ダイヤモンドなど別材料や更なるデバイス工夫が検討中。

## 実践ポイント
- 廃炉向けロボットや現場無線を考える設計者は「酸化膜に弱い要素を避ける」「トランジスタの幾何を変える」「PMOSを減らす」という設計指針を取り入れると良い。  
- 受信器レベルでの放射線試験を早期に実施し、システム全体（送受信・電源・アンテナ）の耐性評価を行う。  
- 日本の廃炉現場ではケーブルレス化の恩恵が大きく、産学連携で実地試験や標準化を進める価値が高い。
