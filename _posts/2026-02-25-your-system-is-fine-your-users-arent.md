---
layout: post
title: "Your system is fine. Your users aren't - システムは正常でもユーザーは満足していない"
date: 2026-02-25T15:17:43.344Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.incrementalforgetting.tech/p/your-system-is-fine-your-users-arent"
source_title: "Your system is fine. Your users aren&#x27;t - by Dunya Kirkali"
source_id: 958707827
excerpt: "メトリクスが緑でも顧客が離れる真因と、ビジネスSLOで価値を測る実践法を解説"
image: "https://images.unsplash.com/photo-1610858562676-a65264bef29b?crop=entropy&amp;cs=tinysrgb&amp;fit=max&amp;fm=jpg&amp;ixid=M3wzMDAzMzh8MHwxfHNlYXJjaHw4MHx8aGFwcHklMjB1c2VyfGVufDB8fHx8MTc3MTk3MDE1NXww&amp;ixlib=rb-4.1.0&amp;q=80&amp;w=1080"
---

# Your system is fine. Your users aren't - システムは正常でもユーザーは満足していない
メトリクスが全部「緑」でもユーザーは離れる――「ビジネスSLO」で本当に価値を測る方法

## 要約
技術的SLO（可用性・レイテンシ等）だけではユーザーが得られる価値を保証できない。ユーザーの成果（ビジネスSLO）を定義し、それを計測するためにドメインイベントを計測・集約する必要がある、という議論。

## この記事を読むべき理由
ダッシュボードの指標が良くても利用者が離れる状況は日本のサービスでも頻発します。特に配車・配達・eコマースなど「瞬時の注文成立」が重要な領域では、技術指標だけでなくユーザー成果を測る設計がビジネス継続に直結します。

## 詳細解説
- 技術SLOとビジネスSLOの違い  
  - 技術SLO：インフラ・APIの正常性（例：レイテンシ、エラー率）。ガードレールとして必須。  
  - ビジネスSLO：ユーザーが期待する結果（例：乗客がリクエスト時に半径2km内に3台以上見つかる確率99.5%）。これが最終目的。

- ビジネスSLOをどう定義・測るか（SLIへの変換）  
  - まず顧客が満足と感じる「成果」を明文化する。  
  - 測定可能なSLIへ落とす：N（台数）、R（半径）、時間窓（リクエスト時点か30秒以内か）、スコープ（都市別/ゾーン別/時間帯別）。  
  - これらはプロダクト判断（ビジネス側）が主導で決めるべきトレードオフ。

- データ収集の要点（インフラ監視とは別）  
  - 必要なのはドメインイベント：ユーザーがリクエストした瞬間の「利用可能ドライバー数」などをログ／イベントとして吐く設計。  
  - 流れ：リクエスト時にドメイン情報を記録 → イベントパイプラインへ送る → 集約してSLI算出 → SLO違反でアラート／作業へ繋ぐ。  
  - 技術SLOは支援的役割。目標は常にビジネスSLO。

## 実践ポイント
- まず最重要なユーザージャーニーを一つ選ぶ（例：注文→成立）。  
- ユーザー視点で「成功」を定義する（数値化する）。  
- SLIの次元（N, R, 時間窓, スコープ）をビジネスと合意する。  
- リクエストフローで必要なドメインイベントを必ず記録する（intent時の状態をキャプチャ）。  
- イベントを集約して定期的にSLOを算出、SLO違反時に実行する運用手順を作る。  
- 小さく始める：ひとつのビジネスSLOを達成可能にして学ぶ。

以上。ビジネスSLOは「本当に届けたい価値」を測る尺度に変わります。
