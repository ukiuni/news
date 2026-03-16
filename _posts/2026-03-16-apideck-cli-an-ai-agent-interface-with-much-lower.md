---
layout: post
title: "Apideck CLI – An AI-agent interface with much lower context consumption than MCP - あなたのMCPサーバーがコンテキストを食い潰している。もっとシンプルな方法"
date: 2026-03-16T17:52:58.090Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.apideck.com/blog/mcp-server-eating-context-window-cli-alternative"
source_title: "Your MCP Server Is Eating Your Context Window. There&#x27;s a Simpler Way"
source_id: 47400261
excerpt: "ApideckのCLIで初期プロンプト約80トークンに抑え、MCPのトークン爆食とコストを大幅削減"
image: "https://images.ctfassets.net/d6o5ai4eeewt/57kHNdJ8Hmq3TZjExF9oPy/130624913e15827926b4ed32a3071f9d/Gemini_Generated_Image_zi6xqwzi6xqwzi6x.png"
---

# Apideck CLI – An AI-agent interface with much lower context consumption than MCP - あなたのMCPサーバーがコンテキストを食い潰している。もっとシンプルな方法
MCPの“トークン地獄”を回避する80トークンの現実解 — CLIベースのAIエージェント統合

## 要約
MCP（Model-as-a-Controller/Tool）方式はAPIスキーマを大量にコンテキストに注ぎ込み、数万〜十万トークンを消費してしまう。一方で、ApideckはCLIをエージェントインターフェースにすることで初期プロンプトを約80トークンに抑え、必要時にだけ--helpで詳細を逐次取得する設計を採用している。

## この記事を読むべき理由
日本のSaaS／FinTech事業者やプロダクト開発者にとって、トークン課金・応答信頼性・安全性はコストと運用リスクに直結する。本手法は大規模連携で発生する「トークン爆食」「外部サーバー依存」「プロンプト注入リスク」を実務的に軽減する有力な選択肢を示す。

## 詳細解説
- 問題点（コンテキスト膨張）
  - MCPは各ツールの名前・説明・JSONスキーマ・フィールド説明……で事前に数万トークンを占有。例：GitHub/Slack/Sentryの小規模セットで55,000トークン消費、複数で143,000トークンに達する報告あり。
- 業界の3つの対策
  1. MCP＋圧縮／オンデマンド読み込み：小さな操作なら有効だがレジストリや検索・キャッシュなど追加インフラが必要。
  2. コード実行（Duet型）：エージェントがAPIドキュメントを読み、スクリプトを書いて実行する。柔軟だが「任意コード実行」に伴う安全性・サンドボックスの負担が大きい。
  3. CLIをエージェントインターフェースにする（Apideckの提案）：初期プロンプトは約80トークン、必要なときだけ--helpで詳細を取りにいく「漸進的開示（progressive disclosure）」によりトークン消費を劇的に削減。
- トークン・信頼性・コストの差
  - CLI初期プロンプト ~80トークン。必要時の--help呼び出しが都度50–200トークン程度。
  - ベンチマークでは同等作業でMCPがCLIの4〜32×のトークンを消費。スケール時の月次コスト差も大きい。
  - ローカルバイナリ（CLI）はMCPのような中継サーバーのタイムアウト問題がないため信頼性が向上。
- 安全性（構造的セーフティ）
  - 「DELETEはデフォルトブロック」「POST/PUTは確認必須」といった権限ルールをバイナリ内に組み込むことで、プロンプト注入による権限逸脱を抑止。
  - 例（設定イメージ）: ~/.apideck-cli/permissions.yaml で細かく上書き可能。
- 実装上のポイント
  - Apideck CLIは単一静的バイナリが起動時にOpenAPIスペックを解析してコマンドツリーを動的生成。TTY判定で人間向けか機械向けかを切替（非TTY時はJSON出力）でエージェントフレンドリー。
- 日本市場との関連
  - 日本のSaaS事業／銀行連携、会計・人事系APIが多数ある環境では、API表現が膨大になりやすい。トークン課金／可用性／コンプライアンスを抑えつつ外部サービスと連携するにはCLI戦略が有効。オンプレ／閉域網運用でもローカル実行は利点が大きい。

（例：エージェントに渡す最小プロンプト）
```bash
Use `apideck` to interact with the Apideck Unified API.
Available APIs: `apideck --list`
List resources: `apideck <api> --list`
Operation help: `apideck <api> <resource> <verb> --help`
APIs: accounting, ats, crm, ecommerce, hris, ...
Auth is pre-configured. GET auto-approved. POST/PUT/PATCH prompt (use --yes). DELETE blocked (use --force).
For clean output: -q -o json
```

## 実践ポイント
- まずは小さなPoCでCLIとMCPのトークン消費を比較してみる（同じタスクで計測）。
- エージェント側には約80トークンの「使い方プロンプト」を渡し、必要時に`--help`で逐次情報取得させる設計にする。
- destructive操作はCLI側でブロック／確認を必須にし、さらにエージェントフレームワーク側でも実行許可ポリシーを設ける。
- 日本のSaaS連携では、社内規程やオンプレ制約を踏まえローカルバイナリ運用を検討すると可用性・監査性が向上する。
