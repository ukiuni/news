---
layout: post
title: "Parsing Advances"
date: 2025-12-28T21:17:15.170Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://matklad.github.io/2025/12/28/parsing-advances.html"
source_title: "Parsing Advances"
source_id: 437192221
excerpt: "進行アサートでパーサーの無限ループとOOMを即検出する実践的手法"
---

# パーサーの無限ループを一発で見つける技 — 「進行アサート」で堅牢なエラーハンドリングを実装する

## 要約
エラーレジリエントなトップダウンパーサーで陥りがちな「トークンを消費しないままループ／再帰して無限ループになる」問題を、進行（advance）を明示的にアサートする小さなAPIで防ぐ手法を紹介する。

## この記事を読むべき理由
日本でも言語処理系、静的解析ツール、VSCode拡張などで安定したパーサーは必須。デバッグが難しい無限ループやメモリ枯渇（OOM）を未然に防ぎ、テストで早期に失敗を検出できる実践的なテクニックだからだ。

## 詳細解説
背景
- エラーレジリエントなパーサー（構文木と診断を返す）は、入力の誤りに遭遇しても可能な限り解析を続ける。
- だが「エラー回復のためにトークンを消費しない分岐」を許すと、ループやPrattパーサーの再帰呼び出しによってトークン未消費のまま同じ位置を繰り返し処理し、無限ループ→最終的にOOMや巨大なスタックトレースになる。

従来の回避策
- Fuel（カウンタ）を導入して強制終了させる（原因箇所から遠いスタックでクラッシュすることが多い）。
- 「どの関数が必ずトークンを消費するか」の頭の中のマップに依存してコーディングする（人的ミスが入りやすい）。

提案された解決法（進行アサート）
- Parserに「進行管理スタック」を持たせ、ループや再帰の開始時に現在の位置を記録（advance_push）、トークンを確実に消費できたらadvance_pop、消費が不要だったと判明したらadvance_dropで取り下げる。
- 進行を期待する箇所でトークン消費（p.bump() など）を明示すると、消費しなかった場合に即座にアサーションで検出でき、どのループ／再帰で止まったかがスタックトレースに残る。

基本API（抜粋）
```typescript
class Parser {
  private tokens: Token[];
  private index: number = 0;
  private advances: number[] = [];

  advance_push() { this.advances.push(this.index); }
  advance_pop() {
    const advance = this.advances.pop();
    assert(advance !== undefined);
    assert(advance < this.index); // ここで「必ず進んだ」ことを検証
  }
  advance_drop() { this.advances.pop(); }
  // bump() はトークンを1つ消費して index を進めるものとする
}
```

Prattパーサーの代表的な問題（修正前）
```typescript
function expression_pratt(p: Parser, left: TokenTag): Expression {
  let lhs = expression_delimited(p);
  while (p.at("(")) lhs = expression_call(p, lhs);
  while (true) {
    const right = p.token();
    if (pratt_right_binds_tighter(left, right.tag)) {
      const rhs = expression_pratt(p, right.tag);
      lhs = { tag: "ExpressionBinary", operator: right.tag, lhs, rhs };
    } else {
      return lhs;
    }
  }
}
```
このコードだと `pratt_right_binds_tighter` が false を返し続けた場合、ループ内で何も進まないまま無限ループに入る可能性がある。

修正版（進行アサートを導入）
```typescript
function expression_pratt(p: Parser, left: TokenTag): Expression {
  let lhs = expression_delimited(p);
  while (p.at("(")) lhs = expression_call(p, lhs);
  while (true) {
    p.advance_push();
    const right = p.token();
    if (pratt_right_binds_tighter(left, right.tag)) {
      p.bump(); // 明示的に消費
      const rhs = expression_pratt(p, right.tag);
      lhs = { tag: "ExpressionBinary", operator: right.tag, lhs, rhs };
      p.advance_pop(); // ここで advance_push 以降に index が進んだことを検証
    } else {
      p.advance_drop(); // 進行を期待しない分岐だったため取り下げ
      return lhs;
    }
  }
}
```
- advance_pop のアサーション失敗は、どの関数／ループで「進まなかったか」を明確に示すため、デバッグが圧倒的に容易になる。

## 実践ポイント
- ループや再帰の「入口」では advance_push()、トークンを確実に消費したら advance_pop()、消費が不要な分岐なら advance_drop() を使う。
- p.bump()（またはconsume）を呼ぶ箇所を明示的に置き、消費が期待される場所で消費が起こらないとすぐに検出する。
- 単体テストやコーパス（実ファイル群）に対してフェイルファーストにすることで、不具合はテストで早期発見できる。
- 既存コードへ適用する際は、まず危険なループに対してラップを追加し、CIでコーパスを走らせて異常を洗い出す。
- Fuelは補助策として残しておきはするが、進行アサートで根本的に原因を明示する方が効果的。

