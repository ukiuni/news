---
layout: post
title: "Humans can post on Moltbook without any agent - Moltbookにエージェントなしで投稿できる"
date: 2026-01-31T22:28:31.983Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/shash42/post-a-molt"
source_title: "GitHub - shash42/post-a-molt"
source_id: 46840636
excerpt: "エージェント不要でPythonスクリプトでMoltbookへ即投稿できる方法"
image: "https://opengraph.githubassets.com/91f36e592020ce3fa986c0ff6a336207fac5dcbfe76a662c74b877300772d61a/shash42/post-a-molt"
---

# Humans can post on Moltbook without any agent - Moltbookにエージェントなしで投稿できる
Moltbookへ“手軽に”直接投稿する方法 — 面倒なラッパーなしで始めるローカル開発者向けガイド

## 要約
GitHubのリポジトリは、Moltbookの公開REST APIを直接叩いて投稿・コメント・いいね・ステータス確認を行うPythonスクリプト群を提供します。エージェントラッパー不要で、個人のスクリプトや自動化に組み込みやすいのが特徴です。

## この記事を読むべき理由
Moltbookのような新興プラットフォームへ、安全かつ簡単に投稿を自動化したい日本の開発者やコミュニティ運営者にとって、最小限の手順でAPIを使う方法を知ることは実用的価値が高いからです。

## 詳細解説
- 構成：リポジトリには投稿（moltbook_post.py）、コメント（moltbook_comment.py）、アップボート（moltbook_upvote.py）、ステータス確認（moltbook_status.py）などのスクリプトが入っています。すべてPythonで動作します。
- APIキー取得：まず1回だけエージェント登録APIに対してPOSTし、api_keyを受け取ります。参考コマンド：
```bash
curl -X POST https://www.moltbook.com/api/v1/agents/register \
  -H "Content-Type: application/json" \
  -d '{"name": "YourAgentName", "description": "What you do"}'
```
- 認証情報の保存：推奨される保存場所は ~/.config/moltbook/credentials.json です。例：
```json
{
  "api_key": "moltbook_xxx",
  "agent_name": "YourAgentName"
}
```
- 使い方の例：サブモルト（submolt）を指定して投稿、コメント、いいね、ステータス確認が可能です。
```bash
python3 scripts/moltbook_post.py --submolt general --title "Hello Moltbook" --content "My first post!"
python3 scripts/moltbook_comment.py --post-id POST_ID --content "Great insight!"
python3 scripts/moltbook_upvote.py --post-id POST_ID
python3 scripts/moltbook_status.py
```
- 実運用注意点：サーバー負荷により一時的なエラーが返ることがあるため、失敗時はリトライが必要です。またAPIキーは必ず https://www.moltbook.com/api/v1/* 宛のみ送るようにし、裸のドメインや別ホストへ送らないでください。

## 実践ポイント
- まず登録してAPIキーを取得し、ローカルのcredentials.jsonに保存する。  
- スクリプトを手元で試し、500系やタイムアウトが出たら指数バックオフでリトライを実装する。  
- CIやBotに組み込む場合はシークレット管理（環境変数やシークレットストア）を使い、キーを直接リポジトリに置かない。  
- 日本語コミュニティ向けのサブモルトがあれば --submolt を指定してローカライズ投稿を試す。  
- 必要に応じてスクリプトをフォークして独自の投稿テンプレートやメタデータ送信機能を追加する。

元記事リポジトリ（参考）：https://github.com/shash42/post-a-molt
