---
layout: post
title: "Nanobot: Ultra-Lightweight Alternative to OpenClaw - Nanobot：超軽量クロー・ドボット代替"
date: 2026-02-05T11:50:05.855Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/HKUDS/nanobot"
source_title: "GitHub - HKUDS/nanobot: &quot;🐈 nanobot: The Ultra-Lightweight Clawdbot&quot;"
source_id: 46897737
excerpt: "約4,000行でローカル稼働する超軽量AI助手を即構築できる実践ガイド"
image: "https://opengraph.githubassets.com/6cb5515b8ec4e91b9f2a814d1b1b81b4a96ab6546ec4536447d5ecab72c3accd/HKUDS/nanobot"
---

# Nanobot: Ultra-Lightweight Alternative to OpenClaw - Nanobot：超軽量クロー・ドボット代替
驚くほど小さくて速い「自分専用AIアシスタント」を今すぐローカルで動かす方法

## 要約
nanobotはClawdbotのコア機能をわずか約4,000行で実装した超軽量パーソナルAIアシスタント。研究・学習用途に最適で、ローカルLLMやTelegram/WhatsApp/Feishu連携、Docker対応など実用的な機能を備えます。

## この記事を読むべき理由
コード量が極めて少ないため、AIエージェントの仕組みを短時間で学べる。日本のスタートアップや研究者がローカル運用や低コスト運用で試作・検証するのに向く実装です。

## 詳細解説
- コード規模と目的：コアは約4,000行（Clawdbotの数十万行に対して99%小さい）で、可読性を重視。研究・拡張・改造がしやすい設計。
- 主要機能：LLMプロバイダ対応（OpenRouter等）、ローカルモデル(vLLM)対応、永続メモリ、ツール実行ループ、スキルプラグイン、チャネル（Telegram/WhatsApp/Feishu）、定期タスク（cron）、Dockerコンテナ化。
- アーキテクチャ概要：agent（ループ・コンテキスト・メモリ・スキル）、providers（LLM接続）、channels（各種チャット連携）、cron/heartbeat（スケジューラ／常駐）などモジュール分割で学びやすい。
- ローカル運用：vLLMサーバに接続して完全ローカルで動かせる（apiKeyはダミー可）。モデル例：meta-llama/Llama-3.1-8B-Instruct。
- チャネル連携：Telegramはトークンで簡単、WhatsAppはQRスキャンとNode.js要件、Feishuはロングコネクションで公開IP不要。将来的にDiscord/Slack等の統合も計画。
- 配布と導入：pip/uv/PyPIのいずれでも導入可能。Dockerイメージで設定ディレクトリをマウントすれば永続化・運用が容易。

## 実践ポイント
- 2分で動かす（開発版推奨）：
  1. git clone https://github.com/HKUDS/nanobot.git && cd nanobot
  2. pip install -e .
  3. nanobot onboard → ~/.nanobot/config.json にAPIキーやモデルを設定
  4. nanobot agent -m "Hello!"
- ローカルLLMで運用する場合：vllm serve を起動し、configで apiBase をローカルに向ける（apiKeyは任意文字列で可）。
- Telegram連携は最も簡単：@BotFatherでトークン取得→configに設定→nanobot gateway。
- Docker運用のコツ：docker run -v ~/.nanobot:/root/.nanobot で設定をホストにマウントし、APIキー流出に注意する。
- 学習用途：小さなコードベースを読み進めれば、LLM↔ツールのループやメモリの扱いが実務レベルで理解できる。日本語化・日本語モデルへの差し替えも容易。
- セキュリティ留意点：APIキー管理、チャネルのアクセス制限（allowFrom）を設定すること。

興味があるなら、まずリポジトリをクローンしてREADMEのQuick Startを試し、プロジェクト構造（agent/, providers/, channels/）を追ってみてください。
