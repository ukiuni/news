---
layout: post
title: "Starlink Mini as a Failover - Starlink Mini をフェイルオーバーに"
date: 2026-03-16T09:56:55.744Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.jackpearce.co.uk/posts/starlink-failover/"
source_title: "Starlink Mini as a failover - Jack Pearce"
source_id: 47396264
excerpt: "月£4.50で待機運用、UniFi連携のStarlink Miniで災害時即切替"
image: "https://static.jackpearce.co.uk/images/posts/2025/starlink-uk-install.jpeg"
---

# Starlink Mini as a Failover - Starlink Mini をフェイルオーバーに
魅力的なタイトル: 災害時もネットが切れない！月額わずか£4.50で実現する「Starlink Mini」を家庭のバックアップ回線にする方法

## 要約
Starlink Miniを低コストの待機プラン（£4.50/月）で維持し、UniFi環境で自動フェイルオーバー／IPv6対応を行う実践ガイド。FTTPが落ちた時に瞬時に衛星回線へ切り替えられる構成を解説する。

## この記事を読むべき理由
日本は災害で局所的にブロードバンドが落ちやすく、モバイル回線が不安定な地域もある。安価なStarlink Miniの待機運用は、遠隔ワークやリモート監視、生活インフラ維持に実用的な保険となる。

## 詳細解説
- 機器と料金
  - Starlink Miniは携帯型衛星ディッシュで、£159の本体費用。Standby（待機）プランは£4.50/月で、低速だが常時接続（約500kbps）を維持できる。映像会議やメッセージングの最低限を確保可能。
- 性能の実測
  - 平均レイテンシは約18–65ms、消費電力はソフト更新で約13W。視界確保が必要だが薄いガラス越しでも動作することが多い。
- IPv6とUniFiの落とし穴
  - StarlinkはネイティブIPv6（/56 PD）を提供するが、UniFiはデフォルトIPv6ルートを自動登録しないバグがある。結果、LANからIPv6へ正しくルーティングできない。
  - 対処法（概要）:
    1. UniFiコントローラでWANを手動設定、IPv6をSLAAC、Prefix Delegationサイズを56に。
    2. UniFi機器にSSHで入り、RA（Router Advertisement）をtcpdumpで観測してリンクローカルアドレスを確認。
    3. 手動でデフォルトIPv6ルートを追加。
  - IPv4はCGNATのためポート開放不可。公開サービスが必要ならCloudflare TunnelやIPv6のグローバルアドレス利用を検討。
- フェイルオーバー
  - UniFiでStarlinkをWAN2に設定し、ロードバランス／フェイルオーバー優先度を設定すれば自動切替が可能。太陽光蓄電などと組み合わせれば停電時の“オフグリッド”運用も現実的。

## 実践ポイント
- UniFiでのIPv6初期設定（重要）
  - Settings → Internet → Primary WAN: Advanced = Manual、Enable IPv6、IPv6 Connection = SLAAC、Prefix Delegation Size = 56
- UniFiで欠落するデフォルトルートを手動追加（例）
```sh
# tcpdumpでRAを待つ（例: eth7 が WAN）
sudo tcpdump -i eth7 -vvv icmp6

# 観測したリンクローカルアドレスを使ってデフォルトルートを追加
sudo ip -6 route add default via fe80::200:6edd:3e00:101 dev eth7
```
- 起動時に自動で復元する簡単なブートスクリプト例（UDM系向け）
```sh
#!/bin/sh
# /data/on_boot.d/20-ipv6-route.sh
if ! ip -6 route show default | grep -q default; then
  ip -6 route add default via fe80::200:6edd:3e00:101 dev eth7
fi
```
- 運用上の注意
  - StarlinkのIPv6アドレスは動的に変わる可能性があるため、スクリプトはRAで取得したゲートウェイを使うなど柔軟に。
  - ファームウェア更新でルートが消えることがあるので更新後は動作確認を。

これらを踏まえれば、低コストで信頼できる衛星バックアップを家庭や小規模オフィスに導入できる。日本の災害対策や地方拠点の冗長化に有効。興味があればUniFi機種別の具体的コマンドやRAを自動取得するスクリプト例も提供できます。
