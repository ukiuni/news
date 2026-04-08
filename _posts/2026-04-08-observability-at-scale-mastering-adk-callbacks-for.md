---
layout: post
title: "Observability at Scale: Mastering ADK Callbacks for Cost, Latency, and Auditability [GDE] - 大規模観測性：ADKコールバックでコスト・遅延・監査性を極める"
date: 2026-04-08T03:50:46.768Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/gde/observability-at-scale-mastering-adk-callbacks-for-cost-latency-and-auditability-1mo5"
source_title: "Observability at Scale: Mastering ADK Callbacks for Cost, Latency, and Auditability [GDE] - DEV Community"
source_id: 3461516
excerpt: "ADKコールバックでLLM呼び出しを最小化しコスト・遅延・監査性を同時に改善する実践ガイド"
image: "https://media2.dev.to/dynamic/image/width=1200,height=627,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F0wopqh8z8l9t5jua1jrl.jpg"
---

# Observability at Scale: Mastering ADK Callbacks for Cost, Latency, and Auditability [GDE] - 大規模観測性：ADKコールバックでコスト・遅延・監査性を極める

ADKコールバックで無駄なLLM実行を減らし、遅延・トークンコストを抑えつつ監査可能なワークフローを作る方法

## 要約
Google ADKのコールバックフックを使うことで、エージェント処理の前後やモデル・ツール呼び出しの前後で処理を差し替え、ログ取得・状態管理・レスポンス改変・条件的スキップが可能になり、コストと遅延を大幅に削減できる。

## この記事を読むべき理由
- 日本でもLLMを組み込んだオーケストレーションが増え、実運用でのコストと遅延が課題となっているため。  
- ADKのコールバックは既存ロジックを壊さずに観測性や制御を追加でき、プロダクション移行でのトラブルシュートが容易になる。

## 詳細解説
1. ADKとは  
   - GoogleのAgent Development Kit（ADK）はエージェント開発用のオープンフレームワーク。サブエージェント、ツール呼び出し、セッション状態を持つワークフローを組める。

2. コールバックの種類（主要6種）  
   - beforeAgentCallback / afterAgentCallback：エージェントサイクルの前後  
   - beforeModelCallback / afterModelCallback：LLM呼び出しの前後（ここでスキップ判定可能）  
   - beforeToolCallback / afterToolCallback：ツール呼び出しの前後（状態更新やレスポンス改変）

3. よく使う設計パターン
   - ロギング／パフォーマンス計測（beforeAgentで時刻保存、afterAgentで差分ログ）  
   - セッション状態のリセット（beforeAgentで前回データをクリア）  
   - 動的状態管理（afterToolで検証回数をインクリメントし閾値超えで中断）  
   - リクエスト／レスポンス改変（afterToolでエラーをFATALに変えてエスカレーション）  
   - 条件的スキップ（beforeModelで既に十分なデータならLLM呼び出しを省略）

4. 実装イメージ（抜粋）
```typescript
// TypeScript
import { SingleAgentCallback, AfterToolCallback } from "@google/adk";

const START_KEY = "start_time";
const ATTEMPTS_KEY = "validation_attempts";
const MAX_ATTEMPTS = 3;

export const beforeAgent: SingleAgentCallback = (ctx) => {
  ctx?.state?.set(START_KEY, Date.now());
};

export const afterAgent: SingleAgentCallback = (ctx) => {
  const start = ctx?.state?.get<number>(START_KEY) ?? Date.now();
  console.log(`Agent ${ctx?.agentName} took ${(Date.now()-start)/1000}s`);
};

export function makeAfterTool(fatalMsg: string): AfterToolCallback {
  return ({ context, response }) => {
    const attempts = (context?.state?.get<number>(ATTEMPTS_KEY) || 0) + 1;
    context?.state?.set(ATTEMPTS_KEY, attempts);
    if (response?.status === "ERROR" && attempts >= MAX_ATTEMPTS) {
      context.actions.escalate = true;
      return { status: "FATAL_ERROR", message: fatalMsg };
    }
  };
}
```

5. 実運用上の注意  
   - コールバックを多用するとロジックが散らばるため、用途ごとに再利用可能な関数を作る。  
   - 開発環境と本番でモデルや認証が異なる場合は環境変数で切替え、依存は固定（ピン留め）する。

## 実践ポイント
- beforeModelCallbackで「既に十分な結果があるか」を検証し、不要なLLM呼び出しを止める。  
- beforeAgentでセッションを初期化してサブエージェントをシンプルに保つ。  
- afterToolで試行回数を管理し、閾値超えはFATAL化してループを抜ける。  
- ログはbefore/afterの両方で取り、エージェントごとの遅延を可視化する。  
- 依存バージョンは固定し、ローカルでMailHogなどを使った安全なテスト環境を用意する。

この記事のパターンを取り入れれば、LLMオーケストレーションの無駄を削ぎ、コスト削減・応答速度向上・監査性強化を同時に実現できます。
