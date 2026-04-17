---
layout: post
title: "Iceye Open Data - Iceye オープンデータ"
date: 2026-04-17T16:14:27.011Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.iceye.com/open-data-initiative"
source_title: "Open Data Initiative | ICEYE"
source_id: 47806440
excerpt: "登録不要で即使えるICEYEの高頻度SARデータで災害対応やインフラ監視を始めよう"
---

# Iceye Open Data - Iceye オープンデータ
魅力的タイトル: 登録不要で使える衛星SARデータ—ICEYEのオープンデータで災害対応と解析を今すぐ始める方法

## 要約
ICEYEは世界最大級の合成開口レーダー（SAR）衛星コンステレーションによるオープンデータを無償・登録不要で公開。インタラクティブな地図、STACブラウザ、AWS Data Exchangeの3経路で取得でき、SLC/GRD/COGといった標準フォーマットで利用可能。

## この記事を読むべき理由
日本は台風・洪水・地震などの自然災害が多く、雲や夜間でも観測できるSARデータは災害対応、インフラ監視、保険・公共事業の意思決定に直結するため、技術者や自治体、事業者が即活用できる実践性が高いから。

## 詳細解説
- データ提供手段
  - Open SAR Data Map Browser：地図ベースで撮像日時・モードをフィルタして即ダウンロード。
  - Open SAR Data STAC Browser：メタデータ検索・プレビュー・SLC/GRD/COGなど標準フォーマットでのアクセス。STAC準拠でツール連携が容易。
  - Open SAR AWS Data Exchange：AWSの公開データ経由でS3に直接取り込み、クラウドワークフローに組み込み可能（認証不要）。
- データ形式と用途
  - SLC（Single Look Complex）：位相情報を含み高度な干渉解析（InSAR）や地殻変動解析向け。
  - GRD（Ground Range Detected）：幾何補正済みで解析・可視化が簡単。洪水検知や変化検出に適する。
  - COG（Cloud-Optimized GeoTIFF）：クラウドネイティブな配信、部分ダウンロードで高速処理。
- 技術的利点
  - SARは雲・煙・夜間に強く、災害直後の状況把握に有効。
  - ICEYEの高リフレッシュレート（座標・ミッション運用）で連続監視や戦術的アクセスが可能。
  - STAC対応により、既存のGIS/EOツール（QGIS、EOパイプライン、Pythonライブラリ）と相性が良い。
- 実運用の事例（抜粋）
  - SpaceX Starbaseの連続観測データなどインフラ建設のモニタリング。
  - オーストラリアや東南アジアでの災害インテリジェンス改善事例。日本でも台風・洪水対応で同様の価値が期待できる。

## 実践ポイント
- まずはMap Browserで興味領域を探し、GRD/COGをダウンロードして変化検出を試す。
- 高度解析が必要ならSLCを取得してInSARワークフロー（SNAPHU/GMTSAR等）を試す。
- AWS中心の運用ならData Exchange経由でS3に取り込み、Lambda/EMR/EOパイプラインに組み込む。
- STACブラウザ＋Python（pystac、rasterio、xarray）でメタデータ検索→自動化を構築すると効率的。
- 監督部署（自治体・電力会社・保険）と連携し、利用権や法令（個人情報・安全保障）を確認してから運用を開始する。
