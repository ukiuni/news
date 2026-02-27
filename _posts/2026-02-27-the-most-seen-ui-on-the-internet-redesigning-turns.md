---
layout: post
title: "The Most-Seen UI on the Internet? Redesigning Turnstile and Challenge Pages - インターネットで最も目にされるUI？TurnstileとChallengeページの再設計"
date: 2026-02-27T22:56:34.323Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.cloudflare.com/the-most-seen-ui-on-the-internet-redesigning-turnstile-and-challenge-pages/"
source_title: "The most-seen UI on the Internet? Redesigning Turnstile and Challenge Pages"
source_id: 47186277
excerpt: "Cloudflareが数十億表示の認証UIを再設計し、高齢者や多言語対応で摩擦を激減"
image: "https://cf-assets.www.cloudflare.com/zkvhlag99gkb/2Q3joVJDhDkjxqsQrVcje6/0912ebb79509ff05b04d11d67c4e5116/The_most-seen_UI_on_the_Internet"
---

# The Most-Seen UI on the Internet? Redesigning Turnstile and Challenge Pages - インターネットで最も目にされるUI？TurnstileとChallengeページの再設計
魅せるセキュリティUIへ――「認証ウィジェット」が世界で数十億人に与える影響と、その刷新手法

## 要約
Cloudflareは、毎日約7.67億（注：元記事は7.67 billion = 7.67億か10億か表記揺れあり）回表示されるTurnstileとChallengeページを再設計。冗長な文言や不統一な情報配置を統一し、可読性・アクセシビリティを高めることでユーザー摩擦を大幅に削減した。

## この記事を読むべき理由
日本では高齢化・モバイル中心化に伴い「短時間で理解できるUI」と「多言語／アクセシビリティ対応」がますます重要。世界標準であるCloudflareの大規模UX改善は、日本のプロダクト設計や運用にも直接応用できる実践知です。

## 詳細解説
- なぜ取り組んだか：ボット攻撃の増加で検証チャレンジの発行が急増（2023:2.14B→2024:3B→2025:5.35B／日）。利用頻度の増大は「ユーザー不満」の機会を増やす。
- 設計監査：全状態・エラーメッセージを網羅的に監査。冗長な技術文、曖昧な文言、視覚的一貫性の欠如が多数見つかった。
- 統一情報設計：Turnstile（ウィジェット）とChallenge（全画面）で同一の情報アーキテクチャを採用。アクションや説明の配置を統一し学習コストを低減。
- ユーザーテスト：8か国の多様な参加者を使いA/Bテスト。競合準拠の文言より「状態を説明する」表現（例：「Verifying...」）が好まれる結果に。
- 主要改善点：
  - 「Send Feedback」→「Troubleshoot」：報告ではなく即行動を促すラベリングに変更。
  - 色使い：赤はアイコンに限定。全面赤背景は避け、脅迫感を軽減。
  - 文言を短く、スキャンしやすく：詳細はモーダルに分離して可読性を確保。
  - アクセシビリティ強化：WCAG 2.2 AAAを目標にフォントサイズ・コントラスト・スクリーンリーダー配慮を優先。
  - 多言語対応：40以上の言語をサポートし、テキスト長の違いでも崩れない設計を実現。
- スケールの課題（抜粋）：数十億表示規模でのデプロイは設計変更だけでなくエンジニアリング／運用の連携が必須（元記事は設計・エンジニア・成果の三者視点で展開）。

## 実践ポイント
- ユーザージャーニー全体をマップして「幸せな経路」と「失敗経路」を可視化する。
- エラーメッセージは短く、行動（トラブルシュート）を最優先にする。詳細は別画面へ。
- 色とコントラストは感情に影響する。警告色は限定的に使う。
- 多言語・高齢者・スクリーンリーダーを考慮して、WCAGの上位基準を目標にする。
- 小規模でも多様なユーザーテスト（国籍・年齢・技術力）を行い仮説を検証する。
- 大規模サービスでは変更の一貫性と段階的デプロイを計画的に行うこと。

以上を踏まえれば、単なる「CAPTCHA改善」以上の、誰にとっても優しいセキュリティ体験が作れます。
