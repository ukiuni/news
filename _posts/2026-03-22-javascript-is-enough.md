---
layout: post
title: "JavaScript Is Enough - JavaScriptで十分"
date: 2026-03-22T01:58:55.448Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://geajs.com/"
source_title: "Gea — Lightweight Reactive UI Framework"
source_id: 47473231
excerpt: "学習コストほぼゼロで13KBの超高速UIを実現するGeaとは？"
---

# JavaScript Is Enough - JavaScriptで十分

学ぶ必要なし、ただのJSで超高速UIを作る新フレームワーク「Gea」

## 要約
Geaは「新しい概念を覚えずに使える」コンパイル時リアクティブUIフレームワーク。仮想DOMやフックなしで、ビルド時に差分パッチを生成して直接DOMを更新します。バンドルは約13KB（router含）、ランタイム依存ゼロ。

## この記事を読むべき理由
日本でも軽量で高速なフロントエンドが求められる場面（モバイル向けSPA、組込み系UI、パフォーマンス重視のプロダクト）で、学習コストを抑えて効果的に導入できる選択肢だからです。

## 詳細解説
- コンパイル時リアクティビティ：ViteプラグインがJSXを解析し、どのDOMノードがどの状態に依存するかを特定して「外科的な」更新コードを生成。ランタイムでの差分計算が不要。
- 仮想DOM不要：差分のdiffや再構築はなく、生成されたコードが直接該当要素を更新するためオーバーヘッドが小さい。
- Proxyベースのストア：状態は普通のクラスで定義し深いProxyでラップ。プロパティ変更や配列操作、ネストしたオブジェクトがそのまま反映される。
- 既存のJS文法そのまま：コンポーネントはクラスまたは関数、算出はgetter。シグナル／hooks／特殊APIを新たに学ぶ必要がない。
- パフォーマンスと軽量性：js-framework-benchmarkで上位（Gea ~1.03、Solid 1.12、Svelte 1.14、Vue 1.26、React 1.50、vanilla ~1.02 のスコア概念）。router込みで約13KB gzipped、ランタイム依存なし。
- 付帯機能：組み込みルーター、35+のアクセシブルUIコンポーネント、モバイル向けプリミティブ、HMR、VS Code拡張予定。イベントデリゲーションや配列の細粒度更新など実運用向けの最適化多数。

例（概念的なコード）:

```typescript
// store.ts
import { Store } from '@geajs/core'
class CounterStore extends Store {
  count = 0
  increment () { this.count++ }
  decrement () { this.count-- }
}
export default new CounterStore()
```

```tsx
// Counter.tsx
import { Component } from '@geajs/core'
import store from './store'
export default class Counter extends Component {
  template () {
    return (
      <div class="counter">
        <span>{store.count}</span>
        <button click={store.increment}>+</button>
        <button click={store.decrement}>-</button>
      </div>
    )
  }
}
```

```typescript
// app.tsx
import Counter from './Counter'
const app = new Counter()
app.render(document.getElementById('app'))
```

## 実践ポイント
- 今すぐ試す：npm create gea@latest my-app でスキャフォールド。Vite + TypeScript のテンプレートが手に入る。
- 設計ルール：ストアはクラス、算出は getter、コンポーネントは関数でもクラスでもOK（ビルド時に変換）。
- 適用候補：小〜中規模SPA、モバイル最適化が重要な画面、学習コストを抑えたいチーム。
- 注意点：エコシステムやプラグイン数は成熟フレームワークに劣るため、外部ライブラリ依存が多い大規模プロジェクトは検討が必要。

原著: JavaScript Is Enough (Gea) — https://geajs.com/
