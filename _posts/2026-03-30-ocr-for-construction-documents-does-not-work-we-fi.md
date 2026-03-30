---
layout: post
title: "OCR for construction documents does not work, we fixed it - 建築図面のOCRはダメだった、私たちはそれを直した"
date: 2026-03-30T17:53:08.120Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.getanchorgrid.com/developer/docs/endpoints/drawings-doors"
source_title: "AnchorGrid Developer Docs"
source_id: 47576055
excerpt: "建築図面向けドア検出で文字認識の限界を克服、座標付きジョブ式自動化"
---

# OCR for construction documents does not work, we fixed it - 建築図面のOCRはダメだった、私たちはそれを直した
建築図面から「ドア」を自動検出するAPIで、現場の図面データを実用レベルにした話

## 要約
AnchorGridの「ドア検出」API（POST /v1/drawings/detection/doors）は、PDF化された平面図からドアを矩形で抽出し、ジョブ方式で結果を返す。ページ単位の課金や処理時間、座標系など実務で必要な仕様が明確化されている。

## この記事を読むべき理由
日本の建設業界は図面のデジタル化と労働力不足対応が急務。手作業での拾い出しやOCRだけでは限界があるため、図面専用の物体検出APIが即戦力になる理由と導入時の注意点を知っておく価値がある。

## 詳細解説
- 機能概要：POST /v1/drawings/detection/doors に既にアップロード済みの document_id を投げると推論ジョブをキューに入れる。非同期処理でジョブIDを返し、GET /v1/jobs/{job_id}で完了をポーリングするか（開発/有償プランは webhook 受け取り可）。
- 入力：JSON本文（ファイルの直接アップロード不可）。必須は document_id（UUID）。任意で page_numbers（1始まり配列、省略で全ページ）、webhook_url（上位プランのみ）。
- 出力（完了時）：document_id、doors 配列（各要素に id: "door_"+12 hex、page（PDFの1ベース）、bbox: {x1,y1,x2,y2} — PDF座標系）、doors_found（幾何学フィルタ後の件数）、pages_analyzed、model_version、processing_time_ms。
- 処理特性：無料枠のドア検出はジョブあたり通常2〜4分。処理時間はページ数と図面の密度に依存。Pro/Enterpriseは専用GPUで高速化。
- 課金・制限：課金は送信時に page 数で請求（例：2クレジット/ページ）。ページにドアが無くても請求されるため、無駄課金に注意。レート/クォータ制限とエラーコード（401/402/404/422/429）あり。
- ポストプロセス：サーバー側で幾何学フィルタと中央値面積フィルタを適用しており、返ってくる doors は除外済みの安定結果。

## 実践ポイント
- 事前にPDFをアップロードして document_id を取得するワークフローを作る。
- page_numbers を指定してスキャンページを絞る（無駄な課金を防ぐ）。
- ジョブは非同期：短時間で結果が欲しければ Pro/Enterprise にアップグレードし専用GPUを利用する。
- webhook を使えばポーリング不要で自動処理パイプラインに組み込みやすい（開発/有償プランのみ）。
- bbox はPDF座標系なので、座標変換（表示系やBIM座標へのマッピング）を忘れずに行う。
- エラー（401/402/404/422/429）をハンドリングし、rate-limit の retry_after_seconds を使って再試行設計をする。
- テスト時は少量ページで動作確認→徐々にスケール。まずは代表的な図面で doors_found と生の検出結果の差を確認する。

簡単な呼び出し例（curl）:
```bash
curl -X POST https://api.anchorgrid.ai/v1/drawings/detection/doors \
  -H "X-API-Key: <your-api-key>" \
  -H "Content-Type: application/json" \
  -d '{ "document_id": "550e8400-e29b-41d4-a716-446655440000", "page_numbers": [1,2,3] }'
```

このAPIは「図面特化の検出」でOCRの限界を補い、手作業の省力化や現場連携に直結する実践的なツールです。導入前に課金ルールと座標系変換を必ず設計に組み込んでください。
