---
layout: post
title: "Bubble Sorted Amen Break - バブルソートされたアメン・ブレイク"
date: 2026-03-12T17:49:50.263Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://parametricavocado.itch.io/amen-sorting"
source_title: "Bubble Sorted Amen Break by Vee 🥑"
source_id: 47354098
excerpt: "HTML5で即試せる、Amen BreakをGodotでバブルソート可聴化"
image: "https://img.itch.zone/aW1nLzI0NzQ1MDIxLnBuZw==/original/JSW%2BCe.png"
---

# Bubble Sorted Amen Break - バブルソートされたアメン・ブレイク
Amen Breakをアルゴリズムで“ソート”する、Godot製ミニプロトタイプ

## 要約
インディー作者VeeがGodotで作ったプロトタイプ作品。タイトル通り「Amen Break（有名なドラムループ）」をバブルソート的な発想で扱う音楽的デモで、HTML5とWindows向けビルドが itch.io で配布されています。

## この記事を読むべき理由
クリエイティブコーディング、サウンドの可視化・可聴化、そしてGodotを使った軽量なオーディオ実験に興味があるなら短時間で触れて学びが得られます。日本のインディー音楽制作／教育現場でもアイデアを再利用しやすい題材です。

## 詳細解説
- 元情報：作者 Vee、プロトタイプ、プラットフォームは HTML5 と Windows、Windowsビルド約93MB、タグは Music / Music Production / No AI、itch.ioで「name your own price」配布。評価は1件で5.0。
- タイトルからの解釈：Amen Break（有名なドラムループ）を「バブルソート」になぞらえ、ループをスライスして何らかの比較・交換操作で順序を変化させる表現的なデモである可能性が高い。音の特徴量（音量、長さ、周波数成分など）に基づいてソートすることで、アルゴリズムの動きを可聴化していると考えられます。
- 技術的要素（推定含む）：Godotで作られているため、AudioStreamSample や AudioStreamGenerator／AudioStreamPlayer を使ったサンプル再生・逐次生成、HTML5エクスポートによるブラウザ実行対応が想定されます。エフェクトやフェードでスワップの不連続を和らげる実装も一般的です。
- 配布面：itch.io の「name your own price」モデルで手軽に試せ、HTML5版ならブラウザですぐ体験可能。Windows版は約93MBの単体ビルド。

## 実践ポイント
- まずは itch.io のHTML5版をブラウザで試して挙動を観察する（手軽・即体験）。
- 自分で同様の実験をやるなら、Godot の AudioStreamSample / AudioStreamGenerator とタイムスライス（短いバッファ）で切り分け、比較キー（RMS/ピーク/スペクトル重心など）を用意してソートアルゴリズムを動かしてみる。
- 教育用途には「アルゴリズムの可聴化」として有効：バブルソートの比較・交換が音で分かるため、視覚だけでなく聴覚で理解を深められます。
- サンプル利用時は Amen Break の利用規約・著作権に注意すること（プロジェクト用途や公開配布の前に確認を）。

元記事リンク： https://parametricavocado.itch.io/amen-sorting
