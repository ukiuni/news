---
layout: post
title: "Show HN: Bonsplit – tabs and splits for native macOS apps - Show HN: Bonsplit — ネイティブmacOSアプリ向けのタブとスプリット"
date: 2026-01-25T13:29:05.472Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://bonsplit.alasdairmonk.com"
source_title: "Bonsplit - Native macOS Tab Bar with Split Panes for SwiftUI"
source_id: 46753301
excerpt: "BonsplitでSwiftUI製macOSアプリに高速で直感的なタブ＆分割UIを即導入。"
image: "https://bonsplit.alasdairmonk.com/og-image.png"
---

# Show HN: Bonsplit – tabs and splits for native macOS apps - Show HN: Bonsplit — ネイティブmacOSアプリ向けのタブとスプリット

macOSアプリに「エディタ級」のタブ＆分割レイアウトを一気に導入するライブラリ

## 要約
BonsplitはSwiftUI対応のネイティブmacOSタブバー＋分割ペインライブラリ。120fps級の滑らかなアニメーション、ドラッグでの並べ替え・移動、キーボード操作を備え、アプリへ素早く組み込める。

## この記事を読むべき理由
macOSユーザーや開発者にとって、タブとペインの扱いやすさは生産性に直結する。SwiftUIアプリや社内ツール、エディタ系アプリを作る日本の開発者にとって、Bonsplitは「ネイティブ感」のあるUXを短時間で実現できる有力な選択肢になる。

## 詳細解説
- コア機能
  - タブ生成・更新・削除（タイトル・アイコン・dirtyフラグ対応）
  - ペインの水平／垂直スプリット、空ペイン生成、ペイン閉鎖
  - ドラッグ＆ドロップでのタブ並べ替え・クロスペイン移動
  - キーボードでのペイン間ナビゲーション（上下左右）とフォーカス制御
  - 120fpsレベルのアニメーションとアニメーション無効化オプション

- APIの概要（主要メソッド）
  - createTab / updateTab / closeTab / selectTab
  - splitPane / closePane
  - navigateFocus(direction:) / focusPane(paneId:)
  - クエリ系: allTabIds / allPaneIds / tabs(inPane:) / selectedTab(inPane:)

- 設定とライフサイクル
  - BonsplitConfigurationで細かな挙動を制御（分割許可、タブ閉鎖、空ペイン自動閉鎖、タブ再配置許可など）
  - contentViewLifecycle(.recreateOnSwitch / .keepAllAlive)でメモリと再描画のトレードオフを選択可能
  - 見た目調整: tabBarHeight / tabMinWidth / tabMaxWidth / tabSpacing / 最小ペイン寸法 等
  - プリセット: .default / .singlePane / .readOnly

- 実装面の利点
  - Swift Package Managerで導入可能（GitHubパッケージ）
  - SwiftUIと親和性が高く、既存のビュー階層へ自然に組み込みやすい
  - デリゲートコールバックで外部イベント処理や保存確認などを実装可能

## 実践ポイント
1. まず依存に追加（Package.swift）
```swift
.package(url: "https://github.com/almonk/bonsplit.git", from: "1.0.0")
```

2. 最小の使い方（設定→コントローラ→ビュー）
```swift
let config = BonsplitConfiguration(
  allowSplits: true,
  allowCloseTabs: true,
  autoCloseEmptyPanes: true,
  contentViewLifecycle: .keepAllAlive,
  newTabPosition: .current
)
let controller = BonsplitController(configuration: config)
// SwiftUI内に組み込む
BonsplitView(controller: controller)
```

3. よく使うAPI例
```swift
let tabId = controller.createTab(title: "Document.swift", icon: "swift")
let newPane = controller.splitPane(orientation: .horizontal)
controller.updateTab(tabId, isDirty: true)
controller.navigateFocus(direction: .right)
```

4. 日本での活用案
  - エディタやドキュメント系アプリ（コード・メモ・設計書）、社内ツールの多窓表示
  - SwiftUIで作る社内管理画面に自然な「タブ＋分割」UXを追加して生産性向上
  - contentViewLifecycleの選択でメモリ消費を調整し、日本向けの軽量マシンでも安定動作を目指す

まずは既存のSwiftUIプロジェクトにパッケージを入れて、プリセットで動作確認→必要に応じてコンフィグとデリゲートで微調整する流れが効率的。
