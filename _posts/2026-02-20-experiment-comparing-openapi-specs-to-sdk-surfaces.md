---
layout: post
title: "Experiment: Comparing OpenAPI Specs to SDK Surfaces - 実験：OpenAPI仕様と生成SDKのズレ比較"
date: 2026-02-20T06:58:18.414Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/dharmarajatulya1-hub/sdkdrift"
source_title: "GitHub - dharmarajatulya1-hub/sdkdrift: Never ship a stale SDK again: detect drift between OpenAPI specs and generated SDKs."
source_id: 437238528
excerpt: "CIでスコア判定、OpenAPIと生成SDKの差分を自動検出して古い出荷を防ぐSDKDrift"
image: "https://opengraph.githubassets.com/72778f7c3ecbe533c4c53ded1629660abfc1a774d35f06f5998eb4df5aa22aac/dharmarajatulya1-hub/sdkdrift"
---

# Experiment: Comparing OpenAPI Specs to SDK Surfaces - 実験：OpenAPI仕様と生成SDKのズレ比較
API仕様とSDKの「ズレ」を見つけてリリース前に潰す──新ツール「SDKDrift」の紹介

## 要約
SDKDriftはOpenAPI仕様と生成されたSDKのインターフェース差分（drift）を検出し、何が欠けているかを報告してスコア化するツールです。CIに組み込んで「古いSDKを出荷する」リスクを防げます。

## この記事を読むべき理由
APIファースト開発や自動生成SDKを使う日本のチームでは、仕様の変更とSDK反映のズレがバグ原因になりがちです。SDKDriftを使えば、リリース前に自動で差分を検出して品質ゲートを設けられます。

## 詳細解説
- 何をするか：OpenAPI（spec）とSDKディレクトリを比較し、操作（operationId）やエンドポイント、型の不整合を検出して「スコア」と「所見」を出力します。例えば「missing_endpoint」「wrong_params」などのカテゴリで評価されます。  
- アーキテクチャ：@sdkdrift/cli（CLI）、@sdkdrift/core（パーサ／マッチャ／diff／スコアリング）、言語ごとのスキャナ（現状はPython/TypeScript）が主なパッケージです。  
- 出力：ターミナル、JSON、Markdownが選べ、JSONはCI報告用に便利。SCHEMA.mdで出力レポートの契約が定義されています。  
- 設定：sdkdrift.config.yamlでヒューリスティック閾値やメソッド名のマッピング（operationId→SDKメソッド）を上書きできます。  
- 退出コード：0=成功（閾値以上）、1=実行/設定エラー、2=スコア未達成で失敗（CIで利用）。

使用例（手元で試す）:
```bash
npx @sdkdrift/cli scan --spec ./openapi.yaml --sdk ./sdk/python --lang python --format terminal --min-score 90
```

CI例（GitHub Actions）:
```yaml
name: SDK Drift Check
on: [push]
jobs:
  drift:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npx @sdkdrift/cli scan --spec ./openapi.yaml --sdk ./sdk/python --lang python --min-score 90
```

## 実践ポイント
- まず npx で手元スキャンしてレポート確認。  
- CIに組み込み、--min-scoreで品質ゲートを設定（例90）。  
- SDKの命名規約が違う場合は sdkdrift.config.yaml の mapping で operationId をマップする。  
- 日本語ドキュメントやテストフィクスチャを用意して、チーム運用ルールに組み込むと効果が高い。
