---
layout: post
title: "Unrolling the Codex Agent Loop - コデックスのエージェントループを紐解く"
date: 2026-01-23T21:23:43.596Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://openai.com/index/unrolling-the-codex-agent-loop/"
source_title: "Unrolling the Codex Agent Loop"
source_id: 46737630
excerpt: "Codexエージェントループで安全・効率的に社内コード編集を自動化する実装と注意点を解説"
---

# Unrolling the Codex Agent Loop - コデックスのエージェントループを紐解く
エンジニアの手元で“賢く・安全に・効率的に”コードを書き変える仕組み—Codex CLIの核心である「エージェントループ」をやさしく解説

## 要約
Codex CLIは、ユーザー入力→モデル推論→ツール呼び出しを繰り返す「エージェントループ」で動作する。プロンプト生成、ツール実行、ストリーミング、コンテキスト管理、パフォーマンス最適化（プロンプトキャッシュやZDR対応）などが設計の肝。

## この記事を読むべき理由
日本の開発現場でもローカル実行やオンプレ／クラウド混在運用が増える中、Codexの設計思想は安全性・効率・拡張性の良い手本になる。特に社内コードベースにLLMを導入する際の実務的な注意点と実装の要点を学べる。

## 詳細解説
- エージェントループの全体像  
  ユーザー入力を取り込み「プロンプト」を作成→Responses APIへ推論要求→モデルが「アシスタント応答」か「ツール呼び出し」を返す→ツール実行結果をプロンプトに追加して再推論、を繰り返す。1ターンはこれらの反復を含む会話単位。

- プロンプトの構成と役割（role）  
  Responses APIへ送るJSONのinputは複数アイテムのリストで、roleの優先度は system/developer/user/assistant の順。Codexでは tools（利用可能なツール定義）、developer指示（sandboxやconfigの指示）、プロジェクトドキュメント（AGENTS.md等）を集約して初期入力を作る。

- ツール呼び出しとサンドボックス  
  Codex側で提供するshellツールは明確にサンドボックスされるが、外部ツール（MCP等）は各提供元でガードレールが必要。ツール呼び出しはローカル環境を変えるため、実行権限と安全性の設計が重要。

- 推論とストリーミング（SSE）  
  Responses APIはSSEで結果を返す。部分出力（output_text.delta）でUIにストリーミング表示し、response.output_item.* イベントを次の入力に追加してループを継続する。

- コンテキストウィンドウと成長するプロンプト  
  会話履歴とツール出力を逐次追加するためプロンプトは成長し、モデルのコンテキスト上限に達する可能性が高い。エージェントはコンテキスト管理（不要部分の要約や削除）を担う必要がある。

- パフォーマンス最適化とZDR（Zero Data Retention）設計トレードオフ  
  送信データ量は二次的で、モデルのサンプリングコストがボトルネック。プロンプトキャッシュで以前の計算を再利用することが効率化に直結する。一方、previous_response_id を使うと帯域やステート効率は改善するが、ZDR方針（履歴を保持しない）と矛盾するためCodexは基本的にステートレス設計を選んでいる。

- 実行環境の柔軟性  
  Codex CLIはOpenAIのResponses API、ChatGPTバックエンド、ローカルのgpt-oss（ollama/LM Studio経由）やAzureホストなど複数のエンドポイントに対応。オンプレや社内クラウド運用の選択肢がある。

## 実践ポイント
- まずリポジトリを参照：公式GitHub（openai/codex）で実装と設計議論を読む。  
- 小さく試す：ローカルで--oss＋gpt-oss（ollama/LM Studio）を立てて挙動を確認。  
- AGENTS.mdやdeveloper_instructionsで期待振る舞いを明確化し、プロジェクトルートに説明ファイルを置く。  
- ツールは最小権限でサンドボックス化。外部ツール提供元にガードレールを要求する。  
- コンテキスト管理を組み込む：長期会話では要約・削除ルールとプロンプトキャッシュを検討。  
- ZDRや社内データポリシーに合わせて、previous_response_idの使用可否を決める。  

以上を押さえれば、Codex的エージェントを自社ワークフローに安全かつ効率的に組み込むための設計判断がしやすくなる。
