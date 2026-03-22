---
layout: post
title: "MAUI Is Coming to Linux - MAUIがLinuxへやってくる"
date: 2026-03-22T17:54:02.092Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://avaloniaui.net/blog/maui-avalonia-preview-1"
source_title: "MAUI Avalonia Preview 1 - Avalonia UI"
source_id: 47478687
excerpt: "Avaloniaの.NET MAUI対応でLinux/WASMへ既存アプリを描画UIで展開可能に"
image: "https://framerusercontent.com/images/CUbSIRximmKmuZ0BgveVtIexZSg.png?width=2013&amp;height=1496"
---

# MAUI Is Coming to Linux - MAUIがLinuxへやってくる
Avaloniaが.NET MAUIでLinuxとWASMを一気にカバーする――「描画UI」で実現する新しいクロスプラットフォーム戦略

## 要約
Avaloniaの.NET MAUIバックエンド（Preview 1）が公開され、LinuxとWebAssembly（WASM）上で既存の.NET MAUIアプリを動かせるようになった。Avalonia 12との連携で描画ベースの一貫したUIを提供するのが狙い。

## この記事を読むべき理由
- 日本企業やOSSプロジェクトで「Windows/Macに加えてLinuxデスクトップやブラウザ（WASM）へ展開したい」ケースが増えているため、既存の.NET MAUI資産を流用できる選択肢は価値が高い。
- デザインの一貫性やカスタマイズ性を重視するプロダクト開発者にとって、ネイティブと描画（drawn）UIの選択肢が増えるのは実務的メリット。

## 詳細解説
- 何が出たか：Avaloniaが.NET MAUI向けのハンドラ／バックエンドをPreview 1で公開。これにより.NET MAUIアプリをAvalonia描画エンジン上で動作させ、LinuxデスクトップとWASMへのデプロイが可能になる。
- 技術的特徴：
  - 描画ベース（Avalonia）のため、プラットフォーム間で同一の見た目と挙動を保てる。
  - .NET MAUIのハンドラはAvaloniaのプリミティブ上に構築されており、Avalonia APIでカスタマイズ可能。
  - Avalonia 12で導入された新しいナビゲーションAPIやコントロール群は、.NET MAUI互換性向上の成果。
  - GraphicsViewやSkiaSharp.Views.Mauiなど既存の描画ライブラリとの互換性も確保。Mapsuiなどのライブラリを修正なしで動かせた例あり。
  - WebViewがオープンソース化され、WASM上でのWeb表示やCORS調整などの対応事例がある。
- テスト実績：MauiPlanets、2048、.NET MAUI Control Gallery、AlohaAI、MyConferenceなど多数のアプリをポーティングして検証。テーマ対応、NativeAOTやCORSプロキシ追加など実運用上の調整も実施。
- 今後の課題：Maui.Essentials相当のAvalonia実装、WinUIとの相互運用、ネイティブ向けコントロールから描画版への拡張パターン整備など。

## 実践ポイント
- 今すぐ試す手順（概略）：
  1. .NET MAUIアプリを作成する
  2. NuGetで Avalonia.Controls.Maui.Desktop を追加
  3. net11.0 ターゲットフレームワークを追加
  4. MauiBuilder に UseAvaloniaApp を追加して net11.0 を実行
- チェックすべき箇所：GraphicsViewやSkiaSharp依存箇所、テーマ（ダーク/ライト）、WASM向けのCORSやトリム（サイズ最適化）。
- 日本の現場向けの応用例：社内ツールや管理コンソールを一度MAUIで作っておき、Linuxデスクトップ端末や社内ポータル（WASM）にも展開する運用が現実的。
- 参照：公式リポジトリ／Avalonia 12と.NET 11のプレビューを確認して互換性やサンプルを試すことを推奨。
