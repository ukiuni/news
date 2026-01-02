---
layout: post
title: "Doom in Django: testing the limits of LiveView at 600.000 divs/segundo - DjangoでDOOMを動かす：LiveViewの限界を秒間60万divで検証"
date: 2025-12-31T11:36:57.654Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://en.andros.dev/blog/7b1b607b/doom-in-django-testing-the-limits-of-liveview-at-600000-divssegundo/"
source_title: "Doom in Django: testing the limits of LiveView at 600.000 divs/segundo"
source_id: 46409359
excerpt: "秒間60万divでDOOMを描画、Django LiveViewの限界検証"
---

# Doom in Django: testing the limits of LiveView at 600.000 divs/segundo - DjangoでDOOMを動かす：LiveViewの限界を秒間60万divで検証
秒間60万div！Django LiveViewをDOOMでぶん回して限界を確かめてみた

## 要約
ViZDoomで生成したフレームをDjangoが1ピクセル＝1つの<div>に変換して配信し、100×100ピクセル×60FPSで合計$100\times100\times60=600{,}000$div/秒をDjango LiveViewで描画する実験。結果としてLiveViewはこの極端な負荷を“耐えた”という検証的デモ。

## この記事を読むべき理由
WebリアルタイムUIの限界とトレードオフが一目で分かるため。日本のスタートアップやプロダクト開発で「少ない実装工数でリアルタイム性を出す」選択肢を検討する際、Djangoエコシステム（Channels / LiveView）がどこまで使えるかの有益な指標になる。

## 詳細解説
- 全体の流れ：ViZDoomが1フレームを生成 → Djangoがテンプレートでフレームをピクセルごとの<div>（100×100＝10,000個）に変換 → Django LiveViewが接続中のクライアントへブロードキャスト → CSSで並べてゲーム画面を再現。
- レート：60FPSで動かすため、1秒あたり10,000div × 60 = 600,000divを生成・送信・描画。これはDOM生成・差分配信・ブラウザ描画の全工程に高負荷をかける極端なケース。
- 技術要素：Django LiveView（リアルタイム差分更新）、Django Channels（WebSocketブロードキャスト）、サーバ側テンプレートでのHTML生成という「サーバ主導のUI更新」アプローチを最大限試した実験。
- 示唆：結果は「実行可能」だが、実用面では非効率。ピクセルごとのDOMはネットワーク帯域・レンダリングともコストが高く、通常はcanvas／WebGLやバイナリ差分・画像タイル配信の方が現実的。

## 実践ポイント
- 再現したいなら：ViZDoom環境を用意→Django + Channels + LiveViewセットアップ→フレームをピクセル単位のHTMLに変換→ブロードキャストで配信、を順に試す。
- 代替案（実用的）：大量ピクセル更新が必要ならcanvas/WebGLに描画する。差分送信はバイナリ（画像差分／圧縮）やタイル化が有効。
- 最適化Tips：
  - テンプレートでのフルレンダリングを避け、差分生成を最小化する
  - WebSocketペイロードを圧縮（gzip／brotli）する
  - ブラウザ側はDOM操作を減らし、可能なら一度のinnerHTML差し替えやcanvasを使う
  - 負荷試験は実際の接続数・帯域で再現してボトルネックを測定する
- アイデア用途：リアルタイムダッシュボードやコラボレーション機能のプロトタイプ検証に向く。極端なデモはフレームワークの耐久力を可視化する良い指標になる。

