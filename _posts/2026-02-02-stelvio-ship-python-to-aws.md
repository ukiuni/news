---
layout: post
title: "Stelvio: Ship Python to AWS - PythonをAWSへ数分でデプロイ"
date: 2026-02-02T22:31:01.476Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/stelviodev/stelvio"
source_title: "GitHub - stelviodev/stelvio: Ship Python to AWS in minutes, not days"
source_id: 46860566
excerpt: "設定不要でPythonから数分デプロイ、Stelvioで即実行できるAWS開発体験"
image: "https://repository-images.githubusercontent.com/921676630/44ef67f5-a9f6-444c-8dd1-71e8360da1af"
---

# Stelvio: Ship Python to AWS - PythonをAWSへ数分でデプロイ

Pythonだけでインフラを定義し、設定ファイルやDSL不要でAWSへ素早くデプロイできる「Stelvio」を紹介します — 設定地獄から解放され、アプリ開発に集中できる体験が売りです。

魅力的なタイトル案：Python開発者必見 — 設定不要でAWSに秒でデプロイする「Stelvio」の衝撃

## 要約
Stelvioは純粋なPythonコードでサーバーレスやストレージ等のAWSリソースを定義し、CLI（stlv）で「数分」でデプロイできるOSSフレームワーク。スマートなデフォルトや自動権限設定、ライブ開発モードを備えます。

## この記事を読むべき理由
日本ではAWS採用が進み、PythonはWeb/SRE/データ領域で広く使われています。インフラ設定の敷居を下げれば、エンジニアは短期間で機能を検証・リリースでき、スタートアップや社内PoCで即戦力になります。

## 詳細解説
- コア思想：YAMLや独自DSLを廃し、標準Pythonでインフラとロジックを同一ファイルに書ける。IDEや型チェック、lintersがそのまま使える。
- 主な機能：
  - Pure Pythonで定義（Pulumi等の抽象化＋エスケープハッチで低レイヤーにアクセス可能）
  - Smart Defaults：IAMやネットワーク設定を自動化して複雑さを隠蔽
  - Automatic Permissions：リソースを関数に渡すだけで必要な権限・環境変数を自動設定
  - Live Dev Mode：`stlv dev`でコード変更を即反映、デプロイ待ち時間を削減
- サポートコンポーネント：Lambda（Function）、API Gateway、EventBridge（Cron）、S3、DynamoDB、SQS、SNS、SESなど、サーバーレスで一般的なAWSサービスを高レベルAPIで扱えます。
- 拡張性：内部はPulumi等を使っているため、必要なら低レイヤーの詳細設定にフォールバック可能（企業向けのカスタム要件にも対応）。

簡単な使用例（インフラとルーティングを同じファイルで定義）：

```python
from stelvio.aws.api_gateway import Api
from stelvio.aws.cron import Cron
from stelvio.aws.dynamo_db import DynamoTable

@app.run
def run() -> None:
    todos = DynamoTable("todos-table", fields={"user": "string", "date": "string"}, sort_key="date", partition_key="user")
    cleanup = Cron("cleanup-cron", "rate(1 minute)", handler="api/handlers.cleanup", links=[todos])
    api = Api("stlv-demo-api")
    api.route("GET", "/hello", handler="api/handlers.hello_world")
    api.route("POST", "/todos", handler="api/handlers.post_todo", links=[todos])
    api.route("GET", "/todos/{user}", handler="api/handlers.list_todos", links=[todos])
```

クイックスタート（2分で試せる）：

```bash
uv init my-todo-api && cd my-todo-api
uv add stelvio
uv run stlv init
uv run stlv deploy
```

## 実践ポイント
- まずは小さなAPIやCronジョブで試し、stlv devでローカル→クラウドのワークフローを体感する。
- リソースを関数に「links」で渡すと自動的に権限配布されるので、IAM定義の手間が大幅に減る。
- 企業利用時はPulumiのエスケープハッチで細かいセキュリティ要件やVPC統合を実装する。
- AWSアカウントの請求・権限周りは注意（自動でリソース作成されるためコスト管理を併用すること）。
- 日本の既存CI/CDやガバナンスに組み込むなら、まずPoC→社内標準化の流れが現実的。

短時間でプロトタイプを回したいPythonエンジニア、サーバーレス導入を加速したいチームに特に有効なツールです。
