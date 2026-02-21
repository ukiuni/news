---
layout: post
title: "Building a Cloudflare Workers Usage Monitor with an Automated Kill Switch - Cloudflare Workersの使用量監視と自動キルスイッチの構築"
date: 2026-02-21T23:37:09.797Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://pizzaconsole.com/blog/posts/programming/cf-overage"
source_title: "Building a Cloudflare Workers Usage Monitor with an Automated Kill Switch"
source_id: 401039373
excerpt: "Cloudflare Workersの急増課金を即遮断する自動キルスイッチ構築ガイド"
---

# Building a Cloudflare Workers Usage Monitor with an Automated Kill Switch - Cloudflare Workersの使用量監視と自動キルスイッチの構築
請求書で青ざめないための「止める」監視システム — 即効で無駄課金を遮断する実践ガイド

## 要約
Cloudflare Workersの利用状況を定期取得して閾値を超えたら当該Workerの外部ルートを即刻切断する「キルスイッチ」を実装する仕組みを紹介。日次レポートでコスト見積もりも生成する。

## この記事を読むべき理由
Cloudflareの従量課金はリクエストとCPU時間で簡単に膨らむため、国内スタートアップやトラフィックが急増するサービス運用者にとって「請求のサプライズ」を防げる現実的な対策だからです。

## 詳細解説
- 問題点  
  - Workersはリクエスト（例: Paidプランで10M含む、超過は約$0.30/100万）とCPU時間（例: 30M ms含む、超過は約$0.02/百万ms）で課金。ループやボット攻撃、バグで短時間に大幅増が起こる。標準でハードキャップはない。  

- アプローチ（要点）  
  1. 別のWorkerが5分ごとにCloudflareのGraphQL APIから当月の利用メトリクスを取得。  
  2. 各Workerごとに閾値と比較。  
  3. 閾値を超えたら当該Workerの外部アクセス用ルート（ゾーンルート、カスタムドメイン、workers.devサブドメイン）をAPI経由で削除して即時遮断。Discordにアラート送信。  
  4. 毎朝（日次）にD1保存の履歴とコスト見積もりを含むJSONレポートを生成してDiscordへ送る。

- アーキテクチャ（構成要素）  
  - 単一のWorker＋2つのCronトリガー＋1つのWorkflow。  
    - Cron(5分): オーバーチェック、D1のクールダウンテーブルで重複抑止、オーバーワークフローを発行。  
    - Cron(8am UTC): 日次集計（Workerメトリクス＋アカウント使用量）、集計→D1保存→Discord送信。  
    - OverageWorkflow: 該当WorkerのDNS/ルーティング削除→Discord埋め込み通知。  
  - D1に保存するデータ: overage_state（TTL付きクールダウン）とusage_reports（履歴）。

- 限界（重要）  
  - 公開R2バケットへの直接読み取りはWorkerを経由しないため停止不可。  
  - Worker間の内部再帰呼び出しやDurable Objectの暴走はDNS切断で止まらない。  
  - QueuesやWorkflowsなどは別課金で自動遮断対象外（レポートのみ）。

- 設定例（デフォルト）  
  - REQUEST_THRESHOLD: 500,000（requests）  
  - CPU_TIME_THRESHOLD_MS: 5,000,000（ms ≒ 約83分のCPU）  
  - OVERAGE_COOLDOWN_SECONDS: 3600（1時間）  
  - アカウント/Workerごとの上書き可能、単一APIトークンで複数アカウント操作。

- 日次レポートに含まれる指標  
  - Worker: requests、errors、CPU time、サブリクエスト等  
  - アカウント: D1操作/ストレージ、KV操作/ストレージ、R2リクエスト/ストレージ、Queues/DO/Workflowsの使用量  
  - ISOタイムスタンプ、MB表記のストレージ、Workers Paid価格に基づくオーバーコスト見積もり

## 実践ポイント
- まずはグローバル閾値を設定し、トラフィックが激しいスクリプトだけ個別に低めに調整する。  
- 5分ごとのチェック＋1時間クールダウンの組合せで誤発動を減らす。  
- DiscordやSlackに必ず通知を送り、誰が再有効化するかの運用フローを決める（再有効化は手動推奨）。  
- 公開R2や内部再帰・Durable Objectは別途監視・ガード（例: 認証、レート制限、内部タイムアウト）を用意する。  
- 小規模チームはまずPoCとして1アカウントで導入し、日次レポートでコスト感を掴んでから複数アカウント展開する。  
- 将来的にはログ統合（Workers Logs）、ダッシュボード/再有効化UIを検討すると運用負荷が下がる。

このパターンは「監視して即遮断する」ことで突発的な課金リスクを実務的に抑える設計です。複数アカウントや運用中サービスを抱える日本の現場でもすぐ使える実践的ガイドになります。
