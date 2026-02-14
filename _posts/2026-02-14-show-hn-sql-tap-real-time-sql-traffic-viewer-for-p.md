---
layout: post
title: "Show HN: SQL-tap – Real-time SQL traffic viewer for PostgreSQL and MySQL - Show HN: SQL-tap — PostgreSQL / MySQL のリアルタイム SQL トラフィック可視化ツール"
date: 2026-02-14T05:38:12.447Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/mickamy/sql-tap"
source_title: "GitHub - mickamy/sql-tap: Watch SQL traffic in real-time with a TUI"
source_id: 47011567
excerpt: "コード変更不要でターミナルから本番相当のSQLをリアルタイム監視し遅延原因を即特定"
image: "https://opengraph.githubassets.com/7445262216bc73debc450bd75a199c485188add0d46e642400023b315b20c64b/mickamy/sql-tap"
---

# Show HN: SQL-tap – Real-time SQL traffic viewer for PostgreSQL and MySQL - Show HN: SQL-tap — PostgreSQL / MySQL のリアルタイム SQL トラフィック可視化ツール
クリックせずにはいられない！ターミナルでDBの実行クエリをその場で覗ける「sql-tap」の使い方と活用法

## 要約
sql-tapはアプリとDBの間に立つプロキシ（sql-tapd）と、リアルタイムにクエリを表示・解析するTUIクライアント（sql-tap）で構成されるツール。アプリ側に変更を加えずに送受信されるSQLを監視し、EXPLAINも実行できる。

## この記事を読むべき理由
本番やステージングで発生する遅いクエリやトランザクションの問題を即座に特定でき、日本のSRE/開発チームがデバッグ効率を大幅に上げられるため。

## 詳細解説
- 構成
  - sql-tapd: PostgreSQL / MySQL のワイヤープロトコルを解析するプロキシ。アプリからの接続を受けて上流DBへ転送しつつクエリ情報をキャプチャ。
  - sql-tap: gRPC 経由でsql-tapdからイベントを受け取り、ターミナルUIで一覧・インスペクト・EXPLAINを提供。
- 主な機能
  - 透過的キャプチャ: アプリ側の接続先をプロキシのポートに向けるだけで動作。コード変更不要。
  - トランザクション追跡、プリペアドステートメントとパラメータ、実行時間、影響行数、エラーを記録。
  - EXPLAIN/ANALYZE を実行可能（EXPLAIN実行にはsql-tapdにDB接続情報を与える必要あり）。
  - TUIの操作性: リスト移動、クエリ展開、EXPLAIN、クエリ編集などのキー操作を備える。
- デプロイ方法
  - Homebrew / go install / Docker / ビルド済バイナリで導入可能。Dockerイメージ例はREADMEに記載。
- セキュリティ・運用面の注意
  - プロキシ経由で全クエリが流れるため、機密情報の取り扱いに注意。運用ではステージングで検証してから本番導入を推奨。
  - マネージドDB（RDS/Aurora等）やTLS要件によりプロキシ配置や設定が必要になる場合あり。

## 実践ポイント
- まずはローカル/ステージングで試す手順（例）
```bash
# postgres の例: プロキシを :5433 で起動してローカルPostgres :5432へ転送
DATABASE_URL="postgres://user:pass@localhost:5432/db?sslmode=disable" \
  sql-tapd --driver=postgres --listen=:5433 --upstream=localhost:5432

# 別ターミナルでTUIを接続
sql-tap localhost:9091
```
- 使い方のコツ
  - slow query を再現しながらTUIで実行時間・トランザクションの流れを追う。
  - EXPLAIN を使ってクエリプランを比較し、インデックス不足やフルスキャン箇所を特定。
  - プリペアドステートメントやバインド変数も確認し、ORMによるN+1や不適切なバインドを検出。
- 日本の現場での応用例
  - SaaSの多テナントDBで特定テナントの遅延原因調査
  - レガシーアプリのリファクタ前後でクエリ挙動を比較
  - CIのステージング環境に組み込んで回帰テスト時のクエリ変化を監視

導入は手軽なので、まずは非本番環境で試して「目で見るDBトラフィック」の恩恵を体感してみてください。
