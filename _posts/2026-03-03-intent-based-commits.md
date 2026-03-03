---
layout: post
title: "Intent-Based Commits - 意図ベースのコミット"
date: 2026-03-03T05:34:42.062Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/adamveld12/ghost"
source_title: "GitHub - adamveld12/ghost: Git is the coding agent"
source_id: 47227999
excerpt: "GhostでAIプロンプトをコミットし、生成意図を設計履歴として残す新ワークフロー"
image: "https://opengraph.githubassets.com/fc99532efd6ba41bd770e2cd5547d7e85509721af86d56f2bd62199941f418a0/adamveld12/ghost"
---

# Intent-Based Commits - 意図ベースのコミット
魅力的な日本語タイトル: 「コードではなく“意図”を残す――AIが生成した変更を設計書のように辿る新しいgitワークフロー」

## 要約
Ghostは「コードを直接コミットする」のではなく「プロンプト（意図）をコミットする」CLI。AIエージェントがプロンプトからコードを生成し、生成前後を差分取得して変更だけをステージ、補強されたコミットメッセージに意図とメタ情報を残す。

## この記事を読むべき理由
将来の保守や設計判断の追跡に悩む日本のチームにとって、コミット履歴を“なぜ”の履歴に変える手法は有益。リモート開発やドキュメント不足のプロジェクトでも、決定理由をそのまま履歴に保存できる点が国内の実務でも価値を持ちます。

## 詳細解説
- 基本概念：従来は「何が変わったか」をgit履歴で見るが、Ghostは「何をさせようとしたか（意図）」を保存する。各コミットはプロンプト＋AI出力＋メタデータの組。
- ワークフロー（要点）：
  1. コマンド例：ghost commit -m "add user auth with JWT"
  2. エージェントがプロンプトからコードを生成し、作業ツリーに書き込み
  3. Ghostが生成前後のスナップショットを取り、差分だけをステージ
  4. git commit を行い、コミット本文にプロンプトやエージェント情報などを埋め込む
- サポートするエージェント：claude / gemini / codex / opencode。コミット毎にエージェントやモデルを切替可能。
- コミットメッセージに含まれる主なフィールド例：
  - ghost-prompt（実際の指示）
  - ghost-agent / ghost-model（生成に使ったエージェントとモデル）
  - ghost-session（生成セッションUUID）
  - ghost-files（生成・変更されたファイル一覧）
- コマンドの主要オプション：
  - ghost init / ghost commit -m "…" / --agent / --model / --dry-run / ghost log
  - 環境変数：GHOST_AGENT, GHOST_MODEL, GHOST_SKIP（通常のgitにバイパス）
- 要件：git, bash, uuidgen, 各エージェント用のCLIが環境にインストールされていること。
- 利点と注意点：
  - 利点：意図の保存により将来の判断理由が明確、再現性（同じプロンプトで再生成可能）、ログが設計文書化。
  - 注意：モデルのアップデートで再生成結果が変わる可能性、生成コードのセキュリティ／ライセンス確認が必要。

コード例（実行イメージ）:
```bash
# bash
git clone <repo>
export PATH="/path/to/ghost/bin:$PATH"
cd your-project
ghost init
ghost commit -m "create a REST API endpoint for user registration"
```

## 実践ポイント
- まずはサンドボックスリポジトリで --dry-run を試し、差分と生成物を確認する。
- チームルールで「生成コードは必ずコードレビュー」を義務化し、セキュリティとライセンスをチェックする。
- GHOST_AGENT / GHOST_MODEL をCIやローカルの環境変数で統一し、再現性を高める。
- 日本語プロンプトを使う場合は、モデルの日本語対応度を事前に評価する。
- 長期保存用にプロンプトを別途バックアップ（例：内部ドキュメントや秘匿ストレージ）すると監査やコンプライアンスに有利。
