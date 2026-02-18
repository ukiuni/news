---
layout: post
title: "TinyIce: Single-binary Icecast2-compatible server (auto-HTTPS, multi-tenant) - TinyIce：シングルバイナリのIcecast2互換サーバ（自動HTTPS・マルチテナント）"
date: 2026-02-18T09:01:18.751Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/DatanoiseTV/tinyice"
source_title: "GitHub - DatanoiseTV/tinyice: A tiny audio streaming server (compatible with icecast2) written in Go with multiple mountpoint, multi-source, and relaying support."
source_id: 47057707
excerpt: "TinyIce: 単一バイナリで即導入可能なIcecast互換自動HTTPS多テナント配信サーバ"
image: "https://opengraph.githubassets.com/00c18881eb5aaf5436ff448fc4288a4fab74e005403af5181ebb45b0509a5f05/DatanoiseTV/tinyice"
---

# TinyIce: Single-binary Icecast2-compatible server (auto-HTTPS, multi-tenant) - TinyIce：シングルバイナリのIcecast2互換サーバ（自動HTTPS・マルチテナント）
魅力的タイトル: 数秒で使える「軽量ライブ配信サーバ」—TinyIceで個人放送やコミュニティ局をすぐ始めよう

## 要約
Goで書かれた単一バイナリのIcecast2互換ストリーミングサーバ。自動HTTPS、マルチマウント・マルチソース、リレー対応、管理UIや監視機能を備え、少ない手間で即運用できるのが特徴。

## この記事を読むべき理由
日本のコミュニティラジオ、イベント配信、学校やカフェのローカル配信など、小規模〜中規模の音声配信ニーズが増える中で、設定や運用コストを抑えつつ安全に始められる実用的な選択肢だからです。

## 詳細解説
- アーキテクチャと互換性：Icecast2互換のため、一般的なエンコーダ（BUTT、OBS、Mixxx、LadioCast）や再生側（VLCやブラウザ）と相互運用可能。レガシーなエンコーダは平文HTTPで接続し、リスナーはHTTPSで受ける「デュアルプロトコル」設計を採用。
- 配布形態：テンプレートやアイコンを含む単一バイナリで配布。Go 1.21以上でビルド可能（go build -o tinyice）。
- セキュリティ：初回起動時にランダムな認証情報を生成（tinyice.jsonに保存）、パスワードはソルト付きbcryptで保護。CSRF対策やHTTPヘッダー強化を実装。とはいえ独立監査は未実施のサイドプロジェクトなので注意。
- 自動HTTPS：ACME（Let's Encrypt）に対応し、ゼロコンフィグで証明書取得が可能。ただしポートやDNSの要件（80/443可・正しいFQDN）が必要。
- マルチテナント＆管理：管理者を複数設定でき、管理者ごとに自分のマウントポイントだけを操作可能。新しいストリームはデフォルトで非表示（承認ワークフロー）にするなど運用向け機能あり。
- リレー／エッジ運用：他サーバーのストリームをプルするリレー機能、切断時の自動再接続、リレー内のICYメタデータ解析をサポート。
- 可観測性と履歴：SSEベースのリアルタイムダッシュボード、SQLiteに保存される直近再生履歴（100件/局）、Prometheusメトリクス、構造化ログ。
- 運用機能：動的にマウントやユーザー、リレーを追加・更新・無効化可能。IP禁止など簡単な攻撃対策、/status-json.xslなど既存ツール互換もある。
- 実行例：初回起動で生成されたソースパスワードを使い、エンコーダの設定は Icecast2 としてサーバIP:8000、Mount=/live、Password=生成値 。コマンドラインオプションでバインドホスト、ポート、ログ、デーモン化など設定可。

## 実践ポイント
- まずはローカルで試す：Go 1.21+環境で go build -o tinyice して ./tinyice を実行。初回の生成パスワードは必ず保存。
- エンコーダ接続：エンコーダをIcecast2互換モードで設定（例：Server=your-ip:8000, Mount=/live, Password=generated）。
- HTTPS運用の注意：自動HTTPSを使う場合は公開FQDNと80/443の開放が必要。社内検証では自己署名で先に動作確認。
- セキュリティ運用：初回生成パスワードは変更し、管理者権限は最小限に。history.db（SQLite）は定期的にバックアップ。
- 監視・スケール：Prometheusメトリクスを取り、負荷見積りは同梱のPERFORMANCE.mdを参照。Raspberry Piなど軽量機での運用も想定可能だが負荷限界に留意。
- 運用リスク：サイドプロジェクトで独立監査は未実施。商用サービスや重要インフラで使う場合は自己検証と外部レビューを推奨。

ライセンスはApache-2.0。興味がある人はGitHubリポジトリ（DatanoiseTV/tinyice）でソースとREADME、PERFORMANCE.mdを確認して試してみてください。
