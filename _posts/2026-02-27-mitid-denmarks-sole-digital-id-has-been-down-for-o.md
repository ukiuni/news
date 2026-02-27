---
layout: post
title: "MitID, Denmarks sole digital ID, has been down for over an hour and counting - MitID（デンマークの唯一のデジタルID）が1時間以上ダウン中"
date: 2026-02-27T11:25:52.780Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.digitaliser.dk/mitid/nyt-fra-mitid/2026/feb/driftsforstyrrelser-mitid"
source_title: "digitaliser.dk - [Løst] MitID er fortsat utilgængeligt"
source_id: 47179038
excerpt: "MitIDが1時間以上停止、銀行・行政のログインが麻痺し影響拡大中"
---

# MitID, Denmarks sole digital ID, has been down for over an hour and counting - MitID（デンマークの唯一のデジタルID）が1時間以上ダウン中
国レベルのログイン基盤が停止—あなたのサービスが「使えない」日に備えるべき理由

## 要約
デンマークの唯一のデジタルID「MitID」が、2026-02-27にログイン不能の障害を起こし、運用側が復旧作業を続けた後、12:17にサービス復帰が報告されました。市民・組織のログインが影響を受けました（原因は記事抜粋で特定されていません）。

## この記事を読むべき理由
デジタルIDは行政・金融・医療など多くの重要サービスの認証基盤です。日本のマイナンバー連携やオンライン認証を扱うエンジニア／運用担当者にとって、単一障害点のリスクと現場で必要な対策が直感的に理解できる事例です。

## 詳細解説
- 発表タイムライン：初回通知（27-02-2026 10:40）、途中更新（11:40）、12:17に「MitIDは稼働中でログイン可能」と最終更新。  
- 影響範囲：MitIDでログインする市民・組織が対象。銀行・行政手続き・企業サービスなど、MitID認証を前提にしたあらゆるシステムが一時利用不能となる。  
- 運用側の対応：MitID提供者が復旧作業を最優先で実施、利用者へ謝罪と進捗報告。記事抜粋では技術的な原因は示されていないが、単一ベンダー／単一IDの構成が可用性リスクを高める点は明白。  
- 教訓：認証基盤の可用性設計（冗長化、フェイルオーバー、監視・アラート、定期的な障害対策演習）と、利用者向けの迅速な状況共有が重要。

## 実践ポイント
- 利用者向け
  - 公式の稼働状況ページ（digitaliser.dkのドリフトステータス）をまず確認する。  
  - 垢回復用の代替認証やオフライン手段（窓口・電話）を事前に把握。  
- 組織／開発者向け
  - 認証基盤の冗長化とサプライヤー依存度の評価を行う。  
  - 障害時の代替ログイン経路や簡易化した手続きフローを用意する。  
  - 障害発生時のコミュニケーションテンプレートと監視アラートの整備・演習を実施する。

出典：digitaliser.dk（MitID driftsopdatering, 27-02-2026）
