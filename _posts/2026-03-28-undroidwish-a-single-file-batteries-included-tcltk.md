---
layout: post
title: "Undroidwish – a single-file, batteries-included Tcl/Tk binary for many platforms - Undroidwish：単一ファイルで充実機能の多プラットフォームTcl/Tkバイナリ"
date: 2026-03-28T19:13:42.951Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://androwish.org/home/wiki?name=undroidwish"
source_title: "AndroWish: undroidwish"
source_id: 47556267
excerpt: "単一ファイルでスマホやRaspberry Pi等で動く多機能Tcl/Tk実験ランタイム"
---

# Undroidwish – a single-file, batteries-included Tcl/Tk binary for many platforms - Undroidwish：単一ファイルで充実機能の多プラットフォームTcl/Tkバイナリ
スマホやRaspberry Piまで1ファイルで動く？Undroidwishで始める軽量クロス実行環境

## 要約
UndroidwishはAndroWish由来の単一ファイルTcl/Tk実行バイナリで、SDL/AGG/freetypeベースのX11エミュレーションや多数の拡張を内蔵し、Windows・Linux・Raspberry Pi・Android(Termux)など幅広い環境で動作する実験的なプロジェクトです。

## この記事を読むべき理由
日本ではRaspberry PiやAndroid端末（Termux）を使ったプロトタイピングや教育用途が盛んで、軽量で持ち運べるGUI実行環境は即戦力になります。Undroidwishは「1ファイルで多機能」を目指しており、実機での試作や教育用ツールとして魅力的です。

## 詳細解説
- アーキテクチャ：AndroWishのソースを活用し、ZIP仮想ファイルシステムにスクリプトやデモを埋め込んだ単一バイナリを生成。プラットフォーム依存のビルドスクリプトで各種環境向けに作成される。
- 描画基盤：SDL + AGG + freetypeを用いたX11エミュレーションでアンチエイリアス描画を提供。Ctrl＋ホイールでルートウィンドウを滑らかにズームできるなど描画品質に特徴あり。
- 動画/出力ドライバ：
  - SDL2 Waylandドライバ対応（GNOME/Fedora/Debianなど部分検証済み）
  - KMSDRMでディスプレイマネージャ不要のコンソール実行（GPU/カーネルモード設定が必要）
  - RPIドライバでRaspberry Piのフレームバッファモード対応
  - jsmpegドライバでブラウザ（Firefox/Chrome/Safari）へ出力可能
- 対応プラットフォーム：Windows (32/64)、Intel Linux、ARM Debian（Raspberry Pi/Beaglebone）、FreeBSD、OpenBSD、OpenIndiana、macOS（α）、Haiku、Termux/Android等（多くは部分テスト・実験段階）。
- 同梱拡張：tkpath, tktreectrl, tkimg, Canvas3D（OpenGL 2.x 必要）等のGUI拡張、tcllib / tksqlite / bwidgets などのTclライブラリを内蔵。
- 実行方式：埋め込みZIP内のスクリプトを指定して起動（例：builtin:tksqlite0.5.13/tksqlite.tcl）。多数のデモやユーティリティ（widget, tkcon, tksqlite, Canvas3D 等）がショートカット名で用意されている。
- 注意事項：実験的・証明コンセプトであり、Windows用のポータブルexeはレジストリを書き換えないが「自己責任」での実行が推奨される。

## 実践ポイント
- まずは既成バイナリをダウンロードして試す（Downloadsページ参照）。
- 埋め込みデモを起動して描画や操作感を確認：
```bash
# tksqliteデモを起動（例）
undroidwish.exe builtin:tksqlite0.5.13/tksqlite.tcl
```
```bash
# widgetデモ（POSIX）
./undroidwish builtin:widget
```
- Raspberry PiではDebianベースの環境でRPIドライバを有効にしてビルドすると直にフレームバッファで動作可能。
- ブラウザ表示を試すなら jsmpg ドライバを使って遠隔でUIを確認する手法が便利。
- 開発用途：sdltkやSDLコマンドラインオプションでウィンドウサイズやリサイズ性を制御できるため、組み込みツールや教育用サンプル作成に向く。
- 重要：α・実験段階の機能が多いため本番利用は慎重に。まずはデモで互換性と必要な機能（Canvas3DやOpenGL要件など）を確認すること。
