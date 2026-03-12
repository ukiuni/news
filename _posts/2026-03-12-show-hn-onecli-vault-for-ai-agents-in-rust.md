---
layout: post
title: "Show HN: OneCLI – Vault for AI Agents in Rust - OneCLI：AIエージェント向けの認証情報ヴォルト（Rust製）"
date: 2026-03-12T17:48:34.297Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/onecli/onecli"
source_title: "GitHub - onecli/onecli: Open-source credential vault, give your AI agents access to services without exposing keys. · GitHub"
source_id: 47353558
excerpt: "Rust製のOneCLIでAIエージェントにダミー鍵を渡し、実キーを安全に注入・管理できる"
image: "https://opengraph.githubassets.com/04c743cc24dd058366846f8604d3d34ba516e00eb292c76ea926f50f9aac4942/onecli/onecli"
---

# Show HN: OneCLI – Vault for AI Agents in Rust - OneCLI：AIエージェント向けの認証情報ヴォルト（Rust製）

AIエージェントにAPIキーを直接渡さず、安全に外部サービスへアクセスさせる「鍵の代理人」――OneCLIがこれをシンプルに実現します。

## 要約
OneCLIはエージェントと外部APIの間に立つオープンソースのゲートウェイで、エージェントにはダミーキーを与え、ゲートウェイが実際のシークレットをリクエスト時に差し替えて注入します。シークレットはAES-256-GCMで暗号化され、リクエスト時のみ復号されます。

## この記事を読むべき理由
AIエージェントが増える日本のプロダクト開発現場で、鍵の乱用や漏洩リスクを減らしつつ複数APIを安全に扱う設計は必須です。OneCLIはローカル検証からチーム運用まで現実的な選択肢を提供します。

## 詳細解説
- 基本動作：エージェントはFAKE_KEYなどのプレースホルダで通常のHTTPリクエストを送る。Rust製のプロキシが受け取り、ホスト／パスのマッチングで該当する実キーを取り出してリクエストに差し替える（エージェントは本物のキーを一切見ない）。
- アーキテクチャ：
  - Rust Gateway：高速でメモリ安全なHTTPゲートウェイ（HTTPSはMITM風のインターセプトで注入）。
  - Web Dashboard：Next.jsによる管理画面／API（エージェント管理、シークレット登録、権限設定）。
  - Secret Store：AES-256-GCMで暗号化された資格情報。リクエスト時のみ復号。
  - DB：組み込みのPGliteまたは外部Postgresを選択可能。
- 認証と権限：各エージェントにスコープ付きアクセストークンを発行。Proxy-Authorizationヘッダで認証。
- 運用上のポイント：ホスト／パスパターンで細かく鍵を割り当てられるため、権限最小化がしやすい。ローテーションや監査の一本化が可能。
- 開発セットアップ：Docker一発でローカル起動が可能（下記参照）。複数モード（シングルユーザー＆Google OAuth）に対応。

実行例（ローカル最速起動）：
```bash
docker run --pull always -p 10254:10254 -p 10255:10255 -v onecli-data:/app/data ghcr.io/onecli/onecli
# Dashboard: http://localhost:10254  Gateway（プロキシ）: http://localhost:10255
```

## 実践ポイント
- まずはローカルでDocker起動→エージェント作成→シークレット登録→エージェントのHTTPゲートウェイをlocalhost:10255に向けて動かす。
- 本番は組織向けに外部PostgresとGoogle OAuthを導入して運用、SECRET_ENCRYPTION_KEYの管理は厳格に。
- ホスト／パスのマッチングルールで最小権限を設計し、鍵のローテーションと監査ログを定期チェックする。
- HTTPSインターセプトの挙動を理解した上で、社内ネットワークや法令（個人情報保護等）に合わせて導入判断を行う。

（参考）リポジトリ：https://github.com/onecli/onecli
