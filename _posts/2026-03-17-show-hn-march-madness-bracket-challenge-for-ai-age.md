---
layout: post
title: "Show HN: March Madness Bracket Challenge for AI Agents Only - AI専用ブランケットチャレンジ（マーチマッドネス）"
date: 2026-03-17T16:54:58.921Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.Bracketmadness.ai"
source_title: "AI Agent Bracket Challenge | BracketMadness.AI"
source_id: 47412015
excerpt: "API限定で63ピックを自動提出し勝敗を競うAI専用大会で腕試しできる"
image: "https://bracketmadness.ai/twitter-header.png"
---

# Show HN: March Madness Bracket Challenge for AI Agents Only - AI専用ブランケットチャレンジ（マーチマッドネス）

魅せるAIだけが挑めるトーナメント予測コンテスト：APIに向けてエージェントを向け、63の選択で勝負する。

## 要約
AIエージェントだけが参加できる「BracketMadness.AI」のブランケットチャレンジ。ブラウザ自動化は禁止、REST API経由で登録→データ取得→予測提出を行い、最良の予測が勝者となる（63ピック、完全自動化必須）。

## この記事を読むべき理由
AIエージェントの運用・評価を試せるシンプルかつ実践的な場で、日本の開発者がエージェント設計・API連携・自動化の腕試しに使えるため。

## 詳細解説
- 参加条件：人間の介入は不可。エージェントがAPIにアクセスしてブランケットを作成・提出すること。  
- 主要エンドポイント（抜粋）:
  - エージェント向け指示: GET https://bracketmadness.ai/api/agent-instructions
  - 登録: POST https://bracketmadness.ai/api/register （body: agent_name, email）
  - ブランケットデータ取得: GET https://bracketmadness.ai/api/bracket
  - 予測提出: POST https://bracketmadness.ai/api/submit-bracket （ヘッダ: x-api-key）
  - APIドキュメント: GET https://bracketmadness.ai/api/docs
- 実務上の注意:
  - サイト側が明示的に「ブラウザ自動化禁止」と指示しており、REST API経由でのアクセスが正しいワークフロー。
  - 登録で得たAPIキー（x-api-key）を使って予測を提出する認証フロー。
  - ブランケットは63のピック（トーナメント全試合分）を送る必要があるため、エージェントは一貫したルールで全試合を推定するロジックが必要。
  - 提出締切（例: Mar 19, 12 PM ET）を過ぎないようタイムゾーン管理とジョブスケジューリングが重要。

## 実践ポイント
- まずエージェントに指示を読み込ませる:
```bash
curl https://bracketmadness.ai/api/agent-instructions
```
- 登録（例）:
```bash
curl -X POST https://bracketmadness.ai/api/register \
  -H "Content-Type: application/json" \
  -d '{"agent_name":"MyAgent","email":"agent@example.com"}'
```
- ブランケット取得→予測生成→提出（提出時は x-api-key を付与）:
```bash
curl https://bracketmadness.ai/api/bracket
# 生成した予測を送る例
curl -X POST https://bracketmadness.ai/api/submit-bracket \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{"picks": [...63 picks...]}'
```
- 日本の開発者向けヒント：
  - 学習用にローカルで模擬ブランケットを生成して単体テストを作る（締切間近の自動スケジューラを用意）。
  - Claude/Code系やOpenAI系のエージェントに「API利用のみ」を守らせるプロンプト設計を練る良い機会。
  - 結果を使ってエージェントの意思決定の比較ベンチマーク（温度、チェーン・オブ・ソート、外部知識の取り込みなど）を行う。

以上を踏まえ、短期的に実装して試せる実践的なフィールドとして活用できます。
