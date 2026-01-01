---
layout: post
title: "Show HN: BusterMQ, Thread-per-core NATS server in Zig with io_uring - BusterMQ：Zigとio_uringで作るスレッド毎コアのNATS互換サーバー"
date: 2026-01-01T01:38:44.979Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://bustermq.sh/"
source_title: "Show HN: BusterMQ, Thread-per-core NATS server in Zig with io_uring"
source_id: 46449812
excerpt: "Zigとio_uringで作るNATS互換MQが数百万msg/s級を達成、次世代高スループット設計"
---

# Show HN: BusterMQ, Thread-per-core NATS server in Zig with io_uring - BusterMQ：Zigとio_uringで作るスレッド毎コアのNATS互換サーバー
Zig×io_uringで突き抜ける高スループットMQ──BusterMQが示す「次世代のメッセージング設計」

## 要約
BusterMQはZigで書かれ、io_uringとスレッド毎コア（thread-per-core）アーキテクチャを採用したNATSプロトコル互換のメッセージサーバーで、ローカルのベンチマークでは数百万メッセージ/秒・数GB/s級の帯域を達成しています（現状は非常にアルファ）。

## この記事を読むべき理由
日本でもリアルタイム性と高スループットが求められる分野（金融トレーディング、広告配信、ログ/メトリクス収集、ゲームサーバーなど）が増えています。既存のNATSクライアントを流用しつつ、OSレベルの新技術（io_uring）で性能を引き出す設計は、次世代インフラを考える上で実践的な示唆を与えます。

## 詳細解説
- コア設計
  - Thread-per-core: 各CPUコアに1スレッドを固定し、ローカルデータ構造とキャッシュ効率を最大化。ロック競合やコンテキストスイッチを最小化する設計思想です。
  - io_uring: Linuxの新しい非同期I/Oインターフェースを活用し、syscallオーバーヘッドを減らしてディスク/ネットワークI/Oを効率化します。
  - Busy-poll（スピンループ）モード: ソケットの待ち時間でポーリングを回し、割り込み待ちによる遅延を下げる代わりにCPUを消費する設定も提供。

- プロトコル互換性
  - NATSプロトコル互換を謳っており、既存のNATSクライアントがそのまま利用可能（互換性の範囲は要検証）。
  - 基本操作はPUB/SUB/UNSUB、ワイルドカード購読、キューグループ、将来的にRequest/Replyをサポート予定。

- ベンチマークのポイント（抜粋）
  - テスト条件: 10パブリッシャー、100サブスクライバー（トピックあたり10）、10トピック、5千万メッセージ、128バイトペイロード、AMD Ryzen 9 9950X（16コア）、ローカルホスト。
  - 代表値: 公開されている設定で配信レートが約52M〜59Mメッセージ/秒、帯域は最大約8.2 GB/s。p50 レイテンシは数ms台（構成により変動）。
  - 比較: Go実装のNATSと比べて、適切な設定（io_uring+BusyPoll+Route）で大幅に高スループット／低レイテンシを示していますが、環境依存・チューニング必須。

- 実装スタックとライセンス
  - 実装言語: Zig（軽量でC相当の性能、低レイヤ制御に適合）
  - ビルド: Bazelで起動例が示されている（git clone して bazel run）。
  - ライセンス: Apache 2.0
  - ステータス: VERY ALPHA — 本番投入前の注意喚起あり。

## 実践ポイント
- まずローカルで試す
  - 前提: Linuxカーネルのio_uringサポート（比較的新しいカーネル推奨）。VMよりも物理マシンやCPUコア数が多い環境で差が出やすい。
  - 手順（大まか）: リポジトリをクローン → bazel run でサーバ起動 → 既存のNATSクライアントで接続して動作確認 → 提供ベンチマークを走らせて設定（BusyPoll、Route）を比較。
- チューニングの方向性
  - Busy-pollはレイテンシ改善に有効だがCPU使用量が増えるため、SLAとコストを天秤にかける。
  - Route（シャード認識ルーティング）を有効にするとコア間の移動が減りスループット向上が期待できる。
- 日本での導入検討ポイント
  - 既存のNATSエコシステムを活かせる点は有利。ただし「アルファ」段階なので可観測性・フェイルオーバー・セキュリティ機能の成熟度を評価する必要あり。
  - 国内クラウド／ベアメタルでのIO特性を計測し、io_uringやBusy-pollの効果を実測することが重要。
- リスクと留意点
  - カーネル/ネットワーク設定やハードウェアに強く依存するため、ベンチ結果は環境差が大きい。
  - プロトコル互換を謳うが、細かなクライアント挙動の差異はテスト必須。

## 引用元
- タイトル: Show HN: BusterMQ, Thread-per-core NATS server in Zig with io_uring
- URL: https://bustermq.sh/
