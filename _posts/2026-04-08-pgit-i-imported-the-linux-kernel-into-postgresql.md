---
layout: post
title: "Pgit: I Imported the Linux Kernel into PostgreSQL - Pgit: LinuxカーネルをPostgreSQLに取り込んだ"
date: 2026-04-08T21:21:14.820Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://oseifert.ch/blog/linux-kernel-pgit"
source_title: "pgit: I Imported the Linux Kernel into PostgreSQL - Oliver Seifert"
source_id: 47648538
excerpt: "Linuxカーネル142万コミットをPostgreSQL化し、SQLで依存関係を瞬時に解析"
image: "https://oseifert.ch/og.png"
---

# Pgit: I Imported the Linux Kernel into PostgreSQL - Pgit: LinuxカーネルをPostgreSQLに取り込んだ
1.4百万コミットをSQLで丸ごと解析できるようにしたら、カーネルの「見えない依存関係」が一瞬で見えた話

## 要約
pgitでLinuxカーネル（1,428,882コミット、24.4Mファイル版）をPostgreSQLにインポートし、差分圧縮（pg-xpatch）で実データ約2.7GBに収め、2時間で完了。以降はSQLだけで速く解析できる。

## この記事を読むべき理由
大規模リポジトリの全履歴を「検索可能なデータベース」に変える手法は、企業のモノレポ解析、セキュリティ調査、貢献者分析に直結する—日本の開発現場でも即応用できる実用的なレシピと実績が示されたため。

## 詳細解説
- 概要: pgitはGitライクなCLIだが、オブジェクトと履歴をファイルシステムではなくPostgreSQLに格納する。pg-xpatchでファイル単位の差分チェーンを作り、オンザフライでデコード・圧縮する。
- 規模と結果: 1,428,882コミット／24,384,844ファイル版／3,089,589ユニークblob。インポートは専用サーバで約2時間。Postgres上の「実データ」は2.7GB（インデックス等含めると6.6GB）。gitのpack --aggressiveは1.95GBとより小さいが、pgitは「SQLクエリで履歴を直接操作できる」価値を提供する。
- 環境とチューニング: 実行機はAMD EPYC 24c/48t、512GB RAM、RAID0 NVMe相当のSSD。重要な設定例:
  - shared_buffers ≈ 64GB、effective_cache_size ≈ 400GB、shm_size ≈ 450GB
  - import.workers = 24（物理コアに合わせる）
  - xpatch_cache_size ≈ 350GB（デコード済みコンテンツをメモリに保持）
  これらは「履歴全体をメモリ＋Postgresバッファに乗せて、ランタイムで高速な解析を可能にする」ための配慮。
- 圧縮と比較: xpatchはソーステキストを123GB→1.1GBに圧縮（テキストで114×）。gitはリポジトリ全体をグローバルに差分圧縮できるためサイズ面で有利な点もあるが、pgitはクエリ性を犠牲にしない点が差別化要因。
- 解析事例（SQLで即結果）:
  - 著者数38,506人、コミッタ数1,540人（25:1の比率）
  - コミットの61.3%が1ファイルのみ変更（「小さい単位の変更」文化が有効）
  - ファイル共変化解析（48秒で1.4Mコミットを解析）で、i915ドライバやTCPのIPv4/IPv6同時修正などの実務的パターンを抽出

## 実践ポイント
- まずは小さめリポジトリでpggit/pg-xpatchを試す（Dockerイメージが提供されている）。  
- 必要メモリは「デコード済みコンテンツ想定サイズ + PostgreSQLバッファ + オーバーヘッド」を見積もる（この記事では350GBキャッシュ＋64GB shared_buffers）。  
- 分析例として「ファイル共変化」「一発寄稿者レポート」「マージ権限の可視化」などをSQLで作ると、運用改善やセキュリティ監査に直結する。  
- 日本の現場では、モノレポ解析・外部貢献者分析・サプライチェーン監査でまず価値が出る。コスト対効果を考え、まずは部分的インポート→分析の繰り返しを推奨。
