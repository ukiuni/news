---
layout: post
title: "IronClaw: a Rust-based clawd that runs tools in isolated WASM sandboxes - IronClaw：WASMサンドボックスでツールを安全に実行するRust製クローンAIアシスタント"
date: 2026-02-13T19:10:05.418Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/nearai/ironclaw"
source_title: "GitHub - nearai/ironclaw: IronClaw is OpenClaw inspired implementation in Rust focused on privacy and security"
source_id: 47004312
excerpt: "IronClawはWASMでツールを隔離し、オンプレで機密を安全に処理するRust製AI基盤"
image: "https://opengraph.githubassets.com/8458028ae1f22522f6a0bd3e5902050e05e275bb09d23e1851f69379b82adc6a/nearai/ironclaw"
---

# IronClaw: a Rust-based clawd that runs tools in isolated WASM sandboxes - IronClaw：WASMサンドボックスでツールを安全に実行するRust製クローンAIアシスタント
プライバシー重視で「自分の手元に置ける」AIアシスタント──IronClawで社内データや個人情報を安全に扱う方法

## 要約
IronClawはRustで書かれたOpenClaw由来のAIアシスタント実装で、ツールを能力ベースのWASMサンドボックスで隔離し、機密情報保護やプロンプト注入対策を重視している。

## この記事を読むべき理由
日本企業や開発者はデータ主権・個人情報保護に敏感。クラウドに送らない、監査可能でオンプレ運用しやすいAI基盤を探しているなら、IronClawは実務的な選択肢になる。

## 詳細解説
- コア設計
  - Rustで単一バイナリ化：ネイティブ性能・メモリ安全性。
  - データローカル保存：PostgreSQL（pgvector対応）に暗号化保存、テレメトリ無し。
- サンドボックスと権限モデル
  - WASMサンドボックスで未検証のツールを実行。HTTPやシークレットへのアクセスは明示的に許可（能力ベース）。
  - シークレットはホスト境界で注入され、WASM内から直接参照できない。リクエスト／レスポンスのリーク検出を備える。
- セキュリティ多層防御
  - プロンプト注入対策：パターン検出、コンテンツサニタイズ、ポリシー（Block/Warn/Reviewなど）。
  - エンドポイント許可リスト、レート制限、CPU/メモリ/実行時間のリソース制限。
- 機能面
  - マルチチャネル（REPL、HTTP、WASMチャネル＝Telegram/Slack等、Web UI）、Dockerサンドボックスの選択肢。
  - Routines（cronやWebhook）、並列ジョブ、自己回復機能、ハイブリッド検索（全文＋ベクトル/RRF）を持つ永続メモリ。
  - 動的ツール生成：必要な機能を説明するとWASMツールを組み立てられる設計。MCP（Model Context Protocol）対応で外部モデル連携も可能。
- 実装／運用の入り口
  - 必要要件：Rust 1.85+、PostgreSQL 15+（pgvector）、NEAR AIアカウント（セットアップで扱う）。
  - 開発向け：cargoでビルド・テスト、チャネルはWASMでバンドル。
- OpenClawとの差異
  - Rust（性能・安全）／WASMサンドボックス（軽量で能力ベース）／Postgres（本番向け永続化）／セキュリティ重視設計。

## 実践ポイント
- 試す（ローカル評価）
  - リポジトリを取得してビルド、セットアップウィザードを実行：
  ```bash
  git clone https://github.com/nearai/ironclaw.git
  cd ironclaw
  cargo build --release
  ironclaw onboard
  ```
  - データベースはPostgreSQL＋pgvectorを用意する。
- セキュリティ評価
  - エンドポイント許可リストやシークレット注入設定をまず確認。社内API／SaaSに対するアクセスを最小化する。
- 日本の現場での活用例
  - 社内ナレッジ検索、機密ドキュメント要約、社内システムの自動化ルーチンをオンプレで実行し、外部送信を回避。
  - LINEやSlack連携（社内チャネル）をWASMチャネルで組み込み、運用監査ログを保持する。
- 次の一手
  - 小さなPoCで内部データを扱うジョブを作成し、プロンプト注入やシークレットリーク検出の挙動を確認する。
  - 必要ならOpenClawとの機能差（FEATURE_PARITY）をチェックして移行計画を検討。

短時間で試せて、オンプレ・セキュリティ重視のユースケースに直結するため、まずはローカルでのハンズオンを推奨。
