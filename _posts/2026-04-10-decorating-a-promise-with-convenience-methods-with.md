---
layout: post
title: "Decorating a Promise with convenience methods without subclassing, wrapping, or changing what await returns - Awaitの戻り値を変えずにPromiseに便利メソッドを付ける方法"
date: 2026-04-10T14:57:15.644Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.gaborkoos.com/posts/2026-04-10-Decorating-Promises-Without-Breaking-Them/"
source_title: "Decorating Promises Without Breaking Them"
source_id: 365196168
excerpt: "awaitの戻り値を変えずPromiseに.json/.text等の隠しショートカットを追加する手法"
image: "https://opengraph.b-cdn.net/production/images/74740c4e-d40d-49be-83fb-7170084dbda1.png?token=3Pxj4Ccc7Z93zXgN6-HhJM8U3lpcnqtTs8xNIPoUzF4&height=614&width=620&expires=33290472379"
---

# Decorating a Promise with convenience methods without subclassing, wrapping, or changing what await returns - Awaitの戻り値を変えずにPromiseに便利メソッドを付ける方法
await fetch().json() を一行で――ネイティブを壊さず Promise に便利メソッドを付ける小技

## 要約
fetch の返り値（Promise<Response>）をラップせず、そのままに便利な .json(), .text() 等をインスタンスに追加して一行で使えるようにする手法の紹介。

## この記事を読むべき理由
同様の問題は日本のフロントエンド開発でも頻出。フレームワークやライブラリ連携で native Response を壊さずにエルゴノミクスを改善したいなら即役立つ実装パターンだから。

## 詳細解説
- 考え方：Promise は通常のオブジェクトなので、返された Promise インスタンスに直接プロパティ（メソッド）を追加する。ラップやサブクラス化を行わないため、await が返す値は純粋な Response のまま。
- 実装要点：
  - Object.defineProperties を使い、追加メソッドを enumerable:false, writable:false, configurable:false にして「見えない」「上書き不可」にする。
  - メソッドは this.then(fn) の形でフォワーディングするだけ。パースやエラー処理はネイティブに任せる（再実装しない）。
  - 同一 Promise に複数回デコレートされないよう Symbol マーカーで idempotent にする。
  - TypeScript では intersection 型で Promise<Response> とショートカットインターフェースを表す（型安全に補助）。
- トレードオフ：
  - ボディの消費ルールやパースエラーは変わらない（既読のボディに対して .json() を呼べば例外）。
  - モックや上書きを許したい場合は設計的な判断が必要。

コード例（要点のみ）:

```javascript
function attachResponseShortcuts(promise /* : Promise<Response> */) {
  const descriptor = (fn) => ({
    value: function () { return this.then(fn); },
    enumerable: false,
    writable: false,
    configurable: false,
  });

  Object.defineProperties(promise, {
    json: descriptor((r) => r.json()),
    text: descriptor((r) => r.text()),
    blob: descriptor((r) => r.blob()),
    arrayBuffer: descriptor((r) => r.arrayBuffer()),
    formData: descriptor((r) => r.formData()),
  });

  return promise;
}
```

idempotency（Symbol マーカー）:

```javascript
const DECORATED = Symbol('ffetch.responseShortcutsDecorated');
function attachResponseShortcuts(promise) {
  if (promise[DECORATED]) return promise;
  // defineProperties ...
  Object.defineProperty(promise, DECORATED, { value: true, enumerable: false });
  return promise;
}
```

TypeScript の型例:

```typescript
interface ResponseShortcuts {
  json<T = unknown>(): Promise<T>;
  text(): Promise<string>;
  // ...
}
type DecoratedPromise = Promise<Response> & ResponseShortcuts;
```

## 実践ポイント
- プラグイン／ミドルウェア設計で「オプトイン」の利点を活かす：デフォルトは純粋な fetch の挙動を維持。
- テストでは追加メソッドのモックが難しい（writable:false のため）。必要なら設計時にモック戦略を決める。
- body の二重読みや既に消費されたケースはそのまま失敗するので、ミドルウェアの順序や早期読み取りに注意。
- ライブラリ連携（instanceof チェック等）を壊さないため、ラップは避けるのが安全。
