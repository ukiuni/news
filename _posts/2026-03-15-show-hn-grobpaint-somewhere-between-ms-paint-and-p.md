---
layout: post
title: "Show HN: GrobPaint: Somewhere Between MS Paint and Paint.NET - GrobPaint：MS PaintとPaint.NETの中間を目指すマルチプラットフォーム軽量ペイント"
date: 2026-03-15T01:21:57.183Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/groverburger/grobpaint"
source_title: "GitHub - groverburger/grobpaint: Somewhere between MS Paint and Paint.NET. Multiplatform by default. · GitHub"
source_id: 47382072
excerpt: "余計な機能を省いた軽量レイヤー対応ペイント、macで即戦力に注目"
image: "https://opengraph.githubassets.com/e34c1794dc326b49eed277c2c0664a99af9a2a35d9803947b4767de29b0e304e/groverburger/grobpaint"
---

# Show HN: GrobPaint: Somewhere Between MS Paint and Paint.NET - GrobPaint：MS PaintとPaint.NETの中間を目指すマルチプラットフォーム軽量ペイント
驚くほど軽快で必要十分――Macでも使える「層付きペイント」の新定番候補

## 要約
GrobPaintは「余計な機能を削ぎ落とした」レイヤー対応の軽量イメージエディタ。Web技術＋小さなPythonバックエンドでマルチプラットフォームに動作します。

## この記事を読むべき理由
Paint.NETがmacOS非対応で困っている開発者やドット絵・簡易編集を手早く済ませたいデザイナーにとって、導入ハードルが低く即戦力になる可能性が高いからです。

## 詳細解説
- 目的：Photoshopを狙わず、MS Paintより高機能、Paint.NETより軽いツールを提供。余計な「肥大化」を避ける設計。
- 主な機能：
  - レイヤー（追加・削除・複製・結合・並べ替え、16種のブレンドモード、レイヤー毎の不透明度）
  - ツール：ペン、ブラシ、消しゴム、塗りつぶし、スポイト、線・矩形・楕円・テキスト、選択（矩形・マジックワンド）、移動、回転、拡大縮小、ミラー
  - カラー：HSVピッカー、RGB/Hex、アルファ、パレット（Lospec 500、PICO-8）
  - キャンバス操作：ズーム、パン、グリッド、フィット表示
  - ファイル：PNG/JPEG/BMP/GIF、独自プロジェクト形式 .gbp（ZIP、レイヤーを個別PNGで保持）
  - スプライトシートの分割・統合、各種リサイズ（最近傍／双線形／三次補間）
- 技術スタックとアーキテクチャ：
  - フロントはバニラJS（ESモジュール）で約2500行。モジュール分割（core, renderer, tools, ui, app）。
  - バックエンドは小さなPythonサーバ（grobpaint.py）で、pywebviewを使えばネイティブウィンドウ化、未導入時はブラウザで起動可能。
  - 依存は最小限（JSZipのみCDN利用）。ライセンスはMIT。
- インストール／起動：
  - ソースから：python grobpaint.py（pywebviewでネイティブ起動、未インストール時はブラウザ）
  - ブラウザだけで利用可（index.htmlを直接開く）
  - ビルドスクリプトでmacOSアプリ／バイナリを生成（PyInstaller使用）
- ちょっとした注目点：Undo/redoはスワップベース、.gbpはmanifest.json＋layersフォルダのZIP。開発にはAnthropicのClaudeが関与。

## 実践ポイント
- macOSでPaint.NET代替を探しているなら、まずpython grobpaint.pyで試す（pywebviewを入れればネイティブ感あり）。
- ドット絵やスプライト制作ならPICO-8パレットとスプライトシート分割機能を活用。
- プロジェクト保存は.gbp（ZIP）なので、バージョン管理や差分管理が扱いやすい：layers配下のPNGを直接確認・差し替え可能。
- 拡張・調査：フロントはバニラJSで小さくまとまっているため、ツール追加やUI改造が入りやすい。MITライセンスなので社内ツールのベースにするのも現実的。

元リポジトリ：https://github.com/groverburger/grobpaint
