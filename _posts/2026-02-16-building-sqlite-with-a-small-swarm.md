---
layout: post
title: "Building SQLite with a small swarm - 小さな群れでSQLiteを構築する"
date: 2026-02-16T07:38:25.887Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://kiankyars.github.io/machine_learning/2026/02/12/sqlite.html"
source_title: "building sqlite with a small swarm | Kian Kyars"
source_id: 47031268
excerpt: "複数LLMで並列開発しRustでSQLite類似DBを18–19k行・282テスト全通で再現"
---

# Building SQLite with a small swarm - 小さな群れでSQLiteを構築する

魅力的タイトル: AIエージェント群で本物のSQLiteを再現した実験レポート — Rustで約19k行、テスト282件をパスした理由

## 要約
複数のLLMエージェント（Claude, Codex, Gemini）を並列で動かし、RustでSQLiteライクなエンジン（パーサー〜ストレージ〜WAL〜B+木〜実行器）を実装。約19k行、282個のユニットテストがすべて通った実験的プロジェクトの手法と教訓をまとめる。

## この記事を読むべき理由
AIを開発支援に使う流れは日本の開発現場でも現実的になってきています。本事例は「実コード（低レベルなDB実装）」を複数エージェントで並列開発する際の運用パターン、テスト戦略、ハードル（ロック/デデュープ/レート制限）を具体的に示しており、チーム運用や社内PoCで役立ちます。

## 詳細解説
- アーキテクチャ要素：パーサー、プランナー、Volcano実行器（iteratorベース）、ページャー、B+木インデックス、WAL（Write-Ahead Log）、リカバリ、結合・集計・グループ化、統計に基づくプランニングまで実装。モジュール境界が明確で、agentsが独立に作業できる設計が効いている。  
- エージェントワークフロー：BootstrapでClaudeがプロジェクト骨子・テストハーネスを生成。その後6つのワーカー（Claude×2、Codex×2、Gemini×2）がループでタスクを取り、実装＋テストを行いプッシュ。各エージェントは「ロックして担当タスクを主張→実装→テスト→更新」のサイクルで協調。  
- テストと検証：sqlite3をオラクルとして振る舞わせる「oracle-style」検証、頻繁なテスト実行（cargo test、./test.sh）により品質を担保。結果として282ユニットテストが全て通過。テストが“エントロピーに対する免疫”となる。  
- 調整コスト：154コミット中約54.5%がロック管理やコーディネーション関連で占められるなど、並列化は厳格なタスク分離とロック衛生管理が前提。重複・ドリフト対策として「coalescer（デデュープ用エージェント）」を用意したが、本番実行中に十分稼働させられず課題が残った。  
- 運用上の問題：各プラットフォームのレート制限や利用状況の可視化欠如が進行停滞を招いた。観測性（誰がどれだけトークンを使ったか等）を強化する必要あり。  
- 規模と成果：最終コードは約18–19k行（Rust 14ファイル中心）、154コミットを短期間で達成。ベースのリポジトリと再現手順も公開されている（必要なCLI: claude, codex, gemini, screen, git, Rust toolchain, sqlite3）。

再現コマンド（抜粋）:
```bash
# bash
git clone git@github.com:kiankyars/parallel-ralph.git
mv parallel-ralph/sqlite .
chmod 700 sqlite/*.sh
./sqlite/launch_agents.sh
# restart
./sqlite/restart_agents.sh
# coalesce
./sqlite/coalesce.sh
```

## 実践ポイント
- 小さく狭いタスクを割り振る：モジュール境界（parser→planner→executor→storage）を厳格にしてマージ競合を減らす。  
- 高頻度で自動テストを回す：oracleベースの受け入れテストを用意し、失敗は即フィードバック。テストは並列開発の”真理の源泉”。  
- ロック/クレーム管理を運用設計に入れる： stale-lockの自動クリアやロック期限など、衛生ルールを厳格化する。  
- デデュープ（coalescer）を定期実行：ドリフトは放置すると増殖するため、デデュープ用エージェントは日次で動かす。  
- 観測性を強化：トークン使用率・失敗原因（レート制限等）をログ化し、再現性を保つ。  
- 小規模PoCで先行検証：まずはパーサーやB+木など独立モジュールをエージェントに任せ、運用フローを固めてからスケールする。

短評（結論）：AIエージェントを“人員”として扱うなら、従来の分散開発と同じく設計・テスト・運用ルールが成果を決める。特に日本の現場では、品質管理と観測性を重視した導入が現実的かつ安全です。
