---
layout: post
title: "Show HN: Mines.fyi – all the mines in the US in a leaflet visualization - Show HN: Mines.fyi — アメリカの鉱山をLeafletで可視化"
date: 2026-02-20T22:28:10.482Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://mines.fyi/"
source_title: "mines.fyi — Free US Mine Search | MSHA Mine Data for 91,000+ Mines"
source_id: 47094149
excerpt: "米国内9.1万件超の鉱山をLeaflet地図で検索・属性フィルタやAPIで詳しく調べられるサービス"
---

# Show HN: Mines.fyi – all the mines in the US in a leaflet visualization - Show HN: Mines.fyi — アメリカの鉱山をLeafletで可視化
「91,000件超の鉱山データを地図で一望──オープンデータで見える“地下の実態”」

## 要約
MSHA（米国鉱山安全保健局）の公開データを使い、米国内の91,000件以上の鉱山をLeafletベースの地図で探索できるウェブサービス。API・フィルタ・OpenAPI仕様など開発者向けの機能も揃う。

## この記事を読むべき理由
オープンな政府データを地図可視化している実例として、データ取得・整形・配信・表示の流れを学べる。日本でも災害対応や環境監視、市民向け情報公開に応用できるアイデアが得られる。

## 詳細解説
- データソース：MSHAのOpen Government Dataset APIを利用。鉱山ID、名称、運営者、州、種類（石炭／鉱物／非金属）、地下/露天、稼働状況などの属性を取得している。  
- 表示基盤：Leafletで地図表示、ポイントのクラスターや属性フィルタ（州・種類・状態など）をUIで操作可能。ポップアップに詳細情報を表示し、検索やソートも備える。  
- 開発者向け：Map APIとOpenAPI仕様を公開しており、外部アプリからの利用やデータ連携が容易。バックエンドはAPI経由でMSHAを叩き、GeoJSONやタイル形式でフロントに供給している想定（キャッシュ・レート制御が必須）。  
- 実装上の工夫：大量ポイントの扱いはクラスター／ベクトルタイル／サーバ側ページネーションで負荷抑制。属性検索はインデックス化（DB->Elasticsearchなど）で高速化するのが一般的。CORSやデータ更新の頻度管理も重要。

## 実践ポイント
- まずはサイトで州別／種類別にフィルタして挙動を確認する。APIドキュメントを見てエンドポイントとレスポンス構造を把握する。  
- 再現するなら：1) 公的データを取得、2) 正規化してGeoJSON化、3) 簡易APIで配信、4) Leafletで表示（クラスター＋属性フィルタ）という順序がおすすめ。  
- 日本での応用例：国土地理院やAISTの地質・資源データ、地方自治体の産業遺産データを同様に可視化すれば、地域のリスクマネジメントや観光・教育コンテンツに活用可能。  
- 開発上の注意：大量データはベクトルタイル化やキャッシュ、OpenAPIでの仕様公開、利用制限（レート）設計を必ず行う。

元記事（英語）: https://mines.fyi/
