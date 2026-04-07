---
layout: post
title: "Three hundred synths, 3 hardware projects, and one app - 300のシンセ、3つのハードウェア、そして1つのアプリ"
date: 2026-04-07T08:50:12.200Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://midi.guide/blog/three-hunded-synths-one-app/"
source_title: "300 synths, 3 hardware projects, and one app - MIDI CC and NRPN database"
source_id: 47670981
excerpt: "iPadで300機を一括制御──CSVデータベースと実機採用で実用化したConduktの舞台裏"
image: "https://midi.guide/static/images/blog/2026-04-06-three-hunded-synths-one-app/comparative-knob-morphology-dark.png"
---

# Three hundred synths, 3 hardware projects, and one app - 300のシンセ、3つのハードウェア、そして1つのアプリ
iPadで「全部のシンセを一括コントロール」する夢を叶えたコミュニティプロジェクトの裏側

## 要約
MIDI GuideはMIDI CC／NRPNの実装をCSVで公開するコミュニティデータベースで、300台超の機器対応、複数のハードウェア採用、そしてiOS/macOS向けコントローラアプリConduktのリリースにより実運用フェーズに入った。

## この記事を読むべき理由
MIDI機器のパラメータ管理は面倒で日本でも同様の悩みが多い。開発者やライブ／スタジオ環境を整えたい音楽家、ハード／ソフトメーカーにとって、既存の網羅的データと自由なライセンスは即戦力になるから。

## 詳細解説
- MIDI Guideの中身：MIDI CC（Control Change）とNRPN（Non-Registered Parameter Number）をCSV形式で整理。目標は「機械で解析できること」と「普通のミュージシャンが読めること」の両立。
- 進化の経緯：2019年開始→段階的に外部貢献を受け入れ、ドメイン移行やデザイン刷新を経て拡張。主要マイルストーンは外部貢献増加（2024）、ハード採用（NeuzeitのDrop、Reliq等、2025）、そしてConduktの正式リリース（2026）。
- 技術的ポイント：CSV仕様はシンプルでExcel等から編集可能。機器ごとにCC番号、範囲（例: 0–127）、NRPNのマッピングなどを定義。ウェブ表示は人間向けに冗長性を削ぎ、空欄非表示や表の折り畳みで可読性を確保。
- ライセンスと採用：データはCC-BY-SA 4.0で公開され、ハード／ソフトプロジェクトでの利用・再配布が可能（帰属と同一ライセンスでの共有が条件）。既に複数の商用ハードで採用実績あり。
- コミュニティ運用：gitが使えない寄稿者がメールでCSVを送ることも多く、運営は受け入れやすいフォーマット設計を重視した。

## 実践ポイント
- まず試す：midi.guideで自分のシンセを検索し、CSVをダウンロードしてマッピングを確認する。
- Conduktを試す：iPad／MacでConduktを動かして、複数シンセのパフォーマンスマッピングを体験する（必要なケーブルと電源に注意）。
- プロジェクトで活用：CC-BY-SA 4.0に基づき、製品やオープンソースツールに組み込める（帰属表記と同一ライセンスでの公開を忘れずに）。
- コントリビュート：マニュアルや実機でCC/NRPNを確認したら、CSV形式で寄稿（メールでも可）。日本の珍しい機材情報は特に価値が高い。
- ハードメーカー/教育者へ：既存データを使えばMIDI互換性の実装や教材作成の工数を大幅に短縮できる。

出典：Three hundred synths, 3 hardware projects, and one app（midi.guideの記事を要約・翻訳）
