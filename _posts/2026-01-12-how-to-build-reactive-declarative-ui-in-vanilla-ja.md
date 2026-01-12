---
layout: post
title: "How to Build Reactive Declarative UI in Vanilla JavaScript - フレームワーク無しで宣言的リアクティブUIを作る方法"
date: 2026-01-12T13:00:41.513Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://jsdev.space/howto/reactive-vanilla-js/"
source_title: "Howto Build Reactive Declarative UI in Vanilla JavaScript"
source_id: 46587033
excerpt: "Vanilla JSだけで深い変更検知と自動ポーリング式モーダルを宣言的に実装する手法を解説"
image: "https://jsdev.space/og/reactive-vanilla-js.png"
---

# How to Build Reactive Declarative UI in Vanilla JavaScript - フレームワーク無しで宣言的リアクティブUIを作る方法
フレームワーク不要でここまでできる？Vanilla JSで作る「宣言的モーダル×自動ポーリング」の実践ガイド

## 要約
純粋なWeb API（DOM、Proxy、fetch、Promise）だけで「宣言的に記述できる」「深い変更を検知する」リアクティブUIを実現する実験的手法を紹介。モーダルがAPIを定期ポーリングして、条件を満たしたら自動で閉じる一連の流れを、責務を分離して書くやり方を解説する。

## この記事を読むべき理由
- 日本では軽量化や保守性の観点から「フレームワークを必ず使う」文化が見直されつつあります。既存フレームワークに頼らず、ネイティブ機能で宣言的・再利用可能なUIを作る設計感覚は現場で即役立ちます。
- ランディングや管理画面の一部など、バンドルサイズを抑えつつ可読性を担保したい場面で有効です。

## 詳細解説
この記事のアプローチは主に4つのレイヤーに分かれます。

1. DOMユーティリティ（DomToolkit）
   - 役割：要素生成・属性・スタイル設定などのボイラープレートを一箇所に集約する。
   - メリット：ビジネスロジック側は「何をしたいか（宣言）」に集中でき、DOM作成ルールの変更も一箇所で済む。

2. 深いリアクティブ状態（DeepStateProxy）
   - 技術：ネイティブの Proxy を使ってオブジェクトの深いプロパティ変更を監視する。
   - 仕組み：wrap関数で再帰的に子ノードをProxy化し、set/deleteハンドラで変更を通知するため、明示的なセッターが不要になる。
   - 利点：状態はプレーンなオブジェクトのまま、変更検知と副作用（ログ、UI更新）を分離できる。

3. ポーリングロジック（runPolling）
   - 技術：非同期タスクをループし、所定の条件で停止する抽象関数。
   - ポイント：DOMや状態から独立しているためテストが容易で、再利用可能なユーティリティになる。

4. モーダルオーケストレータ（ModalOrchestrator）
   - 役割：上の3つを組み合わせ、ユーザーが宣言的に「どう振る舞うか」だけを書けるAPIを提供する。
   - 典型的な設定例：endpoint、requestPayload、shouldContinue（ポーリング継続判定）、intervalMs、buildContent、onResolved/onRejected。

全体の設計思想は「責務の分離」と「振る舞いの宣言化」。消費側は「いつ閉じるか」「成功/失敗時に何をするか」を宣言し、フレームワーク固有の概念（コンポーネントライフサイクルやhooks）は不要です。

簡易コード例（骨格）

```javascript
// javascript
class DeepStateProxy {
  constructor(target, { onSet, onDelete } = {}) { /* wrapして返す */ }
  wrap(node, path = []) { /* Proxy化の実装 */ }
}

async function runPolling({ task, shouldStop, intervalMs }) {
  while (true) {
    const result = await task();
    if (shouldStop(result)) return result;
    await new Promise(res => setTimeout(res, intervalMs));
  }
}
```

## 実践ポイント
- まずは小さなDomToolkitを作る：createElementの共通処理（classes, attrs, styles, innerHTML）を抽象化すると見通しが良くなる。
- DeepStateProxyはデバッグフックを付けて段階的に導入する：最初は読み取り専用ログ→次にUIバインドへ。
- ポーリングはrunPollingのように分離する：副作用を切り離せばユニットテストが容易になる。
- オーケストレータに渡す設定は「何をしたいか（shouldContinue, onResolved）」を中心に簡潔に保つ。
- 日本の現場での活用例：バンドルサイズ制限のあるプロジェクト、レガシーに新機能を小さく差し込む場面、セキュリティやコンプライアンスで外部ライブラリを制限されるケース。

短くまとめると、フレームワーク無しでも「宣言的でテストしやすいUI」を作ることは可能。重要なのは抽象レイヤー（DOM工具箱、状態トラッカー、非同期ユーティリティ）を明確に切ること。まずは上の小さな部品から試して、必要に応じて抽象を洗練させていくとよい。
