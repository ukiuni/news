---
layout: post
title: "I built a free Chrome extension to track Claude usage & export chats (now supports Claude Code!) - 無料のChrome拡張を作りました：Claudeの使用量を追跡しチャットをエクスポート（Claude for Code対応）"
date: 2026-02-17T01:55:28.657Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://chromewebstore.google.com/detail/madhogacekcffodccklcahghccobigof"
source_title: "Claude Usage Tracker &amp; Chat Exporter - Chrome Web Store"
source_id: 439820675
excerpt: "無料Chrome拡張でClaudeの使用量を可視化、対話をMarkdown保存"
image: "https://lh3.googleusercontent.com/tqu3TW4lZ8OZTil8FRsWl6OrqL2XA8ckgyZkCGUJsWdLBXGcnRWf7eKucxHJw1OLVPReXeMDeF_KF4ZMb0MLzE3CKg=s128-rj-sc0x00ffffff"
---

# I built a free Chrome extension to track Claude usage & export chats (now supports Claude Code!) - 無料のChrome拡張を作りました：Claudeの使用量を追跡しチャットをエクスポート（Claude for Code対応）

Claudeユーザー必携：使用量をリアルタイム可視化し、会話をMarkdownで瞬時に保存・新規チャットへ引き継げる軽量拡張。

## 要約
Claude.ai と Claude for Code の利用量（5時間セッション・週次制限など）をブラウザ内でリアルタイム表示し、会話を選んでMarkdownでエクスポート、ワンクリックで新規チャットへ貼り付けられるChrome拡張（無料・オープンソース）。

## この記事を読むべき理由
Claudeを業務や開発で使う日本のエンジニア／UX担当者は、セッションやAPI制限で作業が途切れがち。使い過ぎを未然に防ぎ、重要な対話を失わず次セッションへ移行できる実践的なツールです。

## 詳細解説
- 主な機能
  - リアルタイム利用量トラッキング：5時間セッション、週次の全モデル合算、週次Opusなどの制限をclaude.aiとClaude for Code両方で監視。
  - 統合サイドバー：Claudeの画面内に直接使用状況が表示されるため別タブ不要。
  - スマートエクスポート：会話を20％／50％／100％など任意の割合でMarkdown出力可能。
  - ワンクリックワークフロー：Export → Download → New chat → 自動ペーストを最短3秒で実行。
  - マルチプラットフォーム対応：ブラウザ版（claude.ai）とCLI版（Claude for Code）の両方で動作。
  - 適応UI：サイドバーの展開・折り畳み状態に追従。
- 利用シナリオ
  - 長時間の会話でコンテキスト制限に達しそうなときの保全。
  - CLIでの開発フロー（Claude for Code）でAPI使用量を監視したい開発者。
  - 重要なやり取りをMarkdownで社内ドキュメントに残すケース。
- プライバシーと実装
  - データ収集なし、外部サーバ経由しない（端末内で処理／Claude APIへ直接通信）。
  - オープンソースでコード確認可能。拡張は小容量（約46.5KiB）、公開バージョンは v1.1.9（更新日: 2026-02-11）。

## 実践ポイント
- 導入：Chromeに追加するだけでclaude.ai／Claude for Codeでサイドバーに表示される。
- 保存のコツ：長い会話はこまめに20〜50%で分割エクスポートしておくと、途中でコンテキストが切れても復元・再開が楽。
- 開発現場で：Claude for Code利用時は週次の合算使用量をチェックし、CIやコスト管理に組み込むと安心。
- セキュリティ確認：社内規定に合わせて拡張のオープンソースリポジトリ（プライバシーポリシー）を確認してから導入を。
