---
layout: post
title: "Allocating on the Stack - スタック上の割り当て"
date: 2026-02-27T18:30:28.700Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://go.dev/blog/allocation-optimizations"
source_title: "Allocating on the Stack - The Go Programming Language"
source_id: 47182487
excerpt: "Go 1.26で小スライスをスタック割当しGC負荷とヒープ割当を大幅削減"
image: "https://go.dev/doc/gopher/runningsquare.jpg"
---

# Allocating on the Stack - スタック上の割り当て
小さなスライスで劇的に速くなる？Goの「ヒープ依存」を切り替える最新コンパイラ最適化

## 要約
Goコンパイラが小さなスライスのバックストアをスタックに置く最適化を導入し、短命な割り当てやGC負荷を大幅に減らす（Go 1.25〜1.26で段階的に改善）。

## この記事を読むべき理由
ヒープ割り当てとGCはクラウドコストやレイテンシに直結します。特にGoを使う日本のバックエンド／マイクロサービス開発者は、コンパイラの最適化で簡単にパフォーマンス改善が得られます。

## 詳細解説
- 問題点：forでappendを繰り返すと、最初は小さい容量(1,2,4…)で複数回ヒープ割り当てが発生し、GC負荷とコピーが増える。
- 定石：make(..., 0, N)で初期容量を確保すると起動時の割り当てを減らせるが、従来はヒープへ配置されると1回の割り当てに留まるのみ。
- Go 1.25：コンパイラが一定箇所で「小さな（例:32バイト）」スタックバッファを用意し、定数容量のmakeでスタック割り当て可能に。
- Go 1.26：appendが使われる箇所でも同様の小さなスタックバッファを推測的に使えるようになり、ループ開始時の複数ヒープ割り当てを回避。さらに、関数から返却する（エスケープする）スライスでも、必要なら最後にheapへ移す(runtime.move2heap相当の変換)ことで最適化を保つ。
- 結果：小〜中サイズのスライスが多い実ワークロードでヒープ割り当てがゼロ〜最小に。GC負荷、起動時コピー回数、キャッシュ効率が改善。

コード（短縮例）:
```go
package main

func process(c chan task) {
    var tasks []task
    for t := range c {
        tasks = append(tasks, t) // Go 1.26 では小さなスタックバッファを使える
    }
    processAll(tasks)
}
```

デバッグ用フラグ（最適化を切る）:
-gcflags=all=-d=variablemakehash=n

## 実践ポイント
- まずGoを最新安定版（1.26以上）にアップグレードして効果を確認する。
- ベンチ: go test -bench . -benchmem で割り当て回数（allocs/op）を比較。
- pprofやpprofのヒーププロファイルでヒープ割り当ての変化を確認する。
- API設計時に無理にcapacityを指定する前にコンパイラの最適化に任せつつ、頻出ホットパスは手動でmake(cap)して効果を測る。
- 最適化で挙動不審なら上記-gcflagsで切って問題を報告する。

この記事を読めば、まずはGoのバージョンを上げてベンチするだけで即効性のあるメモリ／パフォーマンス改善が期待できることが分かります。日本のクラウド運用コスト削減や低レイテンシ要件にも直結する改善です。
