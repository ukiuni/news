---
layout: post
title: "I built a terminal UI for PostgreSQL schema exploration (Go + tview) - PostgreSQLスキーマ探索のためのターミナルUIを作った（Go + tview）"
date: 2026-02-25T09:42:50.325Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/cristoferluch/persephone"
source_title: "GitHub - cristoferluch/persephone: Terminal UI for exploring PostgreSQL schemas — tables, columns and indexes at a glance."
source_id: 398182624
excerpt: "Go+tview製のPostgres TUIでライブ検索しスキーマを瞬時把握"
image: "https://opengraph.githubassets.com/e18f909edd07b70763928b8d8a0de57530ae66a6bfb0e6abb32dd69970c6f139/cristoferluch/persephone"
---

# I built a terminal UI for PostgreSQL schema exploration (Go + tview) - PostgreSQLスキーマ探索のためのターミナルUIを作った（Go + tview）
CLIだけでPostgresのテーブル・カラム・インデックスを瞬時に把握できるTUIツール。ターミナル中心の開発者に刺さる軽量ユーティリティ。

## 要約
Go製のターミナルUI（tview/tcell）でPostgreSQLのスキーマを対話的に探索するツール。ライブ検索、カラム詳細、インデックス表示、インメモリキャッシュを備え、バイナリ配布とソースからのビルド両対応。

## この記事を読むべき理由
ターミナルで手早くスキーマ把握できれば、マイグレーションやコードレビュー、障害対応の速度が大幅に上がる。日本でもPostgresはクラウド（RDS/Aurora）やオンプレで広く使われており、CLI主体の現場で即戦力になるツールです。

## 詳細解説
- 技術スタック
  - tview：ターミナルUIフレームワーク（tcellベース）でリストや入力欄を簡潔に構築。
  - tcell：ターミナル描画ライブラリ。
  - Viper：設定管理（settings.yaml読み込み）。
  - lib/pq：Postgresドライバ。
  - 実装言語はGo（単一バイナリで配布可能）。
- 主な機能
  - ライブ検索：テーブル名を入力すると即時にフィルタリング。
  - カラムインスペクタ：カラム名・型・長さ・精度・NULL可否・主キー情報を表示。
  - インデックスビューア：テーブルごとのインデックスとキー一覧を表示。
  - インメモリキャッシュ：カラム＆インデックス情報は最初に取得してキャッシュすることで高速な移動を実現。
  - マウスサポート＆キーボード操作：Ctrl+Kで検索、Tabでフォーカス移動、↑↓で一覧移動、Ctrl+Cで終了。
- 配布とビルド
  - リリースのバイナリをダウンロードしてパスに置くだけで利用可能（Linux/macOS/Windows）。
  - ソースからは git clone → go build でビルド可能。
- 設定例（settings.yaml）
```yaml
host: localhost
port: 5432
user: your_user
password: your_password
database: your_database
sslmode: disable
```

## 実践ポイント
- まずはリリースバイナリをダウンロードして試す（/usr/local/bin に置くなど）。
- VS Codeの統合ターミナルで起動すれば、エディタと並行してスキーマ確認が可能。
- マイグレーションやALTER前にライブ検索＋カラム詳細で依存関係を素早く把握する習慣を付ける。
- 社内のDBアクセスルール（RDSの接続先/認証方法）に合わせてsettings.yamlを用意する。
- 改良案やローカル運用用のパッチはリポジトリへプルリクで貢献可能。
