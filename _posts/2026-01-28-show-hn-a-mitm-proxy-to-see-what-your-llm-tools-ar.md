---
layout: post
title: "Show HN: A MitM proxy to see what your LLM tools are sending - LLMツールが送るデータを可視化するMitMプロキシ"
date: 2026-01-28T22:20:59.316Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/jmuncor/sherlock"
source_title: "GitHub - jmuncor/sherlock: Intercept LLM API traffic and visualize token usage in a real-time terminal dashboard. Track costs,       debug prompts, and monitor context window usage across your AI development sessions."
source_id: 46799898
excerpt: "mitmproxyでLLM通信を可視化し、トークン課金とプロンプトをリアルタイム監視"
image: "https://opengraph.githubassets.com/7388d404bf795194a99ee8626a030133e7748b9ab08fb805bf8c8cf09a2c9f1e/jmuncor/sherlock"
---

# Show HN: A MitM proxy to see what your LLM tools are sending - LLMツールが送るデータを可視化するMitMプロキシ
魅力タイトル：LLMの「黒箱」を覗く—トークン課金もプロンプトも丸見えにするターミナル・インスペクター

## 要約
Sherlockはmitmproxyを使ってLLM APIのHTTPS通信を中間で傍受し、リアルタイムでトークン消費やプロンプトをターミナル上に可視化するツールです。コスト追跡・プロンプトのデバッグ・コンテキスト上限の監視が手軽にできます。

## この記事を読むべき理由
日本でもLLMを業務導入・試験運用する場面が増えています。API課金やコンテキスト切れ、プロンプト漏洩など「見えないコスト／リスク」を把握するために、通信内容を安全に観察できるツールは即戦力になります。

## 詳細解説
- 仕組み：Sherlockはmitmproxyをプロキシとして立て、HTTP(S)要求を解析してモデル名・トークン数・リクエスト本文を抽出。ダッシュボードに「Context Fuel Gauge（累積トークン量）」やリクエストログをリアルタイム表示します。
- 主な機能：
  - トークン使用量のライブ表示（モデル単位／累積）
  - コンテキスト上限に対する視覚的なゲージ（緑→黄→赤）
  - 受信したプロンプトをMarkdown/JSONで保存（後からレビュー可）
  - 追加のプロバイダ対応は設定ファイルとパーサーを追加して拡張可能
- 対応状況：現時点でAnthropic（Claude）対応。OpenAIやGoogleは「coming soon」として拡張可能設計。
- プライバシー／セキュリティ：mitmproxyは自己署名CAを生成してシステムにインストールする必要があります。企業利用時は社内ポリシーや法規（個人情報の扱い）を確認してください。
- 技術要件：Python 3.10+、Node.js（Nodeアプリの傍受時）。

簡単な流れ：
1. Sherlockを起動してCAをインストール（初回のみ）
2. LLMクライアントをプロキシ経由で動かす（環境変数 or sherlock run）
3. ターミナルでトークン使用量や保存されたプロンプトを確認

例（導入・実行コマンド）：
```bash
# リポジトリをクローンして開発モードでインストール
git clone https://github.com/jmuncor/sherlock.git
cd sherlock
pip install -e .

# Sherlockを起動（初回はCA作成と導入案内が出る）
sherlock start

# Node製ツールなどをプロキシ経由で起動
sherlock run --node node your-llm-app.js

# 環境変数を手動で設定する例
export HTTP_PROXY="http://127.0.0.1:8080"
export HTTPS_PROXY="http://127.0.0.1:8080"
```

証明書インストール例（macOS / Ubuntu）：
```bash
# macOS
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain ~/.mitmproxy/mitmproxy-ca-cert.pem

# Ubuntu/Debian
sudo cp ~/.mitmproxy/mitmproxy-ca-cert.pem /usr/local/share/ca-certificates/mitmproxy-ca-cert.crt
sudo update-ca-certificates
```

## 実践ポイント
- まずローカル環境で動作確認：sherlock start→自分のツールをsherlock runで動かし、トークン消費とプロンプト保存を確認。
- コスト管理：モデル別トークン使用量を見て、プロンプト長さや温度設定を調整しコスト最適化する。
- セキュリティ運用：社内で使う場合はCA導入手順とログ保存ポリシーを整備し、機微情報が含まれるプロンプトは扱いに注意。
- プロバイダ追加：自社で使うAPIホストが未対応なら、sherlock/config.pyにホスト追加、parser.pyにパーサを実装して即対応可能。

興味がある方はGitHubリポジトリ（jmuncor/sherlock）をチェックして、ローカルで一度「何が飛んでいるか」を可視化してみてください。
