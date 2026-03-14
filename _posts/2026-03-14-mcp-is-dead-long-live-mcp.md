---
layout: post
title: "MCP Is Dead; Long Live MCP - MCPは終わった？されどMCP万歳"
date: 2026-03-14T20:55:01.237Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://chrlschn.dev/blog/2026/03/mcp-is-dead-long-live-mcp/"
source_title: "@chrlschn - MCP is Dead; Long Live MCP!"
source_id: 47380270
excerpt: "CLI礼賛の流行に異議、企業向けには認証・監査・配信が強力な中央MCPの導入戦略を解説"
image: "https://chrlschn.dev/img/mcp/death-to-mcp-long-live-mcp.png"
---

# MCP Is Dead; Long Live MCP - MCPは終わった？されどMCP万歳
CLIブームの先にある「企業で本当に使えるMCP戦略」

## 要約
SNSでのCLI礼賛とMCPバッシングは行き過ぎ。個人レベルではCLIに利点があるが、組織／エンタープライズではHTTP経由の中央集約型MCPが認証・観測・配信の面で圧倒的に有益だ、という主張。

## この記事を読むべき理由
日本の開発組織でも、CI/CDやクラウド連携、監査要件を抱えるチームは増えています。CLIだけで済ませると運用・権限・可視化で痛い目を見る可能性が高く、MCPの“中央化”設計は現場の課題解決に直結します。

## 詳細解説
- インフルエンサー・サイクル：短期的な流行（MCP礼賛→MCP否定→CLI礼賛）は多くがマーケティング起点。技術選定はユースケースで判断すべき。
- トークン節約の実態：
  - モデルが学習済みの汎用CLI（curl, jq, git など）は一発で使えるためコンテキスト節約が効く。
  - カスタムCLIや独自APIはモデルに説明（スキーマやREADME）を与えないと誤動作する。結果、追加コンテキストで節約が相殺されることが多い。
  - CLIは「段階的にヘルプを読み込む」ことで最初のコンテキストを減らせるが、複雑なフローでは結局多くを探索する必要がある。
- MCPの二面性（stdio vs HTTP）：
  - ローカルstdioモードは単純で冗長に感じることが多い。個人用途や小さなツール群にはCLIで十分。
  - だがストリーム可能なHTTP経由の中央サーバ型MCPは企業ユースで強力。利点は以下。
- 中央集約の利点：
  - リッチな基盤能力（共有DB、グラフ検索、インデックス化されたコンテキスト）を薄クライアントから利用可能。
  - エフェメラルな実行環境（GitHub Actions等）に対して状態管理や重い処理をオフロードできる。
  - 認証とセキュリティ：API鍵を個々の開発者に配る必要がなく、OAuthなどでアクセスを一元管理・監査可能。
  - テレメトリと可観測性：どのツールが使われているか、失敗率は、影響度はを集約して分析できる（OpenTelemetry等）。
  - コンテンツとスキルの即時配信：MCPのPrompts/Resourcesで動的にSkillやDocsを配信・更新でき、バージョン問題を軽減。
- 結論的な整理：CLIとMCPは対立ではなく使い分け。個人の試作や既知ツールはCLI、組織横断の運用・セキュリティ・観測を重視するならHTTPベースの中央MCP。

## 実践ポイント
- 既知の汎用CLI（curl, git等）はまず使う。学習済みモデルには強みあり。
- カスタムCLIを使うならAGENTS.md/READMEで明確にドキュメント化し、モデルに参照させる。
- 組織用途はHTTP経由での中央MCPを検討：OAuthで認可、一元的に鍵を管理・監査する。
- テレメトリは最初から計画（OpenTelemetry）し、ツール利用状況を継続観測する。
- 小さな中央サーバから導入して、段階的にスキル（Prompts/Resources）配信を始める。これで運用管理とアップデート負担を削減できる。
