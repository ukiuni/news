---
layout: post
title: "Peter Steinberger – WhatsApp CLI: sync, search, send - WhatsApp CLI：同期・検索・送信"
date: 2026-04-15T07:50:33.939Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/steipete/wacli"
source_title: "GitHub - steipete/wacli: WhatsApp CLI · GitHub"
source_id: 47775628
excerpt: "ターミナルでWhatsAppをローカル同期・全文検索し送信まで自動化できるCLIツール"
image: "https://opengraph.githubassets.com/ad5f8089ab93e3d7396ea8d89e43a4a20afc269e1dd76ec46e02cf80fa5e7e21/steipete/wacli"
---

# Peter Steinberger – WhatsApp CLI: sync, search, send - WhatsApp CLI：同期・検索・送信
魅力タイトル: ターミナルからWhatsAppを自在に操る——ローカル同期×オフライン検索が可能な「wacli」でできること

## 要約
wacliはWhatsApp Webプロトコルを使ったサードパーティ製CLIで、ローカルにメッセージを同期・蓄積し、高速なオフライン検索やメッセージ送信、グループ管理をターミナルで実現します。

## この記事を読むべき理由
国際的な開発チームや海外顧客対応でWhatsAppを使う日本のエンジニアにとって、GUIに頼らずログの検索や自動化ができるツールは生産性向上とトラブルシュートで強力な武器になります。

## 詳細解説
- 基盤技術：whatsmeow（WhatsApp Webプロトコル）上に構築。WhatsApp公式とは無関係なサードパーティツール。
- 主な機能：
  - ベストエフォートでのローカルメッセージ同期＋継続キャプチャ（初回はQR認証が必要）。
  - オフラインでの全文検索（SQLite FTS5を利用するビルド推奨）。
  - メッセージ送信（テキスト／ファイル）、メディアダウンロード、連絡先・グループ操作。
  - 履歴のバックフィル（プライマリ端末がオンラインであることが必須、最大件数はリクエスト単位で指定可能）。
- 運用面：
  - デフォルトのストアは ~/.wacli（--store で変更）。
  - JSON出力対応で自動化しやすい（--json）。
  - 環境変数でリンク端末のラベルやプラットフォームを上書き可能（WACLI_DEVICE_LABEL / WACLI_DEVICE_PLATFORM）。
- ビルド／インストール：
  - Homebrewでのインストール（簡単）
  - もしくはソースビルド（例: go build -tags sqlite_fts5 ...）でFTS5検索を有効化。
- 注意点：
  - バックフィルはベストエフォートで、プライマリ端末がオンラインでないと取得できない。
  - サードパーティ製であるため、利用は自己責任。WhatsAppの利用規約やセキュリティに留意。

## 実践ポイント
- まずはHomebrewで試す：  
  ```bash
  brew install steipete/tap/wacli
  wacli auth        # QRで認証、初回同期
  wacli sync --follow
  ```
- フルテキスト検索を使いたいならSQLite FTS5有効でビルド：  
  ```bash
  go build -tags sqlite_fts5 -o ./dist/wacli ./cmd/wacli
  ```
- 自動化／スクリプト連携にはJSON出力とjqを併用：チャット一覧取得→バックフィルを一括実行などが可能。
- 運用時はプライマリ端末（スマホ）をオンラインに保ち、バックフィルは1チャットあたり50件前後を目安にすると安定しやすい。
- 法的・セキュリティ面を確認：企業利用ではWhatsAppの規約や個人情報保護に注意。

この記事を読んで興味が湧いたら、まずはローカル環境で認証→同期→検索の流れを試し、業務フローに組み込めるか評価してみてください。
