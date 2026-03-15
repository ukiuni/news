---
layout: post
title: "Show HN: What if your synthesizer was powered by APL (or a dumb K clone)? - シンセがAPL（あるいは簡易Kクローン）で動いたら？"
date: 2026-03-15T15:33:44.902Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://octetta.github.io/k-synth/"
source_title: "ksynth"
source_id: 47386983
excerpt: "短いAPL風式でブラウザ上で即音作成・演奏／WAV保存できる実験的シンセ"
---

# Show HN: What if your synthesizer was powered by APL (or a dumb K clone)? - シンセがAPL（あるいは簡易Kクローン）で動いたら？

1行で音を作る衝撃──APL系の小さな言語でブラウザ上に組まれた実験的シンセ「k-synth」を紹介します。

## 要約
APL／K風の配列言語を実行するランタイム（WASM）でブラウザ内シンセを動かすデモ。パッチを短い式で書き、パッドで演奏、WAV出力やパッチ保存が可能です。

## この記事を読むべき理由
配列プログラミングの“短さ”と音響処理の相性を直感的に体験できるため、音響DSP入門、ライブコーディング、プロトタイピングに刺激を受けたい日本の開発者・音楽制作者に有用です。

## 詳細解説
- 言語面：APL／K系は配列演算を核にした言語で、表現が非常にコンパクト。波形生成やフィルタ処理を短い式で記述できるため、パッチが実験的かつ可搬性高くなります。
- 実装技術：ブラウザ上で動くランタイムはWebAssemblyを利用。UIはパッド（drum / melodic）やplay/stop、patchの保存・読み込み、WAVダウンロード等を備え、即時に音を鳴らせます。
- インタラクション：画面のパッドをクリックして音をトリガー。エディタに式を書いて実行（キーボードショートカット例：run = Ctrl+Enter、clear = Ctrl+L）。サンプル単位の設定（base rate／slot pitch 等）で音程や再生レートを調整できます。
- 意義：短い配列式でDSPを試せるため、学習コストを下げつつ新しい音色の試作が可能。コード量を抑えることでライブコーディングやアイデア出しに向く設計です。

## 実践ポイント
- まずは公式ページを開き、pads → melodic → play の流れで試す。  
- エディタで式を書き、Ctrl+Enterで実行。気に入ったらWAVをダウンロードして保存。  
- 短い配列演算で波形（例：加算・位相シフト・簡易フィルタ）を組んでみると効果が分かりやすい。  
- 日本のチップチューン／ライブコーディングイベントやプロトタイプ作成に流用可能。MIDI入力やWebAudioとの連携も検討すると実用性が広がります。

元プロジェクト（octetta/k-synth）のページで実際に触ってみてください：https://octetta.github.io/k-synth/
