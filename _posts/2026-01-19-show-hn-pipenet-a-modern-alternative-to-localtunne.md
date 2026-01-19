---
layout: post
title: "Show HN: Pipenet – A Modern Alternative to Localtunnel - Pipenet：Localtunnelのモダンな代替"
date: 2026-01-19T16:51:22.721Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://pipenet.dev/"
source_title: "pipenet"
source_id: 46680597
excerpt: "セルフホスト対応のPipenetでWebhook検証やリモート共有を安全に公開"
---

# Show HN: Pipenet – A Modern Alternative to Localtunnel - Pipenet：Localtunnelのモダンな代替
魅力的タイトル: 自分で運用できる「トンネリング」の新定番——Pipenetでローカルサービスを安全に公開する方法

## 要約
PipenetはLocaltunnelの設計を現代化したOSSトンネリングツールで、クライアントとサーバーを同梱しセルフホストやSDK組み込みに最適化されている。

## この記事を読むべき理由
ローカル開発で外部と連携（Webhook検証、リモートデモ、チーム共有）する機会が増えている日本の現場では、セキュリティやドメイン制御ができるセルフホスト型トンネルの需要が高い。PipenetはTypeScript/ES Modules対応でクラウド環境にも適し、既存ツールの代替として検討価値が高い。

## 詳細解説
- 基本コンセプト：Pipenetは1つのnpmパッケージでクライアントとサーバーを提供。パブリックサーバを使うか、自前でトンネルサーバを立ててドメインやTLSを管理できる。
- 対応プロトコル：HTTP/HTTPSの通常リクエスト、WebSocket（HTTP upgrade 経由）、SSE、チャンク転送などHTTPベースのトラフィックを透過的にローカルへプロキシする。
- モダン環境向け設計：TypeScriptとES Modulesで実装されており、クラウドの単一ポート共有（tunnelPort）を想定した構成が可能。Localtunnelに比べてメンテナンスが活発で拡張性が高い。
- プログラム的利用：APIを通じてテスト自動化やツール内組み込みが容易。クライアントはイベント（request/error/close）を受け取り、サーバー側はライフサイクルフック（onTunnelCreated/onTunnelClosed/onRequest）を持つ。
- 運用面：サーバーはカスタムドメイン、TLS有無、ルートリダイレクト、最大ソケット数などを設定可能。監視用のエンドポイント（/api/status, /api/tunnels/:id/status）を備える。

## 実践ポイント
- まず試す（パブリックサーバ利用）:
```bash
# ローカル3000を公開
npx pipenet client --port 3000
# サブドメイン指定
npx pipenet client --port 3000 --subdomain myapp
```

- セルフホスト（基本）:
```bash
# サーバー起動（例: ポート3000）
npx pipenet server --port 3000
# ドメイン指定＋トンネル用ポート
npx pipenet server --port 3000 --domain tunnel.example.com --tunnel-port 3001
```

- SDK組み込み（自動化やテストに）:
```javascript
// JavaScript
import { pipenet } from 'pipenet';
const tunnel = await pipenet({ port: 3000 });
console.log(tunnel.url);
tunnel.on('request', info => console.log(info.method, info.path));
```

- 日本の現場での活用例：
  - 外部サービス（GitHub、Stripe、LINE等）のWebhook検証に使う。自社ポリシーで外向け経路を制御したい場合はセルフホスト推奨。
  - クライアント向けデモやリモートレビューで、短時間の公開URLを発行して安全に共有。
  - 自社ツールに埋め込んで、エンジニア向けの開発支援機能を提供。

- 運用上のチェックリスト：
  - TLSとカスタムドメインの設定（社内ポリシー、証明書管理）
  - 最大同時接続数（maxTcpSockets）やレート制限の設計
  - ログと /api/status による監視・死活監視
  - 無効証明書許可（allowInvalidCert）はテスト限定に留める

Pipenetは「手早く外に出す」利便性と「自分で制御する」運用性を両立しているため、まずはパブリック経由で試し、要件が固まったらセルフホストで本番運用に移す流れが現実的。
