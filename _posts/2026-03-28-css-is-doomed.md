---
layout: post
title: "CSS is DOOMed - CSSは滅びるのか"
date: 2026-03-28T21:24:01.591Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://nielsleenheer.com/articles/2026/css-is-doomed-rendering-doom-in-3d-with-css/"
source_title: "CSS is DOOMed - Rendering DOOM in 3D with CSS | Hello my name is Niels Leenheer"
source_id: 47557960
excerpt: "CSSだけでDOOMを再現する実験で最新CSS機能の限界と可能性を実演"
image: "https://nielsleenheer.com/wp-content/uploads/2026/03/css-doomed.png"
---

# CSS is DOOMed - CSSは滅びるのか
CSSだけでDOOMを動かして見せた男が語る、モダンCSSの“ここまでできる”実験

## 要約
古典ゲームDOOMのレンダリングを「描画は全部CSS、ロジックはJS」で再現。CSSのカスタムプロパティ、3D変換、クリップパス、@propertyなど最新機能を駆使してブラウザの限界を探った作品。

## この記事を読むべき理由
フロントエンド技術の進化を「実際に動くデモ」で理解できる。日本のWeb開発者や学生にとって、CSSがレイアウト以外でここまで使えることを知る良い教材になる。

## 詳細解説
- 構成の考え方  
  - ゲームループと状態はJavaScript、描画はCSSに完全分離。JavaScriptはWAD（DOOMのマップ）から座標・高さなどの原データを読み取り、CSSカスタムプロパティに流す薄いレンダラ層を担う。

- 座標とジオメトリ（ブラウザ側で三角法）  
  - 壁は&lt;div&gt;にDOOM座標をカスタムプロパティで与え、CSSの関数で幅や角度を計算。ブラウザ側で三平方やatan2を使えるため、計算負荷をCSSエンジンへ委譲している。  
  $$\Delta x = x_{end}-x_{start} \quad \Delta y = y_{end}-y_{start}$$
  $$width = \sqrt{\Delta x^2 + \Delta y^2}$$
  - 実装ではCSSの hypot() と atan2() を利用。

- DOOM座標 → CSS 3D のマッピング  
  - DOOMはトップダウンでYが北上、CSSはYが上方向・Zが手前のため、transformで座標を反転させる（例: translate3d(x, -z, -y)）。カメラは使えないため「世界を動かす」トリックで視点を実現（プレーヤー座標を負にしてシーン全体をtranslate/rotate）。

- 床・複雑ポリゴン・テクスチャ整列  
  - フロアは回転で水平にし、clip-path（polygon / path + evenodd）や新APIの shape() で非矩形領域や穴を表現。  
  - テクスチャの継ぎ目を消すために「ワールド座標基準で background-position を決める」ことで隣接セクタ間でタイルがシームレスになる。

- アニメーションと @property  
  - ドアやリフトはDOMコンテナのtransformをCSSトランジションで動かす。プレーヤーの高さ（--player-z）など数値カスタムプロパティは @property で型を登録し、アニメーションを滑らかにする。

- スプライトとミラー技法（ビルボーディング）  
  - 敵は常にカメラを向くbillboard div。rotateYで視線合わせ、scaleXで左右反転（ミラー）。歩行フレームは steps() を使ったスプライトシートアニメーションで実現。同期感の除去はランダムなanimation-delayで調整。

- プロジェクタイルなどの動き  
  - 弾や爆発は到達点と所要時間をJSで算出し、エレメントのカスタムプロパティ(--start/--end/--duration)を設定してCSSアニメーションに任せる手法を採用。JSは衝突判定など論理だけ担当。

## 実践ポイント
- 小さく試す：まずは1枚の壁を&lt;div&gt;で作り、CSSの hypot() / atan2() で幅と回転を計算してみる。  
- @property を覚える：数値カスタムプロパティを登録すると、トランジションやアニメーションが滑らかになる。  
- テクスチャ同期：背景の world-origin を使い、background-position をワールド座標基準でセットすると継ぎ目が消える。  
- 複雑形状は clip-path / shape()：非矩形フロアや穴は path() と evenodd で一発。ブラウザ互換は要確認。  
- 「世界を動かす」発想：カメラが無いプラットフォームでは視点移動をシーン側の逆変換で実装する。  
- パフォーマンス注意：数千のDOM要素を使うため、実機（特にモバイル）でのプロファイルは必須。Chromium系での挙動が安定しやすい。

この記事を起点に、自分のポートフォリオ用デモや教育用の小さな実験（1ルームの3Dルームレンダラ等）を作ってみると、モダンCSSの実力と限界を実感できる。
