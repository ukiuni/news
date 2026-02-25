---
layout: post
title: "Show HN: Quantifying opportunity cost with a deliberately \"simple\" web app - 機会損失を数値化する「あえてシンプル」なウェブアプリ"
date: 2026-02-25T09:40:21.391Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://shouldhavebought.com/"
source_title: "SHOULDHAVEBOUGHT.COM_"
source_id: 47138631
excerpt: "売買日を入れるだけで逃した利益が即可視化される後悔ジェネレーター"
image: "https://shouldhavebought.com/images/og-main.png"
---

# Show HN: Quantifying opportunity cost with a deliberately "simple" web app - 機会損失を数値化する「あえてシンプル」なウェブアプリ
クリックした瞬間に後悔が見える――「もし売らなければ得られた額」を即座に可視化する後悔ジェネレーター

## 要約
ユーザーが資産・購入日・売却日・数量を入れると、過去の価格データから「失った（または逃した）利益」を計算して表示するシンプルなウェブアプリ。結果は共有用URLや「WALL_OF_SHAME」で公開できるユーモア強めのサービス。

## この記事を読むべき理由
日本でも個人投資や暗号資産の普及で「売り時／買い時の判断」を後悔する人が増えています。本アプリは機会損失を直感的に示すことで、損益感覚を鍛える教材やプロダクトアイデアのヒントになります。

## 詳細解説
- 主要機能
  - CALCULATOR：資産（BTC, ETH, SOL, DOGE, NVDA, GLDなど）・購入日・売却日・金額を入力し、過去価格で機会損失を計算。
  - WALL_OF_SHAME：ユーザーが公開した後悔エントリを一覧表示（ログのtail風表現で演出）。
  - SHARE_LINK_GENERATOR：/p/asset/amount/buyDate/sellDate の形式で共有リンクを生成し“公開恥”を促進。
- UI/UXは黒いユーモア寄りの文言（例："YOU COULD HAVE OWNED THAT ISLAND"）で感情に訴える設計。
- データソースと精度
  - 価格フィードは Gemini Exchange 等の取引所APIを使用。計算は過去の取引価格ベースの推定値。
- 技術スタック（原文に基づく）
  - Backend: Laravel 12.x、PHP 8.5（JIT）
  - Frontend: Alpine.js 3
  - Data feed: Gemini exchange API
  - ログ/監視: tail -f風のログ表示、稼働率表記あり
  - 決済/寄付: USDT（EVMネットワーク対応）、サイドバー広告枠（暗号で支払い）
- ライセンスと思想
  - “OPEN_PAIN_v1.0”、著作権表記は「NO_RIGHTS_RESERVED」。教育目的ではなく“感情の喚起”が主眼。

## 日本市場との関連性
- 日本でも個人投資家の数が増え、暗号資産や米国株（NVDA等）への注目が高い。取引ミスや早売りの後悔をネタに共有する文化はSNSで広がりやすい。
- 法令順守と個人情報保護（※ログ公開や共有リンクの取り扱いに注意）を重視する日本のサービス設計に対して、本アプリの“公開羞恥”モデルは議論を呼ぶ可能性がある。

## 実践ポイント
- まず自分の過去トレードで試す：購入・売却日を入れて機会損失を確認し、感覚を数値化する。
- 技術的に真似するなら：
  - 価格取得は信頼できる取引所API（例：Gemini）を使い、APIレートリミットと時刻整合を意識する。
  - フロントは軽量なAlpine.jsで十分。LaravelでAPI層とシェア用URL生成を組むと早い。
  - ログ公開は匿名化と同意を必須にして法令順守を確保する。
- 注意点：表示は過去価格の単純計算であり投資助言ではない。公開する際はプライバシーと名誉毀損リスクを確認すること。

短く言えば、このプロダクトは「感情を可視化するデータ体験」の好例。プロダクトや学習素材として真似る価値があります。
