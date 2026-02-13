---
layout: post
title: "My Business as Code - 私のビジネスをコード化する"
date: 2026-02-13T11:37:06.905Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.42futures.com/p/my-business-as-code"
source_title: "My Business as Code - by Daniel Rothmann - 42futures"
source_id: 442782990
excerpt: "プレーンテキスト×git×AIで個人事業の請求・顧客管理を自動化する実践手法"
image: "https://substackcdn.com/image/fetch/$s_!V4n0!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4f1823f7-00f6-481c-ac25-be38f2c41f52_1628x1028.png"
---

# My Business as Code - 私のビジネスをコード化する
ビジネスを「プレーンテキスト」で自動化する――個人事業の情報をコード化してAIと連携する現実的ワークフロー

## 要約
著者は自分の小さなソフトウェア事業で「Business-as-Code」を実践するツールFirmを作り、プレーンテキストDSL＋git＋CLI＋AIエージェントで業務データの記録・検索・自動化を行い、生産性と信頼性を高めた。

## この記事を読むべき理由
日本でもフリーランスやスモールスタートアップが増える中、監査・請求・顧客管理といった定型業務を「見える化」して自動化できればコスト削減とコンプライアンス強化になる。ツールの考え方は既存のSaaSに頼らず自分でデータ主導の運用基盤を作る実践的な手法を示す。

## 詳細解説
- 根本アイデア：クラウドインフラを宣言的に管理するTerraformの発想を業務データに応用。業務エンティティ（contacts, interactions, opportunities, projects, tasks, invoices…）をDSLで定義し、参照でグラフ化する。
- 技術要素：
  - Firm DSL：人間にも機械にも読みやすいプレーンテキストでエンティティを定義。バリデーション可能で差分管理がしやすい。
  - Graphモデル：各エンティティがノード、参照がエッジとなることで履歴追跡や関連検索が容易に。
  - CLI＋Queryエンジン：フィルタや関連ノード探索で未完タスクや新規リードを抽出。
  - MCPサーバ（Micro Connector Protocol的なもの）：ローカル／クラウドで変更を受け付け、検証・ブランチで運用。チャットアプリやエージェントから安全に操作可能にする。
  - AI連携：LLMやコード重視エージェント（例：Claude Code）を接続し、自然言語からDSL操作やクエリ発行、音声入力の取り込みで対話的に業務を更新。
- メリット：機械可検証な構造＋プレーンテキストの人間可読性、gitによるバージョン管理で自動化の安全性を確保。AIと人の「共通の表面」を作る点がポイント。
- 限界と用途：現状は技術者向けでCLI慣れが前提。大企業の複雑なプロセスに即適用できるかはまだ不明だが、小規模事業／プロトタイプには有効。

## 実践ポイント
- 小さく始める：まずは連絡先→会話→案件→タスクの簡易モデルをDSLで作る。
- gitで管理：全変更をブランチ運用・PRでレビューし、自動化の安全弁にする。
- クエリを作る：日次の未完タスク抽出や、新規リードのスコアリングなど汎用クエリを整備する。
- AI連携は段階的に：最初は読み取り専用でLLMにクエリさせ、信頼が得られたら書き込み権限を与える。
- 日本市場向けの応用：請求データを弥生やfreeeへ結合する、監査証跡をエクスポートして内部統制・ISMS対応に活用する。
- バリデーションと権限設計を固める：自動化が進むほど「誤操作のコスト」が上がるので、MCPやスキーマ検証を必ず導入する。
