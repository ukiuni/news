---
layout: post
title: "What I learned building an opinionated and minimal coding agent - 意見を持ったミニマルなコーディングエージェントを作って学んだこと"
date: 2026-02-01T10:41:52.025Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://mariozechner.at/posts/2025-11-30-pi-coding-agent/"
source_title: "What I learned building an opinionated and minimal coding agent"
source_id: 46844822
excerpt: "コスト・コンテキストを抑えたミニマルLLMエージェント構築法"
image: "https://mariozechner.at/posts/2025-11-30-pi-coding-agent/media/header.png"
---

# What I learned building an opinionated and minimal coding agent - 意見を持ったミニマルなコーディングエージェントを作って学んだこと
たったの「必要最小限」で作る自分専用コーディングAI——複雑化するツール群に疲れた人へ捧ぐミニマル設計の教科書

## 要約
作者は多様なLLMハーネスの肥大化に嫌気が差し、自分用に「pi-」シリーズ（pi-ai, pi-agent-core, pi-tui, pi-coding-agent）を作って得た設計上の気づきを紹介する。ポイントは「多モデル対応」「コンテキスト制御」「ツール呼び出しの構造化」「端末UIの差分描画」「最小限主義」。

## この記事を読むべき理由
日本でも企業・開発者が複数のLLMやセルフホスト環境を試す局面が増えています。プロジェクトや社内ツールにLLMを組み込む際、コスト追跡・コンテキスト継承・ツール出力の扱いで痛い目を見る前に知っておくべき実践的な設計観点が詰まっています。

## 詳細解説
- 全体構成と哲学  
  - pi-ai：複数プロバイダー（Anthropic, OpenAI, Google, xAI, Groq, Cerebras…）にまたがる統一API。ストリーミング、ツール呼び出し（TypeBoxでスキーマ検証）、思考トレース／コンテキスト手渡し、トークン/コストの最小限追跡を提供。  
  - pi-agent-core：エージェントループ。ツール実行、検証、イベント発行、メッセージキュー管理を行う。  
  - pi-tui：ターミナルUIフレームワーク。差分描画と出力同期でちらつきを減らす。エディタやマークダウン表示コンポーネントを備える。  
  - pi-coding-agent：CLIレイヤー。セッション管理やプロジェクトコンテキストを扱う。

- マルチプロバイダーの現実  
  - 実際に必要なのは「四つのAPI」に集約可能（OpenAI Completions/Responses、Anthropic Messages、Google Generative API）。だが各社の実装差（reasoning tracesの扱いやパラメータ名の違い）を吸収する橋渡しロジックが必要。  
  - トークン／キャッシュ報告の不一致や、リクエスト中止の際の部分結果扱いなど、正確な課金連携が難しい点をpi-aiは「ベストエフォート」で扱う。

- コンテキストの受け渡し（handoff）  
  - プロバイダーを跨いだ会話継続は簡単ではない（各社が思考トレースや署名付きデータを別形式で返す）。pi-aiは思考トレースをタグ化するなどしてシリアライズ／復元可能にしている。

- ツール呼び出しとUI表示の分離（重要）  
  - ツール実行結果を「LLM向けテキスト/JSON」と「UI向け詳細（画像・構造化データ）」に分けて返せる設計は実用性が高い。TypeBox + AJVでツール引数の自動バリデーションを行い、エラーを明確にする実装も学びどころ。

- ストリーミング・中断の扱い  
  - 中断（Abort）をパイプライン全体でサポートし、部分結果を取り出せるようにすることは必須。ツール呼び出しや部分JSONパースのストリーミング対応はUXを大きく改善する。

- ミニマル主義（YOLO by default）  
  - 「要らない機能は作らない」。過剰な自動化・サブエージェント・背景タスクを排して、制御可能で見える化されたセッションを優先する。

例：プロバイダー切替とストリーミング（簡略）
```typescript
import { getModel, complete, Context } from '@mariozechner/pi-ai';

const claude = getModel('anthropic', 'claude-sonnet-4-5');
const context: Context = { messages: [] };
context.messages.push({ role: 'user', content: 'What is 25 * 18?' });
const claudeResponse = await complete(claude, context, { thinkingEnabled: true });
context.messages.push(claudeResponse);

// 別プロバイダへ移行（thinkingはタグ化される）
const gpt = getModel('openai', 'gpt-5.1-codex');
context.messages.push({ role: 'user', content: 'Is that correct?' });
const gptResponse = await complete(gpt, context);
```

## 実践ポイント
- 小さく始める：まずは「ツール呼び出し＋型検証」「中断可能なストリーミング」を実装してUXを改善する。  
- コンテキストは自前で制御する：プロバイダーが勝手に挿入する情報に依存しない形で会話を保存・復元できるように。  
- ツール結果は「LLM用」と「UI用」に分ける設計を採る（画像や構造化データを添える）。  
- コスト追跡はベストエフォートでも有用：開発段階からトークン計測を組み込んでおく。  
- 日本市場向け注意点：データセンシティブな用途やオンプレ/セルフホスト（国内法・社内ポリシー）を想定する場合、プロバイダー切替やローカルモデル対応は必須要件になる。

短く言えば：LLMをプロダクトに入れるなら「見える化」「制御」「最小限の機能セット」を設計の第一優先に。pi-*の設計はその良い出発点です。
