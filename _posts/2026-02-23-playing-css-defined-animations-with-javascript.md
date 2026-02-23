---
layout: post
title: "Playing CSS-defined animations with JavaScript - CSSで定義したアニメーションをJavaScriptで再生する"
date: 2026-02-23T02:15:44.728Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://benhatsor.medium.com/99573ef4738b"
source_title: "Playing CSS-defined animations with JavaScript"
source_id: 400176540
excerpt: "CSSの@keyframesを再利用しJSで自在に再生・逆再生できるKeyframeKit"
---

# Playing CSS-defined animations with JavaScript - CSSで定義したアニメーションをJavaScriptで再生する
CSSで書いたアニメーションをそのままJSで「再生・一時停止・巻き戻し」できる！KeyframeKitでマイクロインタラクションが格段に扱いやすくなる

## 要約
CSSの@keyframesで作ったアニメーションを、Web Animations API側に取り込み、JavaScriptで直感的に再生・制御できるライブラリ「KeyframeKit」を紹介する記事の解説。

## この記事を読むべき理由
ホバー中にアニメが途中でパッと戻ってしまうなど、CSSアニメの操作性の限界に悩むフロントエンド開発者は多いはず。KeyframeKitは既存のCSS定義を再利用しつつWeb Animations APIの強力な再生制御を使えるようにするため、手早くUXを改善できます。

## 詳細解説
- 問題点：CSSアニメーションは宣言的で読みやすい反面、途中停止・逆再生・進捗取得といった再生制御が苦手。ホバーを外した瞬間に状態が「スナップ」する挙動が典型的。
- 解決手段：Web Animations APIはハードウェアアクセラレーションを持ちつつ再生制御が得意だが、標準的にCSSの@keyframesを直接読み込む手段がない。KeyframeKitはスタイルシートから@keyframesを解析して、Web Animations APIで使えるKeyframeEffect／Animationに変換する。
- 仕組み（概略）：ドキュメントのスタイルシートを取得→指定のアニメ名を検索してキーフレームを抽出→toKeyframeEffectでDuration/Easing等を指定→対象要素にアタッチしてAnimationインスタンスにする、という流れ。
- 付加価値：型定義（TypeScript）やユーティリティ関数を備え、既存のCSS資産を最小限の手間で再利用可能にしている。

## 実践ポイント
- 使い方例（概念的な流れ）:
```javascript
// javascript
import KeyframeKit from 'keyframekit';

const sheets = await KeyframeKit.getDocumentStyleSheetsOnLoad();
const kf = KeyframeKit.getStyleSheetKeyframes({ of: 'rotate-small', in: sheets });
const effect = kf.toKeyframeEffect({ duration: 700, easing: 'ease' });
const anim = effect.toAnimation({ target: document.querySelector('.el') });
anim.play();
```
- できること：play/pause、playbackRateの反転（逆再生）、overallProgressの取得、finishedで完了待ちなど。
- ブラウザ対応：Web Animations APIは主要ブラウザでサポートが進んでいるが、古い環境や一部のSafariでは差異があるため必要ならpolyfillを検討すること。
- 実務での活用例：ボタンやリンクのマイクロインタラクション、SPのスクロール連動アニメ、A/Bでのアニメ評価などに即効性あり。
- 参考（公式ドキュメント／GitHub）：KeyframeKit docs https://keyframekit.berryscript.com/ 、GitHub https://github.com/benhatsor/KeyframeKit/

短時間でUXを改善したい人、既存のCSS資産を捨てずに高度な再生制御を使いたい人は一度触ってみる価値があります。
