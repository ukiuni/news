---
layout: post
title: "Analyzing Geekbench 6 under Intel's BOT - IntelのBOTでGeekbench 6を解析"
date: 2026-04-01T05:07:33.489Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.geekbench.com/blog/2026/03/analyzing-geekbench-6-under-intels-bot/"
source_title: "Analyzing Geekbench 6 under Intel's BOT - Geekbench Blog"
source_id: 47596457
excerpt: "IntelのBOTがGeekbench 6を実行時に書換え、一部ワークロードで最大30%向上"
---

# Analyzing Geekbench 6 under Intel's BOT - IntelのBOTでGeekbench 6を解析
驚きの「実行時最適化」——ベンチマークを“作り変える”IntelのBOTが意味するもの

## 要約
IntelのBinary Optimization Tool（BOT）は、特定バイナリを実行時に書き換えてCPU向けに最適化し、Geekbench 6のスコアを引き上げる。これによりベンチマーク結果が実際の利用状況を反映しにくくなる可能性がある。

## この記事を読むべき理由
ベンチマークはCPU選定や製品比較で重要な指標です。BOTのような実行時最適化がスコアに影響すると、日本のエンジニアや購買担当者が性能を読み違えるリスクがあるため、仕組みと見分け方を押さえておく必要があります。

## 詳細解説
- 試験環境と対象  
  - Panther Lakeノート（MSI Prestige 16 AI+、Intel Core 9 386H）でGeekbench 6.3/6.7をBOT有効／無効で比較。
- 起動遅延の観察  
  - Geekbench 6.3：BOT有効時、初回は約40秒の起動遅延、その後は約2秒。BOT無効では遅延消失。  
  - Geekbench 6.7：BOT有効時は常に約2秒の遅延。BOT無効で遅延消失。
- スコア差（代表例）  
  - Geekbench 6.3：Single 2955 → 3119（+5.5%）、Multi 16786 → 17705（+5.5%）。一部ワークロード（Object Remover、HDR）は最大約30%向上。  
  - Geekbench 6.7：ほぼ同等（差はほぼゼロ〜僅差）。
- BOTの動作推定  
  - 実行時に実行ファイルのチェックサムを計算し、既知のバイナリなら最適化を適用。  
  - IntelのSDEでHDRワークロードを解析すると、総命令数が約14%減り、スカラー命令が大幅減（約62%減）、ベクトル命令が大幅増（約1366%増）。  
  - つまり、BOTは単なる並べ替え以上に「ベクトル化（同時に複数データを処理する命令へ変換）」など高度な変換を行っている。
- 問題点  
  - 実際のアプリは多様なコードスタイルだが、BOTは特定バイナリをCPU向けに“最適化済みバイナリ”に置き換え、ピーク性能を測る傾向に。これが比較性を損ない、Intel製CPUが相対的に有利に見える可能性がある。

## 実践ポイント
- Geekbench 6.7以降はBOT検出とフラグ表示が追加されるので、ベンチ結果を確認するときは「BOTフラグ」を必ずチェックする。  
- 公正な比較が必要な場合は、BOT無効の結果、または実アプリでのベンチ（実ワークロード）を併用する。  
- 短時間のプロセスではBOTの起動遅延（2～40秒）が逆に不利になる点を考慮する。  
- ベンダー公表のレビューやクラウドベンチ結果を見る際は、最適化の有無と検出方法に注意する。  

（元記事：John Poole / Primate Labs — Geekbench Blog）
