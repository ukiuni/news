---
layout: post
title: "Go 1.26 is released - Go 1.26 がリリースされました"
date: 2026-02-10T22:21:19.620Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://go.dev/blog/go1.26"
source_title: "Go 1.26 is released - The Go Programming Language"
source_id: 973721673
excerpt: "Go 1.26登場：Green Tea GC標準化とnew拡張で性能とコードが大幅向上"
image: "https://go.dev/doc/gopher/runningsquare.jpg"
---

# Go 1.26 is released - Go 1.26 がリリースされました
newで初期値が書ける！GCが標準化、コンパイラやツールも大幅強化されたGo 1.26の要点

## 要約
Go 1.26では言語仕様の微修正（newが式を受け取る、自己参照ジェネリクス許可）と、Green Tea GCの既定化、cgo負荷低減、コンパイラの最適化、go fixの全面改装など、性能・生産性を一段と向上させる変更が入っています。

## この記事を読むべき理由
日本のサービス開発や組込み・クラウド運用でGoを使う現場は多く、GCやcgoの改善は性能／コストに直結します。言語面の小さな変化はコード可読性やデータ構造設計にも影響するため、早めに把握して移行計画やベンチマークを行う価値があります。

## 詳細解説
- newの拡張: newのオペランドに式を渡せるようになりました。例えば
```go
x := int64(300)
ptr := &x
// ↓簡潔に
ptr := new(int64(300))
```
- ジェネリクス改良: 型パラメータリスト中で自己参照が可能になり、複雑なデータ構造やインターフェース実装が簡潔になります（たとえば自己参照型の制約定義など）。
- ガベージコレクタ: 以前実験的だった「Green Tea GC」が既定化。遅延・スループットの改善が期待できます。
- cgoとコンパイラ: cgoの基本オーバーヘッドが約30%低減。加えてスライスのバックストアをスタックに割り当てるケースが増え、関数呼び出しのコストが削減されます。
- ツール群: go fixがGo analysisフレームワークで書き直され、「modernizers」群（安全に新機能へ移行する提案）や //go:fix inline 指示を利用するinlineアナライザが追加されました。
- 新規パッケージ: crypto/hpke、crypto/mlkem/mlkemtest、testing/cryptotest など。
- 実験機能（オプトイン）: simd/archsimd（SIMD操作）、runtime/secret（秘匿データの安全消去）、runtime/pprofのgoroutineleakプロファイルなど。将来一般化予定なので早期評価が推奨されます。

## 実践ポイント
- まずローカルでGo 1.26へアップデートして、既存リポジトリをビルド・テスト（リリースノートを参照してオプトイン設定を確認）。
- Green Tea GCの挙動をベンチして性能差を確認（p95/p99のレイテンシ影響を重視）。
- cgoを使う部分や大規模スライス操作のベンチマークを実施し、コスト削減効果を確認。
- go fixのmodernizersで自動修正を試し、CIで安全に適用できるか検証する。
- SIMDやruntime/secretなどの実験機能はリスクを踏まえつつ試用し、フィードバックを提出する（リリースノート参照でオプトイン方法を確認）。

詳細は公式のGo 1.26 Release Notesを参照し、重要な変更はステージング環境で検証してから本番導入してください。
