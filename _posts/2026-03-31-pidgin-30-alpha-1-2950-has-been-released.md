---
layout: post
title: "Pidgin 3.0 Alpha 1 2.95.0 has been released - Pidgin 3.0 Alpha 1（2.95.0）がリリースされました"
date: 2026-03-31T21:28:13.417Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://discourse.imfreedom.org/t/pidgin-3-0-alpha-1-2-95-0-has-been-released/378"
source_title: "Pidgin 3.0 Alpha 1 2.95.0 has been released! - Pidgin - Instant Messaging Freedom&#39;s Discourse"
source_id: 1096143588
excerpt: "Pidgin 3.0 α公開：API刷新とZulip統合でプラグイン移行必須"
image: "https://discourse.imfreedom.org/uploads/default/original/1X/1631c0f5af627cb3d4eb33f0fb376407e637f56e.png"
---

# Pidgin 3.0 Alpha 1 2.95.0 has been released - Pidgin 3.0 Alpha 1（2.95.0）がリリースされました
魅力的な新世代へ――古参IMクライアント「Pidgin」が3.0へ本格始動、開発者向けAPI安定化の大波

## 要約
Pidginの3.0開発ライン初のアルファ版（公式版番 2.95.0）が公開されました。プロトコルAPIの安定化やAccountSettingsへの全面移行、Zulipプラグイン追加など開発者向けの大改修が中心です。

## この記事を読むべき理由
日本でもLinuxデスクトップや社内チャット連携を扱うエンジニアやOSSメンテナは、プラグイン互換性や配布方法（Flatpak/Flathub）への影響を早めに把握しておくと、移行計画や検証が楽になります。

## 詳細解説
- リリース形態と注意点：Alpha 1は開発スナップショット（多数の未完成機能・バグあり）。SourceForgeで入手可能、Flathub Betaへ順次公開予定。OS直インストールはアンインストール難のため避け、Flatpakかmeson devenvでのビルド推奨。
- API安定化：古い AccountOption API を AccountSettings API に置換。新APIはバインド可能に設計され、Python/Lua等でのプロトコルプラグイン開発が容易に。
- アカウント編集UI：AccountSettings対応に合わせてアカウントエディタを再設計。設定は一覧化され、advanced設定を同一画面で操作可能。プロトコル側で表示順を制御できるweightや validate_account を提供。
- Zulipプラグイン：インツリーでZulipクライアントの骨格実装を追加。REST/long-pollingベースで将来的にDM等のサポートが進む予定。
- 開発者モード：未完成要素や実験的プロトコルを切り替え表示できるモードを導入。
- 依存削減：XML設定からSQLite移行が完了し、libxml2依存を除去。パッケージ管理上のメリット（依存軽減、セキュリティ面の単純化）。
- バックエンド/内部大改修：SeagullベースのPresence/AccountManager等へ移行、Conversation/Messageに色やアイコン、replying-to等のプロパティ追加、core周りやUiの再編成、多数のAPI名変更・削除（usernameプロパティ削除など）。
- リリース計画：次は Alpha 2（2.96.0）を2026-06-30予定。開発進捗はBurndown Chartや月次の「state-of-the-bird」で公開。

## 実践ポイント
- 試したい場合：SourceForgeからダウンロード、またはFlathub Beta / READMEのFlatpakビルド手順かmeson devenvでビルド。OS直インストールは避ける。
- パッケージャーへ：現時点でユーザ向けに配布しないこと（サポート負荷増大のため）。
- プラグイン開発者向け：早めに AccountSettings APIへ移行を開始し、Purple.Protocol.validate_account を実装して接続前チェックを整備する。バインディングでPython/Luaを狙うなら今回の安定化は追い風。
- 開発者向け確認項目：developer-modeで未完成プロトコルを表示、Zulipプラグインの進捗を追う、依存関係（libxml2→SQLite）を考慮したパッケージ構成を検討する。

以上。興味があればBurndown ChartやソースリポジトリのChangeLogで細項目を追うと具体的な移行作業が見えます。
