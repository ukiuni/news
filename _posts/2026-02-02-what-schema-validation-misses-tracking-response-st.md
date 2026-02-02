---
layout: post
title: "What schema validation misses: tracking response structure drift in MCP servers - スキーマ検証が見落とすもの：MCPサーバーにおけるレスポンス構造のドリフト追跡"
date: 2026-02-02T02:06:55.608Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/dotsetlabs/bellwether"
source_title: "GitHub - dotsetlabs/bellwether: Open-source testing tool for Model Context Protocol (MCP) servers. Detect breaking schema changes before they reach production. Free deterministic validation with optional LLM-powered behavioral exploration. CI/CD ready with GitHub Actions support."
source_id: 411555715
excerpt: "MCPのJSONレスポンス変化をCIで自動検出しsilent breakを防ぐBellwether"
image: "https://opengraph.githubassets.com/b99b840c3b267c660c9191e5b69e50e08ca0e87d0ac834fe0699ca908823e8bc/dotsetlabs/bellwether"
---

# What schema validation misses: tracking response structure drift in MCP servers - スキーマ検証が見落とすもの：MCPサーバーにおけるレスポンス構造のドリフト追跡
クリックせずにはいられないタイトル: AIツール連携で「いつの間にか壊れている」を防ぐ――MCP用の無料ドリフト検知ツール「Bellwether」を使って先回りテスト

## 要約
Bellwetherは、MCP（Model Context Protocol）で公開されるツールのJSONスキーマ変更（ドリフト）をCIで自動検出し、実稼働前に破壊的変更を防ぐオープンソースツールです。軽量な決定的チェックと、必要に応じたLLM駆動の挙動探索を提供します。

## この記事を読むべき理由
日本でもAIアシスタントと外部ツール連携（社内データアクセス、API連携、自動化フロー）が増えています。仕様変更で会話型アプリが黙って壊れる「silent break」はユーザー信頼と業務に直結するため、CI段階での自動検知は必須です。

## 詳細解説
- MCPとは：ClaudeなどのAIアシスタントが外部ツール（ファイル操作、DB、API）を呼ぶ際のプロトコル。各ツールはJSONスキーマで能力を定義する。  
- 問題点：スキーマのパラメータ名変更、型変更、必須化、ツール削除などが発生するとAIのフローが静かに失敗する。従来のスキーマ検証だけでは「いつ」「どの変更が影響するか」をCIで把握しづらい。  
- Bellwetherのアプローチ：  
  - checkモード（無料・決定的）：サーバーの現在のレスポンスを既存のベースラインと比較して「ドリフト」を検出。CIで毎PR実行して早期検出。  
  - exploreモード（任意・LLM利用）：ローカルや深掘り解析でLLMを使って振る舞い探索（OllamaやOpenAI等のAPIが必要）。  
- 検出できる事象：ツール追加/削除、パラメータの必須化/型変更、パラメータ名のリネーム、説明文の変更、性能退化（遅延）などを重大度（breaking/warning/info）で返す。  
- CI統合：ベースラインをgit管理しておき、PRで bellwether check を走らせ、重大度に応じてジョブを失敗させられる（fail-on-severity）。GitHub Actions用の公式Actionも提供。  
- 主要コマンド：init（設定生成）、check（ドリフト検出）、baseline save/compare/accept、explore（LLM探索）。終了コードは重大度に応じて設定され、CIでの自動判断に使える。

## 実践ポイント
- ローカル導入（最短）：
```bash
# bash
npm install -g @dotsetlabs/bellwether
bellwether init npx @mcp/your-server
bellwether check
```
- ベースライン保存とCI連携（推奨ワークフロー）：
```bash
# bash
bellwether baseline save
git add bellwether.yaml bellwether-baseline.json
git commit -m "Add Bellwether baseline"
```
- GitHub Actionsでの簡単設定（例）：
```yaml
# yaml
- uses: dotsetlabs/bellwether@v1
  with:
    server-command: 'npx @mcp/your-server'
    baseline-path: './bellwether-baseline.json'
    fail-on-severity: 'warning'
```
- ローカルで深掘りするならOllamaを使えばLLMコストを抑えられる（exploreモード）。OpenAI/AnthropicはAPIキーが必要。  
- 運用提案：ベースラインはリリース時に更新（意図的な変更は baseline accept で記録）、PRで自動検出→レビューで意図しないドリフトを阻止。

短期間で導入でき、MCPベースのAIサービス運用品質を上げる実用的なツール。まずは check をCIに入れて「silent break」を防ごう。
