---
layout: post
title: "Why NaN !== NaN Makes Perfect Sense (I Promise) - なぜ NaN !== NaN は理にかなっているのか（本当です）"
date: 2026-01-27T09:15:30.646Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/sylwia-lask/why-nan-nan-makes-perfect-sense-i-promise-2lke"
source_title: "Why NaN !== NaN Makes Perfect Sense (I Promise) - DEV Community"
source_id: 3179318
excerpt: "NaN!==NaNはIEEE‑754の仕様で安全設計、JSの数値バグを防ぐ理解法"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F7ka4bze0fq1ufr8hkqac.png"
---

# Why NaN !== NaN Makes Perfect Sense (I Promise) - なぜ NaN !== NaN は理にかなっているのか（本当です）
NaNが自分と等しくないのは当たり前だった — JSの“謎”をスッキリ解説

## 要約
$NaN$ は「特定の値」ではなく「未定義／無効な計算結果」を表すため、比較は常に失敗します（$NaN \neq NaN$）。これは JavaScript のバグではなく、IEEE-754 浮動小数点規格に基づく設計です。

## この記事を読むべき理由
Web フロント／バックエンド（ブラウザ、Node.js、TypeScript）で数値処理やバリデーションを扱う日本のエンジニアは、NaNの挙動を知らないとテストで見逃したりバグを招きます。金融系やデータ処理の現場では特に重要です。

## 詳細解説
- 意味論：NaN は「値がない／計算できない」ことを示すマーカーで、特定の値を指していません。複数の内部表現が許されるため「同一性」を証明できない、という考え方です（IEEE-754）。
- 挙動（例）:

```javascript
// javascript
NaN === NaN      // false
NaN !== NaN     // true
0/0             // NaN
Math.sqrt(-1)   // NaN
```

- 比較と順序：$NaN$ を含む比較はすべて false（`NaN < 1`, `NaN >= 1` など）。これは「不正な値を誤って受け入れない」ための設計。
- 検出法：直接比較（`value === NaN`）は常に失敗する。正しくは以下を使う：

```javascript
// javascript
Number.isNaN(value)   // 推奨：厳密に NaN を判定
isNaN(value)          // グローバル版は型変換を行うので注意
```

- 精密比較：`Object.is(NaN, NaN)` は true を返します。また `Object.is(+0, -0)` は false（`===` は true）。低レイヤーや数値厳密処理で有用です。
- 言語横断：この挙動は Java、Python、Rust、C/C++ 等の IEEE-754 準拠言語でも同様です。JavaScript固有の奇妙さではありません。

## 実践ポイント
- 絶対にやらない：`value === NaN` での判定。
- 代わりに使う：`Number.isNaN(value)`（ほとんどの場合これでOK）。
- 精密比較が必要なら：`Object.is(a, b)` を検討（NaN や +0/-0 を区別したい場合）。
- サニタイズ：外部入力や計算結果は `Number.isFinite()` や明示的な検証で正規化する。
- テスト＆Lint：数値の端ケース（NaN, Infinity, ±0）をユニットテストでカバーし、TypeScript の型ガードや厳格な ESLint ルールを導入する。

元記事のポイントを日本の現場向けに噛み砕くと、「$NaN \neq NaN$ は仕様であり、安全性のための決定」— 理解しておけばデバッグが早くなります。
