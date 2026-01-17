---
layout: post
title: "Finding and Fixing a 50k Goroutine Leak That Nearly Killed Production - 5万のGoroutineリークが本番を危機に陥れた話"
date: 2026-01-17T12:55:51.925Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://skoredin.pro/blog/golang/goroutine-leak-debugging"
source_title: "Finding and Fixing a 50,000 Goroutine Leak That Nearly Killed Production | Serge Skoredin"
source_id: 46577968
excerpt: "キャンセル漏れやTicker未停止で発生した5万goroutine漏れの原因と即効・恒久対策を公開"
image: "https://skoredin.pro/images/og-golang-debugging.png"
---

# Finding and Fixing a 50k Goroutine Leak That Nearly Killed Production - 5万のGoroutineリークが本番を危機に陥れた話
深夜の救命劇：5万のGoroutineが増殖した原因と、現場で効いた“即効”と“根本対策”

## 要約
本番サービスで6週間かけて徐々に増えた約50,000のGoroutineが応答遅延・メモリ爆増を引き起こした事例。原因は「キャンセルされないコンテキスト」「StopされないTicker」「閉じられないチャネル」の組合せで、pprof/goleakと簡単な運用対応で回復・防止した。

## この記事を読むべき理由
Golangの並行処理は強力だが、ライフサイクル管理を怠ると気付かないままリソースが枯渇します。日本のSaaS／API運用チームやWebSocketを使う開発者が直面しやすい実録と対処法が学べます。

## 詳細解説
- 症状の経緯  
  小さな遅延→タイムアウト増→メモリ増加という“徐々に悪化する”パターン。週ごとに goroutine と RAM が指数的に増え、6週目にピーク（約50k goroutines、47GB）に到達。

- 根本原因（“完璧に見えた”コードの盲点）
  1. Cancelが呼ばれていない：Subscribeでcontext.WithCancelを作るが切る側が存在しないため goroutine が永久に待機。  
  2. TickerをStopしない：heartbeatで time.NewTicker を作るが Stop を呼ばないとタイマー構造体が残留してリークを増幅。  
  3. チャネルが閉じられない：メッセージ送信側が送り続ける／チャネルをCloseしないことでメモリが増える。

- デバッグ手法
  - pprof の goroutine dump を取得して関数ごとの件数を集計し、どの関数が大量に走っているかを特定。
  - Uber の goleak を単体テストに導入して、テスト段階でリークを検出。
  - 緊急診断エンドポイントでサブスクリプション一覧と「実際に生きている接続数」を突き合わせることで“死んだサブスクが残っている”ことを確認。

- その場で効いた手当てと復旧
  - 即時対応：新規の“goroutine受け入れ制限”で止血（runtime.NumGoroutine()で閾値超えたら503を返すなど）。  
  - 一括クリーンアップ：現存するサブスクリプションに ping 送信し応答がないものを Unsubscribe。徐々に goroutine とメモリが回復。  
  - 恒久対策：Subscribe/Unsubscribe 周りの修正と監視、テスト強化を導入。

- 運用・セキュリティ面
  - GoroutineリークはDoSの入り口になり得る。作成頻度を制限する、監視アラートを設定する、負荷下での挙動を確認することが重要。

- テストと監視
  - goleak を使った単体・負荷試験でリーク検出を自動化。  
  - Prometheus による go_goroutines_count や websocket_subscriptions_total / websocket_connections_active のメトリクスを追加し、しきい値アラートを設定。

短い修正例（要点のみ）

```go
package service

import (
    "context"
    "time"
    "github.com/gorilla/websocket"
)

type subscription struct {
    userID  string
    ws      *websocket.Conn
    messages chan Message
    cancel  context.CancelFunc
}

func (s *NotificationService) Subscribe(userID string, ws *websocket.Conn) {
    ctx, cancel := context.WithCancel(context.Background())
    sub := &subscription{
        userID:  userID,
        ws:      ws,
        messages: make(chan Message, 10),
        cancel:  cancel,
    }

    s.mu.Lock()
    s.subscribers[userID] = sub
    s.mu.Unlock()

    ws.SetCloseHandler(func(code int, text string) error {
        s.Unsubscribe(userID)
        return nil
    })

    go s.pumpMessages(ctx, sub)
    go s.heartbeat(ctx, sub)
    go s.monitorConnection(ctx, sub)
}

func (s *NotificationService) Unsubscribe(userID string) {
    s.mu.Lock()
    defer s.mu.Unlock()
    if sub, ok := s.subscribers[userID]; ok {
        sub.cancel()
        close(sub.messages)
        delete(s.subscribers, userID)
    }
}
```

緊急デバッグ用の goroutine ダンプ取得（一例）:

```bash
curl http://api-server:6060/debug/pprof/goroutine?debug=2 > goroutines.txt
```

テストでの goleak 例（簡略）:

```go
import "go.uber.org/goleak"

func TestNotificationService_NoLeak(t *testing.T) {
    defer goleak.VerifyNone(t)
    svc := NewNotificationService()
    ws := mockWebSocket()
    svc.Subscribe("u1", ws)
    ws.Close()
    time.Sleep(100 * time.Millisecond)
}
```

## 実践ポイント
- 全ての goroutine に「停止手段」を与える（context を渡し cancel を呼べる設計にする）。  
- time.NewTicker は必ず Stop() する（defer で忘れ防止）。  
- make(chan) は所有者が必ず閉じる（close）。送信側が閉じる設計にする。  
- 単体テストで goleak を導入し、継続的にリーク検出を行う。  
- 本番では runtime.NumGoroutine() をメトリクス化しアラートを設定する。閾値を超えたら即対応できる仕組みを用意する。  
- WebSocketなど「接続ごとに複数のgoroutineを生む」機能はスケールを見越した設計と上限管理（プールやセマフォ）を行う。

この事例が示すのは「小さなミスの組合せで大事故になる」という普遍的な教訓です。Golangの並行処理は便利ですが、ライフサイクル管理と監視を必須にすることで、夜中の復旧劇は防げます。
