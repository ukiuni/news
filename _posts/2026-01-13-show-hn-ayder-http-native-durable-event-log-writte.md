---
layout: post
title: "Show HN: Ayder – HTTP-native durable event log written in C - Ayder：HTTPネイティブな耐久イベントログ（C製）"
date: 2026-01-13T18:46:10.141Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/A1darbek/ayder"
source_title: "GitHub - A1darbek/ayder"
source_id: 46604862
excerpt: "curlだけで使えるC製の軽量イベントログ、Raft+AOFでKafka並み耐久を簡単導入"
image: "https://opengraph.githubassets.com/265e5efba7169a7f4181ba9f231c6ac241911db53fd89c324f6c2b36dc2fe591/A1darbek/ayder"
---

# Show HN: Ayder – HTTP-native durable event log written in C - Ayder：HTTPネイティブな耐久イベントログ（C製）

curlだけで使える軽量イベントストリーミング「Ayder」──Kafka級の耐久性をシンプルなHTTPで実現

## 要約
AyderはCで書かれた単一バイナリのイベントログ／メッセージバスで、クライアントはcurlだけで十分。Raftによる同期多数決レプリケーション＋AOF（append-only file）で耐久性を確保しつつ、運用は極めてシンプルに保てます。

## この記事を読むべき理由
日本の中小〜大規模チームやエッジ案件では、Kafkaの運用コスト（JVM、Zookeeper、パーティション管理）が負担になりがちです。Ayderは「強い耐久性」と「HTTPでの扱いやすさ」を両立するため、短期間でプロトタイプやオンプレ/エッジに導入しやすい選択肢になります。

## 詳細解説
- アーキテクチャ概要  
  - 単一バイナリで動作。外部にJVMやZooKeeperは不要。  
  - RaftでHA（3/5/7ノードクラスタをサポート）し、同期多数決（sync-majority）で書き込みを確定させるため、書き込みの耐久性が強い。  
  - データはシーリングされたAOF（append-only files）に永続化され、クラッシュ後の復旧時にAOFを再生して欠損分をリーダーからストリームで取得する。  
- APIと使い勝手  
  - REST/HTTPベースのAPI：トピック作成、produce、consume、commit、retention操作など。curlで普通に操作できる。  
  - 消費は /broker/consume/{topic}/{group}/{partition}、オフセットは明示コミット式（consumer group による位置管理）。  
  - バッチ入力はNDJSONで受け付け、binary-safeな取得はbase64エンコードで対応。  
- 性能と復旧特性（元ベンチより）  
  - 3ノードRaft、実ネットワーク（DigitalOcean）での持続書き込み：約50K msg/s（wrk2 @ 50K req/s）。クライアントP99は約3.5ms、サーバ側ハンドラP99.999は約1.22ms。  
  - クラッシュ復旧：8MオフセットのケースでSIGKILL→再起動→クラスター全復旧が約40–50秒。Kafkaと比べて迅速（運用工数・ダウンタイムが小さい点が強み）。  
  - ARM64でも高性能（Snapdragon X Eliteで10万/s超の計測あり）──エッジや低電力サーバでも有望。  
- 機能一覧ハイライト  
  - パーティションごとのappend-onlyログとオフセット、consumer groups、コミットと再開、AOFシールによる確実な永続化、RaftベースのHA、簡易KV（CAS/TTL）、プロミューテーション用メトリクス（Prometheus/Grafana同梱のCompose構成あり）。  
- 実装／ビルド要件  
  - 依存: libuv 1.51+, OpenSSL, zlib, liburing。Docker Composeで起動すれば開発検証はすぐ始められる。

## 実践ポイント
- まずはDocker Composeで動かしてみる（Prometheus/Grafana同梱で可視化も確認可能）：
  ```bash
  # リポジトリをクローンして起動
  git clone https://github.com/A1darbek/ayder.git
  cd ayder
  docker compose up -d --build
  ```
- curlでサクッと試す（トピック作成→produce→consumeの最短例）：
  ```bash
  # トピック作成
  curl -X POST localhost:1109/broker/topics \
    -H 'Authorization: Bearer dev' \
    -H 'Content-Type: application/json' \
    -d '{"name":"events","partitions":4}'

  # メッセージをproduce
  curl -X POST 'localhost:1109/broker/topics/events/produce?partition=0' \
    -H 'Authorization: Bearer dev' \
    -d 'hello world'

  # 消費（base64エンコードでbinary-safe）
  curl 'localhost:1109/broker/consume/events/mygroup/0?limit=10&encoding=b64' \
    -H 'Authorization: Bearer dev'
  ```
- 日本のユースケースでの提案  
  - 小〜中規模の社内イベントバスやログ集約（オンプレ／クラウド混在）に最適。  
  - エッジデバイス群や工場IoTのゲートウェイで、ARM64端末にデプロイしてローカルで耐久ログを保ちつつ、必要時にクラスタで同期する構成が有効。  
  - ただしKafkaの豊富なエコシステム（Connect、MirrorMaker、広範なエコシステム依存）や大規模マルチテナント要件がある場合は、移行に慎重になるべき。Ayderはシンプルさと低運用コストを重視する場面で強い選択肢です。
- 注意点  
  - 現状はコミュニティプロジェクト（READMEやベンチ情報を確認して自己検証を推奨）。運用環境への適用前に耐障害やスループットの実測を。  
  - セキュリティ／認証（Bearerトークン方式の例あり）やバックアップ戦略は自組織の要件に合わせて整備すること。

Ayderは「HTTPだけで扱える、高速で堅牢なイベントログ」を求めるチームにとって魅力的な新しい選択肢です。まずはDockerで動かして、既存のHTTPツールチェーン（curl, nginx, Prometheus）でどこまで簡単に作れるか試してみてください。
