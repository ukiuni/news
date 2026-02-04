---
layout: post
title: "Show HN: Craftplan – I built my wife a production management tool for her bakery - 妻のために作ったベーカリー向け生産管理ツール「Craftplan」"
date: 2026-02-04T00:58:32.360Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/puemos/craftplan"
source_title: "GitHub - puemos/craftplan: Self-hosted software for managing artisanal D2C micro-businesses"
source_id: 46847690
excerpt: "自家ホスティングでレシピ・在庫・発注を一元管理するベーカリー向けツール"
image: "https://repository-images.githubusercontent.com/907760604/9f68b8cd-8533-4f57-8b17-6a72cc612ed9"
---

# Show HN: Craftplan – I built my wife a production management tool for her bakery - 妻のために作ったベーカリー向け生産管理ツール「Craftplan」
小規模ベーカリー／クラフト事業向けの自家ホスティングERP――手作りビジネスの業務を一つにまとめる「Craftplan」

## 要約
Craftplanは小規模なD2C／クラフト製造向けに設計されたオープンソースの生産管理ツールで、カタログ・BOM・在庫・発注・生産スケジューリング・請求・CRMを一元化し、自宅サーバーで動かせます。

## この記事を読むべき理由
日本では個人経営のベーカリーや食品スタートアップが多く、原価管理やアレルゲン表記、少量多品目の生産管理が課題です。Craftplanはそのまま使える機能群と自家ホスティングで、コストとデータ制御の両面にメリットがあります。

## 詳細解説
- 主な機能
  - カタログと写真付き商品管理、バージョン管理されたBOM（レシピ）とネストしたコスト集計（cost rollups）
  - 生産バッチ管理：原料の自動消費、ロット追跡、完成数量の追跡
  - 在庫管理：原材料のロット追跡、入出庫、在庫調整
  - 発注・仕入れ管理、受入時にロット作成
  - 注文処理とカレンダー連携（iCal）、請求書発行
  - アレルゲン・栄養成分の追跡（食品事業者に有用）
  - API（JSON:API / GraphQL）、カスタム認証キー、ポリシーベースのアクセス制御
- 技術スタック
  - Elixir、Ash Framework、Phoenix LiveView、PostgreSQL、Tailwind CSS
- デプロイ／導入
  - 自家ホスティングを前提にdocker-composeで即起動可能。Fly / Railway などクラウド向けの設定も同梱。
  - ライセンスはAGPLv3。商用利用や派生配布時のソース公開要件に注意。
- なぜ技術的に有利か
  - LiveViewでリアルタイムUI、Elixir/Erlangで高い同時接続性能。BOMのバージョン管理とコスト集計は小ロット製造の原価把握に直結。

## 実践ポイント
- まずデモを触る（READMEのデモ資格情報あり）。実運用前にUIとワークフローを確認する。
- ローカルで試す手順（例）:
```bash
# bash
curl -O https://raw.githubusercontent.com/puemos/craftplan/main/docker-compose.yml
curl -O https://raw.githubusercontent.com/puemos/craftplan/main/.env.example
cp .env.example .env
# .env を編集してシークレットを設定してから
docker compose up -d
```
- 日本の食品表示・アレルゲン対応に合わせてアレルゲン項目とラベル出力を確認する。
- 自家ホスティング利点：顧客データやレシピを社外に出さず管理できる。注意点：バックアップと運用監視は必須。
- ライセンス確認：AGPLv3は改変・配布時にソース公開義務あり。自社専用で運用する分には問題ないが、カスタム配布は法務チェックを。

短時間で導入して業務フローに合わせたカスタマイズを試せるため、個人経営の工房や小さな食品D2C事業にとって即効性のある選択肢です。
