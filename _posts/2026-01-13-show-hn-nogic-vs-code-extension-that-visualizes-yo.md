---
layout: post
title: "Show HN: Nogic – VS Code extension that visualizes your codebase as a graph - Nogic — コードベースをグラフで可視化する VS Code 拡張"
date: 2026-01-13T22:02:35.013Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://marketplace.visualstudio.com/items?itemName=Nogic.nogic"
source_title: "Nogic - Visual Studio Marketplace"
source_id: 46605675
excerpt: "NogicでVSCode内リポジトリをグラフ化、影響範囲と設計を瞬時把握"
image: "https://Nogic.gallerycdn.vsassets.io/extensions/nogic/nogic/0.0.14/1768337321494/Microsoft.VisualStudio.Services.Icons.Default"
---

# Show HN: Nogic – VS Code extension that visualizes your codebase as a graph - Nogic — コードベースをグラフで可視化する VS Code 拡張
コードをファイルツリーだけで追う時代は終わり。Nogicでリポジトリを「図」で俯瞰し、設計や呼び出し関係を直感的に把握しよう。

## 要約
NogicはVisual Studio Code拡張で、プロジェクトのファイル・クラス・関数をインタラクティブな階層グラフとして可視化するツール。ボードやクラス図、コールグラフなどでコード構造を素早く理解できる。

## この記事を読むべき理由
大規模リポジトリ、レガシーコード、モノレポが増える日本の開発現場では「どこがどう繋がっているか」を素早く把握することが生産性と品質に直結する。NogicはVS Code内で手軽に視覚化でき、オンボーディングや設計レビュー、影響範囲調査に即効性があるためチェックする価値がある。

## 詳細解説
- インストール／起動
  - VS Codeの拡張マーケットからインストール。コマンドパレットで「Nogic: Open Visualizer」を実行して可視化を開始。
  - 初回はプロジェクトのインデックス作成（許可が必要）によりコードを解析する。

- 主な機能
  - 統合ビュー（Unified View）：ファイル／クラス／関数を階層グラフで表示。木構造的に掘り下げられるので関係性が分かりやすい。
  - Boards：関心のある部分だけを集めたカスタムボードを作成でき、モジュール単位やタスク単位でフォーカス可能。
  - Class Diagrams：クラスの継承やメソッド構造を図示。OOP設計の把握に有効。
  - Call Graphs：関数呼び出し関係をたどれるため、影響範囲の調査やパフォーマンス調査のヒントになる。
  - Quick Search：Cmd/Ctrl+Kで要素を即検索。
  - Auto-sync：ソースの変更が自動反映され、いつでも最新の図を参照できる。

- 操作のコツ
  - エクスプローラーでファイル／フォルダを右クリックして「Add to Nogic Board」で素早くボード化。
  - ノードのダブルクリックでエディタを開き、クリックでメソッド展開、ドラッグでパン、スクロールでズーム。

- サポートと言語
  - 複数言語対応だが対応範囲は拡張されつつあるため、自分のスタック（例えばJava, TypeScript, Pythonなど）がどこまでサポートされているか確認が必要。

## 実践ポイント
- 今すぐやること
  1. VS CodeにNogicを入れて「Nogic: Open Visualizer」を実行。
  2. 主要モジュールを右クリック→「Add to Nogic Board」でボードを作成し、設計図のベースにする。
- コードレビュー／オンボーディングに活用
  - PR説明にボードのスクリーンショットを添えると、変更の意図や影響範囲が伝わりやすくなる。
  - 新メンバーにはまず該当モジュールのボードを見せて「全体像→詳細」の順で教えると理解が速い。
- 影響範囲調査
  - 変更前にCall Graphで上流・下流を確認し、テストケースや検証ポイントを洗い出す。
- 注意点
  - 大規模リポジトリでは初回インデックスに時間がかかる可能性がある。プライバシーやファイルスキャンの許可設定を確認すること。

Nogicは「コードを読む量」を減らし「構造を把握する精度」を上げるツール。まずは自分のプロジェクトでボードを一つ作って、設計理解がどれだけ速くなるか試してみる価値がある。
