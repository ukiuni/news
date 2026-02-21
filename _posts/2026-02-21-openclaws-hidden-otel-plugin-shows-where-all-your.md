---
layout: post
title: "OpenClaw's hidden OTel plugin shows where all your tokens go - OpenClawの隠れOTelプラグインでトークン消費の全貌を可視化"
date: 2026-02-21T18:34:00.893Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://signoz.io/blog/monitoring-openclaw-with-opentelemetry/"
source_title: "OpenClaw&#x27;s hidden OTel plugin shows where all your tokens go | SigNoz"
source_id: 399942029
excerpt: "隠しOTelでOpenClawのトークン消費を即可視化し無駄な課金を発見"
image: "https://signoz.io/img/signoz-meta-image.webp"
---

# OpenClaw's hidden OTel plugin shows where all your tokens go - OpenClawの隠れOTelプラグインでトークン消費の全貌を可視化
OpenClawの「見えないトークン消費」を丸裸にする——隠しOTelプラグインで誰がどれだけ使っているかを即可視化

## 要約
OpenClawに同梱されている diagnostics-otel プラグインを有効化すると、OpenTelemetry（トレース・メトリクス・ログ）でモデル呼び出しやツール実行のトークン消費・遅延・エラーを可視化でき、トークン課金を正確に把握できます。

## この記事を読むべき理由
LLMの利用はトークン課金が直接コストに直結します。日本の開発チームでもOpenClawで自動化ワークフローを組むなら、無駄な呼び出しと予算超過を防ぐために必須の可視化手段です。

## 詳細解説
- 何が出るか：traces（モデル呼び出し／webhook処理のスパン）、metrics（トークン数・コスト・ヒストグラム・キュー深さ・セッション状態）、logs（構造化ログをOTLPで輸出）。
- 価値：どのセッションが高コストか、遅延の原因（LLMかツールか）、ツール失敗の検出などを追加計測なしで得られる。
- 注意点：diagnostics-otelは同梱だがデフォルトで無効。プロトコルは現状 "http/protobuf" のみ（grpcは無視）。SigNoz Cloudを使う場合はポート443、headerに signoz-ingestion-key が必要。flushIntervalMs は最小1000ms（デフォルト60s、短めにすると短時間処理も追える）。

主な手順（要点のみ）
1. プラグイン有効化
2. OTLPエクスポーター設定（endpoint、headers、protocol、traces/metrics/logs有効化、sampleRate、flushIntervalMs）
3. gateway再起動してSigNozでサービス（openclaw-gateway）を確認
4. 必要ならカスタムダッシュボードJSONをインポート

## 実践ポイント
- プラグイン有効化（端末で実行）
```bash
openclaw plugins enable diagnostics-otel
```
- OTEL設定例（SigNoz Cloud向け）
```bash
openclaw config set diagnostics.enabled true
openclaw config set diagnostics.otel.enabled true
openclaw config set diagnostics.otel.traces true
openclaw config set diagnostics.otel.metrics true
openclaw config set diagnostics.otel.logs true
openclaw config set diagnostics.otel.protocol "http/protobuf"
openclaw config set diagnostics.otel.endpoint "https://ingest.<region>.signoz.cloud:443"
openclaw config set diagnostics.otel.headers '{"signoz-ingestion-key":"<YOUR_SIGNOZ_INGESTION_KEY>"}'
openclaw config set diagnostics.otel.serviceName "openclaw-gateway"
openclaw config set diagnostics.otel.sampleRate 1.0
openclaw config set diagnostics.otel.flushIntervalMs 5000
```
- 設定確認と再起動
```bash
openclaw config get diagnostics
openclaw gateway restart
```
- ログ有効化が必要な場合（現状ワークアラウンド）—フォークのブランチを使う手順
```bash
git clone https://github.com/LuffySama-Dev/openclaw.git
cd openclaw
git switch logsIsolationIssueFixed
pnpm install
pnpm build
npm install -g .
# 必要ならPATHに ~/.npm-global/bin を追加
```
- SigNozでサービス名 openclaw-gateway を開き、付属ダッシュボードかカスタムJSONをインポートして「どのセッションが何トークン使ったか」をすぐに可視化する。

短時間でトークン消費と失敗箇所を把握できれば、無駄なAPI呼び出しや予算超過を防げます。導入は数分〜10分程度なので、まずはプラグイン有効化とエンドポイント設定から始めてください。
