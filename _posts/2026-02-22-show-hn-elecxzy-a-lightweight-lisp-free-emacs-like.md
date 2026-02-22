---
layout: post
title: "Show HN: Elecxzy – A lightweight, Lisp-free Emacs-like editor in Electron - Elecxzy：Lisp非搭載の軽量Emacs風エディタ（Electron）"
date: 2026-02-22T11:24:56.595Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/kurouna/elecxzy"
source_title: "GitHub - kurouna/elecxzy: elecxzy project"
source_id: 47100328
excerpt: "Emacs操作感そのまま、Lisp不要で高速起動のElectron製エディタ"
image: "https://opengraph.githubassets.com/209033e51305b0c11ed2e6348a556490a1512230302c50905334f01f1284ead8/kurouna/elecxzy"
---

# Show HN: Elecxzy – A lightweight, Lisp-free Emacs-like editor in Electron - Elecxzy：Lisp非搭載の軽量Emacs風エディタ（Electron）
Emacsの操作感そのまま、設定ゼロで使える“軽量版Emacs”――迷わず試せる新鋭エディタ

## 要約
Electron＋Reactで再設計されたEmacs風テキストエディタ。Lispを廃し軽快さを優先、Emacsのキーバインドや分割画面、Piece Tableによる高速バッファ操作などを実装したアルファ版です。

## この記事を読むべき理由
Emacsのワークフローに慣れているが、重い初期設定やEmacs Lispに煩わされたくない日本の開発者やライターにとって、即戦力になり得る選択肢だからです。日本語IMEへの最適化やWindows向けバイナリ提供も日本ユーザーに優しい点です。

## 詳細解説
- 基本設計：Electron（Node.js）上にReact＋TypeScriptで独自レンダリングを構築。モダンUI（フローティングミニバッファ、ステルススクロールバー等）を採用。
- 操作体系：Emacs準拠のキーバインド（C-f/C-b/C-n/C-p/C-x 系列、M-x など）を提供し、再帰的なウィンドウ分割とEmacs風のリサイズコマンドをサポート。
- 軽量化方針：Emacs Lispエンジンを持たず、設定は最小限のデフォルトで即使用可能に。拡張性より「起動・操作の軽さ」と「メンテ性」を優先。
- バッファエンジン：Piece Table構造を用い、大ファイルの編集と無限に近いUndoを高速に実現。
- 言語サポート：TypeScript/JavaScript/C/C++/Python/Go/Rust/SQL/YAMLなどのメジャーモードとHighlight.jsによるシンタックスハイライト。Markdown/HTMLのリアルタイムプレビュー有。
- 日本語対応：IME挙動を最適化（C-\ または C-] でIME切替可能）、既知のフォント問題（MS ゴシック等）に対する推奨フォント（BIZ UDGothic）表示あり。
- 制約と現状：改良中のアルファ段階で不安定な機能あり。現時点で右端での自動折り返し（word wrap）は非対応。Windows用バイナリはリリースから入手可。ソースは一部非公開の旨記載あり。

## 実践ポイント
- まずはWindowsリリースを試す（アルファのためバックアップ推奨）。
- Emacs慣れしているならデフォルトのキーバインドですぐ使える：C-x 2/3で画面分割、M-xでコマンド実行。
- 日本語入力は C-\ / C-] で切替。表示がおかしい場合は推奨フォント（BIZ UDGothic等）を試すか M-x set-font / JSONで設定。
- 大きなファイル編集やUndoの挙動を確認して、Piece Tableの恩恵を体感する。
- 欲しい機能（折り返し、マウス水平スクロール挙動改善等）はGitHubのIssuesで報告・要望を出すと開発に反映されやすい。
