---
layout: post
title: "Setting Up OpenClaw on exe.dev with Discord - exe.devでOpenClawをDiscordと連携して動かす方法"
date: 2026-02-02T23:38:19.920Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/bdougieyo/setting-up-openclaw-on-exedev-with-discord-27n"
source_title: "Setting Up OpenClaw on exe.dev with Discord - DEV Community"
source_id: 3220101
excerpt: "exe.devでOpenClawを隔離VMに導入しDiscord連携を安全に検証"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fpbn6d6mqh5coh8ym07of.png"
---

# Setting Up OpenClaw on exe.dev with Discord - exe.devでOpenClawをDiscordと連携して動かす方法
隔離された実験環境で「AIエージェント×Discord」を安全に試す──exe.devを使った導入手順と注意点

## 要約
OpenClaw（旧Clawdbot）をexe.devのエフェメラルVMで動かし、Discordボットと連携する手順を実践的にまとめる。安全性・可観測性を重視したセットアップとトラブルシュートも解説する。

## この記事を読むべき理由
Discordをコミュニティ運営や社内ツールに使う日本の開発者にとって、権限を持つAIエージェントは魅力的だがリスクも高い。exe.devの一時VM＋テレメトリを組み合わせれば、ローカルや本番に影響を与えずに安心して検証できる。

## 詳細解説
- 背景
  - OpenClawは会話コンテキストを理解しAPI操作などを行えるAIエージェント。Discordボット権限で動くため、誤動作の影響が大きい。
  - exe.devは素早く使い捨てできるVMを提供。実験用途に最適で、問題があればVMを破棄して再構築できる。

- 準備物
  - exe.devアカウント、Discordボットのトークン、（Claude利用時は）Anthropic APIキー。

- 主要手順（要点）
  1. VM作成・接続
     - SSHで新規エフェメラルVMに接続。
```bash
# 例
ssh exe.dev new
ssh <vm-name>.exe.xyz
```
  2. 必要パッケージとOpenClawインストール
```bash
sudo apt-get update
sudo apt-get install -y git curl jq ca-certificates openssl nginx
curl -fsSL https://openclaw.bot/install.sh | bash
openclaw onboard --non-interactive --accept-risk
```
  3. nginxでリバースプロキシ（OpenClawは内部で18789ポートを使用）
```nginx
server {
  listen 80;
  server_name _;
  location / {
    proxy_pass http://127.0.0.1:18789;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_read_timeout 86400s;
  }
}
```
  4. Discord連携（~/.openclaw/openclaw.jsonにトークンを設定）
```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "token": "YOUR_DISCORD_BOT_TOKEN"
    }
  }
}
```
  5. ペアリング承認（ダッシュボード接続時の承認フロー）
```bash
openclaw devices list
openclaw devices approve <id>
```
  6. ヘルスチェックとログ確認
```bash
openclaw health
openclaw logs
openclaw gateway restart
```

- 可観測性（推奨）
  - Anthropicを使う場合は「tapes」などのプロキシを挟んでAPI呼び出しを記録すると、プロンプト・応答・トークン使用量を監査できる。設定はOpenClawのprovider設定を書き換えてプロキシ先を向ける。

- セキュリティ上の注意
  - 設定ファイルはコマンドで上書きされやすい。~/.openclaw/openclaw.jsonはバックアップを取ること。
  - 常時稼働の本番で使う前に必ず最小権限で検証し、監査ログを有効化する。

## 実践ポイント
- まずはexe.devのテンプレート（exe.new/openclaw）で素早く試す。手動手順は内部動作理解に有効。
- テレメトリやtapesでAPI呼び出しを必ず記録する（デバッグ＋監査のため）。
- ペアリング承認フローを忘れて「接続できない」トラブルが多いので、openclaw devices list→approveを習慣化する。
- Discord側はボットに必要最小限の権限を付与し、サーバー導入前にテストサーバーで検証する。
- 設定が不安ならVMを破棄して再作成できるexe.devの特性を活かし「やり直し可能な実験」を前提に進める。

短時間で安全に試せる点が最大のメリット。日本のコミュニティ運営やプロトタイプ開発で「まず動かして観察する」用途に非常に向いている。
