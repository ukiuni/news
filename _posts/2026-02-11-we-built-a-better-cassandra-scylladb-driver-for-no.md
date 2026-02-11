---
layout: post
title: "We Built a Better Cassandra + ScyllaDB Driver for Node.js – with Rust - Node.js向けにRustで作ったより速いCassandra/ScyllaDBドライバ"
date: 2026-02-11T21:01:24.147Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.scylladb.com/2026/02/11/cassandra-scylladb-driver-for-node-js-with-rust/"
source_title: "We Built a Better Cassandra + ScyllaDB Driver for Node.js – with Rust - ScyllaDB"
source_id: 445293991
excerpt: "Rustコアで高速化、NAPI最適化済みのNode.js向けScyllaDBドライバを解説"
image: "https://www.scylladb.com/wp-content/uploads/1200x628-js-driver-rust-core.jpg"
---

# We Built a Better Cassandra + ScyllaDB Driver for Node.js – with Rust - Node.js向けにRustで作ったより速いCassandra/ScyllaDBドライバ
Node.jsアプリを「そのまま速く」する――Rust製コアをラップした新ドライバの舞台裏と実戦で使える最適化。

## 要約
ScyllaDBのRustドライバを裏側に据え、Node.js向けにN-API経由でラップした新ドライバの設計・選択肢・性能改善の取り組みを紹介。初期はNAPI-RSのオーバーヘッドで遅かったが、データ表現／ブリッジ戦略の見直しで実用レベルへ到達しつつある。

## この記事を読むべき理由
Node.jsを使う日本の開発チームにとって、スループットや低レイテンシを必要とするリアルタイム系／データ集約系サービスで「既存のJSドライバより有利になる可能性」があるため。特にScyllaDBの shard‑per‑core や高並列処理を活かしたい場合に重要な知見が得られる。

## 詳細解説
- 動機：既存のDataStax Node.jsドライバはCassandra互換で問題なく動くが、ScyllaDB固有の設計（シャード単位処理など）を活かしきれない。Rust製の公式ドライバをバックエンドに使えば機能追従や性能面で有利。
- 実装アプローチ：Rustドライバを「ラップ」してNode側APIを提供。C/CPP向けの低レイヤ（N-API/V8）を直接触る代わりに、unsafeを少なくするラッパーライブラリ（NAPI‑RS と Neon）を検討し、可読性・開発速度・性能から NAPI‑RS を採用。
- NAPI‑RS vs Neon の判断基準：自動シリアライズによるコードの簡潔さ、若干優れたコール性能、ドキュメントの使いやすさで NAPI‑RS を選択。
- 性能問題の発見：初期実装はNAPI‑RS経由でのJSオブジェクトのやり取りが大きなオーバーヘッドになり、純粋なRust実装や既存のDataStaxドライバに比べ遅延が目立った（ベンチで大幅差）。
- 最適化方針：クロスランゲージの境界ではJSオブジェクトを多用せず、Buffer や組み込み型を優先。パラメータ／結果のパースやページングなど頻出パスを最適化し、NAPIコールを減らすことで性能回復を図った。
- サポート機能（2025年5月時点の主な機能）：通常のSELECT/INSERT、バッチ、全CQL型のマッピング、prepared/unprepared両対応、ページング（自動／手動／page‑state転送）、並列実行用の専用エンドポイント（内部で最適化し単純並列実行より約35%高速化）、prepared statement のキャッシュをRustのDriver Caching Sessionで利用。
- エラーハンドリングとシャットダウン：Rust側の細分化されたエラーを可能な限りそのまま透過しつつ、自ラッパー生成エラーは既存ドライバ互換を意識。接続はクライアントオブジェクトが破棄されたら自動で閉じる挙動を採用（shutdown手動呼び出しも可）。  
- ステータス：ワルシャワ大との共同プロジェクト（ZPP）で開発され、以降ScyllaDBドライバチームが採用・保守。ほぼ本番対応段階へ。

## 実践ポイント
- まずは最新版のリポジトリ／readmeを確認し、テスト/ベンチを自環境で再現する。  
- 大量クエリは prepared statements + prepared cache を活用する（同一文の再準備を避ける）。  
- 多数の類似クエリを投げる場面では「並列実行エンドポイント」を使うとオーバーヘッドを抑えられる（内製の並列実行より高速化）。  
- ページングは用途に応じて自動／手動／page‑state転送を選択。ステートを渡せばステートレスなWebサーバ群にも適用可能。  
- Node↔Rust間のデータは可能な限り Buffer やプリミティブ型で渡し、JSオブジェクトの頻繁な往復を避ける（NAPIコール削減で大きく性能改善）。  
- Node.jsサービスで低レイテンシ・高スループットを求めるなら、ScyllaDB＋このドライバの組合せをステージングで評価する価値あり。

（参考）この取り組みはScyllaDB公式のRust実装を活かす設計思想で、今後の新機能対応や言語間一貫性の面でも恩恵が期待される。
