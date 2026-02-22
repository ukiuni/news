---
layout: post
title: "Using New Bridges of FreeBSD 15 - FreeBSD 15 の新しいブリッジ機能の使い方"
date: 2026-02-22T23:54:40.931Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.feld.me/posts/2026/02/using-new-bridges-freebsd-15/"
source_title: "Using The New Bridges of FreeBSD 15 &ndash; Makefile.feld"
source_id: 47115575
excerpt: "FreeBSD 15の新ブリッジでVLAN設定が激変、単一ブリッジで複数VLANを簡潔運用"
image: "https://blog.feld.me/static/site_logo_512.png"
---

# Using New Bridges of FreeBSD 15 - FreeBSD 15 の新しいブリッジ機能の使い方
FreeBSD 15でブリッジ周りがスッキリ：VLANネイティブ対応で設定が劇的に簡単に

## 要約
FreeBSD 15はブリッジ実装を刷新し、VLANをネイティブにサポート。これにより複数VLANやVNET/Jailの接続設定が大幅に簡素化される。

## この記事を読むべき理由
日本の自宅ラボ〜中小インフラ運用まで、VLANを多用する環境での設定負荷を劇的に下げられるため。FreeBSDを使うエンジニアは移行方針と落とし穴（L3アドレスの非許容やツール側の未対応）を知る必要がある。

## 詳細解説
- 何が変わったか  
  - 新ブリッジはメンバーインターフェース上でのL3アドレスを事実上廃止（以前は member_ifaddrs 管理）。これは「スイッチとしての挙動」に近づける設計で、FreeBSD 16で完全に削除予定。  
  - 最大の利点は「単一ブリッジで複数VLANのタグ/アンタグを管理」できる点。以前のようにVLANごとにブリッジを作る必要がなくなる。

- 旧来の設定（複雑で面倒）
```sh
# 旧: VLANごとにbridgeを作る（抜粋）
cloned_interfaces="bridge0 bridge1 bridge2"
ifconfig_ix1="up ... -vlanhwfilter -vlanhwtag ..."
ifconfig_vlan2bridge="addm vlan2 up"
```

- 新しい設定（シンプル）
```sh
# 新: 単一ブリッジにタグ指定で追加
cloned_interfaces="bridge0"
ifconfig_ix1="up ... -vlanhwfilter -vlanhwtag ..."
ifconfig_bridge0="vlanfilter addm ix1 tagged 2,3,128"
```
  - 注意: ブリッジに vlanfilter フラグが必須。無いと tagged 追加時に "Invalid argument (extended error VLAN filtering not enabled)" エラーになる。

- VNET / Jail周り
  - epair(4) と組み合わせる際は、epairの作成時に -vlanhwfilter を付ける必要がある（カーネル側挙動の変化）。また epair の MAC 安定化はカーネル側でサポートされているため、Jib スクリプトの一部機能は不要になった。  
  - 例: 簡易スクリプト（要調整）
```sh
#!/bin/sh
# /scripts/vnetif ENAME BRIDGE VLAN
NEW=$(ifconfig -D epair create -vlanhwfilter up)
NUM=$(echo ${NEW##epair} | tr -d '[a]')
ifconfig ${NEW} inet6 ifdisabled -auto_linklocal -accept_rtadv no_radr
ifconfig epair ${NUM} a name e0a_${1}
ifconfig epair ${NUM} b name e0b_${1}
ifconfig ${2} addm e0a_${1} untagged ${3}
```

- bhyve / vm-bhyve
  - vm-bhyve は新ブリッジ対応が追いついていないため、現状はtapを事前作成してbridgeに addm する手法で回避。VM用の安定MACはtap作成時に明示的に設定する必要あり。

- 注意点
  - router-on-a-stick（ルータがタグを扱う単一インターフェース）的構成での影響は残課題。性能面では member 数増加時の劣化が改善されているが、10Gbps帯域での影響は要検証。  
  - net.link.bridge.member_ifaddrs は非推奨→削除予定なので、L3をメンバーに置く運用は今後保証されない。

## 実践ポイント
- まずは vlanfilter を有効にして単一ブリッジ運用へ移行してみる。テスト環境で以下を試す：  
```sh
ifconfig bridge0 vlanfilter addm ix1 tagged 2,3,128
```
- VNET/Jail では epair を作る際に -vlanhwfilter を指定し、名前付けと bridge への addm を自動化する短いスクリプトを用意する。  
- bhyve は当面 tap を事前作成して bridge に追加、MACは作成時に指定する。vm-bhyve のアップデートを待つかパッチを検討。  
- FreeBSD 16 での sysctl 削除を見据え、L3を直接置く慣習はやめる。10Gbps等で性能が気になる場合はベンチ実測を行う。

以上を踏まえ、まずは小規模なテスト環境で新ブリッジ＋VLAN運用を試し、既存ツールや運用スクリプトを順次更新してください。
