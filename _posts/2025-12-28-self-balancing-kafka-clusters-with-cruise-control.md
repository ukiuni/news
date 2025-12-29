---
layout: post
title: Self-balancing Kafka Clusters with Cruise Control
date: 2025-12-28 18:18:32.563000+00:00
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: https://cefboud.com/posts/kafka-cruise-control/
source_title: Exploring Kafka Cruise Control | Moncef Abboud
source_id: 435994260
excerpt: Cruise ControlでKafkaの偏りを自動検知・修復、手を動かす導入手順付き
---
# Kafkaクラスタを“放置しない”運用へ：LinkedIn製 Cruise Controlで自動バランスを実現する方法

## 要約
Kafkaの負荷偏り（ブローカーにトラフィックやディスクが集中する問題）を自動検知・是正するLinkedIn製のツール「Cruise Control」を、手を動かして試せるクイックスタートと運用上のポイントをわかりやすく解説します。

## この記事を読むべき理由
大規模/成長中のKafkaクラスタでは「新しいブローカーがアイドル」「既存ブローカーが過負荷」になることがよく起きます。日本のSRE/プラットフォーム/データチームは、サービス可用性・コスト効率・運用負荷低減のために自律的な再配置（self-healing / rebalance）を導入する価値が高まっています。Cruise Controlはその代表的な実装で、実運用で役立つ知見が得られます。

## 詳細解説
- 何をするツールか  
  Cruise ControlはKafkaクラスタのメトリクスを継続的に集め、事前定義した「ゴール（Disk / CPU / ネットワークの均衡、リーダー配置 など）」に照らして偏りを検出し、最適なパーティション移動とリーダー移行を提案・実行します。LinkedInが開発した堅牢な運用向けコンポーネントです。

- メトリクスの流れ（仕組みの肝）  
  各Brokerに CruiseControlMetricsReporter を metric.reporters として組み込み、ブローカー内の KafkaMetric（bytes in/out, partition size, queue size, replica info など）を専用トピック __CruiseControlMetrics に送り、Cruise Control 本体がそのトピックを消費してクラスタの状態を学習します。

- クイックスタート（概要）  
  1) リポジトリをビルドして Reporter JAR を作る  
  ```bash
  # bash
  git clone https://github.com/linkedin/cruise-control.git
  cd cruise-control
  ./gradlew jar
  ```  
  2) DockerでKafkaブローカー複数台を起動し、作成した reporter JAR を各ブローカーの classpath にマウントして metric.reporters を設定する（__CruiseControlMetrics に送信される）  
  3) Cruise Control を起動（デフォルトで REST/UI を提供）  
  ```bash
  # bash
  ./kafka-cruise-control-start.sh config/cruisecontrol.properties 9090
  ```  
  4) 故意にアンバランスなトピックを作成してデータを投入すると、DiskCapacityGoal などで違反が検出される。差し替えは手動で API を叩くか、自動修復を有効化しておけば Cruise Control が実行する。  
  ```bash
  # bash - 手動でリバランスをトリガー
  curl -X POST "http://localhost:9090/kafkacruisecontrol/rebalance?dryrun=false&json=true"
  ```

- 主要設定と動作の注意点  
  - capacity.json：各ブローカーの容量（DISK:MB, CPU:%, NW_IN/NW_OUT:KB）を設定。テストではデフォルトを小さくして違反を作ると挙動がわかりやすい。  
  - disk.capacity.threshold：デフォルトは 0.8 。つまり容量の80%超で DiskCapacityGoal による移動候補になる。  
  - Goals の並び順や有効化／無効化で最終的な最適化結果が変わる（例：RackAwareGoal を外すと配置制約が緩む）。  
  - Self-healing はデフォルトで無効。実運用で自動実行するか、検知→人間判断で実行するワークフローにするかはリスク許容に依る。

- 内部のさわり（なぜ賢く動くか）  
  Cruise Control は時系列ウィンドウでメトリクスを学習し、複数のゴール群に対するコスト関数を評価して、移動プラン（どのパーティションをどのブローカーへ、どの順序で移動するか）を生成します。移動は「リーダー移行」と「レプリカ移動（インターブローカー）」を伴い、所定の制約（バランス、スループット、移行中の負荷など）を考慮します。

## 実践ポイント
- まずはステージングで検証を：小規模クラスタで capacity.json を調整して違反→修正の流れを再現して挙動を把握する。  
- Self-healing の運用ポリシーを決める：自動実行（短時間で改善）か、人間承認フロー（誤動作のリスク回避）か。  
- Goals の選定と順序が肝：Rack/Throughput/Replicaバランス等、優先度を運用目標に合わせて調整する。  
- 容量情報は動的に：固定値が合わない環境では BrokerCapacityConfigResolver を利用して実リソースを反映させる。  
- 監視とアラートを連携：UI/REST での状態確認に加え、異常検出時は監視ツール経由で通知（移動が長時間続く、IO負荷増など）。  
- 破壊的テストを定期実施：ブローカー停止・追加・高負荷時の挙動を定期的に検証しリカバリ手順を作る。

