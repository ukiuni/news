---
layout: post
title: "How do Wake-On-LAN works - Wake-On-LANはどう動くか"
date: 2026-04-15T17:40:06.833Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.xaner.dev/post/wake-on-lan/"
source_title: "How do Wake-On-Lan works? - Xaner&#39;s Blog"
source_id: 47729507
excerpt: "マジックパケットでLAN越しにPCを瞬時起動する仕組みとGo実装"
image: "https://blog.xaner.dev/img/avatar-icon.png"
---

# How do Wake-On-LAN works - Wake-On-LANはどう動くか
電源オフのPCをネット越しに“瞬時起動”する仕組みと、Golangで自作する最短ルート

## 要約
Wake‑On‑LAN（WoL）はNICが受信する「Magic Packet」によってマシンを起動する仕組みで、パケットは同期ストリーム（6バイトの0xFF）＋対象MACを16回繰り返したデータで構成されます。

## この記事を読むべき理由
在宅・オフィスの省電力運用、夜間の一括メンテ、リモート開発環境のオンデマンド起動など、国内でも実務で頻出する課題の根本を理解し、実装（例えばRaspberry Piや小さなGoツール）で即活用できるからです。

## 詳細解説
- 仕組み：NIC（イーサネット）が省電力状態でも受信を監視し、Magic Packet検出時にBIOSへ起動信号を送る。Wi‑Fiでは一般的にサポートされない。
- Magic Packetの構造：先頭に6バイトの0xFF（同期ストリーム）、続けて目標のMACアドレスを区切り無しで16回繰り返す。オプションでパスワード領域を付けられる機器もあるが、BIOS依存。
- 送信方法：TCP/UDPのどれでも良いが、手軽さからUDPでブロードキャスト（例：255.255.255.255 やサブネットのブロードキャスト）に投げるのが一般的。よく使われるポートは7または9（0もあり得る）。
- 制約：同一L2セグメント／VLAN内でしか確実に届かない。送信先のMACアドレスが必須。到達や起動の成功確認はプロトコル上できない。ルータやスイッチ設定、ブロードキャストの扱いで動作が左右される。
- IPv6：ブロードキャストは無く、マルチキャスト等の別手段が必要。

簡単なGo実装の要点：
- MACフォーマット検証（正規表現で2桁×6）→区切り文字を除去
- 同期ストリーム + MAC×16 を16進文字列→バイト列へデコード
- UDPでブロードキャスト先に送信（net.Dial("udp", addr) + Write）

例（要点のみ）:

```go
package main

import (
  "encoding/hex"
  "fmt"
  "net"
  "strings"
)

func createMagicPacket(mac string) ([]byte, error) {
  mac = strings.ToLower(strings.ReplaceAll(strings.ReplaceAll(mac, ":", ""), "-", ""))
  if len(mac) != 12 { return nil, fmt.Errorf("invalid MAC") }
  sync := "ffffffffffff"
  pktHex := sync + strings.Repeat(mac, 16)
  return hex.DecodeString(pktHex)
}

func sendMagicPacket(mp []byte, addr string, port int) error {
  conn, err := net.Dial("udp", fmt.Sprintf("%s:%d", addr, port))
  if err != nil { return err }
  defer conn.Close()
  _, err = conn.Write(mp)
  return err
}
```

## 実践ポイント
- BIOSとOSでWoLを有効化する（チップセット・NICのドライバ設定を確認）。
- 物理接続は有線必須。サーバーやNASは省電力設定と合わせて検証。
- 同一サブネット外から起こすなら：VPNでLANに接続するか、LAN内に小さなプロキシ（Raspberry Pi等）を置いてHTTP→Magic Packet変換をさせる。
- ルータでブロードキャストを通さない場合が多いので、サブネットブロードキャスト（例：192.168.1.255）や静的ARP／DHCP固定IPを活用すると安定しやすい。
- テストはWiresharkでMagic Packetの生パケット（6×FF + MAC×16）を確認すると確実。

以上を押さえれば、社内の夜間バッチや家庭のNAS起動を安全かつ効率的に自動化できます。
