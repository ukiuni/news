---
layout: post
title: tc-ematch(8) extended matches for use with "basic", "cgroup" or "flow" filters
date: 2025-12-28 17:17:20.272000+00:00
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: https://man7.org/linux/man-pages/man8/tc-ematch.8.html
source_title: tc-ematch(8) - Linux manual page
source_id: 46412327
excerpt: tc-ematchでバイト単位の精密マッチによりipsetやメタ情報で高度なトラフィック分類を実現
---
# tc-ematchでパケットを“精密フィルタ”する — iproute2拡張マッチ徹底ガイド

## 要約
tc-ematchはtcの"basic", "cgroup", "flow"フィルタで使える拡張マッチ群を提供し、パケット内部のバイト比較やメタ情報、ipset/xtablesやCANなど多彩な条件でパケットを精密に選別できます。

## この記事を読むべき理由
トラフィック制御やQoS、コンテナ/カーネル側のトラフィック分類を行う日本のエンジニアには、iptables/nftablesだけでなく、tc側で細かくパケットを識別できる手段が必要です。tc-ematchを理解すれば、ハードなトラフィックポリシーやカスタム計測、IFBを使ったリライトなどがより強力に実装できます。

## 詳細解説
- 基本概念  
  tc-ematchは式（EXPR）でマッチを組み立てます。論理演算（and/or/not）で複合条件を作れ、各MATCHはモジュール名と引数で指定します（例: cmp(...), meta(...), nbyte(...), ipset(...), ipt(...), canid(...)）。これをtc filter add ... basic match 'EXPR'のように使います。

- 主なマッチ種類（要点）
  - cmp (比較): パケット中の数値を取り出してeq/lt/gtで比較。ALIGN（u8/u16/u32）、OFFSET、mask、layer（link/network/transport）などで位置と幅を指定できます。トランスポート層やネクストヘッダ位置（nexthdr+）指定も可能。
  - meta: カーネルが付与するメタデータ（nf_mark, tcindex, vlan, sk_rcvbufなど）を比較できます。idやシフト、マスクで細かく扱えます。
  - nbyte: 固定バイト列の比較。文字列やCエスケープ列で指定してオフセット比較。
  - u32: よく使われるバイナリ抽出比較。ALIGNやMASKで柔軟に取り出し。
  - ipset / ipt: ipsetセットやxtablesマッチを利用して、セットメンバーシップや拡張マッチの結果で判定可能。ipsetの"hash:net,iface"などでインターフェース情報と組み合わせた判定が可能。
  - canid: CANフレーム識別用（SFF/EFF）で業務用環境や車載系で有用。

- 実装上の注意（Caveats）
  - シェルで括弧や波括弧を解釈されないようにエスケープやクオートを適切に使う必要があります（systemdサービス内やスクリプトでは特に注意）。
  - ifbデバイス上でipsetを使う場合、"outgoing device"がifb自身になる点に留意。到着元インターフェースと出力インターフェースの扱いを理解すること。
  - ematchはパケットデータを直接扱える分、バイトオーダやプロトコルヘッダの位置取りを正確に指定する必要があります。

## 実践ポイント
- すぐ試せる例
  - u16フィールドを比較してflowidを設定する例：
  ```bash
  # bash
  tc filter add dev eth0 protocol ip parent 1:0 prio 1 basic match 'cmp(u16 at 3 layer 2 mask 0xff00 gt 20)' flowid 1:10
  ```
  - nfmarkやtcindexでフローを絞る：
  ```bash
  # bash
  tc filter add dev eth0 parent 1:0 prio 2 basic match 'meta(nfmark gt 24) and meta(tcindex mask 0xf0 eq 0xf0)' flowid 1:20
  ```
  - ipsetでソースIPを参照：
  ```bash
  # bash
  tc filter add dev eth0 parent 1:0 prio 3 basic match 'ipset(bulk src)' flowid 1:30
  ```
- デバッグと運用のコツ
  - まずはnbyteやcmpで小さなサンプルパケットを送り、tcpdumpでヘッダ位置を確認してからOFFSETを調整する。
  - systemdユニットやcronで自動化する際はシェルのクォートで条件式が壊れないように注意する（単一引用符で囲うなど）。
  - ipset連携を使うと大量のIPリストを効率的に扱え、日本のデータセンターやISP環境でのブラックリスト/ホワイトリスト運用で有効。
  - cgroupやflowフィルタと組み合わせれば、コンテナ単位や接続単位で詳細な帯域制御が可能。

