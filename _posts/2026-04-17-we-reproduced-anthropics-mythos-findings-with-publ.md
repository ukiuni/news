---
layout: post
title: "We Reproduced Anthropic's Mythos Findings with Public Models - 公開モデルでAnthropicのMythos結果を再現した話"
date: 2026-04-17T14:59:16.929Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.vidocsecurity.com/blog/we-reproduced-anthropics-mythos-findings-with-public-models"
source_title: "We Reproduced Anthropic&#x27;s Mythos Findings With Public Models - Vidoc Security Lab"
source_id: 47806116
excerpt: "公開モデルでMythosの多数事例を再現、検証体制と自動化で実運用化を急げ"
image: "https://blog.vidocsecurity.com/og/we-reproduced-anthropics-mythos-findings-with-public-models"
---

# We Reproduced Anthropic's Mythos Findings with Public Models - 公開モデルでAnthropicのMythos結果を再現した話
魅力的な日本語タイトル: 「Mythosは特権じゃない――公開モデルで“深刻バグ発見”は既に再現可能になった」

## 要約
Anthropicが示した「Mythos」はフロンティアAIの脆弱性発見力を示すが、Vidocの再現実験ではGPT-5.4とClaude Opus 4.6（オープンなAPI＋opencodeハーネス）で主要な事例の多くを再現できた。差分は「発見」から「検証／実運用化」へ移っている。

## この記事を読むべき理由
日本のソフトウェア開発・セキュリティ担当者は、モデルの「発見力」が専有物ではない現実を理解し、検証ワークフローやパッチ対応の体制を今のうちに整える必要があるため。

## 詳細解説
- 再現環境と手法  
  - 利用したのは opencode（オープンソースのコーディングエージェント）と公開APIベースのGPT-5.4、Claude Opus 4.6。  
  - ワークフローは「コードベースの分割調査 → ファイルランク付け → 並列試行 → 人手による2次レビュー」で、Anthropicが公開した手順に近い流れ。  
  - 1ファイル当たりのスキャンコストは概ね$30未満。

- 主な再現結果（要点）  
  - 成功（両モデルで安定再現）：FreeBSD（NFSのメモリ破壊系）、Botan（証明書トラストの誤り）。  
  - モデル差あり：OpenBSDの長年残存バグはClaude Opusが3/3で再現、GPT-5.4は0/3。  
  - 部分的再現：FFmpegやwolfSSLは両モデルとも「有望な手がかり」は出すが完全再現には至らず。  
  - 意味合い：脆弱性の「発見」は公開モデルでも既に可能。実際の難所は出力の検証・優先順位付け・攻撃パスの自動化（エクスプロイト化）であり、ここがまだ“競争上の堀”になっている。

- 技術的示唆  
  - 単純なパターンマッチやヒューリスティック以上に、状態推論や証明書ロジックへの理解が必要な問題も公開モデルで扱える例が出ている。  
  - モデルごとに得意／不得意があり、複数モデル＋繰り返し試行で成功確率が上がる。

## 実践ポイント
- まず受け入れるべき現実：モデルによる脆弱性発見は既に公開範囲で現実的。秘密扱いにしすぎず、検出と検証の体制を整える。  
- 短期アクション（すぐできる）  
  - 重要コードのモデル支援スキャンを試行（opencodeのようなハーネスを利用）。  
  - 出力は「人による二次レビュー」で必ず検証。誤検出を前提にワークフロー化する。  
  - コスト感を把握：小規模なファイル単位スキャンなら現実的な費用で回せる。  
- 中長期対策  
  - パッチ優先度とエクスプロイト可能性評価を自動化する基盤を作る（検証用テストベッド、差分実行、メモリ解析ツール連携）。  
  - サプライチェーンや証明書処理など「ロジック系」脆弱性に注意し、セキュリティレビューの観点を拡張する。  
  - 複数モデルや手法を組み合わせた検査を定期化して、発見→検証→修正のリードタイムを短縮する。

以上。公開モデルの脅威と利点を正しく評価し、実務的な検証・修正ワークフローに投資することが日本の現場にとっての優先課題です。
