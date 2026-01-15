---
layout: post
title: "Show HN: OpenWork – an open-source alternative to Claude Cowork - Show HN: OpenWork — Claude Cowork のオープンソース代替"
date: 2026-01-15T21:17:23.556Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/different-ai/openwork"
source_title: "GitHub - different-ai/openwork: An open-source alternative to Claude Cowork, powered by OpenCode"
source_id: 46612494
excerpt: "ローカルで監査・権限管理可能なClaude風GUIで業務自動化を即導入"
image: "https://opengraph.githubassets.com/e9cd57c81897f0f830d2eb5a5a3caca4122cdb69e3e34c848d733f0569b1fd01/different-ai/openwork"
---

# Show HN: OpenWork – an open-source alternative to Claude Cowork - Show HN: OpenWork — Claude Cowork のオープンソース代替

CLI不要で「エージェント的な仕事」をデスクトップで使える——OpenWorkは知識労働者向けに設計されたオープンソースのワークフローアプリです。手元で動かせて権限管理・監査も可能なので、日本の企業や個人のプライバシー要件にもマッチします。

## 要約
OpenWorkはOpenCodeを裏で動かすネイティブデスクトップアプリで、ワークスペース選択→実行→進捗/許可管理→テンプレ再利用の流れをGUI化している。ローカル運用やリモート接続、プラグイン（スキル）管理、実行プラン・SSEのライブ更新などを備える。

## この記事を読むべき理由
- 日本の企業ではデータ国内保持や説明責任（監査・ログ）が重要。OpenWorkはローカルホスティングや許可ログ表示をサポートし、企業導入のハードルが低い。  
- CLIに慣れていない現場担当者でも使えるGUIがあるため、AIワークフローの実運用に着手しやすい。

## 詳細解説
- 基本コンセプト：OpenCode（エージェント基盤）をGUIで包み、「Claude Cowork風」のワークフロー体験を提供。目的は「端末や設定を学ばせるのではなく、プロダクトとして使えること」。
- 主な機能（v0.1）
  - Host mode：選んだフォルダでローカルに opencode serve を立てる。
  - Client mode：既存のOpenCodeサーバにURLで接続。
  - Sessions：セッション作成・選択・プロンプト送信。
  - ライブストリーミング：SSE（サーバ送信イベント）でリアルタイム更新を表示。
  - 実行プラン：OpenCodeのtodoをタイムラインで可視化。
  - パーミッション管理：権限要求を表示し、一回許可／常時許可／拒否が可能。
  - テンプレート＆スキル：よく使うワークフローを保存、.opencode/skill を管理。opkg（OpenPackage）経由でインストール可能。opkgが無ければ pnpm dlx で代替。
- アーキテクチャ（高レベル）
  - デスクトップはTauriで実装（クロスプラットフォーム）。Hostモードではローカルで opencode サーバをプロセス起動し、フロントエンドは @opencode-ai/sdk/v2/client を使って接続・SSE購読・todo読み出し等を行う。
- 必要環境と開発起動
  - Node.js、pnpm、Rustツールチェイン（Tauri用）、OpenCode CLI（opencode）が必要。
  - 開発/実行コマンド例：
```bash
# 依存を入れる
pnpm install

# デスクトップ開発用
pnpm dev

# Web UIのみ
pnpm dev:web

# ビルドや型チェックなど
pnpm typecheck
pnpm build:web
pnpm test:e2e
```
- セキュリティ設計
  - モデルの推論過程や敏感なツールメタデータはデフォルトで隠蔽。Hostモードはデフォルトで127.0.0.1にバインドして外部アクセスを防ぐ。ライセンスはMIT。

## 実践ポイント
- まずローカルで試す：企業のデータポリシーが厳しい場合はHost modeで起動し、127.0.0.1バインドを確認してから運用を検討する。
- テンプレート化で現場導入を早める：よくある作業（レポート作成、リサーチまとめ、メール下書きなど）をテンプレ化して非エンジニアにも配布すると効果が高い。
- スキル管理で拡張性を確保：共有したい自動化処理は .opencode/skill に入れてチームで管理。opkgで配布すれば再利用しやすい。
- 監査ログと権限フローを確認：権限要求の履歴や実行計画（timeline）を使って、出力理由や誰が許可したかを残す運用を作る。
- 日本語化・社内適用：UIやスキルの日本語化、既存社内システム（SaaSやオンプレDB）との接続スキルを用意すれば現場導入が進む。

興味があるなら公式リポジトリのリリースページからdmgを試すか、ソースからビルドしてローカルで動かしてみると実感が掴みやすい。GitHub上でスターやフォーク、ISSUEでの要望提出も歓迎されている。
