---
layout: post
title: "McCLIM and 7GUIs - Part 1: The Counter - McCLIMと7GUIs 第1回：カウンター"
date: 2026-01-26T15:13:36.605Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://turtleware.eu/posts/McCLIM-and-7GUIs---Part-1-The-Counter.html"
source_title: "TurtleWare"
source_id: 1043389620
excerpt: "GadgetsとPresentationsで作るMcCLIMカウンターの利点と移行手順を実例で解説"
---

# McCLIM and 7GUIs - Part 1: The Counter - McCLIMと7GUIs 第1回：カウンター
CLIM入門：たった数行で作る「クリックで増えるボタン」を Gadgets と Command Loop で比べる

## 要約
McCLIM を使って 7GUIs の最初の課題「カウンター」を2通り（Gadgets＋Layouts と Command Loop＋Presentations）で実装し、各手法の仕組みと利点を示す記事です。

## この記事を読むべき理由
GUI 実装の基本概念（イベント駆動のガジェット vs. コマンドループと提示表現）を、実用的なサンプルで比較できるため。日本の組込み系や業務アプリ開発でも、簡潔で再利用性の高い UI 設計は重要です —— 小さなカウンターから学べる設計知識はそのまま応用できます。

## 詳細解説
- 共通の土台：パッケージ作成と McCLIM の読み込み（ql:quickload "mcclim"）で始め、define-application-frame でアプリの枠組みを定義する点は両アプローチ共通。
- Version 1（Gadgets＋Layouts）:
  - :panes でラベルやボタンといった「ガジェット」を名前付きで定義し、:layouts で配置。
  - ボタンの :activate-callback によりクリックで即座にモデル（フレームの slot）を更新し、ラベルの表示を差し替える。イベント→即時描画の流れが直感的。
  - 利点：簡単にプロトタイプ化でき、少ないコードで動く。UI の外観調整（spacing, bordering）もレイアウトで行える。
- Version 2（Command Loop＋Presentations）:
  - 単一または複数のストリーム（pane）上で表示とコマンド表を使う。表示は display-function によって再描画される。
  - define-presentation-type で「意味を持つ出力（例：counter-button）」を定義し、define-presentation-to-command-translator でその出力への操作（クリックやスクロール）を特定のコマンドへ翻訳する。
  - プレゼンテーションは「見た目」と「意味」を結びつけ、同じ表示がマウス操作、メニュー、ショートカットで同一コマンドに結びつくため拡張性が高い。
  - 独自ジェスチャ（スクロールで増減）やヘルプ用アクション（describe）も自然に追加できる。
- 比較まとめ：
  - Gadgets：素早いプロトタイプ、直感的なイベント処理。
  - Presentations/Commands：意味的に豊かで再利用・拡張しやすい。大規模アプリや独自 UI メタファーに向く。

## 実践ポイント
- まずは Gadgets で素早く動くプロトタイプを作る（define-application-frame の :panes と :layouts を活用）。
- プロトタイプが固まったら Presentations に移行し、ユーザー操作をコマンドにまとめると拡張が楽になる。
- プレゼンテーションを使えば、同じ「表示」をメニューやジェスチャに簡単に結びつけられる（define-presentation-to-command-translator を活用）。
- 開発環境：Quicklisp で mcclim をロード、CLIM-EXTENSIONS は McCLIM 固有の拡張として意識する。
- 日本語対応：表示文字列やフォーマットは CLIM の表示関数で簡単にローカライズ可能。業務アプリ向けにはプレゼンテーションで意味付けしておくと多言語対応が楽。

以上を踏まえ、まずは短い counter-v1 を動かし、次に counter-v2 のプレゼンテーションで拡張性を体感してみてください。
