---
layout: post
title: "The Incredible Overcomplexity of the Shadcn Radio Button - Shadcnのラジオボタンがとんでもなく過剰に複雑な件"
date: 2026-01-19T21:02:10.868Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://paulmakeswebsites.com/writing/shadcn-radio-button/"
source_title: "The Incredible Overcomplexity of the Shadcn Radio Button"
source_id: 1392677553
excerpt: "Shadcnのラジオボタンが不要な依存と複雑性を呼び、CSSで簡潔に代替できる理由とは？"
---

# The Incredible Overcomplexity of the Shadcn Radio Button - Shadcnのラジオボタンがとんでもなく過剰に複雑な件
たった一つのラジオボタンが3つのライブラリを召喚する話 — 「便利」が招く余計なコスト

## 要約
Shadcn（＋Radix）で提供されるラジオボタンは見た目やアクセシビリティのためにネイティブの<input type="radio">を使わず、ボタン＋ARIA＋多数のスタイル／依存を使う。だが、近年のCSSだけでもシンプルに美しく実装でき、不要なJSや複雑さを招くことがある。

## この記事を読むべき理由
日本のプロジェクトでもコンポーネント流用は当たり前。だが「楽に見た目を整える」選択が、パフォーマンス・保守・アクセシビリティの負債につながることがある。小さなUIでも依存やバンドルサイズを意識する価値は大きい。

## 詳細解説
- 何が起きているか：ShadcnのRadioコンポーネントはRadixのプリミティブを土台にし、さらにTailwindクラスや外部アイコンを組み合わせている。結果として数十行のReactコード、複数のインポート、場合によっては隠し<input>やARIAロールでネイティブ要素の代替をしている。
- なぜそうするか：歴史的にブラウザ間でラジオの見た目を揃えるのは難しく、カスタム実装でコントロールしやすくしている。Radixはアクセシビリティの抽象を提供し、Shadcnはスタイルを乗せる役割。
- 問題点：JSの依存が増えると初期表示や操作の反応がJSロードに依存しやすく、バンドル増加、デバッグコスト、理解すべきレイヤー増加を招く。さらに「First Rule of ARIA」に従えば、可能な限りネイティブ要素を使うのが望ましい。
- 代替（シンプルな実装例）：ネイティブ<input type="radio">にCSSでスタイルを当てるだけで十分なケースが多い。

HTML（最小例）:
```html
<input type="radio" name="beverage" value="coffee" />
```

CSS（スタイル例）:
```css
input[type="radio"] {
  appearance: none;
  margin: 0;
  width: 1rem;
  height: 1rem;
  border: 1px solid #000;
  border-radius: 50%;
  display: inline-grid;
  place-content: center;
}
input[type="radio"]::before {
  content: "";
  width: 0.6rem;
  height: 0.6rem;
  border-radius: 50%;
  background: transparent;
}
input[type="radio"]:checked::before {
  background: #000;
}
```

## 日本市場との関連性
- モバイル回線・低速環境がまだ意識される日本では、不要なJS増加はUX悪化に直結する。
- 企業サイトや公共サイトではアクセシビリティ要件（WCAG準拠やJIS基準）への対応が重要で、ネイティブ要素の方が堅牢なケースが多い。
- 社内デザイナーとフロント実装者の分業が多い環境ほど、ライブラリのブラックボックス化が保守コストを上げる。

## 実践ポイント
- まずネイティブ要素で足りないか検討する（見た目＝CSSで解決できることが多い）。
- コンポーネント導入前にバンドルサイズと依存関係を確認する（LighthouseやBundle Analyzerを活用）。
- Radix/Shadcnを使うなら、実際にブラウザの要素（DevTools）で何がレンダリングされるか確認する：隠し<input>はあるか、ARIAは正しく付与されているか。
- アクセシビリティ要件が厳しい場合はライブラリの実装を分解して理解しておく。
- まずは簡単なCSS実装でプロトタイプを作り、必要ならライブラリへ移行する「段階的導入」を検討する。

短い結論：便利なコンポーネントは強力だが、シンプルなHTML＋CSSで十分な場面も多い。まずは「本当に複雑化する価値があるか」を一呼吸おいて考えること。
