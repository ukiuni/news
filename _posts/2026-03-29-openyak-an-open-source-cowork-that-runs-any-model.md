---
layout: post
title: "OpenYak – An open-source Cowork that runs any model and owns your filesystem - OpenYak：あらゆるモデルを動かし、ファイルを完全に掌握するオープンデスクトップAI"
date: 2026-03-29T05:36:34.256Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/openyak/desktop"
source_title: "GitHub - openyak/desktop: Yak is all you need · GitHub"
source_id: 47560380
excerpt: "OpenYakは機密データを外に出さずローカルで自動化・解析するデスクトップAI"
image: "https://opengraph.githubassets.com/aec59cd1cd61c63c61573f29ab61af1d9de8247aa69870c6c229ed107b5d69da/openyak/desktop"
---

# OpenYak – An open-source Cowork that runs any model and owns your filesystem - OpenYak：あらゆるモデルを動かし、ファイルを完全に掌握するオープンデスクトップAI

魅力的なタイトル案：ローカルで完結するAIアシスタント「OpenYak」が日本の業務を変える理由

## 要約
OpenYakはローカル中心のオープンソースデスクトップAIで、ファイル操作・データ解析・自動化・メッセージ連携をクラウドに上げずに実行できるツールです。多数のモデル接続やBYOK対応、エージェント機能を備えます。

## この記事を読むべき理由
データ取り扱いとプライバシーが厳しい日本企業やスタートアップにとって、「クラウドに送らないAI」は即戦力になります。社内文書や顧客データを外に出さず高度な自動化・分析を実現できる点は実務価値が高いです。

## 詳細解説
- アーキテクチャ：デスクトップ向けフレームワーク（Tauriを想定する構成）でフロント／バックエンドが分かれ、主要言語はPythonとTypeScript中心。リポジトリはAGPL-3.0ライセンス。
- ローカルファースト：ファイル読み書き、バッシュ実行、検索（glob/grep）などをローカルで完結。長期メモリも端末保存でテレメトリなし。
- モデル接続：OpenRouter経由でClaude、GPT系、Gemini等多数の最新モデルを利用可能。さらに自分のAPIキー(BYOK)を20以上のプロバイダで使えるためコスト管理やレギュレーションに柔軟対応。Ollama等でローカルモデルを動かすことも可能。
- エージェントとツール：7種のエージェントモード（ビルド、計画、探索など）やマルチステップツール呼び出し、サブエージェントをサポート。ファイル編集、長期記憶、Web fetchなど20以上の組込ツールが自動化を強力に支援。
- インテグレーション：OpenClaw経由でWhatsApp、Discord、Telegram、Slack、Feishu、Signal、iMessageなど複数チャネルと連携。日本市場向けにはLINEや企業向けチャネル連携の追加検討がポイント。
- 運用機能：cronベースの定期ジョブ、監査可能なファイル変更ログ、セキュアなワンタッチトンネル（QRで端末接続）でリモートワークにも対応。
- 開発者向け：frontend/README.md、backend/README.mdでビルド手順あり。OSSとして拡張やカスタムコネクタ作成が可能。

## 実践ポイント
- まずはインストーラー（Windows/macOS）で試し、無料モデル1Mトークン枠で感触を掴む。  
- 自社規程でAPIを使うならBYOKをセットしてデータ流出リスクを低減。  
- 機密データの分析やレポート自動生成はローカル実行で即効果。医療・金融のPoC候補。  
- チャット連携で社内通知を一元化。日本向けはLINE連携や社内SaaSへの接続を検討。  
- 利用・導入前にAGPL-3.0の商用影響を法務に確認すること。

原典（ソース）: OpenYak リポジトリ（GitHub: openyak/desktop）
