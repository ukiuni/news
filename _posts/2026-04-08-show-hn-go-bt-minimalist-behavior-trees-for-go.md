---
layout: post
title: "Show HN: Go-Bt: Minimalist Behavior Trees for Go - Go-Bt：Go向けミニマリストな行動ツリー実装"
date: 2026-04-08T16:13:10.948Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/rvitorper/go-bt"
source_title: "GitHub - rvitorper/go-bt: Minimalist BT implementation in Go · GitHub"
source_id: 47690797
excerpt: "Go向け軽量BTで非同期待ち・再試行・タイムアウトを簡潔に実装"
image: "https://opengraph.githubassets.com/5d83207aaf228affa80664b7c80de88cbc301da06e29b58f3a80c2e6f81e309f/rvitorper/go-bt"
---

# Show HN: Go-Bt: Minimalist Behavior Trees for Go - Go-Bt：Go向けミニマリストな行動ツリー実装
Goで「時間待ち・非同期・状態管理」をスマートに置き換える小さなライブラリ — go-bt入門

## 要約
go-btはGo向けの軽量なBehavior Tree実装で、time.Sleepや無限ループを使わず協調的にタスクを管理し、テスト用に時間を差し替えられるのが特徴。

## この記事を読むべき理由
サーバーワーク、ゲームAI、IoTやバックグラウンド処理で「非同期の待ち」「再試行」「タイムアウト」を明確に書きたい日本の開発者にとって、go-btはシンプルで導入が容易な選択肢になる。

## 詳細解説
- コア設計
  - ノードはステートレス。実行時の状態は汎用の `BTContext[T]` に集約されるため、ツリー自体は再利用しやすい。
  - ノードの戻り値は常に $1$（Success）, $0$（Running）, $-1$（Failure）のいずれか。これにより協調的に制御が戻る。
  - `BTContext[T]` は標準の `context.Context` を組み込み、キャンセルやタイムアウトをネイティブに扱える。
  - テスト向けに時刻関数を差し替え可能（Time-Travel Testing）。長時間待ちをモックして単体テストを高速化できる。
- 用意されたノード群
  - Composites: Selector, Sequence, MemSequence（状態を保持する順次実行）  
  - Decorators: Inverter, Optional, Timeout, Retry, Repeat  
  - Leaves: Condition, Action, Sleep（非ブロッキング待ち）
- 実行モデル
  - Supervisorがバックグラウンドで定期的にツリーを"ティック"し、ノードが `Running` を返したらそのまま戻して次のティックで再開する協調マルチタスク方式。

## 実践ポイント
- 使い始め:
  1. モジュールを追加: `go get github.com/rvitorper/go-bt`
  2. Blackboard（任意の struct）を定義して状態を保持する。
  3. ノードを組み合わせてツリーを構築し、Supervisorで一定間隔でティックする。
- テストでの工夫: `BTContext` の時刻関数をモックして Timeout/Sleep を瞬時に進めると CI が速く安定する。
- 日本市場での活用例: バッチ処理の再試行ロジック、エッジデバイスのコネクション管理、ゲーム内AIの簡潔な実装など。

簡単な例:
```go
// go
type WorkerState struct {
    IsConnected  bool
    PendingTasks int
}

// Supervisor 起動（概略）
ctx, cancel := context.WithCancel(context.Background())
btCtx := core.NewBTContext(ctx, &WorkerState{IsConnected:false, PendingTasks:2})
tree := BuildWorkerTree(cancel) // ノードを組み立てる関数
supervisor := core.NewSupervisor(tree, 100*time.Millisecond, func(err any){ println("panic:", err) })
wg := supervisor.Start(btCtx)
wg.Wait()
```

まずはリポジトリの examples を見て、黒板（Blackboard）設計と時刻モックの使い方を試すと理解が早い。
