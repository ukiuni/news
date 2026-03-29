---
layout: post
title: "heerich.js - heerich.js — SVGにレンダリングする3Dボクセルの小さなエンジン"
date: 2026-03-29T06:46:45.875Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://meodai.github.io/heerich"
source_title: "heerich.js — Interactive Guide"
source_id: 952081817
excerpt: "heerich.jsでボクセルを彫刻的に組み合わせ、解像度無限のSVG作品を自在に生成する方法"
image: "https://meodai.github.io/heerich/social.png"
---

# heerich.js - heerich.js — SVGにレンダリングする3Dボクセルの小さなエンジン
SVGで彫る3Dボクセル — 軽量エンジン heerich.js の美学と作り方

## 要約
heerich.jsは、3Dボクセルをプログラムで生成して高品質なSVGとして出力する極小のJavaScriptエンジン。ベクターとしてDOMに置かれるため、CSSで自在に操作でき、無限に拡大しても劣化しない「彫刻的」表現が可能になる。

## この記事を読むべき理由
SVGを活用したスケーラブルでスタイラブルな3D表現は、Webサイトの軽量化、印刷・高DPI対応、モバイルWebViewでの互換性、そしてデザイン／プロトタイプ制作で即戦力になります。Webフロント寄りの日本の開発者・デザイナーにとって、WebGLに頼らない新しい表現手段です。

## 詳細解説
- 基本構造：Heerichインスタンスは3Dグリッド（ボクセル）を保持し、投影して2DのSVGを生成する。デフォルト値で動作し、engine.toSVG()で自動センタリングされたSVG文字列を得られる。  
- プリミティブ：box/sphere/lineなどを追加でき、各ボクセルは1×1×1。  
- ブール操作：modeに union / subtract / intersect / exclude を指定してボクセルの合成や彫り込みが可能（例：箱から球を削る）。  
- 回転と配置：90°単位のrotateオプションでパーツを回転。位置は最小コーナーを基準とするので、揃える場合は差分で調整。  
- 面ごとのスタイル：top/front/left/right/bottom/back と default を指定でき、SVGのpresentation属性（opacity, strokeDasharray, CSS var() 等）を直に渡せる。関数スタイルで座標に応じた色付けも可能。  
- 投影モード：oblique（平行投影）とperspective（1点透視）をサポート。視点や距離を切り替えて表現を変えられる。  
- コンテンツと透明：ボクセル内に任意のSVGを埋め込む「content」や、opaque:falseで隣接描画を透過扱いにすることで、インフォグラフィック的表現もできる。  
- 検査とシリアライズ：getNeighbors(), hasVoxel(), forEach() 等でメッシュ情報にアクセス可能。toJSON()/fromJSON()で保存・復元ができる。  
- アニメーション：エンジンはタイマーを持たないため、requestAnimationFrameで値をTweenして毎フレーム再構築する方式を取る。内部は差分再計算のため比較的効率的。

美術的背景としてErwin Heerichの幾何学的造形にインスパイアされており、「積み重ね」と「引き算」による彫刻性をコードで再現することを狙っている。

## 実践ポイント
- 最短の始め方（モジュール読み込み例）:
```javascript
import { Heerich } from './src/heerich.js'
const engine = new Heerich({
  tile: [30, 30],
  camera: { type: 'oblique', angle: 315, distance: 25 },
  style: { fill: '#ddd', stroke: '#333', strokeWidth: 0.5 }
})
engine.addBox({ position: [0,0,0], size: [6,4,3] })
engine.addSphere({ center: [3,3,3], radius: 3, mode: 'subtract' })
document.body.innerHTML = engine.toSVG({ padding: 30 })
```
- デザイン実務での応用：
  - レスポンシブなアイコンや装飾要素（SVGなので解像度フリー）
  - 商品カスタマイザやコンフィギュレータ（DOM操作で色やパーツを動的変更）
  - 印刷物やポスター用のベクターワーク（拡大しても滑らか）
- テクニカルなコツ：
  - 内部のグリッド線を消すには fill と stroke を同色にする（滑らかな塊表現）。  
  - CSS変数をスタイルに渡せばランタイムでテーマ切替が容易。  
  - 複雑なパターンはスタイルに関数を渡して座標依存で自動生成すると手間が減る。  
  - アニメは値の整数境界を利用して「削る」アニメーションを作ると美しい（removeBoxをフレームごとに呼ぶ）。

heerich.jsは「コードで彫刻する」感覚を手軽にWebに持ち込めるツールで、日本のウェブデザインやプロダクト開発にも手触りの良い表現手段を提供する。興味があるならデモを触って、viewBoxやCSS変数を組み合わせたライブテーマ切替を試してみてほしい。
