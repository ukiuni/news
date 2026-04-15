---
layout: post
title: "My 14-Year Journey Away from ORMs - How I Built pGenie, the SQL-First Postgres Code Generator - ORMからの14年：SQLファーストなPostgresコードジェネレータ「pGenie」誕生記"
date: 2026-04-15T12:12:40.807Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://nikita-volkov.github.io/pgenie-in-production-part-1/"
source_title: "My 14-Year Journey Away from ORMs - How I Built pGenie, the SQL-First Postgres Code Generator &#8211; Functional programming debugs you"
source_id: 715492655
excerpt: "ORMを捨て型安全なSQLファーストでDBをAPI化するpGenie誕生記"
image: "https://nikita-volkov.github.io/images/default-thumb.png"
---

# My 14-Year Journey Away from ORMs - How I Built pGenie, the SQL-First Postgres Code Generator - ORMからの14年：SQLファーストなPostgresコードジェネレータ「pGenie」誕生記

ORMをやめて「データベースをAPIにする」発想へ――型安全なSQLファースト開発を実現するpGenieの全貌

## 要約
著者は長年のORM運用の失敗からRaw SQLを前提とした設計に転じ、クエリ単位で型安全を確保するツールpGenieを作った。マイグレーション＋クエリをDBのAPIとみなすSQL-Firstの実践と、生成される型安全なクライアントが特徴。

## この記事を読むべき理由
日本のプロジェクトでもスキーマドリフトやORMの限界で保守コストが高まる事例は多い。pGenieはローカルでスキーマ再現→検証→型安全コード生成を行い、CIでのドリフト検出やLLM生成SQLの検証に直結する実用解となるため必読です。

## 詳細解説
- 背景：著者は最初にScalaのORM（SORM）を作ったが、複雑なクエリでDSLの限界とスキーマ同期問題に直面しORMアプローチを放棄。以降Raw SQLを安全に扱うライブラリ（hasql, hasql-th）を作って発展させた。  
- キーとなる気づき：
  1. SQLを覆い隠すのではなく「統合点」として使うべき（Queryがインテグレーションポイント）。  
  2. クエリそのものが要求するパラメータ型と戻り値構造を基準にコードを作ると依存が減る。  
  3. 「マイグレーション＝契約」「クエリ＝操作」と捉えればDBが一次ソースになる（SQL-First）。  
- pGenieの仕組み：CLIで migrations/ と queries/ を指し、実際のPostgresコンテナを立ち上げてマイグレーションを適用・クエリを準備・information_schemaを解析して、Haskell/Rust/Javaなど向けに100%型安全なクライアントコードを生成する。Dhall署名でビルド時にスキーマドリフトを検出し、JSONBや配列・複合型など高度なPostgres機能にも対応。  
- ビジネス面：2022年にSaaSで公開したが企業がスキーマを外部に出すのを敬遠したため、2026年にOSS化してローカル完結できるモデルに移行。

## 実践ポイント
- リポジトリを migrations/ と queries/ で整理しておく。  
- CIでpGenieを実行し、ビルド時にスキーマドリフトを検出する（Dhall署名を活用）。  
- LLMで生成したSQLはpGenieで検証→型安全SDKを自動生成して組み込むワークフローを構築する。  
- 日本の企業ではオンプレ/OSS運用が受け入れられやすいので、まずOSS版で社内PoCを回すのが現実的。  
- まずはドキュメントとデモ（pgenie.io/docs／GitHub）を確認して、小さなサービスで試してみてください。
