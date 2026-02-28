---
layout: post
title: "Stop Putting Secrets in .env Files - .envファイルに秘密を置くのをやめよう"
date: 2026-02-28T05:30:12.348Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://jonmagic.com/posts/stop-putting-secrets-in-dotenv-files/"
source_title: "Stop Putting Secrets in .env Files"
source_id: 1310654995
excerpt: "1PasswordやKeychainで.envを実行時注入し秘密漏洩と運用負荷を即削減"
image: "https://jonmagic.com/images/posts/stop-putting-secrets-in-dotenv-files/secure-env-demo.webp"
---

# Stop Putting Secrets in .env Files - .envファイルに秘密を置くのをやめよう
もうローカルに平文で秘密を置かない：1Password／macOS Keychainで実行時に環境変数を注入するシンプルなパターン

## 要約
.envファイルにAPIキーやパスワードを平文で置く代わりに、1PasswordやmacOS Keychainなどの“ボールト”から実行時に秘密を取得してプロセスの環境変数として注入する方法を紹介する。秘密はディスクに平文で残らず、共有やローテーションが楽になる。

## この記事を読むべき理由
日本の個人開発者や小〜中規模チームでも簡単に導入でき、盗難や誤コミットのリスクを大幅に減らせる実践的な手法だから。

## 詳細解説
問題点（要約）
- .envはgitignoreしていても平文がローカルに残るため、端末侵害やスクリーン放置で簡単に漏れる。
- 複数プロジェクトに同じキーが散らばる、回転時に探し回る、といった運用負荷がある。

パターン（原則）
- 「ディスクに書かない」「実行時に注入する」
- アプリ側のコードは変えず、プロセスの環境変数を参照するだけ（例: process.env.API_KEY）。

実装例（簡潔）
- 直接読み込む代わりにラッパーで実行：
```bash
# bash
# NG: 平文を読み込む
source .env && node server.js

# OK: ボールトから注入して実行
./with-1password.sh node server.js
```

- 1Password（op CLI）を使う例：.env.1password は安全にコミット可能（秘密はURI参照）
```bash
# .env.1password（コミット可）
API_KEY=op://Development/secure-env-demo/api-key
DATABASE_URL=op://Development/secure-env-demo/database-url
WEBHOOK_SECRET=op://Development/secure-env-demo/webhook-secret
```

ラッパー（非常にシンプル）
```bash
# bash
#!/usr/bin/env bash
exec op run --env-file=".env.1password" -- "$@"
```
op run は参照を解決して環境変数を注入し、秘密を平文でディスクに残さない。標準出力に現れた値は自動でマスクされる。

- macOS Keychain を使う例（Keychain はOS組込で Touch ID/パスワードで保護）
```bash
# bash (概略)
declare -A SECRETS=(
  [API_KEY]="secure-env-demo/api-key"
  [DATABASE_URL]="secure-env-demo/database-url"
)
for var in "${!SECRETS[@]}"; do
  service="${SECRETS[$var]}"
  value=$(security find-generic-password -a "$USER" -s "$service" -w)
  export "$var=$value"
done
exec "$@"
```

比較とメリット
- 平文ファイルを消す（ディスクに残らない）
- シングルソース（回転が一箇所で済む）
- アクセス制御と監査ログ（1Password/Keychain）
- 言語・フレームワーク非依存（docker/pytest/任意のコマンドで利用可）

考慮点
- 大規模チームや自動化要件がある場合はVault系（HashiCorp Vault等）検討が必要
- CIやコンテナ環境では別途ランタイム注入の仕組みが要る（CIのシークレットストア連携など）

## 実践ポイント
- まず選ぶ：既に使っているなら1Password、MacならKeychainが導入コスト低め。
- ボールトにアプリ用アイテムを作成し、参照ファイル（例:.env.1password）をプロジェクトに置く。
- 簡単なラッパースクリプトでコマンドを包んで運用（既存コードは変更不要）。
- チームには「.envを配らない」運用を徹底し、セットアップ手順（1Passwordログイン/Keychain登録）をREADMEに記載する。
- 将来に備え、CI/デプロイでのシークレット注入方法もドキュメント化する。

導入は小さな手間でセキュリティと運用性が大きく改善する。まずはローカルで一つのプロジェクトから試してみてほしい。
