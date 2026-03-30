---
layout: post
title: "Turning Weekly GitHub Activity Into Blog Posts on Notion + DEV.to - 週次GitHub活動をNotionとDEV.toのブログ投稿に変える"
date: 2026-03-30T14:33:19.101Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/yashksaini/i-built-a-3-agent-pipeline-that-turns-my-github-activity-into-weekly-blog-posts-on-notion-devto-1ndn"
source_title: "Turning Weekly GitHub Activity Into Blog Posts on Notion + DEV.to - DEV Community"
source_id: 3416677
excerpt: "週次GitHub活動を自動生成しGeminiで文章化してNotionとDEV.toへ投稿"
image: "https://media2.dev.to/dynamic/image/width=1200,height=627,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fuliq11zg996tdxt4pv35.png"
---

# Turning Weekly GitHub Activity Into Blog Posts on Notion + DEV.to - 週次GitHub活動をNotionとDEV.toのブログ投稿に変える  
忘れがちな「先週の作業」を自動でまとめる！GitHub→Gemini→Notion/DEV.to 自動化パイプライン

## 要約
毎週のGitHub活動（コミット、PR、レビュー等）を自動で収集し、Geminiで一人称のブログ文にナレーションしてNotionの「プランナー」ページとDEV.toの下書きに同時公開する3-agentパイプラインを紹介。

## この記事を読むべき理由
月曜のスタンドアップで「あれ何やったっけ…」を防ぎ、週次記録を自動化して時間を節約。日本でもチーム共有・個人の振り返り・OSS活動の可視化に即使える実践的パターンです。

## 詳細解説
- 全体像：3つの専門エージェント（Harvest / Narrate / Publish）を直列で実行。Mastraでワークフローを組み、GitHub Actionsで毎週自動実行。
- Harvest（github-harvest-agent）：GraphQLで週次データ（コミット、PR、Issue、レビュー、言語統計、貢献日数）を取得。Zodでスキーマ検証。ここは決定論的処理なのでLLMは使わない。
- Narrate（narrator-agent）：Gemini（LLM）で生データを一人称のブログ記事に変換。構造化出力は遅いのでYAMLフロントマター付きプレーンテキストを使い、パース失敗時は決定論的フォールバックで必ず記事を生成する設計にして可用性を担保。
- Publish（publisher-agent）：DEV.toに記事下書きを作成→Notionに「プランナー風」ページを作成（統計テーブル、リポジトリ一覧、PR/Issueテーブル、言語比率、全文記事）。Markdown Content APIを使いページ全体を一度にPATCHで置換することでブロック単位の細かい操作とレート問題を回避。Notion MCPと直接APIツールをマージして足りない機能を補完。
- レート制御：Notion（約3 req/s）、DEV.to、GitHub等それぞれの制限に合わせてp-queue＋p-retryで共通ラッパーを作成し、429や一時障害を吸収。
- 運用上の教訓：LLMは創造的部分にのみ使う、モデルIDは環境変数で可変にする、Zodのバージョン衝突はpnpm overridesで一本化する、構造化出力よりYAML+パースのほうが高速で実運用に向く。

短いワークフロー例（概念）:
```javascript
// javascript
createWorkflow({ id: 'weekly-dispatch' })
  .then(harvestStep)   // GraphQL → WeeklyData
  .then(narrateStep)   // Gemini → blog (fallbackあり)
  .then(publishStep)   // DEV.to draft → Notion planner page
  .commit();
```

Notion Markdown Content APIでページを丸ごと置換するリクエスト（概念）:
```javascript
// javascript
await fetch(`https://api.notion.com/v1/pages/${pageId}/markdown`, {
  method: 'PATCH',
  headers: { Authorization: `Bearer ${NOTION_TOKEN}`, 'Content-Type': 'application/json', 'Notion-Version': '2026-03-11' },
  body: JSON.stringify({ type: 'replace_content', replace_content: { new_str: markdown } })
});
```

## 実践ポイント
- まずはGitHub Actionsの週次cron（例：日曜08:00 UTC）でトリガーするワークフローを作る。  
- HarvestはGraphQLで一回のクエリにまとめ、Zod等で必ず検証する（データ欠損や型変化に強くなる）。  
- LLMは「ナレーション」に限定。取得・公開は純関数で実装してコストと信頼性を確保する。  
- NotionはMarkdown Content APIで一発置換→プランナー風のテーブル・本文をMarkdownで生成すると実装が楽。  
- APIごとにp-queue＋p-retryの共通ラッパーを使い、レート制限と短期障害を吸収する。  
- 開発初期からモデルIDやAPIトークンは環境変数で管理し、Zodなどの依存衝突はパッケージマネージャのoverrideで解決する。

短時間で導入でき、チームの週次振り返り・個人ログの習慣化にすぐ役立ちます。興味があれば、この設計を日本語のREADMEテンプレートに落とし込む手順も提示できます。
