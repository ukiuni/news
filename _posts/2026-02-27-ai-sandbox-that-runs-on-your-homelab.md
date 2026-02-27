---
layout: post
title: "AI sandbox that runs on your homelab - ホームラボで動くAIサンドボックス"
date: 2026-02-27T14:09:20.603Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/deevus/pixels"
source_title: "GitHub - deevus/pixels: Disposable Linux containers for AI coding agents, powered by TrueNAS and Incus."
source_id: 792253050
excerpt: "TrueNAS+Incusで簡単構築、ZFSスナップショットで安全に使えるAIエージェント実験環境"
image: "https://opengraph.githubassets.com/da89e607fe671a2fd77544e72c9c9440b8eeec226ca6edc8d0309998ca3c9bcf/deevus/pixels"
---

# AI sandbox that runs on your homelab - ホームラボで動くAIサンドボックス
魅せるタイトル: 手元のNASで動く「AIの実験場」──TrueNAS×Incusで安全に試せるAIエージェント環境

## 要約
TrueNAS SCALE + Incus上で使えるCLIツール「pixels」は、AIコーディングエージェント用の使い捨てコンテナを素早く作成・復元・破棄できるサンドボックスを提供します。ZFSスナップショットによるチェックポイント、SSHアクセス、外向き通信の厳格な制御が特徴です。

## この記事を読むべき理由
ローカルでAIエージェント（コード生成や自動化ワークフロー）を安全に試したい日本の開発者やホームラボ運用者にとって、クラウドに頼らずプライバシーと再現性を確保しつつ素早く実験できる現実的な選択肢だからです。

## 詳細解説
- アーキテクチャ概要  
  - pixelsはTrueNAS SCALEのIncus仮想化APIを使うCLIツール（Go製）で、コンテナを作成・開始・停止・破棄します。内部でコンテナをZFSスナップショット（チェックポイント）として管理し、スナップショット間のクローンで同一状態の複数インスタンスを作れます。  
- エージェント環境の自動プロビジョニング  
  - 新しいコンテナにはSSH公開鍵注入、miseやNode.js、Claude Code / Codex / OpenCodeなどの開発ツールを非同期でインストール（設定で無効化可）。`--console`でインストール完了まで待てます。  
- ネットワーク（エグレス）制御  
  - outboundは3モード（unrestricted / agent / allowlist）。agentプリセットはAnthropic・OpenAI等のAI API、npm/PyPI/aptなどのパッケージレジストリ、GitHub等を許可するプリセット。内部はnftablesで制御、pixelユーザーには限定的なsudoしか付与しません。  
- 運用上の特徴と制約  
  - ローカルキャッシュでIP取得を最適化。TrueNASのWebSocket API経由で管理。注意点としては、root権限やcap_net_adminを持つプロセスがegress制御を回避できる可能性があり、SECURITY.mdに脅威モデルと緩和策が記載されています。

## 実践ポイント
- 必要環境（ざっくり）  
  - TrueNAS SCALE（Incus有効化）、TrueNAS APIキー、Go 1.25+（ソースビルド時）、SSH鍵ペア。  
- すぐ試せる基本コマンド
```bash
# pixelsをインストール
go install github.com/deevus/pixels@latest

# ベースを作ってコンソールを開く（agentエグレスを有効）
pixels create base --egress agent --console

# チェックポイント作成
pixels checkpoint create base --label ready

# チェックポイントから複製
pixels create task1 --from base:ready

# ネットワーク許可ドメイン追加
pixels network allow task1 api.example.com
```
- 日本での活用案  
  - オフライン環境や社内ネットワーク制約のある案件でのLLM連携実験、SaaSに出せないコード/データでの検証、CI前段の安全な自動化エージェント検証環境。  
- セキュリティ注意点  
  - egress制御はコンテナ内部のnftablesに依存するため、ホスト・管理者権限のアクセス制御やTrueNAS自体の管理を厳格にすること。

原リポジトリ: deevus/pixels (MIT) — TrueNAS + Incusで手元に作るAIエージェント用の disposable コンテナ群。
