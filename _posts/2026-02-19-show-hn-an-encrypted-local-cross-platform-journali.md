---
layout: post
title: "Show HN: An encrypted, local, cross-platform journaling app - 暗号化されたローカル日記アプリ"
date: 2026-02-19T12:55:08.519Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/fjrevoredo/mini-diarium"
source_title: "GitHub - fjrevoredo/mini-diarium: An encrypted local cross-platform journaling app"
source_id: 47072863
excerpt: "オフラインでAES暗号＋鍵ファイル二要素、クロスプラットフォームのローカル日記アプリ"
image: "https://opengraph.githubassets.com/aa72a916444ea250b2f2d6a2d899769a5b87dd78197f1fa6b333db51fa1577cd/fjrevoredo/mini-diarium"
---

# Show HN: An encrypted, local, cross-platform journaling app - 暗号化されたローカル日記アプリ

オフライン完結・AES暗号＋鍵ファイルで「本当に自分だけの」日記を作るMini Diariumの魅力

## 要約
Mini DiariumはTauri＋Rust＋SolidJSで作られたローカル専用の日記アプリ。すべてのエントリをAES-256-GCMで暗号化し、パスワードとX25519鍵ファイルの両方で開錠できる設計が特徴。

## この記事を読むべき理由
個人情報保護や機密メモの管理に関心が高まる日本市場で、「インターネットに一切接続しない」「持ち運べる秘密鍵で二要素的運用が可能」という設計は、リモートワークや個人情報管理で実務的に役立つ選択肢だからです。

## 詳細解説
- 暗号モデル
  - ランダムなマスター鍵（256bit）で全エントリをAES-256-GCM暗号化。
  - 各認証方法（パスワード、鍵ファイル）はこのマスター鍵をラップ（暗号化）したスロットを保持。新しい認証方式の追加・削除はエントリ再暗号化不要（O(1)）。
  - パスワード解除はArgon2で派生した鍵でマスター鍵を復号。鍵ファイル解除はX25519によるECDH＋HKDFでラッピング鍵を導出しAES-GCMでアンラップ。マスター鍵は平文で永続化されない。
- アーキテクチャ
  - フロントエンド：SolidJS。UIからRustバックエンドへはTauriのinvoke()で通信。
  - バックエンド：Rustで暗号処理とSQLite操作を担当。ローカルSQLiteに暗号化データを保存。
  - ネットワーク：ゼロ — テレメトリ、アップデートチェック、同期なし。
- 使い勝手と特徴
  - 鍵ファイル（.key）はX25519秘密鍵の64文字16進表現。USBやパスワードマネージャに格納して物理的な第二要素にできる。
  - インポート/エクスポート（Day One/JSON/Markdown等）、リッチテキスト、カレンダー導線、自動バックアップ（回転）などをサポート。
  - クロスプラットフォーム：Windows(.msi/.exe)、macOS(.dmg)、Linux(.AppImage/.deb)。未署名アプリの初回起動ワーニング対応が必要。
- ビルドと依存
  - Rust 1.75+、Bun 1.x、Tauri v2のシステム依存あり。ソースからビルド可能で再現ビルドを標榜。
- 注意点
  - 最後の認証方法を失うと復旧不可（パスワードとすべての鍵ファイルを失うと復元不能）。
  - 一部ショートカットの不具合など既知の課題あり。セキュリティ設計は公開されている（SECURITY.md）。

## 実践ポイント
- まず試す：公式リリースをダウンロードしてSHA256チェック（Linux向けの手順を参照）で検証してからインストール。
- 鍵運用：鍵ファイルはUSBやパスワードマネージャの安全な添付ファイルに保存。少なくとも1つはバックアップを別媒体に保管。
- マルチ端末運用：端末ごとに鍵ファイルを発行しておけば、1台を失っても他端末の鍵を削除するだけでアクセスを取り消せる（再暗号化不要）。
- ソース確認：暗号・実装に不安がある場合はRustコード（暗号処理部分）と SECURITY.md を読み、必要なら自前でビルドして動作を確認する。
- 運用上の注意：パスワードと鍵ファイルの両方を失うと復旧不可。業務で使う場合は運用ポリシー（バックアップとアクセス管理）を明確に。

元リポジトリ（参考）：https://github.com/fjrevoredo/mini-diarium
