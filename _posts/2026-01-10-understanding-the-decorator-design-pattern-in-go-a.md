---
layout: post
title: "Understanding the Decorator Design Pattern in Go: A Practical Guide - Goにおけるデコレータ設計パターンの実践ガイド"
date: 2026-01-10T14:19:30.567Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://medium.com/design-bootcamp/understanding-the-decorator-design-pattern-in-go-a-practical-guide-493b4048f953"
source_title: "Understanding the Decorator Design Pattern in Go: A Practical Guide"
source_id: 467595409
excerpt: "Goで安全に機能追加するデコレータ設計の実践手法をログ・計測・認証例で解説"
---

# Understanding the Decorator Design Pattern in Go: A Practical Guide - Goにおけるデコレータ設計パターンの実践ガイド
Goで「後から機能を付け足す」テクニック：シンプルで安全なデコレータの作り方

## 要約
デコレータは既存のオブジェクトに振る舞いを追加するパターンで、Goでは継承ではなくインターフェースと合成（composition）で実現する。ログ・計測・認証・リトライなどの横断的関心事を分離して再利用しやすくする。

## この記事を読むべき理由
Goはサーバー・マイクロサービスで広く使われており、運用や監視のコードを本体から切り離すことが重要。デコレータを理解すると、機能追加や変更を安全かつ段階的に行え、チーム開発・運用が楽になります。

## 詳細解説
デコレータの本質：
- 「同じインターフェースを実装するラッパー」を使って、既存機能を破壊せずに前処理・後処理を挟める。
- Goでは継承がないため、interface型を用いて「ラップするオブジェクトをフィールドに持つ」形で実装する。

基本パターン（概念）：
1. 共通のインターフェースを定義する。
2. 基本実装（core）を用意する。
3. デコレータは内部に同じインターフェースを持ち、呼び出し前後で追加処理を行って内部のメソッドを呼ぶ。

簡単な実例（通知 Notifier）：
```go
package main

import (
	"fmt"
)

// go
type Notifier interface {
	Send(msg string) error
}

type EmailNotifier struct{}

func (e *EmailNotifier) Send(msg string) error {
	fmt.Println("Email sent:", msg)
	return nil
}

// デコレータの構造
type NotifierDecorator struct {
	inner Notifier
}

func (d *NotifierDecorator) Send(msg string) error {
	// デフォルトは単に委譲
	return d.inner.Send(msg)
}

// ログを付けるデコレータ
type LoggingNotifier struct {
	NotifierDecorator
}

func NewLoggingNotifier(n Notifier) *LoggingNotifier {
	return &LoggingNotifier{NotifierDecorator{inner: n}}
}

func (l *LoggingNotifier) Send(msg string) error {
	fmt.Println("[LOG] sending:", msg)
	return l.inner.Send(msg)
}
```

ミドルウェアとしての利用（HTTPハンドラ）はGoで特に馴染み深い実装例です。http.Handlerをラップするミドルウェアはデコレータの典型です：
```go
package main

import (
	"log"
	"net/http"
)

// go
func loggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		log.Printf("req: %s %s", r.Method, r.URL.Path)
		next.ServeHTTP(w, r)
	})
}

func main() {
	final := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("OK"))
	})
	http.Handle("/", loggingMiddleware(final))
	http.ListenAndServe(":8080", nil)
}
```

実装上の注意点：
- スレッド安全性：共有状態がある場合は競合に注意（mutex等）。
- エラー伝播：デコレータ層でエラーを覆い隠さないこと。
- デコレータの順序：複数重ねると順序で振る舞いが変わるので設計を明確に。
- テストしやすくするために、各デコレータは小さく単機能に保つ。

## 実践ポイント
- まずは「interfaceを定義」してから実装・デコレータを作る。型依存を避けると差し替えが楽。
- ログ・メトリクス・認証・リトライなどをデコレータに切り出すと本体が薄くなる。
- HTTPではミドルウェアチェーン（関数型のデコレータ）を活用する。順序をドキュメント化すること。
- テストではモックの内部実装を差し替えてデコレータ単体を検証する。
- パフォーマンス敏感な箇所はオーバーヘッドを測定し、必要ならデコレータの数を減らすか軽量化する。

元記事はアクセス制限のため直接参照できない場合があるが、ここで示したパターンと実践ポイントを押さえれば、Goで安全にデコレータを使い始められます。
