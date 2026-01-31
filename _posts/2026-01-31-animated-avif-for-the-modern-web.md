---
layout: post
title: "Animated AVIF for the Modern Web - モダンWebのためのアニメーションAVIF"
date: 2026-01-31T17:01:42.714Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://arthur.pizza/2025/12/animated-avif-for-the-modern-web/"
source_title: "Animated Avif for the Modern Web | Arthur Pizza"
source_id: 46764979
excerpt: "GIFより軽く高画質、ffmpegで簡単に作るアニメーションAVIF"
image: "https://arthur.pizza/image/xmas.avif"
---

# Animated AVIF for the Modern Web - モダンWebのためのアニメーションAVIF
GIFにさよならを告げる軽く滑らかなアニメーション画像の作り方

## 要約
AVIFはアニメーション対応で、GIFより圧縮効率と画質の面で有利。ffmpeg＋libsvtav1で比較的簡単にアニメーションAVIFを作れます（ただし環境によっては一度y4mに中間出力する手順が安定します）。

## この記事を読むべき理由
日本はモバイル利用やページ表示速度が重要な市場です。軽量で高画質なアニメーションはEC、SNS、広告、プロダクト紹介など多くの場面でUXとコスト改善に直結します。

## 詳細解説
- なぜAVIFか：AVIFはAV1ベースの静止画コンテナですが、フレーム列を格納するアニメーションモードを持ち、GIFよりも高圧縮・高画質になります。短くループする表現（GIFの代替）に向きます。  
- 実際の変換手順（概念）：
  1. ffmpegを用意する。  
  2. 元動画／GIFからフレーム列を取り出し、y4mなど中間フォーマットに出力すると安定する環境がある（特にDebian系でlibsvtav1を使う場合）。  
  3. libsvtav1（AV1エンコーダ）でavifにエンコード。crfで品質調整、fpsや解像度で軽さをコントロール。  
- 注意点：ブラウザやプラットフォームのAVIF（アニメーション）対応状況は随時変わるため、配信前に主要環境で互換性確認とフォールバック（動画タグ、APNG、GIFなど）を用意してください。

## 実践ポイント
- 必要なツール（例）
```bash
sudo apt install ffmpeg
```
- 中間y4mを経由する（安定動作のため）
```bash
ffmpeg -i INPUT_VIDEO.webm -pix_fmt yuv420p -an -y output.y4m
```
- 解像度・フレームレート制限例
```bash
ffmpeg -i INPUT_VIDEO.webm -vf "fps=15,scale=720:-1" -pix_fmt yuv420p -an -y output.y4m
```
- libsvtav1でエンコード
```bash
ffmpeg -y -i output.y4m -c:v libsvtav1 -crf 30 -b:v 0 -an -y output.avif
```
- 一発コマンドを試す（環境によっては失敗する場合あり）
```bash
ffmpeg -i INPUT_VIDEO.webm -vf "fps=15,scale=720:-1" -pix_fmt yuv420p -c:v libsvtav1 -crf 30 -b:v 0 -an -y output.avif
```

導入のコツ：まず短いループGIFをAVIF化して比較し、ファイルサイズ・品質・再生互換性を確認してからワークフローを本番に導入すると安全です。
