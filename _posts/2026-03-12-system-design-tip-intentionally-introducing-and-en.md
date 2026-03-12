---
layout: post
title: "System design tip: Intentionally introducing and enforcing constraints produces simpler, more powerful systems - 制約を意図的に導入・強制すると、よりシンプルで強力なシステムが生まれる"
date: 2026-03-12T18:57:11.767Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.rodriguez.today/articles/emergent-event-driven-workflows"
source_title: "What Happens When You Constrain an Event-Driven System to Three Primitives - Roland Rodriguez"
source_id: 384895617
excerpt: "ソース/ハンドラ/シンクの制約で設定ファイルが実行可能なアーキテクチャとなり運用・監視・再現が自動化"
image: "https://www.rodriguez.today/avatar.jpg"
---

# System design tip: Intentionally introducing and enforcing constraints produces simpler, more powerful systems - 制約を意図的に導入・強制すると、よりシンプルで強力なシステムが生まれる

「できることを減らす」ほうが強い――イベント駆動を3つの原始（Source / Handler / Sink）に厳格に分けると、見違えるほど設計・運用が楽になる話

## 要約
システムを構成するコンポーネントを「Source（発行）」「Handler（購読＋発行）」「Sink（購読）」の3役割に厳密に制約すると、構成ファイルが実行可能なアーキテクチャ仕様になり、起動順序・監視・再現性・多言語混在・イベントストアなどが自動的に得られるという設計手法の提案。

## この記事を読むべき理由
イベント駆動の運用・デバッグで「どこが何を出しているか分からない」「起動順で落ちる」「オブザーバビリティが散らばる」などに悩む日本のエンジニアに、構造的にこれらを解消する実践的な設計パターンを示すから。

## 詳細解説
- 3つの原始:
  - Source: 出力のみ（publish）。外部入力をシステムに持ち込む。
  - Handler: 入力を受け取り変換して出力もする（subscribe + publish）。
  - Sink: 入力のみ受け取り副作用（DB/外部通知など）を行う（subscribe）。
- 制約の強制:
  - Rustの型システムで各役割を別構造体にしてコンパイル時に境界を保証（Sourceにsubscribeメソッドが無い等）。「無効な状態を表現できない」設計。
- 設定ファイルがアーキテクチャになる:
  - TOMLで各コンポーネントの publishes / subscribes を宣言するだけで、エンジンはそれを実行可能なトポロジーとして起動・監督する。結果、ソースを読まなくても全体の流れが理解できる。
```toml
# toml
[[sources]]
name = "timer"
publishes = ["timer.tick"]

[[handlers]]
name = "filter"
subscribes = ["timer.tick"]
publishes = ["timer.filtered"]

[[sinks]]
name = "console"
subscribes = ["timer.filtered"]
```
- ライフサイクルと順序付け:
  - 役割の方向性（Sink ← Handler ← Source）から起動/停止順序を自動導出。Sink を先に、Source を最後に起動することでメッセージロスを防ぐ。
- 多言語混在とプロセス分離:
  - 各プリミティブは独立プロセス（IPC/MessagePackなど）で通信するため、言語はコンポーネント単位で自由に選べる（Rust ↔ Python ↔ Deno 等）。
- 中央ルーター→自動イベントストア:
  - 全メッセージがエンジンを経由するため、エンジン側でJSONログ＋SQLiteに自動永続化でき、MessageId（時間ソート可能なUUIDv7ベース）／causation／correlationで完全なトレースやリプレイが可能に。
- 耐障害性・バックプレッシャー:
  - 各アクター（プリミティブ）は分離された受信箱（bounded）を持ち、監視／再起動ポリシー（Erlang風のsupervision）で局所障害が全体停止に至らない。「遅いSink→自然な流量制御」が構造的に実現される。
- Rustらしい型安全性:
  - type-stateパターンでライフサイクルを型で表現し、ランタイムエラーをコンパイル時に減らす。フレームワーク側も unsafe を使わない実装で安全性を担保。

## 実践ポイント
- 小さな実験から始める: 新規パイプラインはまず Source/Handler/Sink に分けて設計してみる。
- 境界をランタイムで強制する: 単なる運用ルールではなく、ランタイム（または型）で違反を検出できるようにする。
- 設定ファイルをソースに: トポロジーはコード分散ではなく中央の設定で記述し、アーキレビューを設定ファイルベースで行う。
- プロセス分離で多言語利点を享受: 言語ごとの強み（データ処理はPython、低レイテンシはRust等）をコンポーネント単位で使い分ける。
- 観測性を設計に組み込む: 中央ルーター経由ならイベントストア（時系列ID・因果関係付き）はほぼ自動で得られる。ログ→分析→リプレイまでのパスを作ると便利。

短く言えば、「できることを増やす」より「できないことを明確にする」設計が、イベント駆動システムの複雑さを減らし、運用性と信頼性を高める――この記事はその実践例と基盤設計（Rust＋actor＋プロセス分離）を示しています。
