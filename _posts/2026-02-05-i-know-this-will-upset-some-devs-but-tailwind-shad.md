---
layout: post
title: "I Know This Will Upset Some Devs, but Tailwind + Shadcn/ui + Shadow DOM = Pain - Tailwind + shadcn/ui + Shadow DOM は地獄だ（開発者には不評かも）"
date: 2026-02-05T17:05:01.156Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/ujja/i-know-this-will-upset-some-devs-but-tailwind-shadcnui-shadow-dom-pain-44l7"
source_title: "I Know This Will Upset Some Devs, but Tailwind + Shadcn/ui + Shadow DOM = Pain - DEV Community"
source_id: 3218481
excerpt: "Tailwind×shadcn/ui×Shadow DOM の相性問題と実務対策"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fphc0s0tl06vkybch007s.png"
---

# I Know This Will Upset Some Devs, but Tailwind + Shadcn/ui + Shadow DOM = Pain - Tailwind + shadcn/ui + Shadow DOM は地獄だ（開発者には不評かも）
Tailwind と shadcn/ui を Shadow DOM と混ぜると意外と悲劇が起きる — 実務で使う前に知っておくべき「現実」と対処法

## 要約
Tailwind（グローバルユーティリティ）＋shadcn/ui（Radix + CVA）＋Shadow DOM（カプセル化）は相性が悪く、スタイル抜け・バンドル肥大・ポータル崩壊・テーマ変数漏れなどの実問題が頻発する。

## この記事を読むべき理由
Web コンポーネントやマイクロフロントエンド、社内 UI ライブラリを作る日本のプロジェクトでは「見た目の一貫性」と「再利用性」が重要。導入前にこの組み合わせの落とし穴を理解しておかないと、パフォーマンス・保守コストで苦労します。

## 詳細解説
- 根本的な対立点：Tailwind はグローバルなユーティリティ CSS を前提にしているのに対し、Shadow DOM はスタイルの境界を作る（外部スタイルが内部に届かない）。結果として Tailwind のクラスが Shadow 内で効かない。
- ポータルの問題：shadcn/ui（Radix ベース）は Dialog/Tooltip/Popover 等で React ポータルを使う。ポータルは document.body に吐き出されるため Shadow DOM の外に出てしまい、Shadow 内にあるコンポーネントのスタイルや CSS 変数が適用されない。
- 動的クラス（CVA）の問題：class-variance-authority 等で runtime に組み合わさるクラスは Tailwind JIT に検出されず、ビルドに含まれない場合がある。safelist で穴埋めすると CSS が巨大化する。
- テーマ変数の継承欠落：shadcn/ui が CSS カスタムプロパティでテーマを定義しても、Shadow DOM 境界で変数が継承されないため再定義が必要になり、単一ソースを失う。

例：Shadow 内で Tailwind クラスが効かない（簡略化）
```javascript
export const MyCard = () => (
  <div className="p-4 bg-white rounded-lg shadow-md">
    <h1 className="text-2xl font-bold">Hello</h1>
  </div>
);
const MyCardWC = r2wc(MyCard, { shadow: 'open' });
customElements.define('my-card', MyCardWC);
// 結果：Tailwind のスタイルが Shadow 内に届かず、見た目が崩れる
```

典型的な「対応策」例と問題点
- 各コンポーネントに Tailwind CSS を import する（動くが CSS を複製してバンドル肥大）
```javascript
// styles.css に @tailwind base; @tailwind components; @tailwind utilities;
import './styles.css'; // コンポーネントごとに読み込む → バンドル×N
```
- Shadow を無効化してポータルを動かす（カプセル化を放棄）
```javascript
const MyDialogWC = r2wc(MyDialog, { shadow: null }); // ポータルは動くがグローバル汚染のリスク
```
- Tailwind の safelist で CVA のクラスを列挙（手間と肥大化）
```javascript
// tailwind.config.js
module.exports = {
  content: ['./src/**/*.{ts,tsx}', './node_modules/@your-ui-lib/**/*.{ts,tsx}'],
  safelist: ['bg-primary', 'text-primary-foreground', 'h-9', 'h-10', /* ... */],
};
```
- CSS 変数を Shadow 内で再定義（重複と同期問題）

## 実践ポイント
- 必要性を見極める：Shadow DOM が本当に必要か（スタイル衝突回避や仕様的隔離が必須でなければ使わない判断も正解）。
- ポータル系コンポーネントは Shadow 外で扱う：Dialog/Popover 等は Shadow を無効化するか、ポータルの代替実装を検討する。
- 共有スタイルは constructable stylesheet（adoptedStyleSheets）で一元化を検討※：複数の shadowRoot に同じ CSSStyleSheet を再利用でき、CSS の重複を抑えられる（ブラウザ対応と制約を要確認）。
- Tailwind の出力をビルド時に CSSStyleSheet 化して配布する（技術的には可能だが設定が複雑）：各 web component はその stylesheet を参照する形にする。
- CVA のクラスはビルド時に確定させる、または safelist を自動生成するスクリプトで管理する（手動管理は破綻しやすい）。
- テーマは Shadow 内で再定義するか、コンポーネント API としてテーマ値を渡す（カスタムプロパティだけに頼らない）。
- 妥協案：Shadow を使わず CSS モジュール / BEM / PostCSS スコープで名前衝突を防ぐ運用は実用的で、導入コストが低い場合が多い。

短いチェックリスト
- Shadow DOM を選ぶ理由を書面化したか？  
- ポータルを使うコンポーネントは分離しているか？  
- Tailwind の CSS 重複対策（adoptedStyleSheets 等）は検討済みか？  
- CVA のクラス生成をビルド側で網羅できるか？  
- テーマの単一ソースはどう担保するか？

以上を踏まえ、理想論（完全なカプセル化＋ユーティリティCSS）に飛びつく前に、実運用でのトレードオフを整理してから設計を決めるのが安全です。
