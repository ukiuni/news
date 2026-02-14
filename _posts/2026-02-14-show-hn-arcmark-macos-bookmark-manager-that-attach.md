---
layout: post
title: "Show HN: Arcmark – macOS bookmark manager that attaches to browser as sidebar - Show HN: Arcmark – ブラウザにサイドバーとして貼り付く macOS 用ブックマーク管理ツール"
date: 2026-02-14T18:12:14.245Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/Geek-1001/arcmark"
source_title: "GitHub - Geek-1001/arcmark: macOS bookmark manager that attaches to any browser window as a sidebar"
source_id: 47016058
excerpt: "ブラウザ横に貼り付くローカル保存ブックマークで作業効率を劇的改善"
image: "https://opengraph.githubassets.com/a6ff622c039132107856f50053cd11cd2a82c839822480f4332d91b2d1044b9a/Geek-1001/arcmark"
---

# Show HN: Arcmark – macOS bookmark manager that attaches to browser as sidebar - Show HN: Arcmark – ブラウザにサイドバーとして貼り付く macOS 用ブックマーク管理ツール
魅力的タイトル：ブラウザ横に常駐する新発想のブックマーク棚「Arcmark」で作業効率を一気に上げる方法

## 要約
Arcmark は Swift / AppKit 製のネイティブ macOS アプリで、Chrome / Safari / Arc / Brave 等のブラウザウィンドウにサイドバーとして“貼り付け”られるローカル保存型ブックマーク管理ツールです。ワークスペース・ネスト・ドラッグ＆ドロップを備え、Arc のワークスペースを丸ごとインポートできます。

## この記事を読むべき理由
ウィンドウ切り替えを減らしブラウザ横に即アクセスできるブックマークは、タブ過多や集中作業が多い日本の開発者・クリエイターにとって即効性のある生産性改善になります。ローカル-first 設計なのでプライバシーやオフライン利用も安心です。

## 詳細解説
- アーキテクチャ：Swift + AppKit のネイティブ macOS アプリ。ブラウザウィンドウに“追従”する実装は Accessibility API を用いたウィンドウ検出／添付が中心。添付を無効にすれば単体ウィンドウとして動作します。  
- ストレージ：全データは単一の JSON ファイル（~/Library/Application Support/Arcmark/data.json）にローカル保存。エクスポートやバックアップが容易。  
- 組織機能：複数ワークスペース（色付き）、フォルダのネスト、ドラッグ＆ドロップで並べ替え、インライン編集、検索・フィルタ。常時表示（Always-on-Top）も可能。  
- Arc 連携：Arc ブラウザのローカルファイル（~/Library/Application Support/Arc/StorableSidebar.json）を解析してワークスペース構成を再現できるインポート機能あり。  
- 動作環境／権限：macOS 13.0+。サイドバー添付機能は Accessibility 権限が必要（権限が無ければ単独ウィンドウモード）。  
- ビルド：Swift 6.2+ と swift-bundler があればソースからビルド可能。代表的な実行手順は下記。

```shell
# Shell
git clone https://github.com/Geek-1001/arcmark.git
cd arcmark
./scripts/run.sh    # ビルドして実行
./scripts/build.sh  # ビルドのみ（オプション --dmg で DMG 作成）
```

## 実践ポイント
- まずは単独ウィンドウで試し、慣れてから Accessibility 権限を付与してブラウザ添付を有効化する（設定→プライバシーとセキュリティ→アクセシビリティ）。  
- Arc から移行する場合は Arc の StorableSidebar.json を使って構造ごとインポートすると手早い。  
- data.json をこまめにバックアップしておけば、別マシン移行や復元が簡単。  
- 常に手元にブックマークを置きたい作業（リサーチ、ドキュメント参照、学習）に有効。複数ワークスペースでプロジェクトごとに切り替えると管理が楽になります。  

興味があれば Releases から .dmg をダウンロードするか、ソースをビルドして試してみてください。
