---
layout: post
title: "Pi – a minimal terminal coding harness - Pi（最小限のターミナル・コーディングハーネス）"
date: 2026-02-24T23:35:48.823Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://pi.dev"
source_title: "pi.dev"
source_id: 47143754
excerpt: "ターミナルで自己ホスト可能な最小限AIコーディング基盤、拡張で実務向けワークフロー構築"
image: "https://pi.dev/social.png"
---

# Pi – a minimal terminal coding harness - Pi（最小限のターミナル・コーディングハーネス）
ターミナルで自分だけのAIコーディング助手を組み立てる—「最小限×拡張性」で作る開発体験

## 要約
Piはターミナル中心の最小限コアに、TypeScript拡張・スキル・プロンプトテンプレート・テーマを自由に組み合わせて自分仕様に拡張できる「コーディング用ハーネス」です。多数のモデルプロバイダを切り替えつつ、ツリー構造のセッションやコンテキスト制御で実用的なワークフローを作れます。

## この記事を読むべき理由
日本の開発現場はターミナル／CLI文化が根強く、社内ポリシーやオンプレ環境での運用が重要です。PiはTUIベースで自己ホストやnpm経由の配布に向き、既存のツールチェーン（tmux、CI、Gitフロー等）に馴染むため、実務で試す価値が高いです。

## 詳細解説
- コア設計：Piは「機能は最小、拡張は自由」を掲げるハーネス。サブエージェントやプランモード等の肥大化機能はコアに持たず、必要なら拡張（TypeScript）で追加する設計。
- 拡張要素：
  - Extensions（TypeScript）：ツール、コマンド、ショートカット、イベント、TUIへアクセス可能。権限フローやSSH実行、カスタムエディタなどを自作できる。
  - Skills：機能パッケージ（オンデマンド読み込み）でプロンプトキャッシュを壊さず段階的に機能追加。
  - Prompt templates：Markdownで再利用可能なプロンプトを定義。簡単に呼び出せる。
- モデル／プロバイダ：Anthropic、OpenAI、Google、Azure、Bedrock、Mistral、Groq、Hugging Faceなど多数をサポート。APIキーやOAuthで認証し、セッション中にモデル切替（/model または Ctrl+L）。
- セッションとコンテキスト：
  - セッションはツリー構造で履歴を分岐保存。/treeで任意の分岐に戻れる。
  - 領域が逼迫すると過去メッセージを自動要約（compaction）してコンテキスト節約。カスタム要約やトピック単位集約も拡張で実装可能。
  - プロジェクト単位で AGENTS.md / SYSTEM.md を読み込めるため、リポジトリ単位の指示やシステムプロンプトを管理可能。
- 入力キューと操作感：Enterで「現在のツール後に割り込むステアリング」、Alt+Enterで「フォローアップ（処理完了後に追加）」という明瞭な操作モデル。
- 実行モード：TUIのインタラクティブ、スクリプト向けのprint/JSON（pi -p "..." / --mode json）、stdin/stdoutベースのRPC、SDK埋め込みの4モードを提供。
- パッケージ配布：extension/skill/prompt/themeをnpmまたはgitでパッケージ化。pi install で追加・pi update/pi listで管理。コミュニティで共有可能。

実例コマンド（まず試す最小セット）：

```bash
# グローバルCLI（例）
npm install -g @mariozechner/pi-coding-agent

# パッケージのインストール
pi install npm:@foo/pi-tools
pi install git:github.com/badlogic/pi-doom

# スクリプト実行例
pi -p "generate a TypeScript function to parse CSV" --mode json
```

## 実践ポイント
- まずローカルで動かしてみる：APIキーだけで多数モデルを切り替えられるため、手持ちの環境でレスポンスや料金を比較する。
- プロジェクト単位のSYSTEM.md/AGENTS.mdを作成：チームのコーディング指針や安全ルールをリポジトリに置けば常に読み込まれる。
- 小さな拡張から始める：まずはPrompt templateや簡単なSkillを作り、慣れたらTypeScriptでツール連携を追加。npmで配布すれば社内共有が楽。
- CIや自動化への応用：--mode json や RPC を使い、既存のCIやテストパイプラインに組み込むと効果的。
- セキュリティ運用を計画する：企業環境ではプロバイダ選択やAPIキー管理、コンテナ実行（権限制限）を合わせて設計する。

Piは「全部入りのAIエージェント」ではなく「自分で作り伸ばすための堅牢な土台」を選びたい現場に適したツールです。日本のチームで安全かつ効率的にAI支援を導入する第一歩として試す価値があります。
