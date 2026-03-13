---
layout: post
title: "TUI Studio – visual terminal UI design tool - TUI Studio — ターミナルUIをビジュアルに設計するツール"
date: 2026-03-13T12:26:55.850Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://tui.studio/"
source_title: "TUIStudio — Design Terminal UIs. Visually."
source_id: 47362613
excerpt: "Figma感覚でターミナルUIを作り、リアルタイムプレビューで複数フレームワークへ出力可能"
---

# TUI Studio – visual terminal UI design tool - TUI Studio — ターミナルUIをビジュアルに設計するツール
ターミナルアプリをFigma感覚で作れる新ツール──コマンドラインUIの設計がぐっと身近に

## 要約
TUI Studioは、ドラッグ＆ドロップでターミナルUI（TUI）を視覚的に設計できるエディタ。デザインを保存して複数のTUIフレームワーク向けコードにエクスポートすることを目指すアルファ版です。

## この記事を読むべき理由
ターミナルベースのツールはサーバ運用や開発者向けユーティリティで根強い需要があります。コーディングでレイアウトを調整する負担を減らし、デザイナー／エンジニア間の協業を容易にする可能性があるため、日本の開発現場でも注目すべきツールです。

## 詳細解説
- ビジュアルキャンバス：リアルタイムANSIプレビューを備え、ズームやライブ表示で見たまま編集可能。Figmaライクな操作感を目指しています。  
- コンポーネント：スクリーン、ボックス、ボタン、テキスト入力、テーブル、リスト、ツリー、タブ、モーダル、スピナー、プログレスバー等、21種類以上を搭載。  
- レイアウトエンジン：Absolute / Flexbox / Grid のモードを提供し、ブラウザのCSSに似たプロパティ制御で細かい配置が可能。  
- カラーテーマ：Dracula、Nord、Solarizedなど8テーマをキャンバスに即時反映。  
- マルチフレームワークエクスポート：Ink(TypeScript/React)、BubbleTea(Go)、Blessed(Node)、Textual(Python)、OpenTUI(TypeScript)、Tview(Go)向けの生成を想定（※現状エクスポート機能はアルファで未完成）。  
- プロジェクト管理：.tui 形式のJSONで保存・共有。アカウント不要でGit管理も容易。  
- プラットフォーム：Mac（Apple Silicon向けネイティブ）、Windows、Docker。macOSのGatekeeperやWindows SmartScreenに関する回避手順を案内（右クリック→開く、あるいはシステム設定の「Open Anyway」など）。  
- 注意点：現時点はアルファ。エクスポートは未稼働で、今後の開発状況を確認する必要があります。

## 実践ポイント
- とりあえず触る：Apple Silicon向けMac版をダウンロードしてUI設計を試し、.tuiファイルをGit管理してチームで共有する。  
- Gatekeeper対策：macOSで「未確認開発元」メッセージが出たら右クリック→開く、または設定の「Open Anyway」を実行。Windowsは「詳細情報→実行」を選択。  
- フレームワーク選定の目安：Goが強い現場はBubbleTea/Tview、Python慣れの現場はTextualを注視。エクスポート実装を見つつターゲットを決める。  
- コラボ活用：デザイナーがワイヤーを作り、エンジニアが.tuiを受け取って実装するワークフローを試すと効率化につながる。  
- 追跡：エクスポート機能やプロ版の有無は随時更新されるため、GitHubや公式ページをフォローして進捗を確認する。
