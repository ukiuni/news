---
layout: post
title: "A Supabase misconfiguration exposed every API key on Moltbook's 770K-agent platform. Two SQL statements would have prevented it - Supabaseの設定ミスでMoltbookの770Kエージェントが全APIキー流出。2つのSQLで防げた"
date: 2026-02-02T18:04:08.098Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.telos-ai.org/blog/moltbook-security-nightmare"
source_title: "Moltbook Is Becoming a Security Nightmare - Telos Blog"
source_id: 412253681
excerpt: "Moltbookのミスで770Kのエージェントから全APIキー流出—2つのSQLで防げた"
---

# A Supabase misconfiguration exposed every API key on Moltbook's 770K-agent platform. Two SQL statements would have prevented it - Supabaseの設定ミスでMoltbookの770Kエージェントが全APIキー流出。2つのSQLで防げた

魅力的なタイトル: 「あなたのマシンが“エージェント”に乗っ取られるかも？Moltbook流出事件の教訓と今すぐできる対策」

## 要約
Moltbookとその基盤フレームワークOpenClaw（Moltbot）の設計・設定ミスで、エージェントが大量に特権アクセスを持ち、公開データベース（Supabase等）の誤設定によりAPIキーやセッション情報が流出した。簡単なアクセス制御で防げた可能性が高い。

## この記事を読むべき理由
日本でも個人/企業がエージェントやBotを導入する流れが急拡大中。権限設計やデータベース設定ミスは日本のプロダクトでも同様に致命傷になり得るため、具体的対策を今すぐ確認すべきです。

## 詳細解説
- 事象の要点：Moltbookはエージェント同士の投稿で成長し、数十万〜77万超のアクティブエージェントが稼働。エージェントはユーザー端末上でシェル実行やファイル参照、外部APIキー利用など高権限で動く。
- 根本的な問題：
  - エージェント側の「exec」機能が入力をそのままシェル実行し、サニタイズが不十分（コマンド/プロンプトインジェクション）。
  - 管理ダッシュボードやAPIが誤ってパブリック公開されていた（Gateway misconfiguration）。
  - エージェントがユーザー権限で動き、サンドボックス化されていない（過剰権限）。
  - APIキーやセッション情報が平文でアクセス可能な場所に保存されていた（平文保存）。
- 被害例と規模：Shodan/ZoomEyeで4,500超のインスタンス露出、.envやcreds.jsonからClaude/OpenAIキー、WhatsAppセッション、Slack/Discordトークン等が抜き出された報告。Simulaの分析では投稿の数％にプロンプトインジェクションが含まれ、プラットフォームの運用が秩序を失った。
- 悪用される経路：公開DB/APIへの直接クエリ、ダイレクトメッセージに仕込まれたプロンプト、ランキング操作で広められた悪質スキル（プラグイン）など。

## 実践ポイント
- 緊急対応（今すぐやる）
  - すべてのAPIキーとOAuthトークンをローテートする。
  - 連携中のメッセージセッション（WhatsApp/Telegram/Slack/Discord/Teams等）から強制ログアウトする。
  - マシンを潜在的に侵害済みと見なし、不審プロセスや新規ユーザー、改変されたファイルを確認する。
- 開発・運用での必須対策
  - エージェントに与える権限を最小化（最小権限の原則）し、可能ならサンドボックス/コンテナで分離する。
  - 入力のサニタイズとプロンプト検査を実装し、外部からのコマンド直渡しを禁止する。
  - 管理ダッシュボードや内部APIはパブリックに公開しない（IP制限、認証強制）。
  - 機密情報は暗号化して保存し、アクセス監査ログを有効化する。
- Supabase向けの即効対策例（公開テーブルに対する最小限の制限）
  - Row Level Security（RLS）を有効化して匿名アクセスを防ぐ：
  
  ```sql
  -- sql
  ALTER TABLE public.api_keys ENABLE ROW LEVEL SECURITY;
  REVOKE ALL ON TABLE public.api_keys FROM anon, public;
  ```
  
  （補足）運用に合わせて適切なポリシーを追加し、認証済みユーザーのみアクセス許可するポリシーを作ること。

- 組織対応
  - エージェントプラットフォームの採用は、セキュリティガイドラインと承認プロセスを通す。Cisco等の勧告に従い、必要なガードレールが整うまでブロックする選択肢も検討する。

簡潔に言えば、「エージェント＝コード実行の入口」を軽く見ないこと。設定一つと権限設計で被害を大幅に減らせます。
