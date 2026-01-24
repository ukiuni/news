---
layout: post
title: "Small Kafka: Tansu and SQLite on a free t3.micro - 無料 t3.micro で動かす小さな Kafka：Tansu + SQLite"
date: 2026-01-24T19:35:31.058Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.tansu.io/articles/broker-aws-free-tier"
source_title: "Small Kafka: Tansu + SQLite on a free t3.micro (AWS Free Tier)"
source_id: 46690779
excerpt: "無料t3.microでTansu＋SQLiteにより低コストでKafka互換ブローカーを迅速構築"
image: "https://blog.tansu.io/articles/broker-aws-free-tier/opengraph-image?4d25d142e2270393"
---

# Small Kafka: Tansu and SQLite on a free t3.micro - 無料 t3.micro で動かす小さな Kafka：Tansu + SQLite
小さなインスタンスで試す、低コストかつ手軽な Kafka 互換ブローカーの始め方

## 要約
Tansu（Rust製のKafka互換ブローカー）を AWS Free Tier の t3.micro 上で SQLite ストレージとして動かし、低コストでプロトタイプやPoCを立ち上げる手順と性能感を紹介します。

## この記事を読むべき理由
無料枠や低スペックインスタンスでメッセージ基盤を素早く立ち上げられる手法は、日本のスタートアップや社内PoCでコストを抑えつつ実験する際に非常に役立ちます。

## 詳細解説
- 環境のポイント
  - t3.micro: 1 GiB メモリ、EBS ベースラインスループット ~10MB/s（上限 ~260MB/s）、CPU はクレジット制。CPUクレジットの監視が重要。
  - Tansu: Apacheライセンスの Rust 製 Kafka 互換ブローカー。ストレージエンジンは SQLite、Postgres、S3 などを選べる。SQLite を使うとメタ/メッセージは単一の tansu.db に収まるためバックアップや移行が簡単。
  - 運用パターン: 単一インスタンス + SQLite（簡易・低コスト） → 負荷時は tansu.db を別インスタンスへコピーしてスケール、もしくは S3 エンジンでステートレス複数インスタンス化。

- 導入の流れ（要点）
  1. Amazon Linux 2023 上で SPAL と docker-compose をインストール、containerd を有効化、ec2-user を docker グループに追加して再起動。
  2. docker-compose で ghcr.io/tansu-io/tansu イメージを起動。環境変数で ADVERTISED_LISTENER_URL と STORAGE_ENGINE を設定し、/data をホストにマウント。
  3. トピック作成や確認は tansu CLI をコンテナ内で実行。性能試験は kafka-producer-perf-test 等で検証。

- 重要なコマンド例
```bash
# システム準備（抜粋）
sudo dnf install -y spal-release docker-compose
sudo systemctl enable containerd.service
sudo usermod -a -G docker ec2-user
sudo /sbin/shutdown -r now
```

```yaml
# compose.yaml（例）
services:
  tansu:
    image: ghcr.io/tansu-io/tansu
    environment:
      ADVERTISED_LISTENER_URL: tcp://YOUR_INSTANCE_NAME:9092
      RUST_LOG: warn
      STORAGE_ENGINE: "sqlite://data/tansu.db"
    volumes:
      - ./ : /data
    ports:
      - "9092:9092"
```

- 実際の挙動と性能感
  - ブローカーは非常にメモリ効率良好（例: 18–27 MB 程度の RSS）。
  - 実測: 単一Macからの負荷で約 6.8 MB/s（約7000レコード/秒、レコードサイズ1KB）を安定して送信。平均レイテンシは数十ms〜百数十ms のレンジ。
  - SQLite ファイルサイズ例: 約 265MB（運用データに依存）。

- t3 ファミリのCPUベースライン（抜粋）
  - t3.micro: vCPU 2, Baseline 10%, CPU credit/hr 12
  - t3.small〜t3.2xlarge はベースライン/クレジットが上がる（需要に応じて上位へ移行）

## 実践ポイント
- 試作/PoC ではまず SQLite を使って tansu.db をバックアップしながら動かす（コピーで復元可能）。
- CPU クレジットを監視し、需要増時は上位インスタンスへ移行または S3 ストレージエンジンでステートレス化する。
- セキュリティグループでアクセス制限し、公開は必要最小限のエンドポイントだけにする。
- ローカルからの負荷試験（kafka-producer-perf-test 等）でスループットとレイテンシを把握する。
- 興味があれば GitHub の Tansu リポジトリをクローンして実際に試す（Apache License）。

以上。興味が湧いたら、まずは Free Tier 上で短時間試して感触を確かめてください。
