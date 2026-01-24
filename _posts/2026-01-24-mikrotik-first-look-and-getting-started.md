---
layout: post
title: "MikroTik first look and getting started - MikroTik: 初見レビューと導入ガイド"
date: 2026-01-24T08:23:15.816Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://rtfm.co.ua/en/mikrotik-first-look-and-getting-started/"
source_title: "MikroTik: First Look and Getting Started"
source_id: 1133439995
excerpt: "MikroTikでWireGuard集中管理とSafe Modeで安全導入する実践ガイド"
image: "https://rtfm.co.ua/wp-content/uploads/2026/01/mikrotik-logo-1.png"
---

# MikroTik first look and getting started - MikroTik: 初見レビューと導入ガイド
自宅＆小規模オフィスが一変するルーター体験：MikroTikで“本格ネットワーク”を手に入れる

## 要約
MikroTikのRB4011とhAP ax3を使った導入レポート。RouterOSの豊富な管理手段（Web UI／WinBox／SSH）、バックアップ、アップデート、WireGuard配置など、最初に押さえるべきポイントを解説する。

## この記事を読むべき理由
家庭や小規模オフィスで使っている一般消費者用ルーターから一歩進んだ管理性・冗長化・VPN運用を目指す日本のエンジニア／趣味者にとって、実践的な移行手順と落とし穴が分かるから。

## 詳細解説
- ハード構成例：RB4011iGS+RM（ゲートウェイ／WireGuard／DNS配置）＋hAP ax3（Wi‑Fi/AP）という組み合わせで、ケーブル中心の「オフィス」とWi‑Fi中心の「自宅」をVPNで接続。
- 接続方法：標準Web UI、WinBox（LANスキャンとMAC接続可）、SSH、公式モバイルアプリ、シリアルの5通り。初期IPは通常192.168.88.1。
- RouterOSコンソール：階層的コマンド構造（例：/ip firewall）。Safe Modeで作業すれば設定ミスでアクセス不能になっても自動巻き戻し可能。タブ補完とF1でヘルプ。
- バックアップ：/export（可読SQL風コマンドの出力、別機種へ移行しやすい）と /system backup（バイナリ、完全復元だが機器依存あり）の使い分け。
- ユーザ管理：デフォルトadminは無効化推奨。新規管理ユーザ作成＋鍵認証でSSH運用。
- アップグレード：RouterOSとRouterBOARD（ファーム）を別々に更新。ダウンロード→install、routerboard upgrade→rebootの手順。
- ネットワーク運用の基本コマンド（ログ、リソース、インターフェース、ルート、DNS、ping/traceroute）で障害切り分けを行う。
- 運用上の設計ポイント：複数回線の優先はルートのDistanceで制御（自動フェイルオーバー）、WireGuardをゲートウェイに置いて中央でピア管理。

簡単なコマンド例：
```bash
ssh 192.168.88.1
```

```bash
/export file=init-backup.rsc
/import file-name=init-backup.rsc
```

```bash
/system package update download
/system package update install
/system routerboard upgrade
/system reboot
```

```bash
/system identity set name=mikrotik-rb4011-gw
/user add name=ops group=full password=XXX address=192.168.0.0/24
```

## 実践ポイント
- 導入前に必ず /export と /system backup を取得する。  
- 初期adminは無効化し、鍵ベースの管理ユーザを作る。  
- まずはWinBoxやWeb UIで機器発見→SSHで細かい設定へ移行。Safe Modeを活用する。  
- WireGuardはゲートウェイ側で集中管理すると運用が楽（ホームラップトップ／クラウドのPeer接続を一元化）。  
- ファームとRouterOSは別更新。更新前にバックアップ→再起動で検証。  
- 複数回線は /ip route の Distance で簡単冗長化を実装。  

以上を踏まえれば、家庭〜小規模オフィスのネットワークを「家電ルーター」から「管理可能なプロ機材」へ安全に移行できる。
