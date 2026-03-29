---
layout: post
title: "Building a Mostly IPv6 Only Home Network - ほぼIPv6専用の自宅ネットワークを構築する"
date: 2026-03-29T15:30:19.854Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://varunpriolkar.com/2026/03/building-a-mostly-ipv6-only-home-network/"
source_title: "Building a Mostly IPv6 Only Home Network &#8211; Varun Sinai Priolkar"
source_id: 47515271
excerpt: "固定/48やDNS64/NAT64で自宅をほぼIPv6化する実践ガイド"
---

# Building a Mostly IPv6 Only Home Network - ほぼIPv6専用の自宅ネットワークを構築する
IPv4と共存する時代に、あえて「ほぼIPv6だけ」の自宅ネットワークを作る――現実的で実践的な移行手順と落とし穴を短くまとめます。

## 要約
海外エンジニアが自宅を「ほぼIPv6専用」に移行した手順と実運用で使った技術（/48トンネル、WireGuard、OPNSense、DNS64/NAT64、Jool、464XLAT、Docker IPv6など）を具体的に解説します。

## この記事を読むべき理由
日本でもISPのIPv6対応が進む中、家庭や小規模サーバでIPv6優先構成を実現したい人向けに、実際に動く設計・設定手順と現場で出た問題点（プリンタやIoT機器の非対応など）を把握できます。

## 詳細解説
- 静的なプレフィックス確保：ISPのDHCP-PDは動的で短めのリースが多いので、/48を安価なVPS/トンネル業者から借りて固定プレフィックスを得る方法。WireGuardトンネルでIPv6を通すとMTUやIPv4依存を減らせる。  
- ルーティングとPBR：OPNSenseでLAN→トンネル向けにポリシーベースルーティング（PBR）を設定し、必要に応じてFRRでプレフィックスを広告する。  
- アドレッシング：/48内で /64 をLANに割当て、SLAAC（RA：M+O+A）＋Kea DHCPv6の併用で静的リースと状態レス利便性を両立。Dockerホストには/56を割り当て、各コンテナネットワークに /64 を配る設計。  
- IPv4サービスへの到達：DNS64＋NAT64（例：Joolをカーネルモジュールで利用）でIPv6-only環境からIPv4-onlyサイトへ透過的に接続。DNS64はUnboundや専用のDNS実装で対応。64:ff9b::/96などを使ってIPv4アドレスをIPv6空間にマッピングする。  
- 464XLATと検出：DHCPv4 Option 108（IPv6-only推奨）とPREF64（RAでDNS64プレフィックス告知）でクライアント側のCLAT（端末側のstateless NAT64）を誘導。Androidや最新Linux（NetworkManager）等でCLATが使える。  
- DockerのIPv6化：daemon.jsonでIPv6とデフォルトアドレスプールを指定して、コンテナにGUAを割り当てる。内部でIPv4を使わないようにすることで運用がシンプルに。  
- IPv6-onlyサーバをIPv4インターネットに公開：IPv4だけの外部からの到達は、IPv4アドレスを持つエッジVMでTLS終端やプロキシを行い、内部はIPv6経路（例：Zerotier経由）で配信する手法が簡単で堅牢。  
- 実運用の障害例：Slackのタイムアウトや一部IoT機器・プリンタのIPv6未対応、Dockerサービスの不具合など、対応が必要なケースがある。

## 実践ポイント
- /48やトンネルは安価（例：年間数ドル〜十数ドル）だが、遅延と冗長性を確認する。  
- OPNSenseでWireGuardトンネルを登録→LANでPBR設定→FRRで必要プレフィックスを広告、の流れが安定する。  
- DNS64＋Jool（NAT64）を用意してからIPv4を徐々に無効化。PREF64とDHCPv4 Option 108で端末のCLAT利用を促す。  
- DockerはIPv6有効化、アドレスプール指定、bridgeを無効化して明示的に/64を割り当てる。例：
```json
{
  "ipv6": true,
  "default-address-pools": [
    { "base": "2602:xxxx:xxxx:2200::/56", "size": 64 }
  ],
  "default-network-opts": {"bridge":{"com.docker.network.enable_ipv6":"true"}},
  "bridge": "none",
  "experimental": true,
  "ip6tables": false
}
```
- テストツール（IPvFoo、ipv6-testサイト等）でDNS64/NAT64動作を確認。問題端末は二段階で対応（ファーム更新→DHCPv4残置→機器交換）。  
- 日本の家庭だとプリンタやIoT機器のIPv6対応が遅れがちなので、まずはサーバ・NAS・スマホから段階的に切り替えるのが現実的。

短く言うと：固定プレフィックスを確保し、DNS64/NAT64＋464XLATの設計で「ほぼIPv6専用」を実現可能。ただし機器互換性の確認と段階的な移行が肝心です。
