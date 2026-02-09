---
layout: post
title: "SecretSpec 0.7: Declarative Secret Generation - SecretSpec 0.7: 宣言的シークレット生成"
date: 2026-02-09T05:56:18.355Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://devenv.sh/blog/2026/02/09/secretspec-07-declarative-secret-generation/#upgrading"
source_title: "SecretSpec 0.7: Declarative Secret Generation - devenv"
source_id: 405609919
excerpt: "SecretSpec 0.7で設定だけで鍵やトークンを自動生成して安全に補完"
image: "https://devenv.sh/assets/images/social/blog/posts/secretspec-0.7-declarative-secret-generation.png"
---

# SecretSpec 0.7: Declarative Secret Generation - SecretSpec 0.7: 宣言的シークレット生成
もう手作業の秘密情報管理は終わり—設定ファイルで「自動生成」を宣言するだけで、開発環境の鍵やトークンを安全に埋めてくれる新機能

## 要約
SecretSpec 0.7では、secretspec.toml内で秘密情報に type と generate を宣言すると、欠けている秘密を自動生成してプロバイダ（例: keyring）へ保存する機能が追加されました。既存値は上書きせず安全に補完します。

## この記事を読むべき理由
- ローカル開発やオンボーディング時の手作業（パスワード生成・配布）を減らせるため、開発効率が上がります。  
- 日本のチームでも、共有リポジトリに安全に「生成ルール」を置けるためミスや漏れを防げます。

## 詳細解説
問題点
- 新人やCIで「どの秘密が必要か」「どう生成するか」をドキュメント→手作業でやる手間とヒューマンエラー。

新機能（要点）
- secretspec.toml の各シークレットに type と generate を追加すると、secretspec check/run 実行時に「欠けているものを自動生成して保存」します。生成は一度だけ（idempotent）で、既にある値は保持されます。
- サポートする生成タイプ（既定の出力と指定可能オプション）：
  - password: 英数字等（length, charset）
  - hex: 指定バイト数を16進で出力（bytes）
  - base64: 指定バイト数をBase64で出力（bytes）
  - uuid: UUID v4
  - command: 任意のシェルコマンドの stdout を利用（command 必須）
- カスタム設定はテーブルで細かく指定可能（例: charset="ascii", bytes=64）。
- 設計方針：欠けていれば生成、既存は絶対に上書きしない。check/run 時に自動生成。回転（rotation）は将来の機能。

簡単な例（設定のイメージ）
```toml
# toml
[project]
name = "my-app"

[profiles.default]
DB_PASSWORD = { description = "Database password", type = "password", generate = true }
API_TOKEN = { description = "Internal API token", type = "hex", generate = { bytes = 32 } }
SESSION_KEY = { description = "Session signing key", type = "base64", generate = { bytes = 64 } }
WG_PRIVATE_KEY = { description = "WireGuard key", type = "command", generate = { command = "wg genkey" } }
```

注意点
- generate + default の矛盾や、command を空で指定するようなミスはエラーになります。  
- command タイプは任意のコマンド実行になるため、実行環境や権限に注意が必要です（秘密の取り扱いポリシーに沿ってください）。

## 実践ポイント
- 導入手順：SecretSpec を 0.7 にアップデートし、auto生成したいシークレットに type と generate を追加。既存設定はそのまま動作します。
- ローカル用のパスワード、セッションキー、テスト用トークンなど、共有する必要のないが存在が必須な値にまず適用するのがおすすめ。
- CI／デプロイ前に secretspec check をCIジョブに入れて欠損を検知・補完させる運用が簡単かつ有効。
- command タイプを使う際は、再現性とセキュリティ（依存コマンドが同一出力を返すか、秘密がログに流れないか）を確認すること。

導入するとオンボーディングがスムーズになり、ローカル／チーム開発での「鍵の穴」を埋めやすくなります。
