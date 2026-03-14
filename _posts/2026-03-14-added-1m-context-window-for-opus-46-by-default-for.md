---
layout: post
title: "Added 1M context window for Opus 4.6 by default for Max, Team, and Enterprise - Opus 4.6で既定のコンテキスト窓を1Mトークンに拡大（Max/Team/Enterprise向け）"
date: 2026-03-14T00:25:31.082Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://raw.githubusercontent.com/anthropics/claude-code/refs/heads/main/CHANGELOG.md"
source_title: "\"Added 1M context window for Opus 4.6 by default for Max, Team, and Enterprise\""
source_id: 47371486
excerpt: "Opus 4.6が法人向けで既定1Mトークン対応、巨大コードレビューが一気に効く"
---

# Added 1M context window for Opus 4.6 by default for Max, Team, and Enterprise - Opus 4.6で既定のコンテキスト窓を1Mトークンに拡大（Max/Team/Enterprise向け）
Opus 4.6が“1Mトークン”対応に。コードレビューや大規模ドキュメント処理で一気に効く、現場で使える大型コンテキストアップデート

## 要約
AnthropicのClaude Codeアップデートで、Opus 4.6モデルがMax/Team/Enterpriseプランでデフォルトで1Mトークンのコンテキスト窓をサポート。多数のバグ修正と開発者向け改善も同梱。

## この記事を読むべき理由
日本の開発チームや企業で、巨大コードベースや長い企画書・ログを扱う機会が増えています。1Mトークンのコンテキストは「一度に大量を理解して推論できる」ため、レビューや自動要約、マルチファイルリファクタの効率が劇的に変わります。さらにVS Code統合や法人向け管理機能の改善で現場導入の負担も下がっています。

## 詳細解説
- コア変更：Opus 4.6のコンテキスト窓が既定で1,000,000トークンに拡張（Max/Team/Enterprise）。従来は追加使用料が必要だったものが標準化された形。長い会話履歴や大規模ソースツリーを丸ごと流しても、より多くの情報を同時に保持できる。
- モデル切替・トークン関連改善：トークン推定の過剰カウントを修正し、思考ブロックやツール利用時の不必要なコンテキスト圧縮を防止。長期セッションでの情報ロスが減る。
- 開発者向け強化：/contextコマンドの「改善提案」機能でコンテキスト過多箇所やメモリ肥大の原因を指摘、autoMemoryDirectory設定でメモリ保存先をカスタム化可能。
- VS Code統合・UX修正：モデル名表示やセッション名、端末統合の不具合多数を修正。VS Codeの統合端末やキー操作（Shift+Enter等）周りの安定性向上。
- Bash／CLI改善：パイプ内での'!'破壊（jq等）の修正、複合コマンドの権限プロンプトやヒアドキュメント周りの不具合修正でスクリプト実行が堅牢に。
- 音声・マイク挙動：macOSでマイク権限が未付与の環境でも適切にプロンプトが出るよう対応。ボイスモードの安定化や遅延対策も実施。
- セキュリティと運用：組織が強制無効化したプラグインはUIから隠れるようになり、管理設定の既定パスが変更（Breaking change：Windowsの管理設定パスに注意）。
- バグ修正の山：メモリタイムスタンプ追加（新旧メモリ識別）、セッション回復の不具合修正、Marketplaceのサブモジュールやプラグイン管理、OAuth回りの堅牢化、RTLテキストやLSPのWindows固有問題対応など、企業導入で困る典型的問題を広く潰している。

## 実践ポイント
- チームでOpus 4.6を使っているなら、1M窓を活かして「全ファイルを渡したコードレビュー」や「長期ログからのインシデント抽出」を試す。まずは小さめのセッションでトークン利用をモニター。
- /contextの改善提案を使ってメモリ肥大・ツール偏在を解消し、無駄なコンテキストを減らす運用ポリシーを作る。
- VS Code拡張を最新版に更新し、VS Code固有の修正（端末、キー操作、スクロール）を取り込む。macOSユーザーはマイク許可の挙動を事前確認。
- 管理者へ：Windowsの管理設定ファイルパス変更（破壊的変更）に注意して、運用ドキュメントと配布スクリプトを更新する。
- 自動メモリ保存先やmodelOverridesなどの設定をチーム運用に合わせて調整し、プラグインやマーケットプレースの挙動を定期的に確認する。
