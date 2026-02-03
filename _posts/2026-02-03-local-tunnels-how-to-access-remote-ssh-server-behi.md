---
layout: post
title: "Local tunnels - how to access remote SSH server behind NAT - NAT越しのリモートSSHサーバにアクセスするローカルトンネル"
date: 2026-02-03T14:06:43.795Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/amak-tech/port-buddy"
source_title: "GitHub - amak-tech/port-buddy: Expose local ports to the internet in seconds"
source_id: 410283853
excerpt: "数コマンドでNAT越しのSSHやWebhookをSSL公開するPortBuddy"
image: "https://opengraph.githubassets.com/90f04d2350ce088755285801e0b561d298574e63509b27a96494e53667291283/amak-tech/port-buddy"
---

# Local tunnels - how to access remote SSH server behind NAT - NAT越しのリモートSSHサーバにアクセスするローカルトンネル
ポートを一瞬で外に出す「PortBuddy」で、ローカル開発やNAT越しアクセスが劇的に楽になる理由

## 要約
PortBuddyはローカルやプライベートネットワーク上のポートを公開する軽量なトンネルサービスで、HTTP/TCP/UDPをSSL対応で外部公開できるツールです。CLIで数コマンド、ダッシュボードで管理できます。

## この記事を読むべき理由
自宅や社内ネットワーク（NAT）で開発・検証している日本のエンジニアにとって、外部からのアクセス（Webhook受信、リモートDB接続、リモートSSHなど）を安全かつ手軽に実現できる手段は必須です。PortBuddyはngrokに似た使い勝手で、SSL・WebSocket・パスコード保護など実務で欲しい機能が揃っています。

## 詳細解説
- 基本機能：HTTP/TCP/UDPトンネル、デフォルトでHTTPにSSLを付与、WebSocket対応、静的サブドメインやカスタムドメイン、パスコードでのプライベート化。
- 使い方（概念）：CLIで認証（APIトークン）→ローカルポートを指定して公開。例：HTTPはポート番号だけ、TCP/UDPはモード指定。
- CLIとアーキテクチャ：CLIはJava 25 + GraalVMでネイティブ実行可能、サーバ側はSpring Bootを中心にnet-proxy/gateway/eureka/ssl-serviceなどのモジュールで構成。自己ホストはDocker Composeで立ち上げ可能。
- 開発・運用要件：公式CLIのダウンロードで即利用可能。構築するならJava 25、Maven、Docker、Node.jsなどが必要。サブスクリプションにより同時トンネル数やカスタムドメイン対応が異なる（無料は1トンネルまで）。
- セキュリティ面：SSL自動発行、トンネルのパスコードやAPIトークンで制御可能だが、公開サービスになるため最小権限・ログ監視・期限付きでの公開を推奨。

例：CLI操作（ログイン→公開）
```bash
# トークンで初期化
portbuddy init YOUR_API_TOKEN

# HTTPでローカル3000番を公開
portbuddy 3000
# 出力例: https://abc123.portbuddy.dev に公開

# TCPでPostgres（ローカル5432）を公開
portbuddy tcp 5432

# UDPサービスを公開
portbuddy udp 9000
```

## 実践ポイント
- Webhook受信やリモートデバッグはまず無料枠で試す。SSL付きで外部テストが簡単。
- 機密性の高いサービスはパスコード・IP制限・短期間のみ公開する。APIトークンは都度再発行。
- 自社運用や企業ポリシーが厳しい場合は、リポジトリをDocker Composeで自己ホストしてネットワーク設計を統制する。
- 日本の開発環境では家庭回線や法人のプロキシ/NATが多いので、TCP/UDPの透過性を試してから運用に移すと安全。

元のリポジトリは PortBuddy（Apache-2.0）で、実プロジェクトに使う前にREADMEとライセンス、サブスク条件を必ず確認してください。
