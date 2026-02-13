---
layout: post
title: "Bullet Garden – a Vampire Survivors-like game in a single 85KB HTML file - Bullet Garden — 85KBの単一HTMLファイルで作られたVampire Survivors風ゲーム"
date: 2026-02-13T10:34:30.870Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.myvibe.so/nategu/sound-garden"
source_title: "Sound Garden"
source_id: 47001037
excerpt: "85KBの単一HTMLで遊べるVampire Survivors風ゲームの作り方と最適化手法を紹介"
image: "https://www.myvibe.so/image-bin/uploads/43ab228eb3047b9f.png?imageFilter=resize&w=800"
---

# Bullet Garden – a Vampire Survivors-like game in a single 85KB HTML file - Bullet Garden — 85KBの単一HTMLファイルで作られたVampire Survivors風ゲーム
85KBしかないのに遊べる！ブラウザだけで動く“バレットガーデン”の作り方とその応用

## 要約
単一の85KB HTMLで作られたVampire Survivors風のブラウザゲーム（Sound Garden、JavaScript必須、ArcBlock上で動作）が公開されています。小さなファイルで高い遊び心を実現するために取られる手法と、日本の開発者に役立つ実践ポイントを解説します。

## この記事を読むべき理由
小規模で配布しやすく、学習やプロトタイプに最適な「単一ファイルゲーム」の作り方は、インディー開発や社内ハックデー、モバイル向け軽量コンテンツ制作で即戦力になります。特に帯域やストレージに制約のある環境でも有利です。

## 詳細解説
- 作品の特徴（元記事のポイント）
  - 1ファイル、約85KBのHTMLで完結する点が目玉。外部アセットに依存せずブラウザだけで動作する。
  - 表示にJavaScriptが必須で、配布は単純。ArcBlockなどのホスティング上で動作しているという記載がある。

- 85KBに収めるために使われる技術（一般的に採用される手法）
  - アセットレス設計：画像や音声を外部ファイルにしないか、あるいは極力省く（手描きスプライトをcanvasで描く、CSSだけで表現）。
  - 手続き的生成：敵出現や弾幕、エフェクトをアルゴリズムで生成してデータ量を節約。
  - 小型化（ミニファイ）とバンドル最適化：余分な空白削除、変数名短縮、デッドコード除去。
  - データURIやBase64埋め込み：どうしても必要な小さな画像は埋め込みで1ファイル化。
  - Web API活用：Canvas APIで描画、WebAudio APIで音声を合成してファイルサイズを下げる。
  - 効率的なゲームループ：requestAnimationFrameと最小限の状態更新で計算コストを削減。

- 実装上の注意点
  - ブラウザ互換性とパフォーマンス。モバイルでのメモリ/CPU消費を意識する。
  - デバッグのしづらさ。単一化は利便性とトレードオフになるため、開発はモジュール分割→最終ビルドで1ファイル化するのが実務向け。

## 実践ポイント
- ソースをまず見る：公開ページで「ページソースを表示」してどの手法を使っているか確認する（JSが有効であることを注意）。
- 小さく作るワークフロー：モジュールで開発 → terser/esbuildでミニファイ → 最終的に1ファイルにバンドルする。
- 手続き的アセットを学ぶ：WebAudioで音を合成、Canvasでスプライトを描く方法を実験する。
- プロトタイプに活用：ハッカソンや社内デモで短時間で魅せるコンテンツを作るのに最適。
- 日本市場向けの応用：軽量ゲーム/広告/チュートリアルコンテンツとして、低帯域環境やSNSでのシェアに強い。

（補足）元ページは「Sound Garden」としてJavaScript必須、ArcBlockでホストされている旨の記載があります。興味があればソースを覗いて手法を学んでみてください。
