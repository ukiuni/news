---
layout: post
title: "Show HN: Calyx – Ghostty-Based macOS Terminal with Liquid Glass UI - Calyx — GhosttyベースのLiquid Glass UIを備えたmacOSターミナル"
date: 2026-03-12T14:38:25.762Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/yuuichieguchi/Calyx"
source_title: "GitHub - yuuichieguchi/Calyx: A macOS 26+ native terminal application · GitHub"
source_id: 47350108
excerpt: "macOS 26専用の美しく高速なGPU端末、タブや分割、コマンドパレットで開発効率を劇的に向上"
image: "https://opengraph.githubassets.com/f20fc540379018413a3e0669ea5af419b2143fa85d90306488be203f5b7921c0/yuuichieguchi/Calyx"
---

# Show HN: Calyx – Ghostty-Based macOS Terminal with Liquid Glass UI - Calyx — GhosttyベースのLiquid Glass UIを備えたmacOSターミナル
見た目も速さも妥協しない——macOS 26専用のネイティブ端末アプリ「Calyx」が注目の理由

## 要約
Calyxはlibghostty（Metalレンダリング）を核に、macOS 26（Tahoe）デザインの「Liquid Glass」UIを備えたネイティブ端末。タブグループ、分割ペイン、コマンドパレット、セッション永続化など開発者が求める機能を一通り揃えます。

## この記事を読むべき理由
日本でもmacOS開発環境やAppleシリコン普及が進む中、ネイティブでGPU加速される端末は作業効率と体験を同時に改善する可能性があります。特にタブ管理や分割、エディタ連携を重視する日本のエンジニアには実用的な代替候補です。

## 詳細解説
- コア技術
  - libghosttyを端末エンジンに採用し、MetalでGPU加速レンダリング（Ghostty v1.3.0）。
  - Swift 6.2 / AppKit（ウィンドウ管理）+ SwiftUI（表示）を橋渡しする設計。GhosttyのC APIはFFI経由で呼ばれる。
- UX・機能
  - Liquid Glass UI：macOS 26 Tahoeのネイティブスタイルを踏襲した視覚設計。
  - タブグループ（色プリセット、折りたたみ、階層管理）、水平/垂直分割、方向フォーカス移動。
  - コマンドパレット（Cmd+Shift+P）で操作検索／実行、セッション自動復元、スクロールバック検索、ネイティブのオーバーレイスクロールバー。
  - WKWebViewを同アプリ内でタブとして併設（http/https、非永続ストレージ、ポップアップブロック）。
  - Gitサイドバー（変更表示、コミットグラフ、インライン差分）や、複数インスタンス間通信のためのClaude Code向けMCPサーバ（IPC）を内蔵。
- 互換性・注意点
  - macOS 26+, Xcode 26+が前提。Ghosttyの設定ファイル（~/.config/ghostty/config）との互換性あり。
  - 日本語／全角文字行での「カーソルクリック移動」がオフセットする既知の制約あり（Ghostty側のセル換算による影響）。

## 実践ポイント
- リリース入手：最新のZIPをダウンロードして /Applications に配置すれば試せます。  
- ソースビルド時の主要コマンド例：
```bash
# bash
git clone --recursive https://github.com/yuuichieguchi/Calyx.git
cd Calyx
cd ghostty
zig build -Demit-xcframework=true -Dxcframework-target=native
cd ..
cp -R ghostty/macos/GhosttyKit.xcframework .
xcodegen generate
xcodebuild -project Calyx.xcodeproj -scheme Calyx -configuration Debug build
```
- 日本語環境での利用：カーソルクリック移動の挙動を確認し、必要なら既知の制約を考慮してワークフローを調整すること。
- すぐ試せる活用：タブグループと分割で複数プロジェクトを視覚的に整理、コマンドパレットで慣れないショートカットを素早く実行。Claude IPCは複数タブでLLMベースのツール連携を試す用途に有効。
- 貢献：興味があればGitHubでIssueやPull Request、ローカルビルドやテストに参加可能。

Calyxは「見た目」だけでなくネイティブ性能と開発者向け機能を両立しており、macOSネイティブの端末体験を試したい日本のエンジニアにおすすめです。
