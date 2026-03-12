---
layout: post
title: "Qt Creator 19 released - Qt Creator 19 リリース"
date: 2026-03-12T18:59:23.546Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.qt.io/blog/qt-creator-19-released"
source_title: "Qt Creator 19 released"
source_id: 384519134
excerpt: "ミニマップ搭載とリモート自動検出でQt開発の環境設定とデバッグが劇的に高速化"
image: "https://www.qt.io/hubfs/QtCreator19-ReleaseFeatured-1200x628.webp"
---

# Qt Creator 19 released - Qt Creator 19 リリース
開発がサクッと快適に変わる！ミニマップ搭載＆リモート自動設定でQt開発の地味なストレスを一掃

## 要約
Qt Creator 19 はエディタのミニマップ、リモートデバイスの自動検出、基本的なMCPサーバ、Cargo/Gradle/Swift等の軽量プロジェクト対応などを導入し、開発体験とパフォーマンスを改善します。

## この記事を読むべき理由
国内の組込み・クロスプラットフォーム開発やチーム開発で「デバイス接続」「プロジェクト立ち上げ」「デバッグ開始」にかかる工数が減るため、オンサイト／リモート問わず生産性が上がります。

## 詳細解説
- ミニマップ：テキストエディタに簡易文書概観を表示。スクロール代わりに利用可能。設定は Preferences > Text Editor > Display > Enable minimap。
- リモートデバイス：デバイス登録後に「Run Auto-Detection Now」で Qt version、コンパイラ、デバッガ、CMake 等を自動検出しキットを自動作成。デバイスのファイルシステムは File System ビューや Locator、File > Open From Device で参照可能。Android 端末／エミュレータも含む。
- MCP サーバ：HTTP POST と SSE による基本的なリモート操作（ファイル/プロジェクトのオープン、ビルド、実行、デバッグなど）を提供。Extensions モードで MCP Server プラグインを有効化して利用。
- 拡張プロジェクト対応：Open Workspace を基に Ant, Cargo, .NET, Gradle, Swift のプロジェクトファイル（例: Cargo.toml）を軽量ワークスペースとして開け、対応ツール（cargo build/run 等）から自動でビルド/実行設定を作成。C# と Swift は言語サーバ検出に対応。
- そのほか主要改善点：設定がダイアログからモードに変更（画面占有が向上）、QMLスキャンやデバイス自動接続、CMake読み込み、WindowsでのMSVC/CDB検出などの性能改善。開発コンテナ設定の表示、GLSLパーサ更新(4.60)＋Vulkan対応、Valgrind プロトコル v5/v6対応、統合端末から同インスタンスへファイルを開く「qtc」コマンド追加。

## 実践ポイント
- まずアップデート：Qt Online Installer（commercial / opensource）または公式ダウンロードから更新。
- ミニマップを有効化して大きなファイルの見通しを改善。
- 新しいリモート自動検出で一度デバイスを登録し、ツールチェーンの初期設定を短縮。
- MCP Server を有効にして CI/エディタ連携やリモート操作を試す（HTTP POST/SSE クライアントが必要）。
- Rust/C#/Gradle/Swift を扱うプロジェクトは軽量ワークスペースで開発開始を簡略化。
- 問題はバグトラッカーへ報告し、変更履歴を確認して互換性を把握する。

（商用・OSSどちらも無償アップグレード可能。詳細は公式ダウンロードとドキュメントを参照）
