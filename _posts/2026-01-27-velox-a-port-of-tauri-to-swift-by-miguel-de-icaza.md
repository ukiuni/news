---
layout: post
title: "Velox: A Port of Tauri to Swift - Velox：Tauri を Swift に移植"
date: 2026-01-27T11:12:09.517Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/velox-apps/velox"
source_title: "GitHub - velox-apps/velox: Velox is a port of Tauri to Swift."
source_id: 46687729
excerpt: "SwiftでTauriを使い軽量なmacOSデスクトップを高速開発できるVelox紹介"
image: "https://opengraph.githubassets.com/37dc7616f1d8e67306da31037e57b4e58ee09d128f76bdf4cddab1322d8284a5/velox-apps/velox"
---

# Velox: A Port of Tauri to Swift - Velox：Tauri を Swift に移植
Swift開発者がHTMLフロントエンド＋Swiftバックエンドで軽量なデスクトップアプリを作れる、新しい選択肢

## 要約
Velox は Tauri を Swift に移植したプロジェクトで、Swift Package Manager と連携するビルドプラグインで Rust FFI を自動ビルドし、macOS 向けのバンドル・開発ワークフロー（ホットリロード／dev server proxy 等）を提供します。

## この記事を読むべき理由
Swift を主戦場とする日本の開発者が、Electron より軽量でネイティブ寄りな選択肢を手に入れられる点は国内のデスクトップアプリ開発やプロトタイプ作成で即戦力になります。特に macOS 環境で Swift に慣れたチームは学習コストを抑えつつモダンなフロントエンドと組めます。

## 詳細解説
- アーキテクチャ: Velox は Tauri の設計を踏襲し、Rust 側の Wry/Tao を FFI 経由で Swift から操作する。Swift 側には VeloxRuntime モジュール（イベントループ、ウィンドウ・WebView 制御、型付けされたイベント）が用意される。
- ビルド連携: Swift Package のビルドツールプラグインが VeloxRuntimeWryFFI をビルドするため、通常は swift build で Rust ライブラリが自動ビルドされる。デフォルトは Cargo のオフライン実行で、ネットワーク取得が必要なら VELOX_CARGO_ONLINE=1 を設定。
- CLI とワークフロー: velox CLI は新規初期化、開発モード、リリースビルド、バンドル生成を提供。
  - velox init：テンプレートからプロジェクト生成
  - velox dev：dev server proxy（Vite 等と連携して HMR を効かせる）またはローカル資産配信の二モードをサポート
  - velox build：リリースビルド、--bundle で .app 作成／署名／notarize 設定が可能
- フロントエンド供給方式:
  1. ローカル資産（assets ディレクトリ）— 単純・軽量だが HMR やトランスパイルは無し
  2. Dev server proxy（devUrl）— Vite 等の HMR を活かせる。本番との URL 一貫性も保てる
- 設定と環境変数: velox.json と .env 系ファイルを優先度付きでマージしてビルド時に注入可能。macOS 用の署名/ハードニング/DMG/Notarization 設定も velox.json で指定できる。
- サンプルと API: リポジトリには多数の Examples（マルチウィンドウ、イベント、トレイ、ストリーミング等）があり、Swift ⇄ Web の IPC、ウィンドウ操作、キーボード・ポインタ情報などがサンプルで確認できる。

## 実践ポイント
- まずは環境準備（Swift toolchain、Rust/Cargo、Node.js はプロジェクトに応じて）して、Examples をビルドして動かすのがおすすめ。
- CLI 実行例:
```bash
# build Swift + Rust FFI
swift build

# 新規プロジェクト作成
velox init --name "MyApp" --identifier "com.example.myapp"

# 開発モード（Vite 等と連携）
velox dev

# リリースバンドル作成（macOS .app）
velox build --bundle
```
- モダンなフロントエンド（TypeScript/React/Vite）を使うなら devUrl + beforeDevCommand を設定して HMR を活かす。簡単なプロトタイプなら assets 配信モードが最速。
- CI/サンドボックス環境では Cargo のネットワーク制限に注意（VELOX_CARGO_ONLINE を使うか事前に依存取得してキャッシュする）。
- macOS 配布（署名・notarize）は velox.json の macos 設定を整える必要があるため、Apple デベロッパーアカウントや証明書の手配を前もって。
- 日本のチームでは「Swift ネイティブで開発しつつ Web 技術を活かす」ワークフロー（デザイナーとの連携や既存 Web 資産の再利用）に特にメリットが大きい。

参考：公式リポジトリ（Examples やドキュメントが豊富）をまずクローンして手を動かすこと。
