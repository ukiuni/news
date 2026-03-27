---
layout: post
title: "OpenTelemetry just standardized LLM tracing. Here's what it actually looks like in code. - OpenTelemetryがLLMトレースを標準化しました：実装でどう変わるか"
date: 2026-03-27T17:59:31.049Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/vola-trebla/opentelemetry-just-standardized-llm-tracing-heres-what-it-actually-looks-like-in-code-2e5f"
source_title: "OpenTelemetry just standardized LLM tracing. Here&#39;s what it actually looks like in code. - DEV Community"
source_id: 3381615
excerpt: "OpenTelemetryのGenAI規約でLLMトレースが統一、実装と移行手順を具体解説"
image: "https://media2.dev.to/dynamic/image/width=1200,height=627,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F71q10hso2j6x3d7crpi2.png"
---

# OpenTelemetry just standardized LLM tracing. Here's what it actually looks like in code. - OpenTelemetryがLLMトレースを標準化しました：実装でどう変わるか
「LLMトレースの“ベンダー地獄”を終わらせる？OpenTelemetry GenAI規約を実践で使う方法」

## 要約
OpenTelemetryがGenAI（LLM）用のセマンティックコンベンションを公開し、スパン名・属性・コンテンツ取り扱いの標準を定めた。これに従えばベンダー間でトレース互換性が得られる。

## この記事を読むべき理由
日本のプロダクトで複数のモデル／監視ツールを使うと、属性バラバラでデバッグやコスト把握が地獄になる。規約に合わせれば可観測性が安定し、監査・個人情報管理やコスト管理も楽になる。

## 詳細解説
- 主要ルール
  - スパンは3種類の操作に分類：chat（モデル呼び出し）、invoke_agent（エージェント呼び出し）、execute_tool（ツール実行）。
  - スパン名は "{operation} {name}"（例: "chat gpt-4o"、"invoke_agent weather-bot"）という固定フォーマット。
- 主要属性（例）
  - gen_ai.provider.name, gen_ai.request.model, gen_ai.usage.input_tokens, error.type などは仕様どおりに使うとバックエンドが認識する。
  - エージェント／ツール属性はネストせずフラット：gen_ai.agent.name, gen_ai.agent.id, gen_ai.tool.name, gen_ai.tool.type。
- コンテンツ（プロンプト／応答）の取り扱い
  - デフォルトではスパンにプロンプト/応答を記録しない（プライバシー優先）。明示的に有効化するか、外部ストレージに保存してスパンには参照を置く。
  - 明示的属性例：gen_ai.input.messages / gen_ai.output.messages（JSON文字列）
- 実装上の注意点
  - 既存実装が独自命名だと他の可観測化ツールで無視される（ベンダーロックインの危険）。
  - 移行戦略としては「dual-emit」（旧属性も併記して互換性維持）→ 将来廃止。例：環境変数で新仕様のみ有効化。
  - テストでトレースがエクスポートされていないケース（spanProcessorを空にした等）に注意。可視化されない設定ミスが潜む。
- 対応バックエンド（記事時点）
  - Jaeger, Arize Phoenix, SigNoz, Datadog, Langfuse, Grafana+Tempo 等がサポート段階。

コード例（TypeScript/JSでの属性設定例）:

```javascript
// 新：OTel GenAI 準拠
span.setAttribute("gen_ai.tool.name", toolName);
span.setAttribute("gen_ai.tool.type", "function");
span.setAttribute("gen_ai.agent.name", "weather-bot");
span.setAttribute("gen_ai.operation.name", "invoke_agent");
span.updateName(`invoke_agent ${agentName}`);

// 旧（誤り／互換性のため一時併出）
span.setAttribute("gen_ai.agent.tool.name", toolName); // 過去実装でよくある誤り
```

## 実践ポイント
- まずやること（チェックリスト）
  1. 各LLMスパンに gen_ai.operation.name を付ける（chat / invoke_agent / execute_tool）。
  2. スパン名を "{operation} {model_or_agent_name}" 形式に揃える。
  3. 公式属性（gen_ai.*）を使い、アプリ固有は自社名前空間（例：gen_ai.myapp.*）へ分離する。
  4. デフォルトでプロンプト/応答を記録しない運用にする（必要ならオプトイン）。
  5. Jaeger + GenAI対応バックエンド（例：Arize Phoenix）で実際に可視化確認する。
- 移行のコツ：当面はdual-emitで互換性を守りつつ、モニタリングとテスト（トレースのエクスポート確認）を必ず行う。

短く言えば：今すぐGenAI規約に合わせて属性とスパン命名を揃えれば、複数バックエンドで追える安定したLLM可観測性が手に入る。
