---
layout: post
title: "I hate: Programming Wayland applications - Waylandアプリ開発が嫌いだ"
date: 2026-03-22T16:54:54.726Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.p4m.dev/posts/29/index.html"
source_title: "I Hate: Programming Wayland Applications"
source_id: 47478298
excerpt: "Waylandではただウィンドウを開くだけで膨大な実装工数と罠を招く理由と回避法を解説"
---

# I hate: Programming Wayland applications - Waylandアプリ開発が嫌いだ
Waylandで「ただウィンドウを開くだけ」が地獄に感じられる理由 — 開発者が教える実態と対処法

## 要約
Waylandはユーザー体験で利点がある一方、低レイヤーで直接扱うとコールバック多発・拡張の断片化・初期化の脆弱性などで「シンプルなアプリ」が非常に作りにくい、という現場の苦言。

## この記事を読むべき理由
近年の主要LinuxデスクトップはWaylandへ移行中で、国内開発者や組み込み／マルチディスプレイ環境で動くアプリを作るなら、Wayland特有の落とし穴を知っておかないと時間を大幅に浪費するため。

## 詳細解説
- X11 vs Wayland: X11はクライアント／サーバモデルの名残でイベントループ中心だが、Waylandはプロトコル的にオブジェクト指向で「グローバル（registry）→コールバック」で状態を受け取る設計。制御フローが分散し予測しづらい。
- 初期化の複雑さ: wl_display_roundtrip()/wl_display_dispatch()でコールバックを駆動しつつ、WlCompositor/WlShm/XdgShellなどのグローバルを取得。OpenGLやソフトウェアレンダリングで必要なバッファ／共有メモリの手順が多く、ミスると無限待ちや無描画状態になりやすい。
- 拡張と断片化: XdgShell、Wlr Layer Shell、xdg-desktop-portalなど多様な拡張があり、仕様はXMLから生成（wayland-scanner）されるため実装・配布位置（例: /usr/share/wayland-protocols）が環境依存になりやすい。
- 入力・表示周りの面倒: キーボードはxkb経由で変換・リピート処理を自前で作る必要がある。モニタ位置やリフレッシュレート情報が統一されておらず、プラグ＆プレイやホットプラグの挙動もコンポジタ依存で不安定。
- 実用的な不都合: クリップボードやスクリーン共有はxdg-desktop-portal経由で実装がばらつく。デバイス（ペン・タブレット）ホットプラグ検出や特定のカーソル種別の列挙も手間がかかる。
- 参考と現実: Wayland.appなどの資料は有用だが、結局「ただ空のウィンドウを出す」だけでも数百〜千行に相当するラッパー実装が必要になることがある。

## 日本市場との関連性
- 多くの日本企業や開発者が使うUbuntu/Fedoraや、軽量環境で人気のsway（Waylandベース）はWayland運用が増加中。ノートPCやタブレット（日本で普及するモバイル端末）での入力装置・高DPI対応・複数ディスプレイ対応は、Wayland特有の扱いを要求する。
- OBSやペンタブ操作など、クリエイティブ領域のツールはWayland移行で実動作に問題が出る例が報告されており、社内ツールや業務アプリをWayland対応させる際のコスト見積もりが重要になる。

## 実践ポイント
- まずは高レベルなライブラリ（SDL、GLFW、raylib、GTK/Qt）を使い、可能ならWaylandの生APIは避ける。  
- スクリーン共有やクリップボードは各ディストリのxdg-desktop-portal実装を確認し、wl-clipboard等の既存ツールで回避策を用意する。  
- 複数コンポジタ（sway/GNOME/KDE）で実動作テストを行い、拡張の有無による分岐を実装する。  
- EGL周りやホットプラグはブロッキングを考慮したフェイルセーフ（タイムアウト・再初期化）を入れる。  
- 必要ならwayland-protocols配布場所やwayland-scanner生成物をパッケージ依存として明示し、開発ドキュメントにまとめる。

（原著: "I hate: Programming Wayland applications" — Felix' Ramblings）
