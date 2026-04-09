---
layout: post
title: "Absurd Workflows: Durable Execution With Just Postgres - Postgresだけで耐久ワークフローを動かす「Absurd」"
date: 2026-04-09T11:09:01.451Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://earendil-works.github.io/absurd/"
source_title: "Absurd - Absurd"
source_id: 367799555
excerpt: "Postgresだけで再起動耐性ある永続ワークフローを実現、外部サービス不要"
image: "https://earendil-works.github.io/absurd/assets/social-preview-1200x630.jpg"
---

# Absurd Workflows: Durable Execution With Just Postgres - Postgresだけで耐久ワークフローを動かす「Absurd」
Postgresだけで“永続実行”を完結させる──インフラをシンプルにする新しいワークフローパターン

## 要約
Absurdは「Postgresのストアドプロシージャとテーブルだけ」で長時間・再起動耐性のあるワークフロー（タスク→ステップ→イベント）を実現する軽量な仕組み。追加のキューやブローカーを不要にするのが肝。

## この記事を読むべき理由
- 日本の多くのチームが既にPostgresを運用しており、追加サービスを避けてコスト・運用負荷を下げたい場合に即応用できる。
- TemporalやCadenceのような外部ワークフロー基盤を使わずに「状態保持・再試行・待機」を安全に実装できる実践的代替案を知れる。

## 詳細解説
- 基本概念：
  - タスク(task)：ワークフローの単位。Queueにディスパッチされ、Workerが処理する。
  - ステップ(step)：タスク内部のチェックポイント。成功時に戻り値をDBに永続化し、重複実行を避ける。
  - イベント(awaitEvent)：外部イベント待ち。イベントは最初の発行をキャッシュ（first emit wins）し、レースフリーを保証。
  - スリープ：時間待ちのサスペンドもサポートし、全てDBで管理されるためプロセス再起動に強い。
- 実装の核：
  - 単一のSQLスキーマ（absurd.sql）とPostgresのみで動作。ストアドプロシージャ／トランザクションを使い、整合性と再試行をDBレイヤで担保。
  - SDKは薄く言語非依存（TypeScript, Python, Go等の軽量ラッパー）。ビジネスロジックはアプリ側で書き、状態管理はDBに任せる設計。
- 運用面：
  - ロングラン処理（分→年）に耐える設計。失敗時は最後のチェックポイントから再開。
  - 保持期間やクリーンアップはSQL・cron・付属ツール(absurdctl)で設定可能。
- 他ソリューションとの比較ポイント：
  - Temporal等は専用サービス・分散コンポーネントが必要だが、Absurdは既存DBで完結し、導入コストと運用の複雑さを下げる。

## 実践ポイント
- まずはローカルPostgresにabsurd.sqlを適用してQuickstartを試す（Queue作成→簡単なタスクを登録→Worker起動）。
- 小さなワークフロー（支払い→出荷待ち→通知）でステップ／イベントの動作を確認してから本番移行する。
- 保守性のためステップは小さく分割し、戻り値はスキーマ化しておく。
- データ主権やログ監査が重要な日本の案件では、全状態がDBに残る利点（監査容易・バックアップで復元可能）を生かせる。
- 比較検討：既にTemporal等の運用があるか、小チームで運用負荷を下げたいかで採用判断をする。

以上。興味があれば、Quickstart手順や日本語での導入チェックリストも作成できます。
