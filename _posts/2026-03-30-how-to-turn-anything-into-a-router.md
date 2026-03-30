---
layout: post
title: "How to Turn Anything into a Router - 何でもルーターにする方法"
date: 2026-03-30T14:32:53.388Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://nbailey.ca/post/router/"
source_title: "How to turn anything into a router"
source_id: 47574034
excerpt: "捨てるはずのPCで、家向けの安価で堅牢なLinuxルーターを自作"
---

# How to Turn Anything into a Router - 何でもルーターにする方法
魅力的タイトル: 捨てるはずのPCが“家のルーター”に早変わり — 安く、自由で堅牢な自作ルーター入門

## 要約
古いミニPCやノートPC、SBCをLinuxで動かして、家庭や小規模オフィス向けのルーター／ファイアウォールを自作する手順と注意点を分かりやすく解説します。

## この記事を読むべき理由
国内でもルーター供給やセキュリティの懸念、カスタム機能の需要が高まっています。安価なハードを活用して柔軟で透明性の高いネットワーク基盤を持てる点は、日本のSOHOや家庭ユーザーにも有益です。

## 詳細解説
- なぜ可能か：市販ルーターも基本は「Linuxに近いOS＋ネットワークスタック」で動くため、汎用PCでも同等の機能を実現できる。利点は可観測性（ログ）、柔軟なファイアウォール／VPN／監視、長期運用性。
- ハード選定：パッシブ冷却のミニPCや古いノート、SBCでOK。必要なのはLinuxが動き、外向き（WAN）＋内向き（LAN）インタフェースが最低1つずつあること。USB→Ethernetアダプタで拡張可能（ただしパフォーマンスは劣る）。
- OSと主要パッケージ：DebianやAlpineが定番。必須パッケージは hostapd（AP化）、dnsmasq（DHCP/DNS）、bridge-utils（ブリッジ）、nftables（ファイアウォール/NAT）。無線用に追加ファームが必要な場合あり（Intel/Realtek/atheros など）。
- ネットワーク設計：eth0 を WAN、eth1/wlan0 を LAN として br0 でブリッジする構成がシンプル。LAN側はDHCP/DNSを担当し、WAN側へはNFTablesでマスカレード（NAT）を適用。ルーター本体は外向きからの不要な着信を拒否するのが基本。
- 永続化と運用：systemd の .link ファイルでインタフェース名を固定、/etc/sysctl.d で IP フォワードを有効化。サービスは systemctl で有効化し、journalctl や dnsmasq のリースファイルで動作確認する。シリアルコンソールを有効にすればヘッドレス運用が楽。
- 拡張性：VLAN、VPN、IDS/IPS、BGPや動的ルーティングなども追加可能だが、ルーター上に大量のアプリを入れすぎないこと（負荷分離はDMZや別サーバで）。

簡単な設定例（抜粋）

bash（パッケージインストール）
```bash
sudo apt update
sudo apt install bridge-utils hostapd dnsmasq nftables
```

text（hostapd の最小例）
```text
interface=wlan0
bridge=br0
ssid=MyWiFi
wpa_passphrase=securepass
hw_mode=g
channel=11
```

text（dnsmasq の最小例）
```text
interface=br0
dhcp-range=192.168.1.50,192.168.1.250,6h
dhcp-option=option:router,192.168.1.1
```

text（nftables の概略）
```text
table ip nat {
  chain postrouting {
    type nat hook postrouting priority 100; oifname "eth0" masquerade
  }
}
```

## 実践ポイント
- まずは不要になったPCで試す：リスク低く検証可能。性能は1.5GHz級CPUでも家庭用途は十分。
- 無線の品質が重要なら専用APをLAN側に接続する（APモードで古いルータも流用可）。
- 日本のISP（フレッツ光や一部プロバイダ）は機器接続やIPv6提供方式が異なるため、事前に仕様（PPPoE/ブリッジ/DS-Lite等）を確認する。
- 重要：ファイアウォール設定を変更する前にリモート接続手段を確保（シリアルや別管理回線）してブロック自己破壊を防ぐ。
- 長期運用ではログ回転・監視・定期アップデートを必ず設定する。

このアプローチは「捨てるはずのハードを再利用して、自分仕様のネットワークを作る」良い出発点です。まずは小さな構成で試し、必要な機能だけを積み上げていきましょう。
