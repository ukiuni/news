---
  layout: post
  title: "Effortless animations with CSS view transitions - CSSのView Transitionsで手軽に作る滑らかなアニメーション"
  date: 2026-01-07T16:22:23.769Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://giacomocavalieri.me/writing/effortless-animations-with-css-view-transitions"
  source_title: "Effortless animations with CSS view transitions"
  source_id: 695123757
  excerpt: "数行のCSSで驚くほど滑らかな、JavaScript不要のページ遷移を実現"
---

# Effortless animations with CSS view transitions - CSSのView Transitionsで手軽に作る滑らかなアニメーション
たった数行で「動く」サイトに見違える。JavaScript不要で実現するモダンなページ遷移の作り方

## 要約
CSSのView Transitionsを使えば、数行のCSSだけでページ間の滑らかなアニメーション（クロスフェードや要素移動）を追加できる。小さな静的サイトでも見た目が一気に洗練される。

## この記事を読むべき理由
日本のプロダクトや個人サイトでも、派手なフロントエンド工事をせずにUXを向上させたいケースが増えています。View Transitionsは「JSを書かずに自然なページ遷移」を実現できるため、開発コストを抑えつつ見栄えを良くしたいエンジニアに特に有益です。

## 詳細解説
- 有効化: ページ全体でView Transitionsを有効にするには、CSSに次のルールを追加します。
```css
/* css */
@view-transition {
  navigation: auto;
}
```
これでページ間遷移時にブラウザが既定のトランジション（クロスフェード等）を適用するようになります。

- グループ全体のカスタマイズ: 全ての遷移対象要素をまとめて制御するには、::view-transition-group()疑似要素を使います。以下はアニメーション時間やイージングの調整例です。
```css
/* css */
::view-transition-group(*) {
  animation-duration: 0.25s;
  animation-timing-function: cubic-bezier(0.78, -0.02, 0.33, 1.15);
}
```
イージングは好みに合わせて変えられます。過度なアニメーションは注意。

- 個別要素の移動アニメーション: ページAの要素とページBの対応要素を「同じ名前」でマークすると、ブラウザが位置やサイズを補間して移動アニメーションを作ります。方法は簡単に view-transition-name を使うだけです。
```html
<!-- html -->
<!-- index.html -->
<a href="writing.html" style="view-transition-name: writing-animation">writing</a>

<!-- writing.html -->
<ol class="breadcrumb">
  <li>...</li>
  <li><h3 style="view-transition-name: writing-animation">writing</h3></li>
</ol>
```
同じ名前を付けた要素同士が「対」になり、自然に移動するように見えます。

- 実装の考え方: 基本はプログレッシブエンハンスメント。View Transitionsは便利ですがブラウザ対応が完全ではないため、JSで不要なポリフィルを書かずとも、未対応ブラウザでは普通の遷移になるように設計します。

- 対応状況: 主にChromium系ブラウザで実装が進んでいます。Firefoxや古いブラウザでは未対応・挙動差があるため、確認が必要です。

## 実践ポイント
1. まずは最小限で試す  
   VS CodeでLive Server拡張を使い、上記の@view-transitionとview-transition-nameを数行だけ追加して動作確認してみる。ブラウザのデベロッパーツールで遷移の様子をチェック。

2. 要素の命名ルールを決める  
   view-transition-name は文字列なので、プロジェクト内で命名規則（例: blockname-animation）を決めれば管理しやすくなる。

3. アニメーションの強さは控えめに  
   durationやtiming-functionで微調整し、ページの用途（ドキュメント、商品ページ、ダッシュボード）に応じて控えめに設定する。

4. フォールバック設計を忘れずに  
   未対応ブラウザでは通常の遷移になるため、UI破綻が起きないことを確認する。アクセシビリティやパフォーマンス上の問題がないか確認すること。

5. 小規模なサイト改善に最適  
   コーポレートサイトや技術ブログ、ポートフォリオなど、JSを増やしたくない場面で特に効果的。ページが軽く、洗練された印象を与えられます。

短い手間で大きな効果を出せるテクニックなので、まずは1箇所だけ導入して挙動を体験してみることをおすすめします。
