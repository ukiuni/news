---
layout: post
title: "Introducing pgtui, a Postgres TUI client - Postgres用TUIクライアント「pgtui」の紹介"
date: 2026-03-16T06:10:08.368Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://kdwarn.net/programming/blog/227"
source_title: "kdwarn: Introducing pgtui, a Postgres TUI client"
source_id: 1080561791
excerpt: "端末でMarkdown/TOMLを編集しつつPostgresを高速操作できる新TUIクライアント"
---

# Introducing pgtui, a Postgres TUI client - Postgres用TUIクライアント「pgtui」の紹介
ターミナルだけでPostgresをサクッと操作できる、新しいTUIクライアント pgtui — エディタ好きな開発者に刺さるワークフロー

## 要約
pgtuiはRust製のPostgres向けTUIクライアントで、ターミナル内でテーブル閲覧・ページネーション・ソート・フィルタ・レコード編集（好きな端末エディタで）などを行えるツールです。TOMLとPostgres型の変換に注力し、sqlx／toml／ratatuiを主要技術として利用しています。

## この記事を読むべき理由
- GUIではなく端末で手早くDB操作したい開発者やSREに直結する新ツールだから。
- Markdown／TOMLで記事やメモをそのままDBに置くワークフローを考えている人、ローカルやリモートサーバ上で軽量に操作したい人に有用です。

## 詳細解説
- 技術スタック：Rustで実装。データ型マッピングにはsqlx、設定やレコード構造にtomlライブラリ、TUI描画にratatuiを使用。
- データ表現：投稿やメタ情報をTOMLで管理し、必要に応じて内部でPostgres型に変換する設計。MarkdownやプレーンテキストをTOMLフィールドに含める運用も可能。
- 主な機能：
  - データベース内の非システムリレーション（テーブル等）を一覧・ソート・フィルタ
  - リレーション定義や説明の表示（現状psqlを一部利用、将来依存解消予定）
  - テーブルデータのページネーション表示、列ソート、WHERE句によるフィルタ
  - 好みの端末エディタでのレコード挿入／編集（編集中の取り消し可、閲覧専用モードあり）
  - レコード削除は確認を要求、多列主キー対応
  - 接続情報を設定ファイルで管理、クライアント内で切替可能
  - 利用可能な操作を画面内に表示
- 開発背景：作者は「テキスト（元はMarkdown、現在はTOML）で書いてDBに保存する」ワークフローを目指しており、その実現過程で生まれたツール。

## 実践ポイント
- まずREADMEからインストールとデモ（0.10.0の動画デモあり）を確認して試してみる。
- 既存のブログ草案やメモをTOML形式にしてpgtui経由でDBに保存すると、エディタ中心の作業がそのままDB運用につながる。
- サーバで軽量に運用したい場合、GUI不要の環境でのDBメンテや簡易クエリ実行に最適。
- 開発者はsqlx/toml/ratatuiの使い方や型マッピングの実装例としてコードを参考にできる（Rust環境が前提）。

オリジナルの詳細・導入手順は元記事とREADMEを参照してください。
