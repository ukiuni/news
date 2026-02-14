---
layout: post
title: "An offline crossplatform desktop app for cleaning dev caches - 開発キャッシュを掃除するオフラインで動くクロスプラットフォームデスクトップアプリ"
date: 2026-02-14T14:06:29.603Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://reclaimr.dev/"
source_title: "Reclaimr — Reclaim Gigabytes from Development Caches"
source_id: 1382307106
excerpt: "Rust/Tauri製のオフラインで開発キャッシュを安全に数GB削除"
image: "https://reclaimr.dev/og-image.png"
---

# An offline crossplatform desktop app for cleaning dev caches - 開発キャッシュを掃除するオフラインで動くクロスプラットフォームデスクトップアプリ
開発環境のゴミを一掃して数GBを取り戻す──ローカルで安心して使える「Reclaimr」の登場

## 要約
ReclaimrはRust＋Tauriで作られたオフラインのデスクトップアプリで、npm/Cargo/pip/Gradle/Docker/XcodeやIDEキャッシュなど100以上の開発ツールを高速かつ安全にスキャンして不要なキャッシュを削除するツールです（現在ベータ、無料）。

## この記事を読むべき理由
ローカル開発やCIで肥大化するキャッシュはSSD容量やビルド時間、バックアップコストに直結します。特に日本の現場で増える大規模リポジトリや複数ツール混在環境では、手作業より安全で高速なキャッシュ整理が生産性改善に直結します。

## 詳細解説
- カバー範囲：npmのnode_modules、Rustのtarget、Pythonの__pycache__/.venv、GradleやDockerイメージ、Xcodeや各IDEのキャッシュなど、100以上のツールを標準で認識。
- スキャン方式：パターンマッチによる再帰探索でプロジェクト配下やグローバルキャッシュを一度に検出。並列スキャンはRust＋Rayonで実装され、現代ハードで数千パスを短時間で処理。
- 安全設計：LOW/MEDIUM/HIGHの3段階リスク分類、スキャン対象のみ削除可能なホワイトリスト方式、パスの正規化とシンボリックリンク解決、ルート保護など「誤削除を防ぐ」工夫が中心。
- UI/操作：ツリー表示で階層ごとに中身を確認、カテゴリ／サイズ／リスクでフィルタ。HIGHリスクは明示的確認が必須。
- 技術基盤：バックエンドはメモリ安全なRust（GCなし）、フロントはTauriでネイティブ風・軽量なバイナリ。macOS（Apple Silicon対応）／Linux／Windowsで動作。
- 配布とライフサイクル：現時点はベータの無料提供。アーリーアクセスは待機リスト方式。

## 実践ポイント
- まずはベータで「ホームと主要プロジェクトフォルダ」をスキャンして、サイズ上位とHIGHリスク項目だけ詳しく確認する。  
- node_modulesやDockerキャッシュは即効で容量削減できるが、ビルド成果物やツールチェーンを消さないようリスク表示を必ずチェック。  
- 定期実行の運用を検討する場合は、CIのキャッシュ戦略（リモートキャッシュ／復元）と併せてポリシーを決める。  
- 社内導入時は、allowlistや削除ログを運用ルールに組み込み、誤削除リスクを低減する。

元記事のベータは無料なので、まず手元で試して効果（GB単位の回復）を確認するのが手っ取り早いです。
