---
layout: post
title: "History of Greenfield (in-browser Wayland compositor) - Greenfield（ブラウザ内Waylandコンポジタ）の歴史"
date: 2026-01-29T15:57:48.787Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://wayouttheresoftware.blogspot.com/2023/07/some-history-about-greenfield.html"
source_title: "Way Out There Software: Some history about Greenfield Part 1"
source_id: 1731185140
excerpt: "ブラウザでWASM/WebGL/k8sを駆使して本格Linuxデスクトップを実現した技術的奮闘記"
---

# History of Greenfield (in-browser Wayland compositor) - Greenfield（ブラウザ内Waylandコンポジタ）の歴史
ブラウザだけで“本物の”Linuxデスクトップを動かす──Greenfieldが描いたクラウドデスクトップの実験記

## 要約
ブラウザ上でWaylandコンポジタを実装し、WebAssemblyやWebGL、Kubernetesまで使って「ブラウザで動く本物のLinuxデスクトップ」を目指した試行錯誤の記録。映像伝送、レンダリング、X11対応、運用自動化まで段階的に解決していく過程を追う。

## この記事を読むべき理由
クラウドネイティブ化する開発環境やリモートデスクトップの設計は日本の企業でも注目度が高い。Greenfieldは「ブラウザ＋WASM＋k8s」でGUIアプリを手軽に配布・隔離する現実的なアプローチを示しており、技術選定や実装上の落とし穴が学べるからです。

## 詳細解説
- 発端と目的：2017年に「ブラウザでWaylandコンポジタを動かしたら面白いのでは」と始動。目標はリモートアプリではなく、ブラウザ内でネイティブに近いGUI体験を提供すること。
- 映像伝送の課題：WebRTCはデータチャネルは使えるが、ビデオフレームにメタデータ（Waylandで必要なバッファ→コミットの紐付け）を付与できない問題が発覚。代替としてGStreamerでパイプラインを構築し、データはWebRTCのデータチャネルや後にWebSocketで運ぶ設計へ。
- デコードと表示タイミング：HTML5 MSEはフレーム単位の表示タイミング制御や不要なコンテナデータで不十分。そこでH.264デコーダ（TinyH264）をASM.js/WASMで動かし、クライアント側でフレームを扱う方式に。
- WaylandプロトコルのJS移植：ブラウザでWaylandクライアント/サーバ相当を扱うため、ネイティブファイルディスクリプタをURLで表現する等のプロトコル工夫、非同期コンポジタ実装による遅いクライアント切り離しなどを導入。
- レンダリング実装：各アプリのサーフェスをHTML5 canvasではなくWebGLテクスチャへ移行（canvasのダブルバッファ問題回避）。さらにブラウザ内ネイティブ描画を目指してSkiaをWASMへ移植。
- UIフレームワーク：WebWorker上で動くアプリ向けに、オフスクリーンWebGLへ出力するカスタムReactレンダラを作成。公式ドキュメント不足で苦労しつつも基盤を確立。
- X11（Xwayland）対応：多くのLinuxアプリはまだX11依存。ブラウザをX11クライアントとして振る舞わせるため、TypeScriptでXプロトコル束（xtsb）を実装し、Wayland上でXウィンドウ管理を再現。
- 運用とスケール：ユーザー側のセットアップ複雑さを解消するため、Kubernetesオペレータを作り、アプリ用コンテナとともにコンポジタプロキシをサイドカーで配備。クラスタ全体へデスクトップアプリを分散配備できるようにした。
- 実用性：プロトタイプで1080p@30fpsが可能になるなど性能面も一定の成果を出す一方、非同期Waylandコンポジタ実装やウィジェットライブラリ不足など実装コストは高い。

## 実践ポイント
- メタデータ付きフレームが必要なら、単純なWebRTCビデオではなく「データチャネル＋別経路でフレーム」を検討する（あるいはWebSocketへ切替）。
- クライアント側デコードはWASMのTinyH264などで現実的（1080p@30fpsレベルが可能）。
- 高速で安定したGUIはWebGLテクスチャ管理とダブルバッファを前提に設計する（canvasは注意）。
- X11互換が必要なら、既存Cライブラリをそのまま持ち込めない環境でのプロトコル移植が現実解になる（TypeScriptバインディングの自作）。
- 運用面はKubernetesオペレータ＋サイドカー構成が有効。日本の企業での集中管理・権限制御に向く。

興味があれば、Greenfieldのアプローチ（WASMでのデコード、Skia移植、WebGLレンダラ、k8sオペレータ）を小さなPoCで順に試すのが学習効率が良いです。
