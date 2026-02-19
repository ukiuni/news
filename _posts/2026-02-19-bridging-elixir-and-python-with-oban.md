---
layout: post
title: "Bridging Elixir and Python with Oban - ObanでElixirとPythonをつなぐ"
date: 2026-02-19T12:56:42.915Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://oban.pro/articles/bridging-with-oban"
source_title: "Bridging Elixir and Python with Oban · Oban Pro"
source_id: 47072539
excerpt: "Postgres経由でElixirとPythonのObanジョブを双方向連携しPDF生成を実現"
image: "https://oban.pro/images/bridging-with-oban/social.jpg"
---

# Bridging Elixir and Python with Oban - ObanでElixirとPythonをつなぐ
ElixirとPythonの“仕事（ジョブ）”をPostgres経由でやり取りして、言語の壁をスッと越える方法

## 要約
Elixir側とPython側が同じPostgresのoban_jobsテーブルを共有することで、Obanを使って言語をまたいだ耐久的なジョブ連携が簡単に実現できる。サンプル「Badge Forge」ではElixirがジョブを投げ、PythonがWeasyPrintでPDFを作り、完了通知をElixirに返す双方向ワークフローを示す。

## この記事を読むべき理由
日本の開発現場でも、Elixirは並列処理・運用性、Pythonは機械学習やPDF生成などのライブラリ群で強みがある。両者を安全かつ低コストで組み合わせる手法は、マイクロサービス移行やツール選定で即役立つ。

## 詳細解説
- 仕組み：両言語のOban実装が同一のob an_jobsテーブルを読み書きし、argsはJSONで保存される。キュー名で受け手を選び、ジョブごとに処理状態を更新する。
- リーダー管理：ElixirノードとPythonプロセスはそれぞれ独立してリーダーシップを管理するため、競合せず協調できる。
- PubSub：PostgresベースのPubSubでリアルタイムのメトリクス／通知をやり取りでき、ダッシュボード表示が容易。
- サンプル構成（要旨）：
  - Elixir：ジョブを badges キューへ投入。worker名は文字列でPython側の完全修飾名と一致させる。
  - Python：@workerデコレータで badges を監視。WeasyPrintでPDFを生成し、完了後に printing キューへ確認ジョブをenqueueしてElixirへ返す。
- セキュリティと運用：両アプリが同DBに接続するため、DB接続設定・権限・マイグレーション管理を厳格に。ジョブの冪等性やファイル出力パスの扱いも注意。

例（要点のみ）：

elixir
```elixir
# Elixir: ジョブ投入（workerは文字列）
Oban.Job.new(%{id: id, name: name}, worker: "badge_forge.generator.GenerateBadge", queue: :badges)
|> Oban.insert()
```

python
```python
# Python: WeasyPrintでPDF作成、完了ジョブをenqueue
from oban import worker, Job, Oban
@worker(queue="badges")
class GenerateBadge:
    async def process(self, job: Job):
        # HTMLレンダリング -> PDF出力
        await Oban.get_instance().enqueue(Job(args={"id": id, "path": path}, queue="printing", worker="BadgeForge.PrintCenter"))
```

## 実践ポイント
- まずは同一Postgresを指す開発環境を構築し、obanのスキーマを両方で共有する（マイグレーションは一元化）。
- キュー名とworker文字列を明確に定義して受け渡しを可視化する。
- 小さな処理（例：PDF生成1件）で試験運用し、冪等性・再試行戦略を検証する。
- Oban Web（Dockerイメージ）でジョブフローを監視すると動作確認が早い：docker run -e DATABASE_URL=... ghcr.io/oban-bg/oban-dash
- 運用上はDB接続の権限分離、ジョブサイズ（argsの大きさ）、長時間処理のタイムアウト設計を検討する。

参考として、まずは「Elixirでジョブを投げる → Pythonで処理して確認ジョブを返す」小さなワークフローを作ることを勧めます。
