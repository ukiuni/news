---
layout: post
title: "Show HN: 3D Mahjong, Built in CSS - CSSで作られた3D麻雀ソリティア"
date: 2026-02-22T16:38:46.222Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://voxjong.com"
source_title: "VoxJong - CSS Mahjong Solitaire"
source_id: 47111981
excerpt: "CSSだけで144枚の麻雀牌を立体表示するブラウザ版ソリティア、実装とデモが学べる"
image: "https://voxjong.com/_nuxt/voxjong-logo.5kOxd6eD.png"
---

# Show HN: 3D Mahjong, Built in CSS - CSSで作られた3D麻雀ソリティア
ブラウザだけで動く「3D麻雀ソリティア」が、CSSの巧みな使い方で視覚的に魅せる――コードを学びたい人も遊びたい人も必見。

## 要約
VoxJongは144枚の麻雀牌を使ったソリティアを、主にCSSの3D変形とレイアウトで表現したブラウザゲーム。視点切替（アイソメ／トップダウン）、ズーム、ヒントやタイマーといったUIも実装されている（https://voxjong.com）。

## この記事を読むべき理由
CSSだけで3D的な表現をどこまで引き出せるかを実例で学べるため。日本のフロントエンド開発者やデザイナーが日常のUI表現やプロトタイプで応用しやすいアイデアが詰まっています。軽量なデモはポートフォリオや技術面接の話題にも使えます。

## 詳細解説
- 表現の中核はCSSの3D機能：perspective、transform（translate3d/rotateX/rotateY/rotateZ）、transform-style: preserve-3dにより各牌を立体的に配置。視点切替はルートクラスの付け替えで行い、各牌のtransformを再計算して見え方を変えます。
- 重なりと選択可能領域はDOMの重ね順（z-index）とペインの配置で制御。牌の個別アニメーションやフェードはCSSトランジション／アニメーションでGPU合成を使い滑らかに。
- ズームはscaleやカメラ相当のperspective調整で実装。144枚というタイル数はレンダリング負荷に影響するため、will-changeやバックフェイスカリング、必要時にレイヤー分割を行うのが実用的。
- ゲームロジック（マッチ判定、ヒント、タイマー、入力処理）はJavaScriptが担い、ビジュアルはCSSが主に担当する構成が自然。タッチ/マウス両対応のポインターイベント処理も必須。
- ブラウザ互換性：Chrome系は問題少、Safariやモバイルブラウザはtransformの挙動やパフォーマンス差に注意。日本でのモバイル比率を考えるとタッチ最適化は重要。

## 実践ポイント
- サイトを開いて要素検査：各牌に割り当てられたtransformやクラス名を確認して学ぶ。
- 小さなスタック（4〜8要素）でまず試作し、transform-styleとperspectiveの挙動を体感する。
- will-changeやtranslate3dでGPU合成を活用し、アニメーションの滑らかさをチェックする。
- タッチ操作とレスポンシブ対応を早期に検証（日本のユーザーはモバイルが多い）。
- プロトタイプやポートフォリオとして転載・改造する際は、著作権とライセンスを確認すること。

元記事（デモ）：https://voxjong.com
