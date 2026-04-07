---
layout: post
title: "Someone good at CSS help, my website design is dying - CSSが原因でカードの角が“にじむ”問題"
date: 2026-04-07T01:23:30.182Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://ahti.space/~nortti/writeups/my-website-design-is-dying.html"
source_title: "Someone good at CSS help, my website design is dying"
source_id: 1410582237
excerpt: "カードの角がダークモードで白くにじむ原因とCSSでの確実な直し方を図示付きで解説"
---

# Someone good at CSS help, my website design is dying - CSSが原因でカードの角が“にじむ”問題
魅力的なカードUIの角がガタつく？ダークモードやアンチエイリアスで生じる“白いにじみ”を正しく直す方法

## 要約
親要素と子要素の角丸・境界線を別々にレンダリングすると、アンチエイリアスで半透明ピクセルが重なり“白っぽく”見えることがある。overflow / compositing 周りの対処で解決できる。

## この記事を読むべき理由
カード型レイアウトは日本のサービスでも多用されるUI要素。ダークモード普及で色の微妙なにじみが目立ちやすく、正しいCSS知識があれば見栄えを安定させられるため必読。

## 詳細解説
問題の本質はレンダリング順とアンチエイリアス：
- 親（article）に角丸＋境界線、子（header）にも角丸や背景があると、ブラウザはそれぞれを個別にアンチエイリアスして重ね合わせる。
- エッジのピクセルは半透明になり、下の背景（多くは白）と合成されて「白い縁」や不自然な中間色が生じる。

対策は「子要素を親の内部でまとめて合成し、切り取る（クリップする）」こと。代表的な手段：
1. 親に角丸 + overflowでクリップ（子に角丸不要）
2. 親に新しい合成コンテキストを作る（isolation）＋overflow
3. 境界線をbox-shadowで描画してアンチエイリアスの重なりを避ける
4. 色やアルファ値を不透明にして合成差を減らす

実際の例を示します。

HTML:
```html
<article>
  <header><h2>title</h2></header>
  <div>content</div>
</article>
```

基本的な修正（親でクリップ）:
```css
article {
  border-radius: 8px;
  overflow: hidden; /* 子要素を親の角で切る */
  border: 1px solid #b19edc;
  background: #d2bfff;
}
header {
  border-radius: 0; /* 親に任せる */
  background: #d2bfff;
}
```

より確実な合成制御（推奨）:
```css
article {
  border-radius: 8px;
  overflow: hidden;
  isolation: isolate; /* 親の内部で先に合成させる */
  box-shadow: 0 0 0 1px #b19edc; /* 必要なら border の代替 */
  background: #d2bfff;
}
```

注意点：
- border と背景色に半透明を使うと合成差が出やすい。可能なら不透明色を使う。
- outline は角丸に追随しないので避ける（代わりに box-shadow が便利）。
- overflow:auto はスクロール要因があると使う目的が異なるので、角のクリップには overflow:hidden が簡潔。

## 実践ポイント
- 親に border-radius + overflow:hidden を付けて子の角丸は消す。
- それでもにじむなら isolation:isolate を親に追加して合成順を安定化。
- 境界線は box-shadow で代用するとアンチエイリアス由来の重なりを回避できる。
- 色は可能な限り不透明にする。ダークモードで背景が変わる場合は特に確認を。

これらを試せば、カードの角が“白くにじむ”問題は高確率で解消します。
