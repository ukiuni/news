---
layout: post
title: "Show HN: Pion SCTP with RACK is 70% faster with 30% less latency"
date: 2025-12-28T22:18:19.109Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://pion.ly/blog/sctp-and-rack/"
source_title: "Show HN: Pion SCTP with RACK is 70% faster with 30% less latency"
source_id: 46413053
excerpt: "PionSCTPにRACK導入で同CPU約71%高速化、遅延約27%減"
---

# Pion SCTPにRACKを入れたら「同じCPUで約71%高速化、遅延は約27%低下」—WebRTC周りの現場で見逃せない改善

## 要約
PionのSCTP実装にRFC 8985で定義されたRACK（Rack-TLP）を導入すると、単体ベンチで「goodput/CPUで約$71\%$向上、p50遅延が約$27\%$改善」など大幅な性能改善が確認されました。

## この記事を読むべき理由
- WebRTCのデータチャネルやリアルタイム系アプリでSCTPは重要。より少ないCPUで高スループット・低遅延を達成できれば、コスト削減とUX向上に直結します。
- 日本のクラウドゲーミング、遠隔医療、ビデオ会議サービス、低遅延マイクロサービスなどで即効性のある改善策です。

## 詳細解説
- SCTPとは：複数ストリームの多重化やマルチホーミングをサポートするメッセージ志向のトランスポートで、WebRTCのデータチャネルなどで使われます。信頼性・順序制御・再送機構を持つのが特徴です。
- 従来の損失回復：SCTPは「fast retransmit（重複通知ベース）」と「RTO（タイムアウト）再送」の二本立てで損失を扱いますが、これが過剰再送や再送遅延を招く場面がありました。
- RACKとは：RFC 8985で定義された「RACK-TLP（Tail Loss Probing）」ベースの損失検出アルゴリズム。送受信の時間情報に基づいて損失をより迅速かつ精密に検出し、TLPで最後尾パケットをプローブして RTT を節約します。Linux/Windows/FreeBSDのTCPでも採用済みで、SCTPへの適用も理論・実装研究（Felix Weinrankの論文など）で裏付けられています。
- なぜ速くなるか：RACKは不要なRTOベースのスパリアス再送を抑え、TLPで1 RTTを節約できるケースを増やします。結果として、同じCPU時間で処理できるデータ量が増え、レイテンシ分布（p50/p99）も改善します。
- ベンチ結果（PionのSCPハーネス、最大バースト・理想環境）：
  - goodput: 234.55 Mbps → 316.42 Mbps (+34.9%)
  - CPU時間: 0.0560 s → 0.0441 s (−21.3%)
  - goodput / CPU-second: 4,189 → 7,177 (+71.3%)
  - latency p50: 16.37 ms → 11.86 ms (−27.5%)
  - latency p99: 36.95 ms → 27.84 ms (−24.6%)
- 注記：これは理想的なマイクロベンチの結果で、実ネットワークでは損失・ジッタが入るため改善幅は変動しますが、RACKのメリットは実運用でも期待できます。

## 実践ポイント
- まずは検証環境で有効化：PionのSCTP実装や利用中のスタックでRACKサポートの有無を確認し、テストハーネス（SCP相当）で goodput/CPU と p50/p99 を計測する。
- 実運用でのA/Bテスト：実トラフィックを使ってRACK有効/無効の比較を行い、特に再送回数、ネットワーク使用量、ピーク時のCPU負荷を観測する。
- Tuning観点：RTO/TLPの閾値やカーブ（congestion control）と相性があるため、RACK導入後は再送・輻輳パラメータを見直すこと。
- 既存サービスへ影響が小さければ順次展開：クラウドゲーミングや低遅延サービスでは即効性が高いので優先度高めで検討するとコスト対効果が良い。
- コントリビュート：Pionや利用中ライブラリのアップデートを追い、未対応であればPRやフィードバックを投げるとエコシステム全体の恩恵を伸ばせます。

## 引用元
- タイトル: Show HN: Pion SCTP with RACK is 70% faster with 30% less latency
- URL: https://pion.ly/blog/sctp-and-rack/
