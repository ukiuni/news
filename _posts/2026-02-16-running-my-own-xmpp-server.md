---
layout: post
title: "Running My Own XMPP Server - 自分で立てるXMPPサーバー運用記"
date: 2026-02-16T15:12:39.448Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.dmcc.io/journal/xmpp-turn-stun-coturn-prosody/"
source_title: "Running My Own XMPP Server » Danny"
source_id: 47034801
excerpt: "Docker+ProsodyでOMEMO・ファイル・音声対応の自前XMPP構築ガイド"
image: "https://blog.dmcc.io/img/android-icon-192x192.png"
---

# Running My Own XMPP Server - 自分で立てるXMPPサーバー運用記
自分だけのメッセージング基盤を作る週末プロジェクト — プライバシーと可搬性を手に入れる方法

## 要約
Prosody を Docker で動かし、ファイル共有・音声通話（coturn）・OMEMO（E2EE）を有効にしたフェデレーテッドな XMPP サーバー構築手順の解説。Signal に頼らない“自分の領域”を作る手順が詰まっている。

## この記事を読むべき理由
日本でもプライバシーやデータ所有権への関心は高まっており、XMPP はフェデレーションでベンダーロックインを避けられる実用的な選択肢。Docker 環境を前提に実務レベルの設定例がまとまっているため、サーバー初心者でも実装の見通しが立つ。

## 詳細解説
- 前提
  - Docker / Docker Compose、ドメイン、TLS（Let’s Encrypt推奨）、DNS編集権限。
- DNS（SRV と A/CNAME）
  - クライアント用とサーバ間フェデレーション用に SRV レコードが必須。
  - 例（要自ドメインへ置換）:
    ```bash
    _xmpp-client._tcp.xmpp.example.com SRV 0 5 5222 xmpp.example.com.
    _xmpp-server._tcp.xmpp.example.com SRV 0 5 5269 xmpp.example.com.
    A    xmpp.example.com -> サーバのIP
    CNAME upload.xmpp.example.com -> xmpp.example.com  # HTTP file upload 用
    ```
- TLS（Let’s Encrypt + DNS チャレンジ）
  - Prosody は証明書必須。Cloudflare DNS チャレンジで certbot を使う例を紹介（トークンを secrets に保存）。
  - 証明書は Prosody コンテナから読めるよう権限調整、定期更新（cron）で自動化。
- Docker 構成（概要）
  - Prosody コンテナで 5222（クライアント）と 5269（s2s）を公開、データはボリュームで永続化。設定と cert をマウント。
    ```yaml
    # language: yaml
    services:
      prosody:
        image: prosodyim/prosody:13.0
        ports:
          - "5222:5222"
          - "5269:5269"
        volumes:
          - prosody-data:/var/lib/prosody
          - ./prosody.cfg.lua:/etc/prosody/prosody.cfg.lua:ro
          - ./certs/live/xmpp.example.com/fullchain.pem:/etc/prosody/certs/xmpp.example.com.crt:ro
    volumes:
      prosody-data:
    ```
- Prosody の主要設定ポイント
  - 重要モジュール: carbons, smacks, mam, cloud_notify（モバイルでの快適さに必須）。
  - セキュリティ: c2s_require_encryption / s2s_require_encryption を有効、認証は internal_hashed、登録は手動化（prosodyctl adduser）。
  - OMEMO: サーバ側の追加設定不要。クライアント（Monal, Conversations, Gajim 等）で使用可能。
  - メッセージ保存: archive_expires_after = "1y"（例）。
  - HTTP (ファイルアップロード): Prosody の 5280 を内部で使い、外部はリバースプロキシ（例: Caddy）で TLS 終端。
- コンポーネント
  - MUC（conference.xmpp.example.com）に muc_mam を有効化、ルーム作成をローカルに制限。
  - HTTP file share コンポーネント（upload.xmpp.example.com）でファイル上限や期限を設定。
- TURN/STUN（音声/ビデオ用）
  - NAT 越えのため coturn を用意。Prosody と共有シークレットで一時クレデンシャルを発行。
  - coturn は network_mode: host で動かすのが現実的。
    ```bash
    # language: bash
    openssl rand -hex 32  # turn secret
    ```
    turnserver.conf の要点: listening-port=3478, tls-listening-port=5349, min/max relay ポート範囲, use-auth-secret, static-auth-secret=YOUR_SECRET
  - Prosody 側に turn_external_host/port/secret を設定し、ファイアウォールで 3478/5349 と relay ポートを開放。
- 運用の基本
  - アカウントは prosodyctl で手動追加（registration off 推奨）。
  - ufw 等で 5222, 5269, TURN ポートを開放。ルーター越しならポートフォワード。
  - 動作確認: docker exec xmpp prosodyctl check と XMPP Compliance Tester を利用。

## 実践ポイント
- まずはサブドメイン一つで試す（例: xmpp.example.com）→ DNS / cert が整ったら Docker-compose を起動。
- モバイル体験向上のため carbons / smacks / cloud_notify / mam は必須と考える。
- 通話を試すなら coturn を先に用意（shared secret を Prosody に設定）。
- セキュリティ優先なら s2s_secure_auth を有効にしておく（古いサーバとはフェデレーションできない可能性あり）。
- クライアント推奨: iOS は Monal、Android は Conversations、デスクトップは Gajim。
- 小規模なら週末で整備可能。まずはテストアカウント数名で運用確認を行うこと。

短時間で「自分のメッセージ基盤」を作り、Signal に頼らない代替手段を持つ価値は大きい。興味があれば、具体的な prosody.cfg.lua や coturn の設定ファイル例も提供可能。
