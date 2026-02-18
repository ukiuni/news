---
layout: post
title: "Is this the actual creator of NoSQL? - これが本当のNoSQLの創始者か？"
date: 2026-02-18T09:02:41.487Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/seanmceligot/dbapi"
source_title: "GitHub - seanmceligot/dbapi: a nosql database I created in 2004 in C"
source_id: 438790585
excerpt: "```text 2004年の軽量NoSQL風DB「greendb」が現代NoSQLの先駆けかを検証 ```"
image: "https://opengraph.githubassets.com/17373e6101372abfa6c6ffbfd4a9ddf7bb1607686dd6ebe186d7d4d503ad72e1/seanmceligot/dbapi"
---

# Is this the actual creator of NoSQL? - これが本当のNoSQLの創始者か？
2004年にC/C++で書かれた“原始的NoSQL”実装を覗く — 軽量DB「dbapi（greendb）」の中身と実用ヒント

## 要約
2004年公開のリポジトリ「seanmceligot/dbapi」は、Berkeley DBベースでC/C++とSWIGバインディングを備えた軽量NoSQL風データストア（greendb）で、現代のNoSQL概念に先行する設計要素が見られます。

## この記事を読むべき理由
NoSQLが流行する前の設計思想や低レイヤ実装の実例を知ることで、データストレージの原理や軽量DBの作り方を学べます。日本の組み込み系やレガシー移行案件、教育用途にも役立つ材料です。

## 詳細解説
- リポジトリ概要：2004年作成のdbapi（greendb）で、C/C++が主、MakefileやPython/Ruby/Guileバインディング、コマンドラインツール（mktable/addrow/list）を含みます。ライセンスはLGPL-2.1。
- アーキテクチャ：内部はTable/Schema/Row/Datum/ResultSetといったオブジェクトで構成され、主キー／外部キー風の検索や行保存が可能。Berkeley DB 4.0をストレージ基盤に使い、独自のデータ表現（IntDatum/StrDatumなど）で操作します。
- 技術スタックと依存：g++-3.2、Berkeley DB 4.0、libgc、SWIG、Guile、古いPython（2.1）など、当時のUnix系ツール群に依存。現代環境では互換性のため工夫が必要です。
- 設計的示唆：スキーマ定義＋行指向保存、再利用可能なDatumオブジェクト、言語バインディングでの利用性向上など、現在の軽量DBや組み込みDB（LMDBやSQLiteの使い方）に通じる考えが散見されます。

## 実践ポイント
- まずはローカルでコードを読む：git clone して README と sample を追う。クラス名（GreenEnv/Table/Row/Datum）を手掛かりに中身を確認。
- ビルド環境：そのままでは最新ディストリでビルド困難。古いDebianコンテナやDockerイメージ（当時のパッケージを入れたもの）を用意すると早い。
- 動かして学ぶ：付属のコマンド（mktable/addrow/list）やサンプルC++/Rubyコードで基本操作を試すと設計理解が早い。
- モダン化の提案：Berkeley DB → LMDB/RocksDB、古い言語バインディングの置き換え（Python3/SWIG更新）で実用的教材や小型組み込みDBのプロトタイプに転用可能。
- 学習用途としての価値：データ表現やシリアライズ、シンプルなクエリ実装を自作したい初学者に最適。既存プロジェクトのアーキテクト検討資料としても有用。

興味があれば、まずリポジトリをクローンしてサンプル実行→古い依存をコンテナ化して動作させる、という順で進めると学びが深まります。
