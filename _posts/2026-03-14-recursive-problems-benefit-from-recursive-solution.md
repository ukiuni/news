---
layout: post
title: "Recursive Problems Benefit from Recursive Solutions - 再帰的な問題は再帰的な解法が向く"
date: 2026-03-14T09:55:39.758Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://jnkr.tech/blog/recursive-benefits-recursive"
source_title: "Recursive Problems Benefit from Recursive Solutions &middot; Programming should be enjoyable"
source_id: 47330946
excerpt: "短時間の仕様変更でも壊れにくい、再帰で作るツリー設計の秘訣を解説"
---

# Recursive Problems Benefit from Recursive Solutions - 再帰的な問題は再帰的な解法が向く
クリックせずにはいられないタイトル例: 「なぜツリーには再帰を使うべきか — 仕様変更に強いシンプルな設計の秘密」

## 要約
再帰的データ構造（例：二分木）を扱う問題では、再帰実装が読みやすく保守しやすいことが多い。反対に、再帰をイテレーティブに置き換えると「偶発的複雑さ」が増え、仕様変更時に脆弱になる可能性がある。

## この記事を読むべき理由
日本の開発現場でもツリーやAST、再帰的構造は頻出。短期間での仕様変更やレビューのしやすさを重視するなら、実装方法の選択が保守性に直結します。新人〜中堅エンジニアが設計判断を下す際の指針になります。

## 詳細解説
- 本質：再帰的データ構造の操作は「自然な再帰的定義（仕様）」と実装が1対1で対応すると分かりやすい。コードが仕様を反映していれば、仕様変更（例：走査順の反転）に対する修正は局所的で済む。
- 例（概念）：
  - 前順（preorder）走査は「根 → 左 → 右」。再帰では累積器を渡して簡潔に表現できる。
  - 後順（postorder）は「右 → 左 → 根（逆順の例）」で、再帰実装を少し変えるだけで対応可能。
- イテレーティブ実装の罠：
  - 明示的なスタック操作や状態管理が必要になり、コードに問題外の「実行制御の雑事」が混入する。
  - 前順→後順のような仕様変更に対して、まったく別のアルゴリズム（単一スタック／二重スタック等）を考え直す必要が出ることが多い。
- 結論：アルゴリズムの「意図」がコードから素直に読み取れることが保守性を高める。再帰はその観点で有効な選択肢。

TypeScript風のイメージ（簡略）：
```typescript
// 再帰（累積器を使った前順）
function flattenPre(node: TreeNode | null, acc: T[] = []): T[] {
  if (!node) return acc;
  acc.push(node.value);
  flattenPre(node.left, acc);
  flattenPre(node.right, acc);
  return acc;
}
```

```typescript
// イテレーティブ（スタックで明示的に管理）
function flattenPreIter(root: TreeNode | null): T[] {
  if (!root) return [];
  const stack = [root];
  const out: T[] = [];
  while (stack.length) {
    const n = stack.pop()!;
    out.push(n.value);
    if (n.right) stack.push(n.right);
    if (n.left) stack.push(n.left);
  }
  return out;
}
```

## 実践ポイント
- ツリーや再帰的データを扱うとき、まずは再帰実装で「仕様と実装の対応」を確認する。
- 仕様変更が想定される箇所は、再帰による表現で意図を明示しておくと修正が楽になる。
- パフォーマンスやスタック制約が問題になる場合のみ、イテレーティブ実装を検討する（その際はコメントで意図と制約を書き残す）。
- コードレビュー時は「この実装は仕様をどれだけ直接的に表しているか」を評価基準に含める。

--- 
（原著: "Recursive Problems Benefit from Recursive Solutions" — 要旨を日本語で再構成）
