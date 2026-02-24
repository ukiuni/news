---
layout: post
title: "Show HN: enveil – hide your .env secrets from prAIng eyes - enveil — .envの秘密をAIの覗き見から隠す"
date: 2026-02-24T06:00:04.779Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/GreatScott/enveil"
source_title: "GitHub - GreatScott/enveil: ENVeil: Hide .env secrets from prAIng eyes: secrets live in local encrypted stores (per project) and are injected directly into apps at runtime, never touching disk as plaintext."
source_id: 47133055
excerpt: "平文の.envを排し、実行時に暗号化ストアから環境変数を注入してAIやログ漏洩を防ぐ"
image: "https://opengraph.githubassets.com/2775c97c66e5e004e5800995c48905c0f06a9b2aafc32ad3c22481ae4b7ebfb5/GreatScott/enveil"
---

# Show HN: enveil – hide your .env secrets from prAIng eyes - enveil — .envの秘密をAIの覗き見から隠す
驚くほどシンプル：平文の.envを消して、秘密は暗号化されたローカルストアから直接プロセス環境に注入するツール

## 要約
enveil は .env を平文で置かないことで、Copilot/ClaudeなどのAIツールや誤ったログ出力による「うっかり漏洩」を防ぐ。秘密はプロジェクトごとの暗号化ストアに保存され、実行時にのみプロセス環境へ注入される。

## この記事を読むべき理由
AI支援コーディングや自動化が普及した今、ローカルリポジトリ内の平文シークレットが思わぬ漏洩経路になります。日本のスタートアップや組織でも、開発環境からの情報漏洩対策としてすぐに導入可能な実践的手法です。

## 詳細解説
- アプローチ：.env に実値を書かず、ev://キー参照だけを置く。実値は .enveil/store（バイナリ）にAES-256-GCMで暗号化して保存する。
- 鍵派生：マスターパスワードから Argon2id（64 MB メモリ、3反復）で 256-bit AES キーを導出。パスワードは対話的に入力（履歴や引数に残らない）。
- 実行フロー：`enveil run -- <command>` がストアを復号して ev:// を解決し、環境変数を注入したうえでサブプロセスを起動。平文はディスクにも標準出力にも書かれない。
- セキュリティ特性：
  - ストアはランダムな12バイト nonce + AES-GCM 認証付き暗号文。nonceは書き込みごとに更新され、改ざんは復号前に検知して拒否。
  - 未解決の ev:// 参照があれば即座にエラー終了（サブプロセスは実行されない）。
  - 値を標準出力に出す get/export コマンドは意図的に無い（漏洩リスク低減）。
- 操作系：`init`（プロジェクト単位ストア作成）、`set`（対話入力で追加）、`list`（キーのみ表示）、`delete`、`import`（既存 plaintext .env を暗号化してテンプレ化）、`rotate`（パスワード再暗号化）、`run`（実行）。
- 実装・配布：Rustで実装。cargo 経由でビルド/インストール可能。ストアはプロジェクトフォルダ内の .enveil/ に置き、必ず .gitignore に追加する。

## 実践ポイント
- すぐ試す（例）:
```bash
# プロジェクト内で初回
enveil init
enveil set database_url    # 対話的に値を入力
# .env は以下のように
```
```text
# .env の例
DATABASE_URL=ev://database_url
PORT=3000
```
```bash
# 実行
enveil run -- npm start
```
- 組織導入：.enveil/ を必ず .gitignore に追加。CIで使う場合はランナー側の秘密管理と組み合わせる（現状はプロジェクト単位のローカルストア）。
- 運用上の注意：マスターパスワード管理、バックアップ方針、定期的なローテーションを運用ルールに組み込む。パスワードを安全に共有する仕組み（Vaultや企業のシークレット管理）との連携検討を推奨。
- 将来的な期待：システムキーチェーン統合やグローバルストア対応が検討中で、複数プロジェクト横断での運用が楽になる可能性あり。

短時間で導入でき、開発中の“AI時代のうっかり漏洩”に対する実効性が高いツールです。興味があれば GitHub リポジトリ（GreatScott/enveil）をチェックして、ローカルで動かしてみてください。
