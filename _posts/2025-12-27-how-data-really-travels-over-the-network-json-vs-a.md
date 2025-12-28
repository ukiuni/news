---
layout: post
title: "How Data Really Travels Over the Network (JSON vs Avro vs Protobuf)"
date: 2025-12-27T20:40:13.102Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://medium.com/@venkateshwagh777/how-data-really-travels-over-the-network-json-vs-avro-vs-protobuf-0bfe946c9cc5"
source_title: "How Data Really Travels Over the Network (JSON vs Avro vs Protobuf)"
source_id: 437979378
excerpt: "帯域・CPU・互換性で差が出るJSON・Avro・Protobufの実務的選び方と計測手法を解説"
---

# ネットワークで「本当に」データはどう移動するか — JSON vs Avro vs Protobuf、現場での選び方

## 要約
テキスト系のJSONと、スキーマ駆動のAvro／Protobufは「見た目」以上に通信コスト・パースコスト・互換性で差が出る。用途（公開API／社内高スループット／ストリーミング）に応じた選択基準を示す。

## この記事を読むべき理由
日本のプロダクト開発では、モバイル回線・IoT・マイクロサービス・Kafka基盤など帯域やレイテンシ、運用性がボトルネックになりやすい。どのシリアライゼーションを選べばコスト削減と保守性向上につながるかを実務目線で整理する。

## 詳細解説
- シリアライゼーションの役割
  - アプリ内オブジェクト → バイト列（ネットワーク越し）へ変換する過程。ここでサイズ・CPU負荷・可読性・互換性が決まる。

- JSON（テキスト）
  - 長所: 人が読める、ブラウザや多くの言語で標準サポート、REST/公開APIとの親和性が高い。
  - 短所: 冗長（キー名がそのまま含まれる）、パースが遅い（文字列解析コスト）、スキーマが明示されないと互換性管理が難しい。
  - 適用例: 公開REST API、デバッグやログ、軽量で頻繁に見るデータ。

- Avro（スキーマ同梱/リポジトリ型）
  - 長所: スキーマが明示され、メッセージにスキーマIDを付ける運用が一般的（Kafkaとの相性◎）。可変長データで効率的、スキーマ進化（互換性）に強い。
  - 短所: バイナリ形式で可読性は低い。言語別のサポートは豊富だが、プロジェクトの導入コストあり。
  - 適用例: イベントストリーミング（Kafka）、バッチ処理、データレイクへの投入。

- Protobuf（バイナリ、IDLベース）
  - 長所: 非常に小さいバイトサイズ、速いパース、gRPCとの親和性が高い。フィールド番号による効率的エンコーディング（varint等）。
  - 短所: スキーマ（.proto）管理が必須。複雑な型やJSONの柔軟さには劣る。可読性は低い。
  - 適用例: マイクロサービス間RPC（gRPC）、モバイルアプリの通信、低帯域I/O。

- サイズと速度（概念的な比較）
  - 一般に: JSON > Avro ≈ Protobuf（JSONが最も大きく遅い）。バイナリ形式は2〜10倍小さくなることが多い（データの構造に依存）。
  - 圧縮（gzip/snappy）を併用すれば差は縮まるが、CPU負荷とレイテンシのトレードオフになる。

- スキーマ進化と互換性
  - JSON: 明示スキーマが無ければ破壊的変更になりやすい。JSON Schemaを使えば改善するが運用が必要。
  - Avro: 互換性ルール（追加はoptional、削除は慎重）を明確に扱える。KafkaエコシステムでSchema Registryを使うのが定石。
  - Protobuf: フィールド番号を予約しておけば下位互換性を保てる。oneofやoptionalの扱いに注意。

- 実践上の注意点
  - 小さな文字列フィールドが大量にある場合はバイナリの恩恵が大きい。
  - リフレクションや動的スキーマを多用すると実行時コストが増える。
  - モバイル・IoTではバイトサイズとCPUが直接ユーザー体験に影響する。

コード例（簡単な比較）
json
{
  "userId": 123,
  "name": "Yamada",
  "active": true
}
protobuf
syntax = "proto3";
message User {
  int32 userId = 1;
  string name = 2;
  bool active = 3;
}

（JSONは可読だがキー名がそのまま転送され、Protobufはフィールド番号で効率的にエンコードされる）

## 実践ポイント
- 公開API（外部開発者向け）→ JSON（またはJSON-LD/OpenAPIで互換性確保）。
- 内部高スループットサービス（gRPC/Kafka）→ Protobuf（RPC）かAvro（イベントストリーミング／Schema Registry）。
- 帯域やコストが重要なら、まずプロトタイプで実測ベンチ（payloadサイズ、CPU、エンドツーエンドレイテンシ）を取る。
- スキーマ運用を自動化する：CIでスキーマ互換性チェック／Schema Registry／生成コードの管理。
- 圧縮は万能ではない：圧縮CPUコストと遅延を評価する。モバイルではバイト削減が優先されることが多い。
- 日本の現場では、既存のMEP（Mobile Edge）やキャリア制約を考え、モバイル通信ならProtobuf＋gRPC-Webや軽量フォーマットを検討する価値が高い。

