---
layout: post
title: "FediMeteo: How a Tiny €4 FreeBSD VPS Became a Global Weather Service for Thousands - FediMeteo：わずか月額4ユーロのFreeBSD VPSが数千人のための世界的天気サービスになった方法"
date: 2025-12-30T15:40:23.392Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://it-notes.dragas.net/2025/02/26/fedimeteo-how-a-tiny-freebsd-vps-became-a-global-weather-service-for-thousands/"
source_title: "FediMeteo: How a Tiny €4 FreeBSD VPS Became a Global Weather Service for Thousands"
source_id: 1599982762
excerpt: "月4ユーロVPSでFreeBSDと簡素スクリプトが数千都市の天気をActivityPubで届けた秘訣"
---

# FediMeteo: How a Tiny €4 FreeBSD VPS Became a Global Weather Service for Thousands - FediMeteo：わずか月額4ユーロのFreeBSD VPSが数千人のための世界的天気サービスになった方法
月4ユーロVPSで世界中の都市を“ActivityPubで配信”──FreeBSDと小さなスクリプトで実現したスケールの秘密

## 要約
小さなFreeBSD VPS＋jail群と軽量ツール群（snac、Pythonスクリプト、Open-Meteo）で、数千都市の天気情報を多言語・アクセシブルにActivityPub上へ定期配信するサービスを作り上げた話。

## この記事を読むべき理由
少ないリソースで実用的にスケールするアーキテクチャ、Fediverse向けの実装上の工夫（ローカライズ、アクセシビリティ、API運用、レート管理）、そして運用で直面した障害と対処法は、日本のスタートアップや個人運用のSRE/インフラ担当にとって即実践可能な示唆が多いから。

## 詳細解説
- 基本設計
  - OS/分離: FreeBSD上でBastilleBSDを使い「国ごとにjailを分離」。ZFSで各jailを個別データセットにしてスナップショット管理。
  - 軽量ミドルウェア: ActivityPub対応の軽量なソフトsnacを採用。低メモリ・低CPUで多数アカウント（各都市をsnacユーザー化）を運用。
  - データ取得: Open-Meteo（主選択）、代替にwttr.in。geopyで座標取得し、APIから現在〜12時間〜7日分を取得してMarkdownで出力。
- 実装の要点
  - 投稿フローは「コマンドラインでMarkdownを出力 → snacのコマンドでstdinから投稿」。APIキー管理や外部HTTPサーバを増やさずに済む。
  - 都市ごとにsnacユーザーを作成。スクリプトでユーザーJSONを編集してbotフラグやプロフィールを設定。
  - 更新はpost.sh（シリアライズされたリクエスト）をcronで6時間毎に実行。完了後にUptime-Kumaへ通知して監視。
  - ローカライズとアクセシビリティ重視：投稿は各地の母語・絵文字・テキストブラウザで読める形式を優先。複数言語や単位（℃/℉）、タイムゾーン対応を追加。
- スケーリングと運用問題
  - コスト低く挑戦: 月4ユーロVPS（共有コア、8GB RAM等）で数十カ国・約3,000都市を扱うまで拡張。負荷はsnacとFreeBSDの効率で抑制。
  - APIとレート制限: 無料枠の上限に達し、Open-Meteo側と交渉して専用APIキーを取得。エラー露見で速やかに鍵をローテーション。
  - 障害対処: Nominatimの失敗に対し座標キャッシュを導入。APIキー漏洩は問題箇所の修正とプロバイダ連絡で対処。
  - 識別の工夫: 同名都市対策に city__state のようなセパレータを導入し州/県を明示。
- インフラ詳細
  - 39 jails構成（haproxy、web、snacコア+国別インスタンス）、ZFSスナップショットは15分毎、ホームページは毎時再生成。フォロワーは7,700+、対応国38、都市数約2,937（執筆時）。

## 実践ポイント
- 小規模から始める: 最初は1台の小VPSで国や機能を分離したjailを運用し、ボトルネックを観測してから拡張する。
- snacのような「小さく効率的な」ツールを選ぶと、ActivityPub運用が格段に楽になる。
- API利用では先にレートやフリープランの限界を調査し、必要なら早めに提供元へ事情説明して協力を得る。
- 外部サービス呼び出しはローカルキャッシュ（座標キャッシュ等）を入れて堅牢化。失敗時のフェイルセーフ（スキップ、再試行、通知）を設計する。
- セキュリティ注意点：デバッグ出力にAPIキーや秘密情報を含めない。CI/デプロイ前に環境変数やログ出力をチェックする。
- アクセシビリティ重視：JS不要、テキストベースでも意味が伝わる表現（絵文字＋簡潔文）を心掛けると受容性が上がる。

