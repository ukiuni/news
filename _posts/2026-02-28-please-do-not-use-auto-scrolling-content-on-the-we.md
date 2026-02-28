---
layout: post
title: "Please do not use auto-scrolling content on the web and in applications - ウェブとアプリで自動スクロールを使ってはいけない"
date: 2026-02-28T14:43:30.904Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://cerovac.com/a11y/2026/01/please-do-not-use-auto-scrolling-content-on-the-web-and-in-applications/"
source_title: "Bot Verification"
source_id: 47195582
excerpt: "勝手に動く自動スクロールが健康と操作を損なう理由と即実装できる回避策を解説"
---

# Please do not use auto-scrolling content on the web and in applications - ウェブとアプリで自動スクロールを使ってはいけない
勝手に画面が動くとイライラ、障害を招く——自動スクロールの問題点と今すぐできる対策

## 要約
自動スクロールや自動で動くコンテンツは視覚・運動・認知に負担をかけ、アクセシビリティ基準に抵触することがある。ユーザー操作がない限り自動スクロールを避け、代替手段と設定を提供すべきだ。

## この記事を読むべき理由
日本でも多くのサイトやアプリが勝手にスクロールやアニメーションを使っており、ユーザー離脱やクレーム、法令・ガイドライン（JIS/WAIC/WCAG）への違反リスクがあるため、実務での対応が必須だから。

## 詳細解説
- 問題点
  - 突然のスクロールはフォーカスを奪い、キーボード操作やスクリーンリーダー利用者を混乱させる。
  - 動きに敏感な人（めまい、発作リスク）には健康リスクを与える。
  - 自動でコンテンツが移動すると閲覧中の情報を見失う、入力中のフォームがずれる等の実用的な不具合を招く。
- 規格・観点
  - WCAGは動的コンテンツに対して「ユーザーが制御できること」「不要な動きを避けること」を求める。日本のガイドラインやJISも同様。
- 技術例と注意点
  - CSSアニメーションやscrollIntoView({ behavior: 'smooth' })はユーザーの意思なしに発火しないように注意する。
  - 自動更新コンテンツ（チャット、ニュースティッカー等）はユーザーの現在位置を尊重し、新着を通知してユーザーが選んでスクロールできる仕組みにする。
  - 「Bot Verification…」のような自動処理や検証ページも、予期せぬ自動遷移やスクロールでユーザー体験を損なわないよう設計する。

## 実践ポイント
- prefers-reduced-motion を尊重する（OS設定で「動きを減らす」を検出）。
- 自動スクロールは「ユーザー操作（クリック／キー入力）」の後にのみ実行する。
- 長時間／繰り返し自動スクロールは避け、停止・一時停止・再開のUIを必ず提供する。
- フォーカスを移動させる場合は明示的にユーザーに通知し、スクリーンリーダーでの読み上げを配慮する。
- キーボードのみ、スクリーンリーダー、モバイル操作で実際にテストする。
- 実装例（reduce設定に対する簡易チェック）:

```javascript
// javascript
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function safeScrollIntoView(el, userInitiated) {
  if (prefersReducedMotion || !userInitiated) return;
  el.scrollIntoView({ behavior: 'smooth', block: 'center' });
}
```

以上を守れば、自動スクロールによる誤操作・健康リスク・アクセシビリティ問題を大幅に減らせます。
