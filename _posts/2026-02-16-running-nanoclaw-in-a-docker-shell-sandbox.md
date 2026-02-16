---
layout: post
title: "Running NanoClaw in a Docker Shell Sandbox - DockerシェルサンドボックスでNanoClawを実行する"
date: 2026-02-16T23:46:36.821Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.docker.com/blog/run-nanoclaw-in-docker-shell-sandboxes/"
source_title: "Run NanoClaw in Docker Shell Sandboxes | Docker"
source_id: 47041456
excerpt: "DockerサンドボックスでNanoClawを隔離実行しAPIキーを安全に検証"
image: "https://www.docker.com/app/uploads/2025/03/image.png"
---

# Running NanoClaw in a Docker Shell Sandbox - DockerシェルサンドボックスでNanoClawを実行する
魅惑のワンクリック見出し: 「あなたのWhatsAppアシスタントを“ホストに触らせない”で動かす方法 — NanoClawをDockerサンドボックスで安全に運用する」

## 要約
Dockerの新しい「shell」サンドボックスを使えば、Claudeベースの軽量WhatsAppアシスタント NanoClaw を、ホスト環境に影響を与えずに隔離して実行できます。ファイルアクセス制限やAPIキーのプロキシ管理でセキュアかつ使い捨てに近い開発が可能です。

## この記事を読むべき理由
個人/社内でAIエージェントを試すとき、APIキーやローカル環境汚染を気にせずに安全に検証したい日本のエンジニアやプロダクト担当に有用です。LINE連携等への展開も同様のパターンで応用できます。

## 詳細解説
- Shellサンドボックスとは：最小限設定のUbuntuベースmicroVMに対話的なbashを落とし、Node.js/ Python/ git等の基礎ツールだけを備えた“何も入ってない”隔離環境。ユーザーが必要なものをインストールする方式。
- セキュリティ上の利点：
  - ファイルシステム隔離：マウントしたワークスペース以外は見えない。
  - 資格情報管理：APIキーは「proxy-managed」経由で注入され、実キーはサンドボックス内部に置かれない。
  - クリーン環境／廃棄容易：ホストのグローバルパッケージやNodeバージョンと競合しない。docker sandbox rmで簡単に消去可能。
- 必要条件：Docker Desktop + docker sandbox CLI（例：v0.12.0 nightly）、Anthropic APIキー（環境変数）。
- 手順（概略）：
  1. ワークスペース作成とサンドボックス生成
  2. サンドボックスに入って npm で Claude Code をインストール
  3. settings.json で apiKeyHelper を"echo proxy-managed"に設定（キーはプロキシで差し替え）
  4. NanoClaw を git clone → npm install → claude でセットアップ → npm start で起動
- 管理コマンド：作成、停止、開始、削除が docker sandbox コマンドで可能。

## 実践ポイント
- 最小のホスト露出：ワークスペースは実験用に専用ディレクトリを用意すること。
- APIキーは常にプロキシ経由で扱う：settings.json の apiKeyHelper に "echo proxy-managed" を使う。
- サンドボックスは使い捨て運用が吉：実験後は docker sandbox rm で完全消去。
- 日本市場向け応用：WhatsAppではなくLINEや社内チャット連携でも同様の隔離パターンが有効（APPI対応や社内政策に合わせやすい）。
- 要点コマンド（参考）：

```bash
# ワークスペースとサンドボックス作成
mkdir -p ~/nanoclaw-workspace
docker sandbox create --name nanoclaw shell ~/nanoclaw-workspace
docker sandbox run nanoclaw

# サンド内で Claude Code をインストール
npm install -g @anthropic-ai/claude-code

# settings.json の例（サンド内）
cat > ~/.claude/settings.json <<'EOF'
{
  "apiKeyHelper": "echo proxy-managed",
  "defaultMode": "bypassPermissions",
  "bypassPermissionsModeAccepted": true
}
EOF

# NanoClaw をクローンして起動
cd ~/workspace
git clone https://github.com/<あなたのリポジトリ>/nanoclaw.git
cd nanoclaw
npm install
claude   # セットアップ対話
npm start

# サンドボックス管理
docker sandbox ls
docker sandbox stop nanoclaw
docker sandbox start nanoclaw
docker sandbox rm nanoclaw
```

元記事の手順を踏めば、ローカルを汚さずにエージェント実験を始められます。
