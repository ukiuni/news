---
layout: post
title: "JSON-render: LLM-based JSON-to-UI tool - JSON-render：LLMでJSON→UIを生成するツール"
date: 2026-01-24T20:41:37.998Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://json-render.dev/"
source_title: "json-render | AI-generated UI with guardrails"
source_id: 46746570
excerpt: "コンポーネントカタログでAI出力を制限し安全にReact UIを逐次生成・エクスポート"
image: "https://json-render.dev/og"
---

# JSON-render: LLM-based JSON-to-UI tool - JSON-render：LLMでJSON→UIを生成するツール
AIが生成したJSONを「定義したコンポーネントカタログ」に縛って安全にUIを出力する、新しいUI自動生成ワークフロー

## 要約
json-renderは「コンポーネントカタログ」でAIの出力を制限し、ストリーミングでJSONを受けながら自前のReactコンポーネントに逐次レンダリング、さらにスタンドアロンのReact/Next.jsコードとしてエクスポートできるツールです。

## この記事を読むべき理由
日本のプロダクト開発ではデザインシステムやセキュリティ要件が厳しく、AI生成UIをそのまま使うのはリスクがあります。json-renderは「使ってほしい部品だけをAIに許可する」設計で現場導入しやすく、プロトタイピングから実運用まで役立ちます。

## 詳細解説
- カタログ（Catalog）: 開発側が使えるコンポーネント、アクション、バリデーションを定義。zod等でpropsの型を宣言し、AIに許可する要素を厳格に制限します。  
  - 例: CardやMetricといったコンポーネントのpropsをzodで定義して登録。
- AI → JSON（ガード付き）: ユーザーのプロンプトに対してLLMが生成するのは「カタログに従ったJSON」のみ。これにより未知のタグや危険な命令が混入しないようにできます。
- ストリーミング & プログレッシブレンダリング: モデルの応答をJSONストリームで受け取り、到着した断片を順次レンダリングしてUXを高速化します。
- データバインディング: JSON Pointerベースの値パスで双方向のデータバインディングをサポート。動的データを既存の状態と結びつけられます。
- アクションと可視性: named actions（アプリ側で実装）や条件付き表示（データや認可に基づくshow/hide）をカタログで制御。
- コードエクスポート: 生成されたUIをランタイム依存なしのReact/Next.jsプロジェクトとして出力可能。プロダクト化や共有が容易です。
- 導入パッケージ: npm install @json-render/core @json-render/react で始められます。

簡単な定義例（要点のみ）:

```javascript
import { createCatalog } from '@json-render/core';
import { z } from 'zod';

export const catalog = createCatalog({
  components: {
    Card: {
      props: z.object({ title: z.string(), description: z.string().nullable() }),
      hasChildren: true,
    },
    Metric: {
      props: z.object({ label: z.string(), valuePath: z.string(), format: z.enum(['currency','percent']) }),
    },
  },
  actions: {
    export: { params: z.object({ format: z.string() }) },
  },
});
```

## 実践ポイント
- まず小さなカタログを作る（フォーム、カード、メトリクス等）→安全性を確認しつつ拡張する。  
- zod等でpropsを厳密に型定義してAI出力を受け止める。  
- ストリーミングを試してUX改善（大きなUIツリーを段階表示）。  
- エクスポート機能を使って生成コードをレビュー→デザインシステムに取り込む。  
- 日本語プロンプトやローカライズ条件（例：日付/通貨フォーマット、アクセシビリティ）をカタログ設計に反映する。  

導入検討時は、社内のデータガバナンスとLLMプロバイダのポリシーを合わせて評価してください。
