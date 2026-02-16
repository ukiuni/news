---
layout: post
title: "WebMCP Proposal - WebMCP 提案"
date: 2026-02-16T18:35:19.722Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://webmachinelearning.github.io/webmcp/"
source_title: "WebMCP"
source_id: 47037501
excerpt: "ブラウザで関数をAIツール公開し安全連携する新API提案で低遅延・プライバシー重視"
---

# WebMCP Proposal - WebMCP 提案
ブラウザ上で自分の機能を「ツール」として公開し、AIエージェントと安全に協働する――WebMCPが切り拓くクライアント側MCP

## 要約
WebMCPは、ウェブページがJavaScript関数を「ツール」としてブラウザ経由でAIエージェントに公開できる新しいAPI提案で、クライアント側でのツール公開・呼び出し・ユーザー対話を標準化しようとするものです（草案・コミュニティ報告書、標準化途上）。

## この記事を読むべき理由
国内のウェブサービスや業務系アプリが、サーバー側を介さずにブラウザ上でAIエージェントと機能連携できれば、ユーザー体験の向上・レイテンシ低減・プライバシー制御が可能になります。日本の企業や開発者は事前に設計やガバナンスを考えるべきです。

## 詳細解説
- 基本概念  
  - 「エージェント」：利用者の目標達成を支援する自律的アシスタント（多くはLLMベース）。  
  - WebMCPはウェブページを「Model Context Protocol (MCP) サーバー」のように振る舞わせ、クライアント側スクリプトでツールを実装・公開します。

- 主要API（草案）  
  - navigator.modelContext （SecureContext、Windowに露出）を通じて操作。  
  - provideContext(options)：現在登録済みのツールをクリアして新しいツール群を登録。  
  - clearContext()：登録済みツールを全解除。  
  - registerTool(tool)：既存ツールを消さずに単体登録（同名があればエラー、inputSchemaの検証あり）。  
  - unregisterTool(name)：指定ツールを削除。

- ModelContextTool の構成  
  - name（必須）：ツール識別子（エージェントが参照）。  
  - description（必須）：自然言語での機能説明（エージェント理解に重要）。  
  - inputSchema：JSON Schemaで入力パラメータを定義（整合性と安全性確保）。  
  - execute（必須）：(input, ModelContextClient) を受ける非同期コールバック。結果をPromiseで返す。  
  - annotations.readOnlyHint：読み取り専用ならtrueを付けてエージェント判断を支援。

- ModelContextClient  
  - client.requestUserInteraction(callback)：ツール実行中にユーザー対話を非同期で要求できる（確認ダイアログ等）。

- セキュリティ・プライバシー・アクセシビリティ  
  - SecureContext限定やユーザー同意、実行権限設計が必要。日本の個人情報保護法（APPI）や企業のデータ取扱い方針と整合させる運用設計が重要です。アクセシビリティ連携も想定（支援技術との共存）。

- 状態（重要）  
  - これはWeb Machine Learning Community Groupの草案であり、W3C標準ではありません。仕様の未確定箇所（草案内のTODO）や実装差異に注意。

## 実践ポイント
- まずは機能検出から：  
  if (navigator.modelContext) { /* 対応環境でのみ登録 */ } else { /* フォールバック */ }

- 簡単な登録例（プロトタイプ）
```javascript
// javascript
const tool = {
  name: "getInvoiceSummary",
  description: "注文IDを受け取り請求情報を要約して返す",
  inputSchema: { type: "object", properties: { orderId: { type: "string" } }, required: ["orderId"] },
  execute: async (input, client) => {
    // 必要ならユーザー確認を挟む
    await client.requestUserInteraction(async () => confirm("この注文情報を共有しますか？"));
    // 実際の処理（例：クライアント側で計算またはAPI呼び出し）
    return { summary: "請求金額: ¥10,000" };
  },
  annotations: { readOnlyHint: true }
};
navigator.modelContext.provideContext({ tools: [tool] });
```

- 設計上の注意点  
  - 入力はJSON Schemaで厳密に定義して検証する。  
  - executeは非同期でエラーやタイムアウトを明確に扱う。  
  - readOnlyHintを活用して安全性を向上。  
  - ユーザー同意ログ、監査トレースを残す。  
  - ブラウザ実装状況（Chromium系の動きなど）を追う。

- 国内向け配慮  
  - 個人情報や機密データのクライアント公開の可否を法務と確認する。  
  - 日本語のdescriptionはエージェントの選定（国内外AIプラットフォーム）に影響するので多言語対応を検討。  
  - 支援技術（スクリーンリーダ等）との互換性を設計段階で確認。

以上を踏まえ、まずは小さな読み取り専用ツールで実験的に導入し、安全性・同意フロー・フォールバックを整備しながらWebMCPの対応に備えることを推奨します。
