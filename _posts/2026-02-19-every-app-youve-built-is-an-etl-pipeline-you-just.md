---
layout: post
title: "Every app you've built is an ETL pipeline (you just didn't call it that) - あなたが作ったアプリはすべてETLパイプラインだった（そう呼んでいなかっただけ）"
date: 2026-02-19T23:21:47.437Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.inngest.com/blog/etl-via-inngest"
source_title: "Every app you&#x27;ve built is an ETL pipeline - Inngest Blog"
source_id: 1747950115
excerpt: "すべてのアプリはETL──LLMの非決定性をステップ単位のチェックポイントで防ぐ設計術"
image: "https://www.inngest.com/assets/blog/inngest-as-etl.png"
---

# Every app you've built is an ETL pipeline (you just didn't call it that) - あなたが作ったアプリはすべてETLパイプラインだった（そう呼んでいなかっただけ）
「気づけばETL化している」日常のコードをスッキリさばく、実務で使える設計術

## 要約
ほとんどのアプリは「抽出→変換→格納」のETLパターンでできている。特にLLMを使うと非決定的な変換が入るため失敗モードやコストが急増する。ステップ単位の耐久性（checkpointed steps）とイベント駆動の分離でその複雑さを解消できる、という話。

## この記事を読むべき理由
日本でもSaaS連携、Webhook処理、AI機能の導入が増え、再現性・観測性・コスト管理の問題に直面するチームが増えています。現場で起きる「リトライで重複」「どこで失敗したかわからない」を設計段階で防ぐ実践知が得られます。

## 詳細解説
- なぜほとんどの機能がETLなのか  
  管理用CSV取り込み、Stripe webhook、サポートチケットの分類など、どれも「どこかからデータを取る → 何か処理する → どこかに書く」という流れ。違いは名前だけで、同じ失敗パターン（抽出失敗、変換ミス、部分的な書き込み、重複）を持つ。

- LLMで問題が深刻化する理由  
  LLMは非決定的で同じ入力が異なる出力を返すことがある。全体を再実行するリトライはコストと重複を招き、ログだけでは原因特定が難しい。

- 典型的な「進化の罠」  
  初期は数行のバッチ処理でも、ステータス追跡、リトライ、冪等性対策、デデュープ、監視ダッシュボード……といった対処を重ねるうちに独自のオーケストレーション基盤を維持する羽目になる。

- 解決策：ステップ単位の耐久性とイベント駆動  
  ステップごとに結果をチェックポイントし、失敗したステップだけを再試行できれば再実行の副作用（重複や余計なコスト）を防げる。さらに、イベント（例：support/thread.created）に対して複数の独立した関数を紐付ける「ファンアウト」により機能ごとに独立し、デプロイや障害影響が局所化する。

- 実装例（概念）  
  Inngestのようなフレームワークでは step.run により各処理をチェックポイント化できる。失敗時はそのステップだけを再試行し、完了済みステップは再実行されない。

```typescript
// TypeScript (概念例)
inngest.createFunction(
  { id: "categorize-support-thread" },
  { event: "support/thread.created" },
  async ({ event, step }) => {
    const replies = await step.run("fetch-replies", async () =>
      fetchAllReplies(event.data.threadId)
    );
    const category = await step.run("classify-with-llm", async () => {
      const r = await llmService.fetchCategoryForReplies(replies);
      if (!VALID_CATEGORIES.includes(r)) throw new Error("Invalid");
      return r;
    });
    await step.run("save-classification", async () =>
      supportThreadRepo.update(event.data.threadId, { category })
    );
  }
);
```

## 実践ポイント
- イベント駆動（イベント＝事実）で機能を分離し、機能ごとに小さなリスナーを作る（ファンアウト）。  
- 変換（特にLLM）の出力はスキーマ検証を必ず行う。非決定性を前提に設計する。  
- ステップごとにチェックポイント（状態保存）できるランタイムやライブラリを検討する（再実行の範囲を限定）。  
- 可観測性を最初から設計：どのイベントが、どのステップで、何を返したかをチーム全員が見られるように。  
- 小さく始めて、インフラを自前で膨らませない。必要ならマネージドなワークフロー基盤を活用して本来のプロダクトに集中する。

以上。これらを取り入れれば、AI/連携機能の増加にも耐える堅牢でメンテしやすいアーキテクチャが作れます。
