---
layout: post
title: "What are you doing this week? - 今週は何してる？"
date: 2026-03-02T11:12:59.395Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lobste.rs/s/dppelv"
source_title: "What are you doing this week? | Lobsters"
source_id: 1325180725
excerpt: "Rust×Wasmやorg-mode、Terraform移行など実務で使える今週の実践ネタ"
image: "https://lobste.rs/story_image/dppelv.png"
---

# What are you doing this week? - 今週は何してる？

魅力的タイトル案: ちょっと覗き見！エンジニアたちの「今週やってること」から学ぶ小さな実践ネタ

## 要約
海外コミュニティの短い投稿から、Rust＋WebAssemblyの個人プロジェクト、org-modeでのCRM運用、サーバーレス→Terraform移行、画像から動的配色を作る試みなど、今すぐ参考になる実務＆趣味の取り組みが見えてきます。

## この記事を読むべき理由
現場で役立つ小さなヒントが詰まっており、特に日本でも注目が高まっているRust/Wasmtime/WasmやInfrastructure as Code（IaC）、ActivityPubやUIの自動配色といったトピックに触れられるため、学習やプロジェクトのネタにしやすいからです。

## 詳細解説
- 個人プロジェクト（Rust + WebAssembly）  
  抜粋では「クリケット（競技）シミュレーションエンジン」をRustで実装し、WebAssemblyでブラウザ実行しているとあります。Rustは高速・安全性が強みで、計算負荷の高いシミュレーションをブラウザで動かす用途に特に適しています。Wasmにすることでフロントエンドとの連携が容易になり、ユーザー向けインタラクティブ体験を低レイテンシで提供できます。

- 個人的ワークフロー（org-mode と Monica CRM）  
  Emacsのorg-modeを用いてCRM的な情報管理を組み立てる例。個人でオープンソースCRM（Monicaなど）を運用・再現することで、既存サービスに依存せずプライバシーを保った管理が可能になります。org-modeはタスク、メモ、テンプレート管理に強く、日本のエンジニアの生産性向上にも有用です。

- インフラ移行（Serverless + ElastiCache → Terraform + Valkey）  
  仕事でServerlessとElastiCacheベースの構成からTerraformを用いた管理へ移行中、イベントトリガーをSNSキューに切り替えるとあります。Terraformでインフラをコード化すると、再現性・レビュー・CI統合が容易になり、大規模サービスでも運用負担を下げられます。SNS（Amazon Simple Notification Service）はイベント駆動アーキテクチャの疎結合なメッセージングとしてよく使われます。

- デザイン周り（画像ベースの動的配色）  
  rampensauやfettepaletteといったライブラリを使い、入力画像から動的にカラーパレットを生成してActivityPubサービスのテーマに反映する試み。画像解析→配色生成はUIの一貫性を保ちつつ個性的なテーマを作る手法で、日本のサービスでも差別化に役立ちます。

- グラフィックス系の知識共有  
  「グラフィックスプログラミングのリソースページを作っている」という投稿もあり、学習リソースをまとめる動きはコミュニティでの知識伝播に貢献します。

## 実践ポイント
- Rust＋Wasmを試すなら、まず小さな計算モジュール（物理シミュレーションやパスファインディング）をWasm化してブラウザで動かしてみる。  
- org-modeをCRM用途で使う場合、テンプレートとプロパティを定義して自動化（capture と agenda）を導入すると効果的。  
- インフラ移行は段階的に行う（テスト環境→カナリア→本番）／Terraformは状態管理と変化差分を必ず確認する。SNS等のイベント切替では遅延や再試行の挙動をテストすること。  
- 画像から配色生成を試すには、既存のライブラリ（上述のようなもの）で色抽出→コントラストチェック→アクセシビリティ確認の流れを作る。  
- 興味がある分野は小さな「今週のタスク」を立てて週単位で実験を回すと学習が続きやすい。

以上を参考に、まずは一つ小さな実験を週内でやってみることをおすすめします。
