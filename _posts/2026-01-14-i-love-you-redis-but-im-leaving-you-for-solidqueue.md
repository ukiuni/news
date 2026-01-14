---
layout: post
title: "I Love You, Redis, but I'm Leaving You for SolidQueue - Redisにありがとう、でも僕はSolidQueueに乗り換える"
date: 2026-01-14T10:54:52.166Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.simplethread.com/redis-solidqueue/"
source_title: "I Love You, Redis, But I&#039;m Leaving You for SolidQueue - Simple Thread"
source_id: 46614037
excerpt: "Rails8でRedis不要に、Postgresだけでジョブ運用を実現するSolidQueue登場"
image: "https://www.simplethread.com/wp-content/uploads/2025/11/redis-tattoo-mattK.jpg"
---

# I Love You, Redis, but I'm Leaving You for SolidQueue - Redisにありがとう、でも僕はSolidQueueに乗り換える
魅力的なタイトル: Rails 8でRedisを卒業？Postgresだけで仕事を回す「SolidQueue」がもたらすシンプル化の衝撃

## 要約
Rails 8はRedisに依存しない新しいキュー／キャッシュ／ActionCable代替（SolidQueue／SolidCache／SolidCable）を導入し、PostgreSQLなど既存のRDBだけでバックグラウンドジョブやスケジューリングを完結できるようにした。

## この記事を読むべき理由
Redis運用のコストや運用負担を減らしたい日本の中小〜ミドル規模のWebサービス運営者やRails開発者にとって、既存のデータベースでジョブ処理を完結できる選択肢は運用面で即効性のあるメリットになるから。

## 詳細解説
- なぜ置き換えが可能か  
  SolidQueueはPostgreSQLの行ロック機構（SELECT ... FOR UPDATE SKIP LOCKED）を活用することで、従来のデータベースキューが直面したロック競合問題を回避する。SKIP LOCKEDはロック中の行をスキップするため、複数ワーカーが同時にクエリしても各ワーカーが重複なくジョブを取得できる。

- アーキテクチャの要点  
  SolidQueueは主に3つのテーブルで動く：solid_queue_jobs（メタ情報）、solid_queue_ready_executions（すぐ実行できるジョブ）、solid_queue_scheduled_executions（スケジュール待ち）。ワーカーはreadyテーブルをポーリングしてFOR UPDATE SKIP LOCKEDで取得→実行→削除する。スケジューラとディスパッチャがscheduled→readyへジョブを移し、オートバキュームでMVCCのゴミは回収される。

- 再発・定期実行の仕組み  
  config/recurring.ymlにcron風の指定を書くだけでSolidQueueのスケジューラが定期ジョブをenqueueする。Fugitを使った自然言語っぽい表記で、GoodJobに似た「次回をスケジューラ側で必ず再登録する」安全なパターンを採用している。

- 同時実行制御（concurrency limits）  
  limits_concurrencyオプションでジョブ単位・キー単位に同時実行数をデータベース内のセマフォテーブルで管理できる。クラッシュしても有効期限で解放されるためデッドロックが残りにくい。

- 運用と監視  
  Mission Control JobsというOSSダッシュボードが用意され、失敗ジョブのトレース、リトライ操作、キュー別メトリクス、SQLでの調査が可能。Redis/Sidekiqの外部UIに頼らず、既存のSQLツールで確認できるのが魅力。

- マイグレーション概略  
  1) config.active_job.queue_adapter = :solid_queue に切替  
  2) gemを追加してマイグレーションを実行  
  3) sidekiq-cron → config/recurring.ymlへ移行  
  4) Procfileを更新してsolid_queue:startを起動  
  5) Redis/Sidekiq関連のgemを除去

- いつ使うべきではないか  
  毎秒数千ジョブを継続的に処理するような極めて高スループット、サブミリ秒の遅延要件、分散pub/subや高度なレートリミットの用途ではRedisが依然有利。目安としては「100ジョブ/秒未満」や遅延許容100ms以上ならSolidQueueで十分なことが多い。

## 実践ポイント
- テスト負荷を必ず計測する：想定ジョブレートでPostgresの遅延とロック挙動を検証する。  
- キュー専用DBを分ける：同一サーバでも別データベース接続にすることでスキーマ管理や運用が楽。例：

```ruby
# Ruby (config/environments/production.rb)
config.active_job.queue_adapter = :solid_queue
```

```yaml
# YAML (config/recurring.yml)
production:
  cleanup_old_sessions:
    class: CleanupSessionsJob
    schedule: every day at 2am
    queue: maintenance
```

```procfile
# Procfile
web: bundle exec puma -C config/puma.rb
jobs: bundle exec rake solid_queue:start
```

- 監視はMission Controlや既存のSQLツールで。失敗率やキューレンジをSQLでクエリしてアラート設定を作ると運用が楽。  
- 自動バキュームの監視：大量のinsert/deleteが発生するため、autovacuum設定と統計をチェックして遅延や膨張を防ぐ。  
- 段階的移行：まず非クリティカルなキューで切り替え、本番トラフィックで問題なければ全体移行する。

まとめ：日本のスタートアップ〜中規模サービスにとって、Redisを運用するコストを見直し、既存RDBで「まずは簡潔に」運用する選択肢は非常に実用的。とはいえ高スループットや特殊要件がある場合はRedis併用や検証を怠らないこと。
