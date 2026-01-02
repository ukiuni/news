---
layout: post
title: "Pidgin 3.0 Experimental 5 (2.94.0) has been released - Pidgin 3.0 実験版5（2.94.0）がリリースされました"
date: 2026-01-01T08:38:01.438Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://discourse.imfreedom.org/t/pidgin-3-0-experimental-5-2-94-0-has-been-released/338"
source_title: "Pidgin 3.0 Experimental 5 (2.94.0) has been released"
source_id: 842837671
excerpt: "Pidgin 3.0実験版5公開：Presence刷新とHSLuv色導入で大改修"
---

# Pidgin 3.0 Experimental 5 (2.94.0) has been released - Pidgin 3.0 実験版5（2.94.0）がリリースされました
Pidgin再設計の“今”を先取り — プレ-alpha版で見える新設計と日本の現場で注意すべきポイント

## 要約
Pidgin 3.0 の5回目実験版（公式バージョン2.94.0）が公開されました。まだプレ‑αで多く未実装・不安定ですが、Presence管理やユーザーカラーの刷新などコア設計の進化が確認できます。

## この記事を読むべき理由
日本でもLinuxデスクトップやオープンソースIMを運用する現場は根強く、今回の変更はプラグイン／ディストリビューション保守やチャットUX改善に直結します。パッケージャーや導入検討者、開発者はAPI/依存関係の変更を把握しておくべきです。

## 詳細解説
- リリース形態と注意点  
  - これは「pre‑alpha（2.94.0）」のタイムドスナップショット。Flathub BetaやSourceForgeで入手可能。OS直インストールはアンインストールが面倒なため、flatpakローカルビルドやmeson devenvでの試用を推奨。パッケージャー向けには「ユーザー向けに配布しないでほしい」と明記されています。
- UI/UXの目立つ変更
  - Presence chooser（プレゼンス選択UI）を実装。IRCやデモプロトコルでaway等の状態管理が可能になり、将来的に状態エディタや永続化が追加される予定。
  - ユーザーカラー生成がXEP‑0392準拠のHSLuvアルゴリズムへ変更。XMPP向け提案仕様だが、Pidgin全体で統一色を採用し会話リストの視認性を向上。
- プラグイン・内部APIの整理
  - KWalletプラグインを削除（libsecret経由で代替検証済）。Keychain/WinCred/secretプロバイダの検索方法がアカウントIDベースへ変更。
  - libpurple側で多数の内部APIリファクタ（PresenceManager、Connection vfunc移動、Conversationのバッジ/ステータスメッセージ追加など）。プラグインやフロントエンドはこれらの変更に合わせて更新が必要。
- 品質管理・テスト
  - ライセンスヘッダ検証や各プロトコルの単体テスト追加、codespellテストなど自動品質チェックが増加。依存バージョン（seagull 0.6.0、birb 0.6.0、ibis 0.15.0 等）の更新も明示。
- 開発スケジュール
  - 次の実験版（Experimental 6 / 2.95.0）は 2026-03-31 を予定。Burndown Chartや「state‑of‑the‑bird」投稿で進捗確認可能。

## 実践ポイント
- 試すなら安全に：Flathub Beta や README にある flatpak / meson devenv の手順でローカル実行。OS直インストールは避ける。
- パッケージ配布は待つ：パッケージャーは公式の「まだユーザー配布しないでほしい」という要請に従い、安定版リリースまで待機を推奨。
- プラグイン開発者へ：libpurple のAPI移動やプロパティ追加（badges、status-message 等）に伴う互換性チェックを早めに始める。依存ライブラリのバージョン更新も確認。
- UX改善のヒント：HSLuv による色付けやプレゼンス管理は、組織内チャットツールの視認性改善に活用可能。社内で試験導入してフィードバックを集めると良い。
- 追跡：Experimental 6 のチケットや Burndown Chart、月次の state‑of‑the‑bird ポストをウォッチして機能の実装状況を把握する。

