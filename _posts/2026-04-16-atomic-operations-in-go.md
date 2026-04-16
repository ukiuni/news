---
layout: post
title: "Atomic Operations in Go - Goのアトミック操作"
date: 2026-04-16T03:15:25.106Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://iampavel.dev/blog/atomic-operations-go"
source_title: "Atomic Operations in Go • Asaduzzaman Pavel"
source_id: 360510309
excerpt: "CASやatomic.PointerでGoのホットパスをロック無しで高速化する方法"
image: "https://iampavel.dev/og/atomic-operations-go.png"
---

# Atomic Operations in Go - Goのアトミック操作
ミューテックスに頼らず性能を引き出す──Goで使うべき「原子操作」の実践ガイド

## 要約
Goの原子操作（atomics）は、スケジューラやカーネルを介さずCPU命令で単一の値を安全に更新できるため、ホットパスの性能を大きく改善できる。一方で用途を誤るとバグや複雑化を招くため、適材適所で使うことが重要。

## この記事を読むべき理由
高スループットなWebSocketやAPIサーバ、リアルタイム処理を日本国内の事業やスタートアップでも増加している。低レイテンシで大量の同時接続を捌く際、不要なゴルーチンのパーキングを避けるために原子操作の知識が役立つ。

## 詳細解説
- ハードウェアレベル: 通常の `counter++` は読み取り・加算・書き込みの3段で競合が起きる。原子命令（例: x86 の LOCK XADD）は特定アドレスへの read-modify-write をCPU/キャッシュコヒーレンシ機構で保証し、カーネルやスケジューラを介さない。
- GoのモダンAPI: Go 1.19以降は型付きラッパー（`atomic.Int64`, `atomic.Pointer[T]`, `atomic.Bool` など）が用意され、ポインタ型ミスやアライメント問題を避けやすくなった。
- atomic.Value の落とし穴: 最初に `Store` した具体型がロックされ、以後は同じ具体型でないとパニックになる。具体型がわかるなら `atomic.Pointer[T]` を優先する。
- CASループ（Compare-And-Swap）: ロックを取らずに「読み→更新を試みる→失敗すれば再試行」というパターン。短時間の競合なら無駄な待ちが少ない。例: レートリミッタ

```go
package main

import "sync/atomic"

type RateLimiter struct {
    count  atomic.Int64
    maxRPS int64
}

func (r *RateLimiter) Allow() bool {
    for {
        cur := r.count.Load()
        if cur >= r.maxRPS {
            return false
        }
        if r.count.CompareAndSwap(cur, cur+1) {
            return true
        }
        // 競合があった場合のみループして再試行
    }
}
```

- 設定のホットリロード: 検証済みの新しい設定オブジェクトを準備してから `atomic.Pointer[T].Store` で差し替えると、読者側はロックなしで常に一貫した設定を得られる。

```go
type Config struct{ Timeout int }

type Server struct {
    cfg atomic.Pointer[Config]
}

func (s *Server) UpdateConfig(c *Config) { s.cfg.Store(c) }
func (s *Server) handleRequest() {
    cfg := s.cfg.Load()
    _ = cfg.Timeout
}
```

- 使うべきでないケース: 複数の値を一貫して更新する必要がある場合は、原子操作で無理にやるより `sync.Mutex` を使う方がシンプルで安全。64-bit 原子は 32-bit 環境でアライメント問題に注意（typed APIが助ける）。

## 実践ポイント
- 単一のカウンタ・フラグ・ポインタには `atomic.*` を検討する。
- 具体型が分かるデータは `atomic.Pointer[T]` を優先。`atomic.Value` は最初に入れた具体型が固定されることを忘れない。
- 複数フィールドを同時に更新する必要があるなら `sync.Mutex` を使う。
- 高負荷環境ではベンチマークして、キャッシュコヒーレンシのオーバーヘッドを確認する（ケースによってはミューテックスの方が速い）。
- 32-bitターゲットで64-bit原子を使う際はアライメントを確認する（パッケージスコープや `new` で確保すると安全）。

以上を押さえれば、Goでホットパスを効率化しつつ堅牢さも保てる。
