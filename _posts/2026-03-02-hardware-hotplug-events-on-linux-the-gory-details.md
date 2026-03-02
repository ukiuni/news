---
layout: post
title: "Hardware hotplug events on Linux, the gory details - LinuxにおけるハードウェアHotplugイベントの詳細解説"
date: 2026-03-02T13:19:12.993Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://arcanenibble.github.io/hardware-hotplug-events-on-linux-the-gory-details.html"
source_title: "Hardware hotplug events on Linux, the gory details - ArcaneNibble's site"
source_id: 1293630196
excerpt: "udev再放送とnetlinkの違いを理解しUSB挿抜での競合を防ぐ実践ガイド"
---

# Hardware hotplug events on Linux, the gory details - LinuxにおけるハードウェアHotplugイベントの詳細解説
USB差し込みでアプリを壊さないための、netlink／udevの「現場の声」

## 要約
カーネルはnetlinkでハードウェアイベントを投げ、udevが処理してからuserspace向けに再放送する。正確に検知するにはNETLINK_KOBJECT_UEVENTの「カーネル群」と「udev群」を理解して受信・解析する必要がある。

## この記事を読むべき理由
USBや外付けデバイスを扱う日本の開発者は、単に「デバイスが来た／消えた」を拾うだけでは権限変更やファームウェア処理などで競合（レース）が生じる。確実な動作や軽量ツール実装のために、カーネル⇄udev⇄アプリの流れを知るべきです。

## 詳細解説
- libusbにはLinux向けhotplugバックエンドが2種類あり、linux_netlink（カーネル直受信）とlinux_udev（udev経由）がある。公式推奨はudev経由（race回避のため）。
- netlink（プロトコル番号: NETLINK_KOBJECT_UEVENT = 15）はカーネル⇄ユーザ空間の通知に使われるソケットAPI。multicast的に複数のリスナへ配信できる。
- グループ（ハードコード）
  - MONITOR_GROUP_KERNEL = 1（カーネルが生成する生イベント）
  - MONITOR_GROUP_UDEV = 2（udevが処理後に再放送するイベント）
- カーネル発のメッセージはNUL終端の文字列群（例: `ACTION=add` `DEVPATH=…` `SUBSYSTEM=usb` 等）。最初の行は `action@/sys/path` を含む。
- udev再放送メッセージはさらに先頭にバイナリヘッダを付ける（libudevマジックとバージョン、ヘッダ長、propertiesのオフセット/長さ、subsystem/devtypeハッシュ、タグ用のブルームフィルタ等）。よく使われるマジックは 0xfeedcafe。
- ハッシュは MurmurHash2 等が使われ、TAGSフィールドはビットマスク（簡易ブルーム）でフィルタリングされる。
- 受信実装の要点
  - AF_NETLINK ソケットを作成し、protocolに NETLINK_KOBJECT_UEVENT を指定。
  - bind時に nl_groups を 1（カーネル）または 2（udev）にする。
  - 必要なら SO_PASSCRED を有効化して送信プロセスの uid/pid を取得。
  - udevヘッダを検査し（"libudev" と 0xfeedcafe）、properties 部分を NUL区切りでパースしてハッシュ等を検証できる。

簡単な受信コード（要点）
```c
int nlsock = socket(AF_NETLINK, SOCK_RAW|SOCK_CLOEXEC, 15 /*NETLINK_KOBJECT_UEVENT*/);
struct sockaddr_nl sa = { .nl_family = AF_NETLINK, .nl_groups = 2 /*MONITOR_GROUP_UDEV*/ };
bind(nlsock, (struct sockaddr*)&sa, sizeof(sa));
```

## 実践ポイント
- まずはlibudev／libusbのudevバックエンドを使うのが最も安全（udevの前処理を待てる）。
- 軽量ツールで直接netlinkを読むなら、MONITOR_GROUP_UDEV (2) を購読してudev再放送を使う（カーネル直受けはraceの危険）。
- 受信時はSO_PASSCREDで送信者情報を確認し、udevヘッダのマジック（"libudev" と 0xfeedcafe）でメッセージ形式を判定する。
- TAGSやSUBSYSTEMのマッチはヘッダ内のハッシュ／ブルームを使って最適化できるが、まずは文字列パースで正確性を担保する。
- 日本の組込み／デバイス向け環境ではファームウェア書込みやパーミッション調整が多いので、必ずudev処理完了後に動作を開始する設計にする。

参考に、udev再放送の存在とヘッダ構造を押さえておけば、USB挿抜で起きる「一見ランダムな失敗」の多くを防げます。
