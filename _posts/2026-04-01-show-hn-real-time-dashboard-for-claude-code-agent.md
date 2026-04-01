---
layout: post
title: "Show HN: Real-time dashboard for Claude Code agent teams - Claude Codeエージェントチーム向けリアルタイムダッシュボード"
date: 2026-04-01T17:19:46.883Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/simple10/agents-observe"
source_title: "GitHub - simple10/agents-observe: Real-time observability of claude code sessions &amp; multi-agents. · GitHub"
source_id: 47602986
excerpt: "Claude Code用の実行イベントを可視化しデバッグを即支援するリアルタイムダッシュボード"
image: "https://opengraph.githubassets.com/d5775ec536e9a7094a03c708e8ab933e1156dea31c95e4d84f9a5232c718b60a/simple10/agents-observe"
---

# Show HN: Real-time dashboard for Claude Code agent teams - Claude Codeエージェントチーム向けリアルタイムダッシュボード
AIエージェントの「何をしているか」が一目で分かる——Claude Code用リアルタイム観測ダッシュボード

## 要約
Claude Codeのマルチエージェント実行をフックで捕捉し、ツール呼び出し・サブエージェント階層・イベントペイロードをSQLiteとWebSocket経由でリアルタイム表示するOSSダッシュボードです。

## この記事を読むべき理由
日本でもAIアシスタントが自動でコード生成・テスト・ドキュメント作成を行う場面が増えています。動作がブラックボックス化したときのデバッグ・監査・運用コストを下げたい開発チームやSREに直結するツールです。

## 詳細解説
- 全体像：Claude Codeの各種イベント（ツール呼び出し、プロンプト、サブエージェントの生成/停止など）をフックで拾い、ローカルのhookスクリプトがイベントをHTTP POSTでサーバへ送信。サーバは構造化してSQLiteに保存し、WebSocketでReactダッシュボードへストリーミングする設計です。
- フック方式の利点：OTELのような汎用トレーシングよりも「生のイベント（コマンド、ファイル操作、grepパターン等）」をそのまま扱えるため、何が実際に実行されたかが確実に把握できます。
- ダッシュボード機能：ツール呼び出しのPreToolUse→PostToolUseをマージ表示、エージェント階層の可視化、フィルタ／全文検索、イベント展開でフルペイロード表示、タイムラインジャンプ、セッションの履歴参照（人間に読みやすいスラッグを付与）など。
- アーキテクチャ：hook → observe_cli.mjs → APIサーバ（Hono、SQLite）→ Reactクライアント（WebSocket）。サーバは「データのストア兼配信」を担当し、クライアント側で状態を派生させます。
- 導入：Docker必須（サーバはコンテナで動作）。claude plugin marketplace経由でのインストールが簡単。ローカル運用ならリポジトリをクローンしてjustコマンドでセットアップ可能。主要コマンド例：just setup-hooks <project>、just start、just test-event、/observe スキルで状態確認。
- 運用で注意すべき点：ポート4981の競合、Dockerデーモンの稼働、AGENTS_OBSERVE_PROJECT_SLUGの設定、WebSocket切断時の自動再接続などがドキュメントに明記されています。

## 実践ポイント
- まず試す：Dockerを起動し claude plugin marketplace add simple10/agents-observe → claude plugin install agents-observe → Claude Codeを再起動。http://localhost:4981 を開いて動作確認。
- フック設定：just setup-hooks my-project で生成される設定を .claude/settings.json に貼る。サーバ到達性は just test-event でチェック。
- デバッグ時はツール呼び出しのPre/Postを追う：出力だけでなく実際のコマンドやファイル編集を見れば「何が本当に起きたか」が分かる。
- 日本のチーム向け運用案：CI内でエージェントが行う自動テスト/コード修正のセッションを保存してパターン分析（よく失敗するツールやコマンド）を抽出し、ルール化・ガードレールを作る。
- トラブルシュートの基本：ポート詰まりは docker stop agents-observe && docker rm agents-observe、DB問題は just db-reset、コンテナログは docker logs agents-observe で確認。

この記事は、Claude Codeなどのエージェントワークフローを導入・拡大する際に「何が起きているか」を短時間で把握し、信頼性と安全性を高めたい日本の現場にすぐ役立つ内容です。興味があればリポジトリ（simple10/agents-observe）をチェックして、ローカルで試してみてください。
