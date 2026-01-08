---
layout: post
title: "Sakila25: Updated Classic Sakila Database with 2025 Movies from TMDB – Now Supports Multiple DBs Including MongoDB - Sakila25：TMDBの2025年映画データで復活、MongoDB含む複数DB対応"
date: 2026-01-08T15:00:24.277Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/lilhuss26/sakila25"
source_title: "GitHub - lilhuss26/sakila25: Re-creation of sakila database with 2025 data from TMDB API, available with multiple database engines"
source_id: 468039546
excerpt: "TMDBの2025年データで現代版Sakilaを再構築、MongoDB含む複数DBで即学習できる教材"
image: "https://opengraph.githubassets.com/9d05140b2827e1f69848bd273ffdfd469f0557c1767985132965bfd207fc2353/lilhuss26/sakila25"
---

# Sakila25: Updated Classic Sakila Database with 2025 Movies from TMDB – Now Supports Multiple DBs Including MongoDB - Sakila25：TMDBの2025年映画データで復活、MongoDB含む複数DB対応

実データで学べる「モダンSakila」—ストリーミング時代のスキーマとNoSQLを一度に試せるサンプルDB

## 要約
Sakila25は古典的サンプルDB「Sakila」を2025年のTMDB実データで再構築し、MySQL/PostgreSQL/SQL Serverに加えてMongoDB（非正規化）をサポートする実践向けプロジェクトです。API駆動で再現可能、CSVエクスポートや既成ダンプも提供。

## この記事を読むべき理由
- 実データ（TMDB）を使った近代的なサンプルで、DB設計・ETL・API統合の学習コースや社内ワークショップに最適。  
- 日本の開発現場でも増える「ストリーミング／サブスクリプション」モデルやNoSQL導入の検証に即使える素材を提供。

## 詳細解説
- 何が変わったか: 旧Sakilaのレンタル店モデルを「プロバイダ（ストリーミング）／サブスク／決済」へ置き換え。映画データはTMDB APIから取得し、顧客情報やカード情報はRandom User/Fakerなどで現実味を持たせている。  
- マルチDB対応: SQL系（MySQL, PostgreSQL, SQL Server）はスキーマ／ビューを用意、Pythonスクリプトで生成可能。MongoDBは読み取り性能を意識した非正規化（filmsにactorsやcategories埋め込み）で実装。接続はSQLAlchemy＋各種ドライバ／pymongoで行う。  
- 再現性: Python 3.12＋requests/pandas等でAPI取得→整形→DB挿入を自動化。CSV出力や事前作成ダンプ（Sakila25フォルダ）があるため、すぐに復元して触れる。  
- 実務的ポイント: ビュー（actor_info, film_list, revenue_by_provider）でよく使う分析クエリを用意。SQL Serverの仕様差（ビュー内でORDER BY不可）などDB間の違いも配慮済み。  
- 技術スタック: SQLAlchemy, pymongo, psycopg2, pymysql, pymssql, pandas, python-dotenv 等。

## 実践ポイント
- まず触る（最短手順）:
```bash
git clone https://github.com/lilhuss26/sakila25.git
cd sakila25
pip install -r requirements.txt
# .env を .env.example を元に作成してから、必要なDBの作成/スクリプトを実行
```
- .envの最低設定例:
```env
TMDB_API_KEY="あなたの_tmdb_api_key"
MYSQL_STRING="mysql+pymysql://user:pass@localhost:3306"
POSTGRESQL_STRING="postgresql+psycopg2://user:pass@localhost:5432/sakila25"
MONGODB_STRING="mongodb://user:pass@localhost:27017/"
```
- 日本での活用アイデア:
  - 社内研修用データセット：実在映画データでETLやクエリパフォーマンスを学べる。  
  - マイグレーション検証：RDB→MongoDBの非正規化設計を比較し、読み取り/書き込み特性を評価。  
  - 分析PoC：CSVエクスポートでBIツールに接続して収益/プロバイダ分析を実演。  
- 注意点: TMDB APIキーが必要、クレジットカードデータはテスト生成なので実運用には適さない。DB接続文字列やファイアウォール設定を確認してから実行すること。

短時間で「モダンDB設計／API連携／NoSQL比較」を体験できる良質な教材リポジトリ。社内ハンズオンや個人の学習環境にぜひ導入してみてください。
