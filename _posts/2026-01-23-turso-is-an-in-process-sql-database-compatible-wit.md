---
layout: post
title: "Turso is an in-process SQL database, compatible with SQLite - TursoはSQLite互換のインプロセスSQLデータベース"
date: 2026-01-23T02:58:43.880Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/tursodatabase/turso"
source_title: "GitHub - tursodatabase/turso: Turso is an in-process SQL database, compatible with SQLite."
source_id: 46677583
excerpt: "SQLite互換でWASM対応・非同期IOを備えたRust製組み込みDB、Tursoを確認しよう"
image: "https://opengraph.githubassets.com/56907d110f8d2fcb13a576d894e9d916e2cd3211943d9ad1d1c5845d387b01fb/tursodatabase/turso"
---

# Turso is an in-process SQL database, compatible with SQLite - TursoはSQLite互換のインプロセスSQLデータベース
SQLiteの“次”を覗く：Rustで書かれた軽量・非同期・WebAssembly対応の新世代組み込みDB「Turso」

## 要約
TursoはRustで書かれたSQLite互換のインプロセス（埋め込み）SQLデータベースで、非同期I/O、WebAssembly対応、マルチ言語バインディング、CDCやベクター検索といった最新機能を目指しています（現在はベータ）。

## この記事を読むべき理由
SQLiteは日本でもモバイル/組み込み/ローカルストレージで広く使われています。Tursoはその互換性を維持しつつRustの安全性・非同期性能・WASMでのブラウザ実行を取り入れることで、エッジやサーバレス、AI連携が必要な日本のプロダクトに新しい選択肢を提供します。

## 詳細解説
- コア設計
  - Rustで一から書かれたインプロセスDB（埋め込み型）。SQL方言、ファイルフォーマット、C APIレベルでSQLite互換を目指す。  
  - 現状はベータ。データ破損を見つけた場合の報奨制度など信頼性向上に注力。

- 主な機能
  - 非同期I/O（Linuxではio_uringを利用）のネイティブサポートで高スループットを狙う。  
  - マルチ言語バインディング：Rust/Go/JS/Python/Java/WebAssemblyなど。既存アプリに組み込みやすい。  
  - 変更データキャプチャ（CDC）でリアルタイムに更新を追える。  
  - ベクターサポート（ベクター検索/操作）、全文検索（tantivyベース）、拡張ALTERや高速スキーマ変更。  
  - 実験的：BEGIN CONCURRENT（MVCCを用いた書き込みスループット改善）、ディスク暗号化、増分計算（DBSP）など。

- AI連携（MCPサーバ）
  - CLIでMCPモードを立ち上げ、AIアシスタントからJSON-RPC経由で安全にDB操作ができる。ツール群（list_tables/execute_query/insert_dataなど）を提供し、ClaudeやCursorなどと連携可能。

- 運用上の注意
  - 現状「本番非推奨」。libSQLとは別の方向性で進化中。導入前はバックアップと充分な評価を必須。

## 実践ポイント
- まず試す（ローカル・検証用）
  - CLIインストール（bash）:
  ```bash
  curl --proto '=https' --tlsv1.2 -LsSf https://github.com/tursodatabase/turso/releases/latest/download/turso_cli-installer.sh | sh
  tursodb
  ```
- 言語別サンプル（短縮）
  - JavaScript:
  ```javascript
  import { connect } from '@tursodatabase/database';
  const db = await connect('sqlite.db');
  const rows = db.prepare('SELECT * FROM users').all();
  console.log(rows);
  ```
  - Python:
  ```python
  import turso
  con = turso.connect("sqlite.db")
  cur = con.cursor()
  print(cur.execute("SELECT * FROM users").fetchall())
  ```
- 日本向け活用案
  - モバイル/デスクトップアプリのローカルDB代替、ブラウザでの複雑クエリ実行（WASM）、エッジデバイスやIoTでの低レイテンシ解析、AIアシスタント経由の安全なクエリ検証など。
- 始め方の心得
  - まずはテスト環境で検証（特にデータ整合性・パフォーマンス）、ベータ状態を踏まえた運用計画とバックアップを必ず用意する。興味があればリポジトリにコントリビュートして挙動を追うのも有益。

以上。興味があれば、試しにローカルでtursodbを立ち上げて既存のSQLiteファイルで互換性を確認してみてください。
