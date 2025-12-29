---
layout: post
title: Why Reliability Demands Functional Programming
date: 2025-12-28 02:16:02.442000+00:00
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: https://blog.rastrian.dev/post/why-reliability-demands-functional-programming-adts-safety-and-critical-infrastructure
source_title: 'Why Reliability Demands Functional Programming: ADTs, Safety, and Critical
  Infrastructure - rastrian blog'
source_id: 46406901
excerpt: 金融や決済での致命的障害を型と関数型でコンパイル時に潰す方法を解説
---
# 型で安心を買う――なぜ信頼性は関数型＋ADTsに依るのか

## 要約
稼働中の金融／通信／決済システムで起きる多くの障害は「存在すべきでない状態」がコード内に混入することが原因だ。関数型の考え方と代数的データ型（ADT）でそのクラスのバグをコンパイル時に潰せる。

## この記事を読むべき理由
日本のミッションクリティカルなサービス（銀行決済、キャリア課金、クラウド基盤など）では「信頼性＝当たり前」であり、運用コストや監査リスクを下げるために型設計でミスを事前に防ぐ手法は即戦力になる。

## 詳細解説
- 問題の本質：多くのインシデントはアルゴリズムの複雑さではなく、「ありえない状態（magic strings、null、矛盾するフラグ、不完全なライフサイクル）」の混入による。これらは実行して初めて表面化する。
- 型による防御：ADT（和型＝sum、積型＝product）でドメインモデルを表現すると、「ある値は絶対に存在しない」とコンパイラに保証させられる。純関数と不変性は副作用を減らし、挙動を予測しやすくする。
- 和と積の使い分け：積型は「かつ（AND）」でフィールドをまとめ、和型は「どれか一つ（OR）」を表す。組み合わせればビジネスルールを型としてエンコードできる。
- 全パターン網羅（exhaustiveness）：パターンマッチや型による排他チェックにより、新しいケースを追加した際に未対応箇所をコンパイル時に検出できるため、安全なリファクタが可能になる。

簡単な例（抜粋、意図を示すためのサンプル）：

```ocaml
(* OCaml *)
type payment =
  | Cash
  | Card of string  (* last4 *)
  | Pix of string   (* key *)

let describe_payment = function
  | Cash -> "Paid in cash"
  | Card last4 -> "Card ••••" ^ last4
  | Pix key -> "Pix " ^ key
```

```typescript
// TypeScript
type Payment =
  | { kind: "cash" }
  | { kind: "card"; last4: string }
  | { kind: "pix"; key: string }

const assertNever = (x: never): never => { throw new Error("Unhandled: " + JSON.stringify(x)) }

function describePayment(p: Payment): string {
  switch (p.kind) {
    case "cash": return "Paid in cash"
    case "card": return `Card ••••${p.last4}`
    case "pix":  return `Pix ${p.key}`
    default: return assertNever(p)
  }
}
```

- 金融の実例：再試行で settle() が二重実行され、二重決済や照合ずれを引き起こすケースは、トランザクションのライフサイクルを型で厳密に表現すれば防げる（Pending→Settled→Reversed の順序や不可逆性を型に反映する）。

## 実践ポイント
- まずは新機能の境界から導入：外部APIの応答、決済の状態、ユーザー認証フローなど「状態が混ざりやすい箇所」をADTでモデル化する。
- TypeScriptなら discriminated union と readonly を使い、null/undefined を避ける。Option/Maybe ライブラリの導入も検討。
- パターンマッチや switch のデフォルトに assertNever を置き、未対応ケースをコンパイル/ビルドで検出する習慣をつける。
- 小さく移行する：まずはデータ構造の表現を変え、次に関数を純化（副作用を分離）し、最後に並列処理やリトライ戦略を型に沿って再設計する。
- テストだけに頼らない：ユニットテストは重要だが、型で表現できる不変条件は型に任せ、テストは振る舞いの検証に集中する。

