---
layout: post
title: "Snow Simulation Toy - 雪のシミュレーション・トイ"
date: 2026-01-27T13:08:30.883Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://potch.me/2026/snow-simulation-toy.html"
source_title: "snow simulation toy | potch dot me"
source_id: 46691548
excerpt: "ブラウザで簡単カスタム雪景色を作れる、物理と描画の学習向けJSデモ"
image: "https://potch.me/img/giraffe-400.png"
---

# Snow Simulation Toy - 雪のシミュレーション・トイ
冬の午後、ブラウザで眺めて癒される「雪」を自作してみませんか？

## 要約
シンプルなブラウザ向け雪シミュレーション。QBasic時代の落雪表現へのノスタルジーから生まれ、JavaScriptと手続き生成で柔軟に遊べる小さなデモです。

## この記事を読むべき理由
冬の季節感を簡単に再現でき、初心者が物理表現・描画・パフォーマンス最適化を学ぶのに最適。日本の季節イベントやウェブ装飾、学習教材にすぐ使えます。

## 詳細解説
- 発想と背景：作者はQBasicの「落雪」から着想を得て、休日にブラウザで作り直した小品。タグは #toys #js #procgen（プロシージャル生成）。
- コア概念：多数の粒子（雪片）を生成してそれぞれに位置(x,y)、速度(vx,vy)、サイズ、不透明度などを持たせる。毎フレームで重力・風・乱流（ノイズ）を適用して位置を更新し、描画する。
- 表現の工夫：サイズや回転、透明度をランダム化して多様性を出す。遠景は小さく薄く、手前は大きく濃くして奥行きを表現する（深度レイヤ）。
- パフォーマンス：CanvasとrequestAnimationFrameを使うのが定番。多数粒子はプール（オブジェクト再利用）でガベージを減らす。複雑な描画はオフスクリーンやスプライトキャッシュで最適化。
- インタラクション：マウスやタッチで風を発生させたり、クリックで降雪量を変えるなど遊びを追加可能。
- 実装スタック：HTML5 Canvas + JavaScript（軽量ライブラリ不要）が手軽。Webサイトのアクセントやスクリーンセーバ代わりに使えます。

## 実践ポイント
- 必要な要素：Canvas初期化、Particleクラス、生成ループ、update/drawループ、プール管理。
- 微調整のコツ：重力はゆるめに、風は時間変化（シンプルな正弦＋ノイズ）で自然に。降雪量とサイズ分布を調整して雰囲気を作る。
- 日本向け応用例：冬季キャンペーンページ、電子年賀状、教育用ワークショップの題材。
- 最低限のサンプル（更新＋描画ループ）：

```javascript
const canvas = document.querySelector('canvas');
const ctx = canvas.getContext('2d');
let particles = [];

class Snow {
  constructor() { this.reset(); }
  reset() {
    this.x = Math.random()*canvas.width;
    this.y = -10;
    this.vx = (Math.random()-0.5)*0.5;
    this.vy = 0.5 + Math.random()*1.5;
    this.size = 1 + Math.random()*3;
    this.alpha = 0.6 + Math.random()*0.4;
  }
  update() {
    this.vy += 0.002; // gravity
    this.x += this.vx;
    this.y += this.vy;
    if (this.y > canvas.height+10) this.reset();
  }
  draw() {
    ctx.fillStyle = `rgba(255,255,255,${this.alpha})`;
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI*2);
    ctx.fill();
  }
}

for (let i=0;i<200;i++) particles.push(new Snow());

function loop(){
  ctx.clearRect(0,0,canvas.width,canvas.height);
  for (let p of particles){ p.update(); p.draw(); }
  requestAnimationFrame(loop);
}
loop();
```

気軽にパラメータをいじって、自分だけの雪景色を作ってみてください。
