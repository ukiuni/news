---
layout: post
title: "Show HN: Ocrbase – pdf → .md/.json document OCR and structured extraction API - PDF → .md/.json ドキュメントOCRと構造化抽出API"
date: 2026-01-20T14:51:24.098Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/majcheradam/ocrbase"
source_title: "GitHub - majcheradam/ocrbase: 📄 PDF -&gt;.MD/.JSON Document OCR and structured data extraction API. PaddleOCR + LLM-powered parsing. Real-time WebSocket updates. Type-safe TypeScript SDK with React hooks. Self-hostable."
source_id: 46691454
excerpt: "自己ホストでPaddleOCR＋LLMによりPDFをMarkdown/JSONへ高精度自動抽出"
image: "https://opengraph.githubassets.com/303650cca29a2c838476996363ce51eab57549e37d0331ebae15a157e2ab31c5/majcheradam/ocrbase"
---

# Show HN: Ocrbase – pdf → .md/.json document OCR and structured extraction API - PDF → .md/.json ドキュメントOCRと構造化抽出API
魅力：自前で動かせる高速ドキュメントOCR＋LLMパースで「PDF→Markdown/JSON」を自動化するツール

## 要約
OcrbaseはPaddleOCR（PaddleOCR-VL-0.9B）で高精度に文字を抽出し、LLMベースのパーサで定義したスキーマに沿ったJSON／Markdownを返す自己ホスト可能なドキュメント処理プラットフォームです。TypeScript製の型安全なSDK（Reactフック対応）とWebSocketによるリアルタイム更新を備え、キュー処理でスケールします。

## この記事を読むべき理由
日本企業は紙帳票やPDFのデジタル化・構造化が喫緊の課題です。オンプレで機密文書を扱いたい場合や、請求書・契約書・報告書の自動抽出をローカル環境で完結させたいチームに特に有用です。オープンソースで自己ホストできるため、国内のセキュリティ要件にも適合しやすい点も魅力です。

## 詳細解説
- コア技術
  - OCR：PaddleOCR-VL-0.9Bを採用し、レイアウトやビジュアルコンテキストを考慮したテキスト抽出を実現。
  - 構造化抽出：抽出したテキストをLLMで解析し、ユーザーが定義したスキーマに従ってJSONやMarkdownへ変換。
  - 実行フロー：ファイルをジョブとしてキューに投入 → OCR → LLMパース → 結果を保存／通知（WebSocketで進捗配信）。
- 開発者向け
  - TypeScript SDK：型安全なAPIとReact用のフックを提供。フロントエンドからジョブ作成や進捗受信が容易。
  - リアルタイム：WebSocketでジョブの状態（進捗や完了）を受け取れるため、UIでステータス表示が作りやすい。
- スケーリングとデプロイ
  - キュー駆動のアーキテクチャで大量ドキュメント処理に対応。
  - 自己ホスト可能：Docker / docker-composeベース。高負荷処理にはCUDA対応GPU（推奨VRAM 12GB以上）を使用。
  - 依存：Bunが開発ツールとして使われている点に注意。
- ライセンスと運用
  - MITライセンスで商用利用もしやすく、オンプレ運用・カスタマイズが可能。
  - サポートやカスタム導入は公開リポジトリの作者にコンタクト可能（READMEに連絡先あり）。

例：SDKでジョブを作る簡単なコード
```typescript
import { createOCRBaseClient } from "@ocrbase/sdk";

const client = createOCRBaseClient({ baseUrl: "https://your-instance.com" });

// ドキュメントを処理
const job = await client.jobs.create({ file: documentFile, type: "parse" });
const result = await client.jobs.get(job.id);
console.log(result.markdownResult);
```

## 実践ポイント
- まずはローカルで試す：リポジトリのQuick Startに従いDocker＋Bun環境で動かしてみる。サンプルPDFを投げて出力を確認するのが早道。
- GPU要件を確認：大量処理や高精度OCRを行う場合はCUDA対応GPU（12GB VRAM以上）を用意する。小規模検証はCPUでも可能だが遅くなる。
- スキーマ設計を先に：抽出したいフィールド（請求先、日付、金額など）を決めておけばLLMパースの精度と運用効率が上がる。
- セキュリティ要件がある場合は自己ホストを検討：特に個人情報や機密文書を扱う場合、クラウド送信を避けられる点は大きな利点。
- 日本語文書の精度検証：PaddleOCRは多言語対応だが、レイアウトやフォントによって差が出るため、実データでの精度評価は必須。

興味があれば、まずリポジトリのREADMEでQuick Startを実行し、社内の代表的なPDF（請求書・契約）でプロトタイプを作るのが最短ルート。
