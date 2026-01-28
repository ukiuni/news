---
layout: post
title: "Somebody used spoofed ADSB signals to raster the meme of JD Vance over Mar-a-Lago - 誰かが偽造ADS‑B信号でマラ・ア・ラゴ上空にJD Vanceのミームを描画（AF2 ICAO識別子使用）"
date: 2026-01-28T22:22:14.403Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://alecmuffett.com/article/143548"
source_title: "Somebody used spoofed ADSB signals to raster the meme of JD Vance over Mar-a-Lago using AF2 ICAO identity &#8211; Dropsafe"
source_id: 46802067
excerpt: "偽造ADS‑Bでマラ・ア・ラゴ上空にJD Vanceのミーム軌跡が描かれ、追跡網の脆弱性が露呈"
image: "https://alecmuffett.com/wp-content/uploads/2026/01/Screenshot_20260128-091014.png"
---

# Somebody used spoofed ADSB signals to raster the meme of JD Vance over Mar-a-Lago - 誰かが偽造ADS‑B信号でマラ・ア・ラゴ上空にJD Vanceのミームを描画（AF2 ICAO識別子使用）
マラ・ア・ラゴ上空に「ミーム飛行」を描いた偽のADS‑B信号――公共受信網の脆弱性が露呈した事件です。

## 要約
海外報告によれば、誰かが偽装したADS‑B信号を送り、特定のICAO識別子（報告ではAF2系）でマラ・ア・ラゴ上空にJD Vanceのミーム的なトラックを表示させたとされます。ADS‑Bの無認証性が悪用された事例です。

## この記事を読むべき理由
ADS‑Bは世界中の民間機追跡サービスや趣味の受信機に広く使われており、日本の飛行監視・データ集約サービスや地上受信ネットワークも同様の脆弱性に晒されています。情報の信頼性や安全運航、データ提供者としてのガバナンスに直結する話題です。

## 詳細解説
- ADS‑Bとは：機体が自ら位置・速度・識別子（ICAO 24bitアドレスやコールサイン）を定期送信する仕組みで、受信機がそれを集約して地図表示やトラッキングを行う。多くのサービスは放送内容を検証せず表示している。  
- なぜ偽装が可能か：ADS‑Bは暗号化・認証を基本にしていないため、安価なSDR（ソフトウェア無線）や既存のエンコーダで任意のメッセージを送出できる。これで偽の位置報告やICAOを流すと、集約サービス上に虚偽トラックが現れる。  
- 「ラスター表示」の手口：大量の偽位置報告を意図的に配置すれば、地図上に図形や文字のようなパターンを描ける（今回のようなミーム表示）。ADS‑B集約サイトや可視化ツールがそのままプロットするため成立する。  
- 検出手がかり：同一ICAOの瞬間的な大量出現、非現実的な速度・高度変化、地理的に不合理なトラック、複数の受信点での受信不一致（受信側での差分）が疑いの目安。  
- 対策案：地上レーダーやADS‑B受信の多地点突合、MLAT（多点測位）による整合チェック、受信側での異常検知ルール、将来的には認証付きのADS‑B拡張（提案段階）など。

## 実践ポイント
- ADSBExchange等で怪しいトラックを見つけたら、時刻・ICAO・座標のスクショを保存して報告する。  
- 自前で受信機（RTL‑SDR等）を持つ場合は、近隣受信データと比較して整合を確認する。  
- データ利用者（開発者/サービス運営者）は、重複ICAO・突発的速度・高度ジャンプなどの簡易ルールでフィルタする。  
- 航空関係者はADS‑B単独に依存せずレーダーや公式管制情報で最終判断する。  
- ハッカー／趣味者向け：実環境でのADS‑B偽装は法的・倫理的問題があるため実行しないこと。

参考として報告ではADS‑B集約サイトのトレース（ICAO adfdf9 等）が示されています。日本でも同様の脆弱性を認識し、運用・監視体制の強化が求められます。
