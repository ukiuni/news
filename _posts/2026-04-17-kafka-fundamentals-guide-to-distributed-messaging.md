---
layout: post
title: "Kafka Fundamentals - Guide to Distributed Messaging - Kafkaの基礎：分散メッセージング入門"
date: 2026-04-17T07:44:39.752Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://sushantdhiman.dev/kafka-fundamentals-guide-to-distributed-messaging/"
source_title: "Kafka Fundamentals - Guide to Distributed Messaging"
source_id: 359564769
excerpt: "Kafkaでイベント駆動に移行し、耐久性とスケーラビリティを備えたリアルタイム連携を実現する方法"
image: "https://static.ghost.org/v5.0.0/images/publication-cover.jpg"
---

# Kafka Fundamentals - Guide to Distributed Messaging - Kafkaの基礎：分散メッセージング入門

サービス間の連携を“呼び出し待ち”から“イベントの流れ”に変える — Kafkaで作る耐久性とスケーラビリティ

## 要約
Kafkaは「イベントを流して誰でもいつでも読む」ことでサービス間結合を緩め、高スループット・耐久性・再生可能なデータ処理を実現する分散イベントストリーミング基盤です。

## この記事を読むべき理由
マイクロサービス化やリアルタイム分析が進む日本の開発現場で、サービス切り離し・障害耐性・監査のための「イベント駆動設計」を採るなら、Kafkaの基本概念を押さえることは必須です。

## 詳細解説
- なぜKafkaが必要か：サービスA→Bの同期呼び出しはBの障害でAも停止する。Kafkaはイベントを公開(publish)し、消費(consume)を独立させてシステムを非同期にする。
- 基本モデル：Producer（送信）→ Topic（論理チャネル）→ Consumer（受信）。データは「イベントの流れ」として扱う。
- パーティション：Topicは複数のPartitionに分割され、各Partitionは追加のみの順序付きログ。並列処理（スケール）と同時にパーティション内での順序保証を提供する。
- オフセット：各メッセージにはPartition内で連番のoffsetが付く。Consumerは自分のオフセットを管理し、再開や再生（replay）が可能。
- コンシューマーグループ：グループ内で各Partitionはちょうど1つのメンバーに割り当てられることで水平スケールとフォールトトレランスを実現する。メンバー増減時は自動再バランスされる。
- ブローカーとクラスタ：Brokerがメッセージを保持し、複数BrokerでClusterを形成して単一障害点を排除する。
- メタデータ管理：従来はZookeeperでクラスタ管理をしていたが、KRaftではKafka自身がRaftを使って内部管理（Zookeeper不要）できるようになった。
- レプリケーションとISR：Partitionはリーダーと複数のフォロワーで複製され、In-Sync Replica（ISR）集合だけからリーダー選出することでデータ損失を防ぐ。
- 配信保証：設定次第で At-most-once（重複なしだが喪失あり）、At-least-once（喪失なしだが重複あり）、Exactly-once（重複なく1回）を実現可能。Exactly-onceは冪等プロデューサやトランザクションAPIを使う。

## 実践ポイント
- 最初はTopic設計でパーティション数を決める（将来のスループットを見越す）。あとから増やせるが手間がかかる。
- コンシューマーはオフセットのコミット戦略（処理後コミット vs 事前コミット）で配信保証を選ぶ。
- レプリケーション因子とISRの監視を必ず行い、運用中のブローカー障害に備える。
- 開発環境ではKRaftの簡易セットアップ、運用ではマネージドKafka（MSK/Confluent等）を検討すると導入負荷を下げられる。
- イベントの再生性を活かして監査ログや状態再構築、ストリーム処理のリプレイ設計を組み込む。

以上を押さえれば、Kafkaを使ったイベント駆動アーキテクチャの第一歩が踏み出せます。
