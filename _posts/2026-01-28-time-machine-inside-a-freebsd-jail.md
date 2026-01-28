---
layout: post
title: "Time Machine inside a FreeBSD jail - FreeBSDのJail内でTime Machineを動かす"
date: 2026-01-28T13:40:16.191Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://it-notes.dragas.net/2026/01/28/time-machine-freebsd-jail/"
source_title: "Time Machine inside a FreeBSD jail - IT Notes"
source_id: 1486631863
excerpt: "FreeBSDのjailでSamba＋ZFSによりmacのTime Machineを安価に構築する方法"
---

# Time Machine inside a FreeBSD jail - FreeBSDのJail内でTime Machineを動かす
自宅や小規模オフィスのMacバックアップをFreeBSDサーバで安全かつ安価に運用する方法

## 要約
FreeBSDのjail（コンテナ）上でSamba + ZFSを使い、macOSのTime Machineバックアップ受け口を構築する具体手順をわかりやすく説明します。

## この記事を読むべき理由
日本でもMacは開発現場やクリエイティブ部門で広く使われています。既存のFreeBSDサーバや低消費電力機器（Raspberry Pi等）を活かして社内バックアップ基盤を作れば、コスト削減とデータ管理（own your data）を両立できます。

## 詳細解説
- アーキテクチャ
  - FreeBSDのjailにTime Machine用のSambaサービスを置く。ネットワークはVNET（仮想NIC）かinherit（ホストのインタフェース直結）を選択。シンプルならinherit、分離が必要ならVNET。
- ストレージ（ZFS）
  - バックアップ先はjail内部に置く方法と、ホスト側で作った外部datasetをnullfsでjailにマウントする方法がある。大容量は別プール（遅いHDD）に置き、jailはSSD上にして性能と容量を分けるのが現実的。
  - 例：600GBの予約付きdataset作成、ユーザーごとのrefquota設定が可能。
```bash
# ZFS dataset作成（例）
zfs create -o quota=600G -o reservation=600G bigpool/tmdata
zfs create -o refquota=500g -o refreservation=500g bigpool/tmdata/stefano
```
- Jail作成（BastilleBSD例）
```bash
# inherit（ホストNIC直結）
bastille create tmjail 15.0-RELEASE inherit igb0

# VNETまたはブリッジを使う例
bastille create -V tmjail 15.0-RELEASE 192.168.0.42/24 igb0
bastille create -B tmjail 15.0-RELEASE 192.168.0.42/24 bridge0
```
- datasetをjailへマウント
```bash
# ホストからnullfsでマウント（bastille管理）
bastille mount tmjail /bigpool/tmdata /tmdata nullfs rw 0 0
```
- ユーザー管理
  - Time Machine用にシステムユーザーを作成（Sambaログイン用）。薄い（thin）jailでは一部操作が制限されるが所有権だけ合わせればOK。
```bash
bastille console tmjail
adduser  # 例でstefanoを作成
mkdir /tmdata/stefano
chown -R stefano /tmdata/stefano/
exit
```
- Samba設定（重要：mac向けvfsとadvertise）
  - Sambaの設定でApple固有のvfs（fruit等）を有効にし、Time Machineとしてadvertiseする。ユーザーごとにパスを分けると安全。
```ini
# /usr/local/etc/smb4.conf（抜粋）
[global]
   workgroup = WORKGROUP
   security = user
   passdb backend = tdbsam
   fruit:aapl = yes
   fruit:model = MacSamba
   fruit:advertise_fullsync = true
   fruit:metadata = stream
   fruit:time machine = yes

[TimeMachine]
   path = /tmdata/%U
   valid users = %U
   browseable = yes
   writeable = yes
   vfs objects = catia fruit streams_xattr zfsacl
   create mask = 0600
   directory mask = 0700
```
- Sambaユーザー追加とmDNS
```bash
smbpasswd -a stefano
```
  - macOSはmDNS（Bonjour）でTime Machineを検出する。AvahiでmDNSを出すとGUIで見つけやすくなる。最近のSambaはAvahi無しでも動作する場合あり。
- サービス起動
```bash
service dbus enable
service dbus start
service avahi-daemon enable
service avahi-daemon start
service samba_server enable
service samba_server start
```
- 運用上の注意
  - Time MachineはAPFSスナップショットに対応しているため、ZFS側でもスナップショット戦略を検討する。
  - バックアップは暗号化を有効化すること（macOS側で暗号化設定を推奨）。
  - マルチネットワーク環境ではmDNSプロキシやルータ設定が必要。

## 実践ポイント
- 小規模ならinheritで手早く立ち上げ、後からVNETに移行して分離する選択肢を持つ。
- 大容量は別プールに置き、ユーザーごとにrefquotaで容量制御する。
- Sambaのfruit/vfsを正しく設定すればmacOS側でTime Machineとして認識される。
- 初期テストは1台のMacで暗号化ありでフルバックアップを1回実行して動作確認する。
- 既存のFreeBSDサーバや低消費電力デバイスを活用すれば、NAS購入より低コストで安全な社内バックアップを構築できる。

必要なら、上のコマンドやsmb.confの最小構成をあなたの環境（FreeBSDバージョン・Bastille有無・ZFSプール名）に合わせて書き換えた例を作成します。どの環境で試す予定ですか？
