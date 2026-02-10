---
layout: post
title: "Show HN: Pipelock – All-in-one security harness for AI coding agents - Show HN: Pipelock — AIコーディングエージェント向けオールインワン・セキュリティハーネス"
date: 2026-02-10T13:11:51.481Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/luckyPipewrench/pipelock"
source_title: "GitHub - luckyPipewrench/pipelock: Security harness for AI agents — egress proxy with DLP scanning, SSRF protection, MCP response scanning, and workspace integrity monitoring"
source_id: 46958597
excerpt: "1行のcurlで秘密が盗まれる前に防ぐPipelockプロキシツール"
image: "https://repository-images.githubusercontent.com/1152497359/9b6fc1b5-1f76-4bf7-ba53-4f1e3c3d7bb5"
---

# Show HN: Pipelock – All-in-one security harness for AI coding agents - Show HN: Pipelock — AIコーディングエージェント向けオールインワン・セキュリティハーネス
AIエージェントが「1行のcurl」で秘密を盗まれる前に止める──開発現場で即使えるプロキシ型防御ツール

## 要約
Pipelockは、シークレットを持つAIプロセスをネットワークから分離し、シンプルなフェッチプロキシを介して全通信を7層で検査するGo製のワンバイナリ。DLP、SSRF防止、プロンプト注入検出、ワークスペース整合性監視などを提供します。

## この記事を読むべき理由
日本でもIDE内やCIでLLMを使った自動化が進んでおり、APIキーや環境変数の流出リスクは現実的です。金融・医療・大企業のシステムでは内部ネットワークやコンプライアンス要件に合う“エージェント脅威対策”が求められており、Pipelockはその即戦力になります。

## 詳細解説
- 基本アーキテクチャ  
  - 「特権ゾーン（AIエージェント：シークレットあり）」と「フェッチゾーン（プロキシ：シークレット無し）」を分離。エージェントは直接外部へ接続せず、プロキシ経由でのみURL取得を行う。
  - すべてのリクエストはプロキシ内のスキャナーパイプラインを通過し、危険性を判定してからエージェントへ返す。

- 7層の主な検査機能  
  - SSRF/内部IPブロック・DNSリバインディング防止  
  - ドメインブロックリスト（例：pastebin等の外部転送先）  
  - レート制限・サイズ制限（データこっそり分割送信を防止）  
  - DLPパターン（APIキーやAWSキー等の正規表現）  
  - 環境変数漏洩検出（生/Base64化のしきい値＋エントロピー）  
  - エントロピー解析（暗号化・エンコードされたデータ片を検出）  
  - URL長チェック

- レスポンス検査（プロンプト注入対策）  
  - フェッチしたコンテンツをプロンプト注入、システムロール上書き、DAN等の脱獄パターンでスキャン。結果に応じて block / strip（赤線で削る）/ warn / ask（TTYで確認）を選択可能。

- ワークスペース整合性と署名  
  - SHA256マニフェストでファイルの追加・変更・削除を検知。git差分スキャン用のフックスクリプトやCI用のコマンドも用意。エージェント間の信頼はEd25519で署名・検証。

- 運用モードと導入の柔軟性  
  - strict（厳格）/ balanced（デフォルト）/ audit（ログのみ）プリセット。単一バイナリで依存無し、Dockerイメージも提供。Prometheusメトリクス、JSON監査ログ対応でCIや監視に組み込みやすい。

- 対応ユースケース  
  - Claude CodeやCursorのようなMCP（Model Context Protocol）ラップ、ローカルプロキシでのIDE連携、CIパイプラインでの差分シークレット検出などに適合。

## 実践ポイント
- とりあえず動かす（ローカル検証）:
```bash
# (bash) Go環境があれば
go install github.com/luckyPipewrench/pipelock/cmd/pipelock@latest
pipelock generate config --preset balanced -o pipelock.yaml
pipelock run --config pipelock.yaml
```
- まずは audit モードでログを見て、誤検知を調整してから balanced/strict に移行する。  
- CI導入：GitHub ActionsやGitLab CIで差分スキャン（git diff | pipelock git scan-diff）を回す。  
- 日本向けカスタムDLP：社内APIキー形式や社外送信先ドメインをpatterns/blocklistに追加する。  
- 高セキュリティ運用では、エージェントを内部-onlyネットワークで動かし、フェッチはPipelockコンテナのみが外部へ出られる構成にする。  
- 監視連携：PrometheusメトリクスとJSON監査ログをSIEMやログ基盤に流し、インシデント時の追跡を簡素化する。

Pipelockは「AIエージェントが持つ秘密を守る」ための実用的なレイヤーを提供します。まずは監査モードで現状把握→CI組み込み→段階的に強化、が現場導入の王道です。
