---
layout: post
title: "Show HN: Webctl – Browser automation for agents based on CLI instead of MCP - Webctl — MCPではなくCLIベースのエージェント向けブラウザ自動操作"
date: 2026-01-14T22:26:47.466Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/cosinusalpha/webctl"
source_title: "GitHub - cosinusalpha/webctl: Browser automation via CLI — for humans and agents"
source_id: 46616481
excerpt: "CLIでPlaywright/Chromiumを操り出力を絞って安全に使える、エージェント向け軽量ブラウザ自動化ツール"
image: "https://opengraph.githubassets.com/344fcb94355e6c68153c8b0de99f50627400847733bbf70a5130a35c92328868/cosinusalpha/webctl"
---

# Show HN: Webctl – Browser automation for agents based on CLI instead of MCP - Webctl — MCPではなくCLIベースのエージェント向けブラウザ自動操作
CLIでブラウザを直接操作し、AIエージェントと人間の両方が使える軽量ツール「webctl」の実用ポイント解説

## 要約
webctlはCLI経由でPlaywright/Chromiumを操作するツールで、サーバ側がコンテキストを勝手に肥大化させるMCP方式の欠点を避け、ユーザー（やエージェント）が取り込む情報を自分で制御できるのが特徴。

## この記事を読むべき理由
- ブラウザ自動化を「ログ／フィルタ／スクリプト」で扱いたい日本の開発者やデータ担当者に直感的な代替手段を提示するため。
- LLMベースのエージェントにウェブ操作を任せる際の安全性・効率性の改善につながるため。

## 詳細解説
- なぜCLIか：従来のMCPツールはサーバ側がページの全アクセシビリティツリーやコンソールログを返すため、短時間で「コンテキストが肥大化」してしまう。webctlはCLIで取得を絞り込み、ローカルでさらにgrep/jq/headなどUnixツールで処理できる点を利点とする。
- フィルタリング中心の設計：--interactive-only（ボタン・リンク・入力のみ）、--limit、--within（コンテナ内限定）、--roles（特定のARIAロール）などで出力を最小化できる。要素指定はARIA roleとname~=（部分一致）が基本で、CSS依存が減るためサイト改修に強い。
- 出力とスクリプト適用：JSONL出力や--result-onlyで機械処理しやすく、出力をファイル化してキャッシュ→再利用、.shに保存してバージョン管理も可能。
- セッション管理：ブラウザはデーモンで常駐し、クッキーをディスクに保持。start/stopで明示的制御。agent向けinitで既成プロンプト（CLAUDE.md等）を生成。
- エージェント連携：webctl initやagent-promptでエージェントにCLIコマンドを渡す運用が想定されている。エージェントと人間が同じコマンド群を使えるのが強み。
- アーキテクチャ：CLI ⇆ JSON-RPC ⇆ デーモン（Playwright + Chromium）。Python 3.11+、pip経由インストールやソースからのセットアップが可能。daemonは自動起動する。

簡単なコマンド例（入門）
```bash
pip install webctl
webctl setup                # Chromiumをダウンロード
webctl start                # ブラウザ起動
webctl navigate "https://example.com"
webctl snapshot --interactive-only --limit 20
webctl stop --daemon
```

## 実践ポイント
- まずは --interactive-only と --limit を使って出力を絞る。大量データを取り込む前に必須。
- 要素検索は role と name~= を使う。UIテキストの微変化に強い。
- 出力はファイル化して jq / grep / head で加工するワークフローに馴染ませると便利（例：snapshot > cache.txt）。
- セッションを使えばログイン状態を保持できるため、テストや自動化ジョブの反復実行が高速化。
- エージェント連携を検討する場合は webctl init で生成されるテンプレートを参考に設定を調整する。

短時間で試せるポイントは上のコマンド群。日本の現場では既存のCIやスクリプト群と組み合わせ、必要な情報だけを確実に取り出すツールとして有用。
