---
layout: post
title: "Show HN: Moltis – AI assistant with memory, tools, and self-extending skills - Moltis — メモリ、ツール、自己拡張スキルを備えたAIアシスタント"
date: 2026-02-13T21:24:47.994Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.moltis.org"
source_title: "Moltis: Your Personal AI Assistant"
source_id: 46993587
excerpt: "ローカルで動く自己拡張AIアシスタント、記憶・ツール連携・セキュリティで機密業務を安全に効率化"
image: "https://moltis.org/og-social.jpg?v=4"
---

# Show HN: Moltis – AI assistant with memory, tools, and self-extending skills - Moltis — メモリ、ツール、自己拡張スキルを備えたAIアシスタント
魅力的な日本語タイトル: ローカルで動く“賢い助手”Moltis — 記憶・ツール・自動拡張で仕事が変わる

## 要約
Moltisは「一つの自己完結バイナリ」で動き、ローカルLLM・長期記憶・ツール連携・実行時にスキルを生成する自己拡張を備えたオープンソースのAIアシスタントです。プライバシー重視のローカル運用からクラウド展開まで対応します。

## この記事を読むべき理由
日本企業や個人開発者が機密データを扱う際、クラウドに頼らずにモデルや履歴を管理できるソリューションは極めて重要です。MoltisはローカルLLMや細かなアクセス制御、監査向けの可観測性を持ち、国内のセキュリティ/コンプライアンス要件に合致しやすい選択肢です。

## 詳細解説
- 配布形態と起動
  - シングルバイナリでランタイム依存がほぼ不要。Homebrew、cargo、deb/rpm、Docker、AppImageなど多様な配布があるため、macOS（Apple Silicon含む）やLinuxサーバへ容易に導入可能。
- ローカルLLMとハイブリッド構成
  - ローカルのGGUFフォーマット埋め込みを自動ダウンロードして使えるほか、OpenAIやCopilotなどクラウドプロバイダとのフォールバックチェーンをサポート。オフライン運用とクラウド利活用を両立。
- 記憶と検索
  - 長期記憶はベクトル検索＋全文検索(FTS)のハイブリッド。埋め込みキャッシュやファイル監視で履歴を即座に同期・検索可能。
- 安全な自動化とブラウジング
  - ブラウズや自動化タスクは隔離されたDockerコンテナで実行。SSRF対策としてループバックやプライベートIPへのファッチをブロック。
- スキルと自己拡張
  - MCP（ツールサーバ）やフックで外部ツールを統合。Piに触発された自己拡張でランタイムにスキルを生成・ホットリロードし、セッション分岐も可能。
- UI／チャネルと可観測性
  - Web UI、Telegram、JSON-RPC API、PWAなど複数チャネルを同じエージェントで提供。Prometheus、OpenTelemetry、構造化ログ、SQLite永続化で運用監視がしやすい。
- セキュリティ機能
  - WebAuthnパスキー、スコープ付きAPIキー、秘密情報のメモリ消去、ヒト承認ワークフロー、起源検証（CSWSH）を備え、安全設計が配慮されている。

## 実践ポイント
- まずはローカルで試す（推奨）
  - 簡単起動例:
  ```bash
  # Install via script
  curl -fsSL https://www.moltis.org/install.sh | sh

  # Dockerで試す（ポート13131）
  docker run -d --name moltis -p 13131:13131 \
    -v moltis-config:/home/moltis/.config/moltis \
    -v moltis-data:/home/moltis/.moltis \
    -v /var/run/docker.sock:/var/run/docker.sock \
    ghcr.io/moltis-org/moltis:latest
  ```
- セキュリティ設定
  - 初回セットアップでパスキーやスコープ付きAPIキーを有効にし、ツール（MCP）やファイルアクセス権は最小権限で与える。
- ローカルLLMを活用
  - 機密情報や社内ドキュメントを扱う場合はローカルモデル＋オンプレ検索でプライバシーを確保。
- 運用監視
  - Prometheusやログでプロバイダごとのメトリクスを追い、ツール実行履歴を定期的にレビューする。
- 注意点
  - 現時点でアルファ段階の機能もあるため、本番環境では権限とアクセス制御を厳格に。自動生成されるスキルは検証してから利用すること。

Moltisは「自分専用かつ拡張可能な」AIアシスタントをローカルやクラウドで実現し、特にデータ保護が重要な日本のユースケースに親和性があります。興味があれば公式サイト（https://www.moltis.org）とGitHubのドキュメントで詳細を確認してください。
