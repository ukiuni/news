---
layout: post
title: "Everything Takes Longer Than You Think - すべては思ったより時間がかかる"
date: 2026-02-12T17:36:11.304Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://revelry.co/insights/software-estimation-everything-takes-longer/"
source_title: "Software Estimation - Building Takes Longer Than You Think"
source_id: 443353837
excerpt: "楽観的見積もりが招く遅延と技術負債を防ぐ、実践的な見積り術と組織対策を学ぶ"
image: "https://revelry.co/wp-content/uploads/2026/02/unnamed-1-1.jpg"
---

# Everything Takes Longer Than You Think - すべては思ったより時間がかかる
「それ、簡単でしょ？」が招く破滅—ソフトウェア見積もりの罠と回避術

## 要約
ホフスタッダーの法則（何事も見積もりより長くかかる）を軸に、見積もり失敗の心理的要因と組織的対策（Planning Poker、BVPなど）を解説し、短期的な楽を避ける実践的な手順を提示します。

## この記事を読むべき理由
日本の開発現場でも「ワンオフの即答」「外向けの楽観見積もり」で工数と技術負債が膨らみがち。案件遅延や品質低下を防ぐ具体策が得られます。

## 詳細解説
- 根本問題：ホフスタッダーの法則（Hofstadter’s Law）＝「予想より常に時間がかかる」。計画の誤差は計画の失敗ではなく、人間の認知バイアス（planning fallacy、optimism bias）が原因。
- 社会的圧力：早く安く答えると受注や信頼獲得に有利だと錯覚し、短絡的に楽観見積もりを出してしまう。Slackや雑談での「簡単でしょ？」が特に危険。
- 技術的要因：UIは単純に見えても裏側は多層構造（依存関係、API、認証、テストなど）。非技術者には複雑さが見えないため期待値のズレが生じる。
- 悪循環：過度な楽観はショートカット→技術負債の蓄積→以降の開発がさらに遅くなるという負のスパイラルを生む。
- 有効な対策：
  - Best Value Procurement（BVP）で過去実績や納期遵守率を重視する。
  - AgileのPlanning Pokerで時間ではなく「複雑さ（ストーリーポイント）」を見積もる。事前に「Acceptance Criteria（受け入れ基準）」を明確化。
  - 見積もりのバッファ（余裕）を明示し、非確実性を共有する。
  - 側面のワンオフ依頼は正式チケット化し、雑なETAを避ける。
  - 見積もり精度を計測して振り返り（実績 vs 見積り）する。

## 実践ポイント
- 次に即答でETAを出す前に「チケットと受け入れ基準を作っていい？」と返す習慣をつける。
- Planning Pokerを導入し、ストーリーポイントで合意してから担当を割り当てる。
- 重要な見積もりに対しては「過去の実績ベースのバッファ（例：+25%）」を明示する。
- 技術負債を見積もりに含め、ショートカットを取る場合は返済計画をドキュメント化する。
- 見積もりと実績を月次で比較し、ずれの原因をチームで共有する。
