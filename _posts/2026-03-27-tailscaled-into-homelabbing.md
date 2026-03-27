---
layout: post
title: "Tailscale’d Into Homelabbing - Tailscaleで始めるホームラボ"
date: 2026-03-27T19:57:01.627Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://rugu.dev/en/blog/homelabbing_01/"
source_title: "Tailscale’d Into Homelabbing | rugu"
source_id: 1423927509
excerpt: "Tailscaleで古PCを安全ホームラボ化、Vaultwarden等をDockerで即導入"
image: "https://rugu.dev/en/blog/homelabbing_01/homelab_lenovo.png"
---

# Tailscale’d Into Homelabbing - Tailscaleで始めるホームラボ
自宅PCでクラウド級の「安全」と「利便性」を手に入れる：Tailscaleで始めるシンプルなホームラボ入門

## 要約
Tailscaleを使えば動的IPやNAT、TLSなどの面倒をほぼ解消でき、古いPCを使った低コスト・自分所有のホームラボ運用が現実的になる。Vaultwarden、Immich、Nextcloud、Obsidian等のローカル優先アプリをDockerで回す構成が紹介されている。

## この記事を読むべき理由
- 日本の家庭回線は動的IP・ルータ管理がネックになりがちだが、Tailscaleなら公開ポート不要で安全にリモート接続できる。  
- コストとプライバシーを重視する開発者や趣味のエンジニアにとって即効性のある実践法が学べる。

## 詳細解説
- Tailscale: WireGuardベースのプライベートP2Pネットワーク。NAT越え・リモートアクセス・端末間の細かい接続制御を提供し、公開インターネットに晒さずにSSHやサービスへアクセス可能。  
- Caddy連携: Caddyをリバースプロキシに据えると、Tailscaleのローカルデーモン経由で*.ts.netの証明書を自動取得・更新できるためTLS運用が非常に楽。  
- 構成方針: 各サービスはhomelabディレクトリ配下にdocker-compose.ymlと.env、データボリュームを置く。Caddy設定は/etc/caddyへシンボリックリンクして一元管理。こうすることでバックアップや移行が分かりやすい。  
- ローカル優先アプリ:  
  - Vaultwarden（Bitwarden互換）: ローカルに暗号化されたボールトを持ちつつ、サーバーで同期。自ホストでOTPなど有料機能も利用可。  
  - Immich: 写真同期・顔認識・メタデータ抽出・軽量NLP検索などを備えるセルフホスト向けフォトサーバ。  
  - Nextcloud + Obsidian: デスクトップはNextcloud同期で即時反映、モバイルはWebDAV経由とRemotely Saveプラグインで対応。  
  - Syncthingとの違い: Syncthingはピアツーピアで細かく制御できるが、Nextcloudは「中央サーバー」体験が欲しい場合に使いやすい。  
- 試して止めたもの: Kavita（オフライン読書クライアント不足）、Ghostfolio（データ対応不足）、Joplin（UI/UXでObsidianに劣る）など、用途に応じて選択が必要。  
- 懸念点と今後: バックアップ設計、UPSと自動起動（WOL/BIOS設定）、監視（リソース可視化）、電源断後の自動復旧などは段階的に整備する。

## 実践ポイント
- まずはTailscaleを導入して自宅PCとノートを接続し、外部公開なしでSSHやRDPを試す。  
- CaddyをリバースプロキシにしてTailscaleの証明書自動化を活用する（*.ts.net）。  
- サービスは1つずつ導入：まずVaultwarden（パスワード）、次にNextcloud（ファイル/ノート）、最後にImmich（写真）など。  
- homelabディレクトリに各サービスのdocker-compose.yml/.envとデータボリュームを置き、バックアップ対象を明確化する。  
- ローカル優先クライアントを選び、オフライン時の利用性を確保する（ObsidianやBitwardenクライアント等）。  
- バックアップは別筐体 or クラウドへ定期的に取り、UPS導入とWOL/BIOS自動起動で可用性を向上させる。  
- 小さく始め、運用上の課題（復元・監視・電源）を順次解決することで継続可能なホームラボにする。

興味があれば、まずはTailscale + Caddy + Vaultwardenの組み合わせで試すと導入のメリットを最も早く実感できる。
