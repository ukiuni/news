---
layout: post
title: "Show HN: Distr 2.0 – A year of learning how to ship to customer environments - Distr 2.0：顧客環境へ届けるための1年の学び"
date: 2026-02-10T14:15:20.351Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/distr-sh/distr"
source_title: "GitHub - distr-sh/distr: The Open Source control plane for self-managed, BYOC, and on-prem deployments. Everything you need to distribute applications to self-managed customers out of the box."
source_id: 46958742
excerpt: "オンプレ/BYOC向けOSS『Distr』で顧客環境へ安全にソフト配布・運用を即試せる方法を紹介"
image: "https://opengraph.githubassets.com/324ed5060fe48312f916fb77134e9438e581310d8f45561cbd44821098b7400c/distr-sh/distr"
---

# Show HN: Distr 2.0 – A year of learning how to ship to customer environments - Distr 2.0：顧客環境へ届けるための1年の学び
オンプレ・BYOC時代のソフト配布を一気通貫で解決するOSS「Distr」を試してみたくなる紹介

## 要約
Distrは、セルフホスト／BYOC／オンプレ向けにアプリ配布を簡素化するオープンソースのコントロールプレーンで、管理UI・エージェント・OCIレジストリ・ライセンス管理などを備え即戦力で使えるのが特徴です。

## この記事を読むべき理由
日本企業はデータ所在地・ガバナンス要件でオンプレや専用クラウドを求められることが多く、Distrはそうした顧客先環境へ安全にソフトを配布・運用するための実用的な選択肢になるからです。

## 詳細解説
- 何をするプロジェクトか  
  Distrは「自社が作ったソフトを、顧客の管理する環境へ配布・管理する」ための制御平面（Hub + Agent）です。中央のHubから各顧客のAgentに対してデプロイ、ログ収集、リモートトラブルシュート、バージョン制御やライセンス配布を行えます。

- 主な機能  
  - 中央管理UI：全デプロイ／アーティファクト／エージェントを可視化。  
  - エージェント（Docker/Helm対応）：顧客環境でのデプロイ自動化と診断。  
  - 組み込みOCIレジストリ：DockerイメージやHelmチャートを配布し、細かなアクセス制御と分析を提供。  
  - ライセンス管理・ホワイトラベル顧客ポータル：顧客側での操作や特定バージョン配布を制御可能。  
  - SDK（現状JavaScript）とMCPサーバ：アプリケーションやLLMクライアントからの連携用APIを提供。

- 技術スタックと導入形態  
  Go（バックエンド）＋TypeScript/Angular（フロント）を中心に、PostgreSQLやオブジェクトストレージ（S3互換）を利用。配布はDocker ComposeかHelmチャートで自己ホスティング可能。開発要件は Node.js 22、Go 1.25など。

- アーキテクチャ（簡易）  
  Hub（中央） ⇄ OCIレジストリ / DB / S3、Hub ⇄ 各顧客のAgent（エージェントがアプリへデプロイ・監視）。Agentはインターネット経由でHubと通信し、顧客側で動作します。

## 実践ポイント
- まずはローカルで動かす（Docker版のクイックスタート）:
```bash
# bash
mkdir distr && cd distr
curl -fsSL https://github.com/distr-sh/distr/releases/latest/download/deploy-docker.tar.bz2 | tar -jx
# .env を必要に応じて編集してから
docker-compose up -d
# 管理画面にアクセス
# http://localhost:8080/register
```
- Kubernetes環境では公式Helmチャートを利用（本番ではvalues.yamlを見直す）。  
```bash
# bash
helm upgrade --install --wait --namespace distr --create-namespace \
  distr oci://ghcr.io/distr-sh/charts/distr \
  --set postgresql.enabled=true --set minio.enabled=true
```
- 日本の導入検討で見るべき点：認証・ネットワーク（顧客側ファイアウォール越え）、監査ログ、SLA、データ所在地、ライセンス配布ポリシー。また既存CI/CDや社内レジストリとの統合を計画すること。  
- 拡張と運用：エージェントを使ったリモート診断、自社プロダクトからのSDK連携、OCIアーティファクトの権限制御を活用して顧客向け配布フローを自動化する。

短時間で試せ、オンプレ要件のある日本のSaaS／ソフトウェア企業やSIerにとって実践的な選択肢になります。興味があれば公式ドキュメント（distr.sh）で自己ホスト手順やSDKを確認してください。
