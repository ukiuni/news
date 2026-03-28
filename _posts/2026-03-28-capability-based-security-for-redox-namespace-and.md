---
layout: post
title: "Capability-based Security for Redox: Namespace and CWD as capabilities - Redox における能力（キャパビリティ）ベースのセキュリティ：名前空間とカレントディレクトリを能力として扱う"
date: 2026-03-28T15:05:05.907Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.redox-os.org/news/nlnet-cap-nsmgr-cwd/"
source_title: "Capability-based Security for Redox: Namespace and CWD as capabilities - Redox - Your Next(Gen) OS"
source_id: 1612371625
excerpt: "ファイル記述子を鍵に変え、Redoxが名前空間とCWDをユーザ空間で安全に管理する仕組みを解説"
---

# Capability-based Security for Redox: Namespace and CWD as capabilities - Redox における能力（キャパビリティ）ベースのセキュリティ：名前空間とカレントディレクトリを能力として扱う
魅力的タイトル: ファイル記述子が“鍵”になる時代へ — Redoxがユーザ空間で名前空間とCWDを能力（capability）化した理由

## 要約
Redox OSは名前空間管理とカレントワーキングディレクトリ（CWD）を「文字列」やカーネル管理のIDから「ファイル記述子を使った能力（capability）」へ移行し、カーネルを簡素化しつつユーザ空間で強力なサンドボックスを実現しました。

## この記事を読むべき理由
能力ベースの設計は将来のOSセキュリティやサンドボックス機能の土台です。日本の組込み・クラウド・セキュリティ開発者にとって、軽量マイクロカーネルとユーザ空間での権限管理がどのように実装され得るかを理解する良い実例です。

## 詳細解説
- 背景：Redoxはマイクロカーネル型で、ファイルやプロセス管理など多くをユーザ空間サービス（Scheme）として提供。従来は「/scheme/...」形式のパスから文字列でスキーム名を切り出し、カーネルが名前空間（namespace）をIDで管理していました。
- 問題点：CWDを文字列で保持すると相対パスのたびに絶対化が必要で、サンドボックス制約（例：下位限定 O_RESOLVE_BENEATH 等）の実装が難しい。カーネルがスキーム名を文字列で把握する設計は攻撃面と複雑さを増やします。
- キーアイデア（openat を主軸に）：openat(dir_fd, path) は dir_fd（ディレクトリのファイル記述子）を起点に相対パスを解決する。dir_fd を制限的に使わせればその記述子自体が「能力（鍵）」になり、外部へのアクセスを封じるサンドボックスになる。
- 実装：ユーザ空間に Namespace Manager（nsmgr）を置き、プロセスが持つ名前空間をファイル記述子（ns_fd）として管理。relibc / redox-rt は open() 呼び出しを内部で openat(ns_fd, path) に変換し、nsmgr がスキーム解決とスキームへのルーティングを担当。CWD も文字列ではなくファイル記述子（Cwd.fd）で保持し、相対パスはそのままファイル記述子起点で処理する。
- 効果：カーネルはスキーム名文字列を保持・解析する必要がなくなり責務が減る。ユーザ空間で能力（ファイル記述子）を用いることで、よりシンプルで安全なアクセス制御と柔軟なサンドボックス実現が可能に。

## 実践ポイント
- 概念把握：openat と「ファイル記述子＝能力」の考え方をまず学ぶ（Linux の openat 実験が参考になる）。
- Redox を試す：Redox の nsmgr と relibc の挙動を仮想環境で動かして、ns_fd／CWD をファイル記述子で扱う流れを確認する。
- サンドボックス設計へ応用：独自ランタイムや小型OS設計では、文字列ベースの名前解決を避け、能力（ハンドル）ベースで設計することで攻撃面を減らせる。
- 日本の現場での意義：組込みやIoT、セキュアなコンテナ実装など、軽量な能力ベース設計は低リソース環境でも有効。既存のUNIX系ソフトを移植する際は relibc の翻訳レイヤー設計を参考に。

興味があれば Redox のドキュメントや nsmgr の実装を追って、openat を軸にした能力ベース設計を手を動かして確かめてみてください。
