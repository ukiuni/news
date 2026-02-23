---
layout: post
title: "Show HN: WARN Firehose – Every US layoff notice in one searchable database - 米国の全レイオフ通知を一元検索できるデータベース"
date: 2026-02-23T02:13:11.296Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://warnfirehose.com"
source_title: "WARN Act Data & Layoff Tracker | WARN Firehose"
source_id: 47116026
excerpt: "米国の全WARN大量解雇通知を時系列検索、企業・地域別に即アラート化できるデータベース"
image: "https://warnfirehose.com/logo.png"
---

# Show HN: WARN Firehose – Every US layoff notice in one searchable database - 米国の全レイオフ通知を一元検索できるデータベース
圧倒的な「レイオフの全履歴」を手元で追える──データで読み解く米国雇用の変化

## 要約
WARN Firehoseは米50州のWARN法（大量解雇通知）を毎日スクレイプして正規化したデータベース。検索・可視化・API・バルクエクスポートで、109,000件以上／1,290万人超の影響データ（1998年以降）を提供する。

## この記事を読むべき理由
米国市場の採用・投資・サプライチェーンに関わる意思決定で、早期の異変検知や人材発掘、景気シグナル把握に直結する一次データが手に入るから。日本の企業や研究者にとって、グローバル戦略やリスク管理の重要情報源になる。

## 詳細解説
- データ収集：50州の公式WARN通知（PDF/Excel/HTMLなど）を自動スクレイパーで取得し、フォーマット差を吸収して統一。日次更新で鮮度を担保。  
- データ規模：109k+ 通知、12.9M+ 被影響者、1998年からの履歴を保持。  
- 提供形態：インタラクティブチャート、CSV/JSON/Parquet/JSON‑LD（schema.org）によるバルク出力、フル機能のREST API（フィルタ・ページング・ソート、OpenAPIドキュメント）。AI連携やML向けフォーマットも用意。  
- ユースケース：ジャーナリズム（早期スクープ）、投資家（業種別労働縮小の先読み）、リクルーター（流出人材の特定）、研究者（労働市場分析）、自治体・人材支援（再就職支援の早期計画）、不動産分析（地域経済インパクト）。  
- 技術面：パイプラインは自動化スクレイピング→正規化→API/エクスポート配信。Parquet/NDJSONなどでそのまま分析パイプラインへ投入可能。

## 実践ポイント
- まずAPIキーを取得して無料枠から試す。  
- 会社名・州・業種でフィルタしてアラートを設定、Slackやメールに連携して早期検知。  
- データはParquet/JSONでダウンロードしてPython/Rで解析（時系列、州別ヒートマップ、企業ランキング）。  
- 日本企業の海外子会社・サプライヤーが影響を受ける兆候を監視して、調達・人員計画に反映する。  
- リクルーターは解雇通知を元にターゲット企業と地域を絞り、早期接触を図る。

--- 
WARN Firehoseは「生の雇用データ」を手早く使える形で出すサービス。米国の雇用動向が事業や投資に影響する日本のプレイヤーほど、活用価値が高い。
