---
layout: post
title: "Trying out Thunderbird Appointment While I Patiently Wait For An Invite - 招待を待ちながら手元で試したThunderbird Appointment"
date: 2026-02-09T16:46:17.797Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.matthewbrunelle.com/trying-out-thunderbird-appointment-while-i-patiently-await-for-an-invite/"
source_title: "Trying out Thunderbird Appointment While I Patiently Wait For An Invite"
source_id: 1409579196
excerpt: "ローカルでThunderbirdの予約ツールを立ち上げ、CalDAV連携や設定の落とし穴を解説"
image: "https://blog.matthewbrunelle.com/content/images/size/w1200/2026/02/thunderbird_accounts_login-1.png"
---

# Trying out Thunderbird Appointment While I Patiently Wait For An Invite - 招待を待ちながら手元で試したThunderbird Appointment
待ち時間ゼロで体験！Thunderbirdの新予約ツール「Appointment」をローカルで立ち上げてみた話

## 要約
Thunderbirdが開発中のオープンソース予約ツール「Appointment」をローカルで動かしてみた。セットアップは一筋縄ではないが、CalDAV（例：Nextcloud）連携で動作確認でき、現状はグループ予約に非対応という課題がある。

## この記事を読むべき理由
日本でもリモート会議やコミュニティのスケジュール調整需要は高く、カレンダー連携を重視する自前運用やプライバシー重視の選択肢として注目に値するため。

## 詳細解説
- 構成要点：AppointmentはThunderbird Accounts（認証）に依存。両方をローカルで動かす必要あり。公式READMEが主な手順源だが、いくつかハマりどころがある。
- 必要環境：uv（Python向けランタイム/ツール）、Docker、docker-compose、hostsのオーバーライド（もしくはdnsmasqでのローカル名前解決）。
- よくあるトラブルと対処
  - bootstrapスクリプトがmail/etcディレクトリを期待して失敗 → 手動で作成して回避。
  - READMEにある manage.py の create_client コマンドは削除済み → スキップして問題なし（Issue報告あり）。
  - docker-composeで複数コンテナが同じポートを露出 → Postgres（5432）、フロントエンド（8080）、Mailpit（1025）などを別ポートへ変更し、backend/.env内の対応値も更新。
  - ログイン手順：デフォルトadminアカウントでAppointmentにそのままログインできないケースあり。テスト用は backend/.env に APP_ALLOW_FIRST_TIME_REGISTER=True を設定すると、初回登録でアカウントが作れる。
  - Google OAuth連携は GCP のクレデンシャル設定が必要で手間がかかるため、簡易テストはCalDAV（NextcloudやStalwartなど）での連携が実用的。
- 機能面：カレンダー選択、可用時間設定、予約ページ作成、招待者向けの確認フローは整っている。ただし「グループ予約（複数人での同時予約や多数参加者向け調整）」は未対応で、用途次第では致命的。

## 実践ポイント
- ローカルで試す短手順（概要）
  1. uv と Docker を用意する。
  2. hosts を編集するか dnsmasq を有効化してローカルドメインを解決する。
  3. Accounts と Appointment の docker-compose を立ち上げる（ポート競合は .env と compose ファイルで修正）。
  4. bootstrap が失敗したら mail/etc を手動作成。
  5. backend/.env に APP_ALLOW_FIRST_TIME_REGISTER=True をセットして初回登録でユーザ作成。
  6. CalDAV（Nextcloud等）を接続して動作確認。
- 設定サンプル（参考）
```nix
# nix (例：dnsmasq設定)
services.dnsmasq = {
  enable = true;
  settings = {
    address = [ "/keycloak/127.0.0.1" "/stalwart/127.0.0.1" ];
  };
};
```
```ini
# env (backend/.env の一部)
APP_ALLOW_FIRST_TIME_REGISTER=True
# Google OAuth を使う場合は以下を設定する必要あり
GOOGLE_AUTH_CLIENT_ID=
GOOGLE_AUTH_SECRET=
GOOGLE_AUTH_PROJECT_ID=
GOOGLE_AUTH_CALLBACK=http://localhost:5000/google/callback
```
- 日本の現場での活用提案：Nextcloud等の国内セルフホスト環境や社内CalDAVサーバと組み合わせれば、プライバシー重視の予約サービスを社内で完結できる。TTRPGや小規模チームの調整ツールとしては有望だが、社内会議室の「グループ枠」運用が必須なら現状は不向き。

以上を踏まえ、興味があればローカルで試してみる価値は高いですが、実運用ではグループ予約対応の動向をウォッチすると良いでしょう。
