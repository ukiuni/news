---
layout: post
title: "Introducing Mystral Native - a native WebGPU JS runtime (no browser) - Mystral Nativeを紹介 — ブラウザ不要のネイティブWebGPU JSランタイム"
date: 2026-01-28T00:05:51.112Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/mystralengine/mystralnative"
source_title: "GitHub - mystralengine/mystralnative: Native WebGPU JS runtime with SDL3"
source_id: 415844994
excerpt: "Mystral Nativeでブラウザ不要にWebGPUゲームを単一実行ファイルで軽快に動かす"
image: "https://opengraph.githubassets.com/cc67c04faf35452f4abc8b718fa22b878f56ae2c6aa96f08c96d4597b88ceb7e/mystralengine/mystralnative"
---

# Introducing Mystral Native - a native WebGPU JS runtime (no browser) - Mystral Nativeを紹介 — ブラウザ不要のネイティブWebGPU JSランタイム
ブラウザを捨てて、WebGPUでネイティブに描く — 軽量JSランタイム「Mystral Native」がゲーム開発を変える

## 要約
Mystral Nativeは、Web API（WebGPU/Canvas/Audio/fetch 等）をそのまま使ってJS/TS製ゲームをネイティブ実行できる軽量ランタイム。ElectronのようにChromiumを含まず、macOS/Windows/Linuxで動作します（α版）。

## この記事を読むべき理由
- ブラウザ依存を外して軽量な配布（単一実行ファイル）を作りたい日本のインディー開発者やツール開発者に即役立つ技術的選択肢だから。
- Apple SiliconやWindows向けネイティブWebGPUの扱い、CI用のヘッドレス実行など実運用で重要なポイントを押さえられる。

## 詳細解説
- コア機能：WebGPU（レンダリング）、Canvas 2D（Skia）、Web Audio、fetch、requestAnimationFrame、ゲームパッドなど主要なWeb APIをサポート。TypeScriptはSWCでトランスパイル。
- アーキテクチャ：JSエンジン（V8/JSC/QuickJS）＋WebGPUバックエンド（Dawn / wgpu-native）＋SDL3等のネイティブライブラリを組み合わせて実現。必要な依存は事前ビルド済みでダウンロード可能。
- プラットフォーム：macOS (arm64/x64)、Windows、Linux を公式サポート。iOS/Android向けの埋め込みも可能（将来的にコンソールも視野）。
- ビルドと実行：公式CLIでインストール後、mystral run <script.js> で実行。mystral compile でアセットを含めた単一バイナリ／.appバンドルを作成可能。
- 開発向け選択肢：開発は V8 + Dawn（完全互換推奨）、CIや小型用途は QuickJS を選択。DawnはChrome実装由来でシェーダ互換性が高い。
- 実例：リポジトリには三角形、立方体、PBRシーン、Sponzaデモなどのサンプルがあり、Dawnビルドで高度なレンダリングを確認可能。
- 自動化用途：ヘッドレスでスクリーンショット取得や --watch モードでホットリロードが可能なので、CIでのレンダリング検証やアセット確認に使える。

javascript
// hello-triangle.js（簡略）
const adapter = await navigator.gpu.requestAdapter();
const device = await adapter.requestDevice();
const context = canvas.getContext("webgpu");
const format = navigator.gpu.getPreferredCanvasFormat();
context.configure({ device, format });
// シェーダ等を作ってレンダリングループを回す...
// 実行: mystral run hello-triangle.js

## 実践ポイント
- まずはCLI一発インストールとサンプル実行：curl/PowerShellスクリプトで導入 → mystral run examples/triangle.js を試す。
- 開発は V8 + Dawn を推奨（シェーダ互換性・パフォーマンス）。CI向けは QuickJS で軽量化。
- 配布は mystral compile --include assets で単一実行ファイル化、macOSは --bundle-only で.app準備。
- 自社ゲームやツールでWeb版のWebGPUコードがあるなら、ほぼそのままネイティブ化できるため、配布サイズ・起動時間の改善が期待できる。
- CIでの可視化や回帰検証には --headless --screenshot を組み込み、レンダリングテストを自動化する。

追加情報・ドキュメントは公式リポジトリ（mystralengine/mystralnative）とサイトを参照。Mystral Nativeは現在α段階のため、実運用前に安定性とプラットフォーム差異を確認すること。
