---
layout: post
title: "Modular Monolith: dependencies and communication between Modules - モジュラーモノリス：モジュール間の依存と通信"
date: 2026-01-22T16:10:45.687Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://binaryigor.com/modular-monolith-dependencies-and-communication.html"
source_title: "Modular Monolith: dependencies and communication between Modules"
source_id: 420469177
excerpt: "境界と契約を明確化し、Outboxや同期で分割と可用性を両立する実践指南"
image: "https://binaryigor.com/assets/og-image.png"
---

# Modular Monolith: dependencies and communication between Modules - モジュラーモノリス：モジュール間の依存と通信
モジュラーモノリスで「後で困らない」依存設計 — 実践的パターンと落とし穴

## 要約
モジュール設計は通信パターンを決める重要要素。同期的なClient/API、アプリ内イベント、Outbox、背景同期それぞれのトレードオフを理解しておけば、将来の分割や運用がぐっと楽になる。

## この記事を読むべき理由
日本の多くの現場はモノリシックな運用から始まり、小規模チームで長く運用することが多いです。将来のマイクロサービス化やデータ分離を見据えた設計判断が現場コストを大幅に下げます。

## 詳細解説
1. モジュール設計の原則
   - 単一責任・自己完結：ある機能を実装する際に複数モジュールを同時に変更する頻度が高ければ設計が悪い。
   - 依存は最小化：理想は依存ゼロ。現実的には「共通の契約（shared module）」だけを参照するようにする。

2. 主な通信パターンと特徴
   - Client / API（同期メソッド呼び出し）
     - シンプルで開発コストが低い。モノリスのままなら十分有効。
     - 欠点：別サービス化するとネットワーク遅延／信頼性の問題、トランザクションの跨りは危険。
     - 例（Java風のインターフェース）:
```java
interface UserClient {
  Optional<User> ofId(UUID id);
  Map<UUID, User> ofIds(List<UUID> ids);
}
```
   - Application Events（インメモリイベント）
     - ある処理の「起こったこと」を他モジュールへ通知。簡単だが、同一DBを暗黙に仮定しがちでトランザクションの境界を汚す恐れがある。
   - Outboxパターン
     - 変更とイベントを同一トランザクションでDBに書き、別プロセスがOutboxを外部に配信する。DB依存を局所化でき、将来の分離が容易。
     - 副作用：配信は at-least-once になるため、消費側は冪等（idempotent）にする必要。
   - Background Data Synchronization（バックグラウンド同期）
     - リクエスト処理中は他モジュールを呼ばない原則。必要なデータは事前に同期してローカルで持つ（イベント購読か定期同期）。
     - メリット：リアルタイム応答で外部呼び出しを避け、可用性向上。注意点は初期データロードや同期遅延の扱い。

3. いつどれを選ぶか（概略）
   - すぐに別サービス化する予定がない → Client/APIで十分。クロスモジュールトランザクションは避ける。
   - 将来的な独立性やDB分離を見越す → Outbox＋イベント駆動を推奨。
   - レイテンシや可用性重視の読み取り用途 → バックグラウンド同期。

## 実践ポイント
- モジュール境界をまず紙に書く：変更時に複数モジュールを変える頻度をチェック。
- 共通契約は shared module に置く（インターフェース／DTOのみ）。
- クロストランザクションを禁止するルールを作る（CIチェックやコードレビューで守る）。
- Outbox導入時は配信処理の監視・リトライ戦略と消費側の冪等化を必須にする。
- バックグラウンド同期を使う場合、初期ロードと差分再送の仕組みを用意する。
- 日本の現場では「まずモノリスで素早く価値を出す」→「必要になったらOutbox等で切り替え」が現実的。

短く言えば：まずは明確な境界と契約を作り、トランザクション境界を守りつつ、将来の分割を見据えてOutboxや背景同期を準備しておくと安全です。
