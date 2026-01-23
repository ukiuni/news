---
layout: post
title: "Replacing Protobuf with Rust to go 5 times faster - ProtobufをRust直結に置き換え、5倍速くする方法"
date: 2026-01-23T10:44:12.310Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://pgdog.dev/blog/replace-protobuf-with-rust"
source_title: "Replacing Protobuf with Rust to go 5 times faster | PgDog"
source_id: 46730214
excerpt: "Protobufを廃してC↔Rust直結、解析が約5倍速化の実例"
image: "https://pgdog.dev/assets/images/logo2_wide.png"
---

# Replacing Protobuf with Rust to go 5 times faster - ProtobufをRust直結に置き換え、5倍速くする方法
高速化の「裏ワザ」：ProtobufをやめてC↔Rustを直結させたら、パーサー性能が劇的に上がった話

## 要約
PgDogがlibpg_queryのProtobuf経由の境界を廃し、bindgen＋生成ラッパー（Claude支援）でC↔Rustを直結させたところ、パースが約5.4倍、デパースが約9.6倍高速化しました。

## この記事を読むべき理由
PostgreSQLを使う多くの日本のサービス（DBプロキシ、ミドル層、マイクロサービス）に直接効く性能改善の実例です。シリアライズ層がボトルネックになる事実、実測での効果、実装上の注意点が学べます。

## 詳細解説
- 背景：PgDogはPostgres向けプロキシで、内部でlibpg_queryを使いSQLのASTを扱う。既存のRustバインディング（pg_query.rs）はProtobufでCとデータ交換していたが、ここがホットスポットと判明（プロファイラ：samply + Firefox profiler）。
- なぜProtobufが問題か：Protobufは汎用で速いが、境界での(デ)シリアライズがCPUコストとメモリアロケーションを生む。特に低レイテンシ／低資源のプロキシでは勿体ない。
- 試した対策：まずはキャッシュ（LRU＋ハッシュマップ）を導入したが、ORMのバグやクライアントドライバ（例：古いpsycopg2）が準備ステートメント非対応でキャッシュが効かないケースがあり限界があった。
- 決断と実装：bindgenでC構造体をRust側に取り込み、Protobufを介さず直接Cポインタ→Rust構造体へ変換するunsafeなラッパーを実装。LLM（Claude）で生成支援を受けつつ、最終的に約6,000行の再帰的な変換コードに。既存のProstで生成されたRust型を再利用し、parse_rawとparseの出力差分を自動テストで厳密検証した。
- 技術ポイント：
  - ASTはツリー構造なので再帰でノードを1回だけ処理する方式を採用（高速でキャッシュフレンドリー）。反復版は余分なアロケーションや探索で遅かった。
  - 各ASTノードごとに変換関数を作り、nullチェックやNodeTagで振り分けるunsafeコードが中心。
  - 対象メソッド：parse, deparse, fingerprint, scan を置き換え、pgbenchで+25%改善も確認。
- ベンチ結果（抜粋）：
  - pg_query::parse (Protobuf) — 613 qps → parse_raw (Direct) — 3357 qps（約5.45×）
  - pg_query::deparse (Protobuf) — 759 qps → deparse_raw (Direct) — 7319 qps（約9.64×）

## 実践ポイント
- まずはプロファイル（samplyなど）で本当のボトルネックを突き止める。感覚で変えるな。
- シリアライズを挟んでいる境界は疑う価値あり。同一言語内で完結できるなら直結を検討する。
- bindgenでCヘッダを取り込み、既存の型（Prost生成型等）と突き合わせると検証が楽になる。
- 大量のunsafeコードを入れるので、自動テストでバイト単位比較を必須にする（差異があれば生成コードを再生成）。
- 再帰は高速だがスタック深度に注意。深いクエリでの安全策を検討すること。
- 日本の現場では、ドライバ（psycopg2等）の準備ステートメント対応状況やORMのクエリ生成の癖も合わせて確認すると効果が出やすい。

興味があれば、実装の見通しやベンチ手順の翻訳・要約を提供します。どの部分を深掘りしますか？
