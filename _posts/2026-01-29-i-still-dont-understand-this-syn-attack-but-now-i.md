---
layout: post
title: "I still don't understand this SYN attack, but now I can block it easily - まだこのSYN攻撃は分からないが、簡単にブロックできるようになった"
date: 2026-01-29T02:17:54.215Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://boston.conman.org/2026/01/28.2"
source_title: "I still don't understand this SYN attack, but now I can block it easily - The Boston Diaries - Captain Napalm"
source_id: 1470153862
excerpt: "TTL差でブラジル発大量SYNをiptablesで簡単に検出・即遮断する実践手順"
---

# I still don't understand this SYN attack, but now I can block it easily - まだこのSYN攻撃は分からないが、簡単にブロックできるようになった
TTL差を使って一網打尽に：謎の大量SYNをiptablesで簡単に止めた実例

## 要約
ブラジル由来と思われる大量のSYNパケットがTTL値で共通点を持っていたため、iptablesのTTLマッチで閾値を設定してDROPしたら効果的に止められた、というハンズオン事例。

## この記事を読むべき理由
同様の「説明はつかないが大量に来るSYN」に悩む国内の小〜中規模サーバ運用者やクラウド利用者が、ログの取り方と短期的な緊急対処（TTLベースのブロック）を学べるため。

## 詳細解説
- 観測ポイント
  - 発信元が多数（異なるソースIP・ポート）でSYNだけを送ってくるパターン。
  - ログから共通点は「TTLが常に100前後（典型的なTTLは約64）」とTCPオプションのパターン。
- ログ取得
  - iptablesのLOGターゲットでTCPオプションやシーケンスを記録すると特徴が掴める（LOGオプションは -j LOG の後に指定する点に注意）。syslogに上がらない場合は dmesg も確認する。
- 対処法
  - TTLが通常より大きい点に着目して、TTLが閾値より大きいパケットをDROPすることで該当SYNをほぼ排除できた。短期緊急対処として有効。
- 留意点
  - 正常なトラフィック（特に海外クライアント）もTTLが高い場合があるため、閾値は環境に応じて慎重に決めること。長期対策はISPやクラウドの上流でのフィルタリングやWAFの導入を検討する。

## 実践ポイント
- ログを取る（LOGオプションは -j LOG の直後に置く）:
```bash
iptables -A INPUT -s 168.195.0.0/16 -j LOG --log-ip-options --log-tcp-options --log-tcp-sequence
```
- dmesg や /var/log/syslog を確認:
```bash
dmesg | tail -n 50
# または
tail -n 200 /var/log/syslog
```
- TTLベースでDROP（まずはテスト環境で動作確認）:
```bash
iptables -I INPUT 1 -m ttl --ttl-gt 70 -j DROP
```
- ルールの確認とカウント:
```bash
iptables -L INPUT -v -n --line-numbers
```
- 注意事項（運用面）
  - まずログで被害パターンを把握してからブロックルールを追加する。
  - ルールは先頭に挿入（-I）して優先させる。閾値は自社アクセス実績を元に調整。
  - 長期的には上流（ISP／クラウド）での対処やレート制限、接続トラッキング（conntrack）などを併用する。

（短時間で有効な緊急対処の一例。導入前に自環境での影響を必ず確認してください。）
