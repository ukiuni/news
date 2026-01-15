---
layout: post
title: "Bubblewrap: A nimble way to prevent agents from accessing your .env files - Bubblewrap：エージェントから .env を確実に守る軽量サンドボックス"
date: 2026-01-15T02:56:53.701Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://patrickmccanna.net/a-better-way-to-limit-claude-code-and-other-coding-agents-access-to-secrets/"
source_title: "A better way to limit Claude Code (and other coding agents!) access to Secrets &#8211; blog"
source_id: 46626836
excerpt: "Bubblewrapで.envやSSH鍵を手軽に隔離しAIエージェントの情報漏洩を防ぐ方法"
---

# Bubblewrap: A nimble way to prevent agents from accessing your .env files - Bubblewrap：エージェントから .env を確実に守る軽量サンドボックス
絶対に見せたくない秘密を守る：BubblewrapでAIコードエージェントのファイルアクセスを封じるワザ

## 要約
Bubblewrapを使えば、Dockerや専用ユーザーより手軽かつ安全に、Claude Codeのような自動化エージェントからホーム配下の秘密ファイル（.env、SSH鍵など）を隔離できます。Linuxのネームスペースを使った軽量な「檻」で、最小限のリソースだけを与えて実行します。

## この記事を読むべき理由
AI支援開発ツールをローカルで使う機会が増えた今、誤って機密ファイルを読み書きさせたり、ネットワーク越しに漏えいさせてしまうリスクが高まっています。特に日本のスタートアップや個人開発者は、手軽に試せて管理負担の少ない対策を求めています。本稿は初級者にもわかる形で、Bubblewrapの考え方と実践的な使い方を示します。

## 詳細解説
- 問題点
  - AIコードエージェントはローカルでユーザー権限で動くため、誤ったプロンプトやバグで `~/.ssh` や `~/.aws`、`.env` を参照・送信してしまう恐れがあります。
  - 「専用ユーザー作る」「ACL調整する」方式は運用コストが高く、ネットワーク制限もできません。Dockerは強力ですが設定やデーモン管理が必要で敷居が高い場合があります。

- Bubblewrapとは
  - Linuxのネームスペース機能を使ってプロセスの視界（ファイルシステム・ネットワーク・PID等）を切り離す小さなツールです。デーモン不要で即実行でき、バイナリも小さく監査しやすい点が特徴です。
  - 主な仕組み：--ro-bindで特定ディレクトリだけ読み取りで見せる、--bindでプロジェクトだけ書き込み許可、--unshare-allでネットワークやマウントを隔離、--die-with-parentで親プロセス終了時に一緒に止める、など。

- 何が守れるか／何を注意するか
  - 守れるもの：ホーム配下の機密ファイル、ブラウザプロファイル、システムの機密情報などへのアクセス。不要なネットワークアクセス（--share-netを使わなければブロック可）。
  - 注意点：BubblewrapはLinux向け（WSL上やサーバー上で有効）。macOSやWindowsネイティブでは同じ方法が使えません。また、どのファイルをマッピングするかは自分で理解して設定する必要があります。さらに、外部クライアント（例：Anthropicの埋め込み実装）を鵜呑みにせず、自分でサンドボックスを掛ける「防御の層（defense-in-depth）」が推奨されます。

## 実践ポイント
- インストール（Debian/Ubuntu）
```bash
# bash
sudo apt update
sudo apt install bubblewrap
```

- 最小サンドボックスの例（説明付き）
```bash
# bash
# PROJECT_DIR を自分のプロジェクトに置き換えて実行
PROJECT_DIR="$HOME/Development/YourProject"

bwrap \
  --ro-bind /usr /usr \                # 実行ファイルとライブラリを読み取りで提供
  --ro-bind /lib /lib \
  --ro-bind /lib64 /lib64 \
  --ro-bind /bin /bin \
  --ro-bind /etc/resolv.conf /etc/resolv.conf \
  --bind "$PROJECT_DIR" "$PROJECT_DIR" \  # プロジェクトのみ書き込み可能
  --bind "$HOME/.claude" "$HOME/.claude" \ # 認証情報を必要ならば明示的に渡す
  --tmpfs /tmp \
  --proc /proc \
  --dev /dev \
  --unshare-all \                       # ネットワーク等を分離（必要なら --share-net を付ける）
  --die-with-parent \
  --chdir "$PROJECT_DIR" \
  --ro-bind /dev/null "$PROJECT_DIR/.env" \            # .env を空ファイルで上書きしてブロック
  --ro-bind /dev/null "$PROJECT_DIR/.env.local" \
  --ro-bind /dev/null "$PROJECT_DIR/.env.production" \
  /bin/bash
```
ポイント解説：
- .env ファイルは実際のパスを指定して /dev/null を --ro-bind するとエージェントから見えなくなります。
- SSH鍵やネットワークアクセスは絶対に必要な場合のみ明示的に --ro-bind か --share-net で許可してください。不要なら与えない。

- 運用上のベストプラクティス
  1. まず「このエージェントが何をする必要があるか」を洗い出す（ファイル・コマンド・ネットワーク）。必要最小限だけ与える。
  2. .env など秘密はプロジェクトディレクトリ外に置くか、上書き（/dev/null）で隔離する。
  3. WAF/プロキシやホストのアウトバウンド制限も合わせて設定しておく（出口対策）。
  4. 他ベンダーが提供するサンドボックスを使う場合でも、自分側で追加のBubblewrap保護を掛けられるようにしておく（サプライチェーンリスク対策）。
  5. 実行前にサンドボックス内で試験用スクリプトを実行し、期待通り外部ファイルやネットワークにアクセスできないことを確認する。

最後に一言（日本向けの視点）
- 多くの日本の開発現場ではローカル実験や軽い自動化が盛んで、誤った設定で機密が流出するリスクが現実的です。Bubblewrapは学習コストが低く、すぐに試せる実践的ツールなので、まずは小さなプロジェクトで試し、自分のワークフローに合う形で導入することをおすすめします。
