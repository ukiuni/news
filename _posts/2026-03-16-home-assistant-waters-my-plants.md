---
layout: post
title: "Home Assistant waters my plants - Home Assistantが植物に給水してくれる話"
date: 2026-03-16T09:57:40.041Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://finnian.io/blog/home-assistant-waters-my-plants/"
source_title: "Home Assistant waters my plants! - Finnian Anderson"
source_id: 47348652
excerpt: "ミニPC＋Home AssistantとLink‑Tapで天候連携・MQTT制御の外出先から使える安全な自動散水システムを構築"
image: "https://finnian.io/img/main/logo.jpg"
---

# Home Assistant waters my plants - Home Assistantが植物に給水してくれる話
家庭菜園が手放せない人へ：ミニPC＋Home Assistantで屋外の散水をスマート化した、失敗しない自作自動化ガイド

## 要約
BeelinkミニPCにProxmox→Home Assistantを入れ、Link-Tapの4ゾーン弁をMQTT経由で制御。天気判定・通知・Zigbeeセンサを組み合わせて、自動散水と観測ができるホームオートメーション構成。

## この記事を読むべき理由
雨が多い/季節変動のある日本では「散水の自動化」は水や手間の節約に直結します。クラウド依存を減らしつつ安価に始められる実例は、家庭菜園や小規模農業に関心ある日本の読者に有益です。

## 詳細解説
- ハード選定：著者はBeelink EQ14（Intel Twin Lake N150、500GB SSD、16GB RAM）をホストに採用。省電力で将来の拡張に余裕がある点を重視。  
- 弁の選択：DIY回路よりも商用のLink‑Tap Q1（4ゾーン）を採用。クラウドとローカルMQTT両対応でHome Assistantと相性が良い。水漏れリスクを避けたい場所では既製品が安全。  
- 仮想化と配置：Proxmox上にHome AssistantをVMとして構築（USBデバイスのパススルー対応のためVM推奨）。MQTTブローカーをコンテナで立て、Link‑Tapと連携。  
- 自動化ロジック：気象予報を参照して「雨なら散水停止」、ゾーンごとのスケジュール、開始時のプッシュ通知などを実装。可観測性（ダッシュボード、ログ）を重視。  
- センサーネットワーク：SONOFF ZBDongle‑Pでzigbee2mqttを稼働、温湿度や土壌水分センサを導入。電池式センサは疎通が不安定になりやすく、メッシュ強化（リピータ追加）が有効。  
- リモートアクセスと安全性：Home AssistantのみをCloudflare Tunnel＋WARP（Zero Trustでアクセス制限）で公開。表面積を最小化して安全にリモート監視。  
- 運用上の注意：NVMeストレージが深睡眠で起動失敗する問題があり、カーネルオプション nvme_core.default_ps_max_latency_us=0 を試した例あり。バックアップはProxmoxの自動スナップショットで定期化。

## 実践ポイント
- 初めは既製の電磁弁ユニット（Link‑Tap等）を使って「水絡みは既製品で安全に」始める。  
- Home AssistantはVMでの運用がUSBパススルーや将来拡張で安定。MQTTでデバイスを統一すると管理が楽。  
- 散水は「天気APIで停止」「稼働通知」「タイムアウト」など失敗ケースを予め想定して自動化を設計する。  
- Zigbeeの安定性はリピータ（常時電源のデバイス）を増やすと改善。国内で使えるデバイスの周波数・認証を確認すること。  
- リモートはCloudflareトンネルやVPNでHome Assistantのみを限定公開。定期バックアップとストレージ監視（SMART）を忘れずに。

以上を踏まえれば、低コストかつ安全に「外出先からも管理できる散水システム」を作れます。興味があれば、機器リストやHome Assistantの自動化YAML例を用意しますか？
