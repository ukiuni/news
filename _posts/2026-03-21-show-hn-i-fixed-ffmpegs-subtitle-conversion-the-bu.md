---
layout: post
title: "Show HN: I fixed FFmpeg's subtitle conversion (the bug from 2014) - FFmpegの字幕変換バグ（2014年発見）を修正しました"
date: 2026-03-21T14:33:31.650Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://connollydavid.github.io/pgs-release/"
source_title: "FFmpeg Subtitle Tools"
source_id: 47415044
excerpt: "ASSのアニメーションや色を保持してPGSへ直接変換可能なFFmpegビルド公開"
---

# Show HN: I fixed FFmpeg's subtitle conversion (the bug from 2014) - FFmpegの字幕変換バグ（2014年発見）を修正しました
魅力的なタイトル例: Blu-rayの動く字幕もそのまま変換！FFmpegの“字幕変換できない”問題を直したビルド公開

## 要約
FFmpegで長年残っていた「テキスト→ビットマップ／ビットマップ→テキスト間の字幕変換ができない」問題を修正したビルドが公開されました。ASSのアニメーションや色・移動を保ったままBlu-ray PGSへ変換したり、画像字幕をOCRでSRTに戻したりできます。

## この記事を読むべき理由
日本の動画制作や自宅のBDリッピング・字幕管理でも、スタイル付き字幕（ASS/SSA）やBD用PGS、画像ベースの字幕(OCR必要)が頻出します。本ビルドはそれらの変換で従来の制約を取り除き、ワークフローを一気にシンプルにします。

## 詳細解説
- 問題の背景  
  2014年から報告されていたFFmpegのバグ（#3819）は「テキストからビットマップ、またはその逆の字幕エンコーディング不可」という制約。結果として、ASS（スタイル付き・アニメーション可能）をBlu-rayのPGS（画像ベース）に正しく変換できませんでした。

- 何が直ったか（主な技術点）
  - PGSエンコーダの追加（関連PR #6843 相当）により、ASS/SSAのフェード・色変化・移動などのアニメーションを自動検出してPGSに反映。手動フラグ付けやフレーム単位の書き出しが不要に。
  - 画像ベース字幕（PGS/DVD/DVB）をOCRでテキスト（SRT等）へ変換する機能を統合。114言語のOCRデータ対応（tessdata）。
  - それまで不可能だった約88種類のフォーマット変換を可能にし、RGBA→GIFなどの直接変換も追加。
  - 重なり合う字幕（異なる表示時間）も正しく処理。

- ビルドとライセンス
  - FFmpeg 8.1 ベースの実行可能バイナリがプラットフォーム毎に用意（Linux x86_64/arm64、macOS x86_64/arm64、Windows x86_64/arm64）。
  - 最小版（ffmpeg + ffprobe）と英語OCRデータ付きの-eng版を提供。その他言語はtessdataに.traineddataを置くだけで追加可能。
  - ライセンスはLGPL 2.1。CIでテスト（FATE等）済み。

## 実践ポイント
- すぐ試すコマンド例
  - SRT/ASS/WebVTT → Blu-ray PGS（1080p出力例）
```bash
ffmpeg -i subtitles.srt -s 1920x1080 output.sup
```
  - MKV内の字幕をPGSで保存（映像・音声コピー）
```bash
ffmpeg -i input.mkv -c:s pgssub -c:v copy -c:a copy output.mkv
```
  - PGS/DVD/DVB（画像字幕）をOCRでSRTへ
```bash
ffmpeg -i input.mkv -c:s srt output.srt
```
  - RGBA動画をGIFに（フィルタパイプ不要）
```bash
ffmpeg -i input.mp4 -c:v gif out.gif
```

- 日本語OCRを使うには  
  tessdataの日本語.traineddataをダウンロードして、実行ファイルと同じ階層にあるtessdata/フォルダに置くと認識可能。

- 導入手順（簡単）
  1. 配布バイナリをダウンロード・展開する。
  2. 既存のffmpegと置き換えるかパスを通す。
  3. 必要ならtessdataを追加して日本語OCRを有効化。

導入すれば、BD用の高品質なPGS作成や、画像化された字幕のテキスト化などが格段に楽になります。興味があれば元リリースページからプラットフォーム別バイナリを入手してください。
