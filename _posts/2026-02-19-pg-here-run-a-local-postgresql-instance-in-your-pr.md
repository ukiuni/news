---
layout: post
title: "pg-here: Run a local PostgreSQL instance in your project folder with one command - プロジェクトフォルダで1コマンド起動するPostgres「pg-here」"
date: 2026-02-19T17:17:13.966Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/mayfer/pg-here"
source_title: "GitHub - mayfer/pg-here: Per-project Postgres instances with instant snapshot &amp; restore to support yolo development methods"
source_id: 1297431901
excerpt: "プロジェクト内で1コマンド起動、スナップショットで即復元できるローカルPostgres"
image: "https://opengraph.githubassets.com/6fe4cf86719b149344a2280fab3dd91d7291d2ff4398531fa018c16df0204785/mayfer/pg-here"
---

# pg-here: Run a local PostgreSQL instance in your project folder with one command - プロジェクトフォルダで1コマンド起動するPostgres「pg-here」
プロジェクトごとにローカルPostgresを瞬時に立ち上げ、スナップショット／復元まで手軽にできるツール

## 要約
pg-hereはプロジェクトフォルダ内にPostgresインスタンスを作り、1コマンドで起動・停止・再利用できるツールです。CLIとプログラムAPIを提供し、開発環境の差分や面倒な全体インストールを避けられます。

## この記事を読むべき理由
ローカル環境で複数プロジェクトを切り替える日本の開発現場では、システム全体にPostgresを入れる手間・バージョン衝突・チームの環境差が悩みの種です。pg-hereは「プロジェクト隔離」「即時スナップショット」「手軽さ」でこれらを簡単に解消します。

## 詳細解説
- 基本動作  
  - CLI: bunx pg-here（デフォルトは username=postgres, password=postgres, database=postgres, port=55432, pg-version=auto）。起動するとプロジェクト下に pg_local/ が作られ、そこにバイナリとデータが置かれます。起動中はプロセスが生き続け、Ctrl+Cで停止します。
- 再利用とキャッシュ  
  - 既存の pg_local/data/ があれば再利用し、バイナリ版とデータフォルダのバージョン差があれば警告して対応します。これによりスナップショット的な即時復元が容易です。
- プログラム的利用  
  - Node/TypeScriptから startPgHere を呼び出せます。返り値に psql で使える接続文字列が含まれ、await pg.stop() で停止できます。

```typescript
import { startPgHere } from "pg-here";

const pg = await startPgHere({
  projectDir: process.cwd(),
  database: "my_app",
  createDatabaseIfMissing: true,
});
console.log(pg.databaseConnectionString); // psql用URL
await pg.stop();
```

- トラブルシューティング  
  - Linuxで libxml2 関連の不足が原因で起動に失敗することがあり、apt/dnf/apkで libxml2 を入れる必要があります。バージョン固定は bunx pg-here@0.1.9 のように指定可能です。

## 日本市場との関連性
- ローカル環境整備が制限されがちな企業環境（ポリシーでグローバルにDBを入れられない等）やオンボーディング時に有効。  
- Dockerを使わない軽量な代替手段として、学習イベントやハンズオン、CIの短時間ワークフローにマッチします。  
- 複数案件を並行するフリーランスやスタートアップで、プロジェクトごとのDB隔離によるトラブル削減が期待できます。

## 実践ポイント
- まず試すコマンド:
```bash
bunx pg-here
# カスタム例
bunx pg-here --username me --password secret --database my_app --port 55433 --pg-version 17.0.0
```
- プロジェクトに導入する際は pg_local/ をバージョン管理対象から除外しつつ、初期スナップショットやデータ移行手順をREADMEに明記する。  
- CIで使う場合は起動→テスト→停止の短いジョブにし、必要ならバージョンを固定して再現性を担保する。  
- Linuxで起動エラーが出たら libxml2 をインストールして再試行する。

短時間でローカルDBを試したい・環境差を減らしたい場面で即戦力になるツールです。
