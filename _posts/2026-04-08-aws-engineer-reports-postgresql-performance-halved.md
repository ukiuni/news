---
layout: post
title: "AWS Engineer Reports PostgreSQL Performance Halved By Linux 7.0, But A Fix May Not Be Easy - Linux 7.0でPostgreSQLの性能が半分に？修正は簡単ではない可能性"
date: 2026-04-08T23:33:10.896Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.phoronix.com/news/Linux-7.0-AWS-PostgreSQL-Drop"
source_title: "AWS Engineer Reports PostgreSQL Performance Halved By Linux 7.0, But A Fix May Not Be Easy - Phoronix"
source_id: 1240207926
excerpt: "Linux 7.0の変更でPostgreSQLが半減、回避策は難航か—運用者は今すぐ影響把握を"
image: "https://www.phoronix.net/image.php?id=2026&image=pgbench_regression"
---

# AWS Engineer Reports PostgreSQL Performance Halved By Linux 7.0, But A Fix May Not Be Easy - Linux 7.0でPostgreSQLの性能が半分に？修正は簡単ではない可能性
PostgreSQLのスループットが半減する問題、Linuxカーネル側の設計変更と“ユーザー空間での対処（RSEQ）”が論点に

## 要約
Linux 7.0のプリエンプション（割り込み再取得）周りの変更で、AWSの報告ではGraviton4上のPostgreSQLスループットが約0.5倍に低下。原因はユーザー空間でのスピンロック滞留で、カーネル側の元の挙動に戻す案はあるが採用されない可能性が高く、PostgreSQL側の対応（RSEQ利用）を提案する声が強い。

## この記事を読むべき理由
多くの日本企業で使われるPostgreSQLと、今後配布されるLinux 7.0（Ubuntu 26.04 LTSも該当）に直結する問題です。サーバ性能やSLAに影響するため、運用者・開発者は早めに影響を把握して対策を検討する必要があります。

## 詳細解説
- 何が起きたか：AWSエンジニアがベンチマークでLinux 7.0が従来カーネル比で約0.51倍のスループットしか出さないと報告。調査で、PostgreSQLプロセスがユーザー空間のスピンロックで待ち続ける時間が増えたことが主因と判明した。
- 根本原因：Linux 7.0で「利用するプリエンプションモデルを制限」する変更（フル/レイジープリエンプションにフォーカス）が入り、以前デフォルトだったPREEMPT_NONE相当の挙動が変わったことにより、ロック保持者がプリエンプト（割り込まれる）されやすくなり、待ち側のスピン時間が増えたとされる。
- 対処案の議論：PREEMPT_NONEをデフォルトに戻すパッチが投稿されたが、元の変更の作者は採用に否定的で、「PostgreSQLがRestartable Sequences (RSEQ) を使って自己対策すべき」と指摘。RSEQはユーザー空間でタイムスライス・ロック回避を助ける拡張で、Linux 7.0ではRSEQサポートも上流に入っている。
- 影響範囲：特にクラウドのARM（Graviton）環境や高スレッド数でのDB負荷に顕著。Linux 7.0はまもなく安定版リリース予定で、多くのディストリに採用されるため短期的に影響が広がる可能性がある。

## 実践ポイント
- まず影響確認：本番でLinux 7.xカーネル／Ubuntu 26.04を予定するなら、同等環境でPostgreSQLベンチを回して性能差を測る。
- 回避策候補：即効性のある対策は少ないが、安定性優先ならリリース直後は旧カーネルやディストリのバックポート版を使う検討を。カーネルを差し替えられない場合はステージングで負荷試験を増やす。
- PostgreSQL側の対応追跡：RSEQ対応や関連パッチが出るかをフォロー。アプリ側でロック設計を見直す余地があるか検討する。
- 情報収集：Linuxカーネルメーリングリスト（LKML）やPostgreSQLのリポジトリ、主要クラウドベンダーのアナウンスを注視する。

短く言えば、Linux 7.0の設計変更がDB性能に直接影響する可能性があるため、導入前の検証とアップストリームの動向チェックを今すぐ始めてください。
