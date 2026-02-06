---
layout: post
title: "Redis/Valkey Replication Internals: The Architecture Behind Zero-Copy Command Propagation - Redis/Valkey レプリケーション内部：ゼロコピーでコマンドを伝播させるアーキテクチャ"
date: 2026-02-06T14:02:22.226Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://frostzt.com/blog/redis-valkey-replication-internals"
source_title: "Redis/Valkey Replication Internals: The Architecture Behind Zero-Copy Command Propagation | Sourav Singh Rawat"
source_id: 407858872
excerpt: "TTLの穴を突く不整合対策とゼロコピーレプリケーションの秘密"
image: "https://frostzt.com/og?title=Redis%2FValkey%20Replication%20Internals%3A%20The%20Architecture%20Behind%20Zero-Copy%20Command%20Propagation"
---

# Redis/Valkey Replication Internals: The Architecture Behind Zero-Copy Command Propagation - Redis/Valkey レプリケーション内部：ゼロコピーでコマンドを伝播させるアーキテクチャ
魅力的タイトル: TTLの「穴」と高速レプリケーションの秘密 — Valkey/Redisが採る“ゼロコピー”戦略を分かりやすく解説

## 要約
Valkey（Redis系）のレプリケーションは、コマンドを書き換え／共有メモリブロック（replBufBlock）の参照カウントで「ゼロコピー」伝播を実現する。一方でTTLやハッシュフィールド単位の有効期限は遅延による不整合を生みやすく、実装上の工夫が重要になる。

## この記事を読むべき理由
日本のサービス（キャッシュ層やセッション管理、分散キャッシュを使うWeb系プロダクト）はTTLとレプリケーションの整合性に敏感です。設計／運用で事故を減らし、スループットを高める実装テクニック（ゼロコピーやコマンド書き換え）を実務目線で理解できます。

## 詳細解説
- 問題事例（TTLとKEEPTTL）  
  ハッシュフィールドにTTLが設定された状態でマスター上のコマンドに KEEPTTL を付けて上書きすると、ネットワーク遅延やパーティションでレプリカ側の元のTTLが先に切れてしまうケースがある。こうなるとレプリカではTTLが失われ、永続化された不整合が起きる（マスターは期限切れ／レプリカは有効、など）。

- ハッシュフィールド有効期限（HFE）の扱い  
  Valkeyはフィールド単位のTTLをサポート。期限回収は「遅延削除（参照時にチェック）」と「バックグラウンド走査（秒間サンプリング）」の組合せで実現。大量のハッシュ内フィールドをスケールさせるために vset 等の補助構造を使う。

- コマンド書き換えでの整合性確保  
  非決定論的な操作（時間、浮動小数点など）はマスター側で最終値へ書き換えられてから伝播される。例：INCRBYFLOAT を SET に書き換える、期限切れフィールドは hdel に置換してレプリカでも削除させる。オリジナルの argv は監視用に残し、実際にレプリケーションに送る argv を書き換える設計。

- replBufBlock：ゼロコピー伝播の要（参照カウントされた共有バッファ）  
  マスターは複数のブロック（replBufBlock）を連結したレプリケーションバッファを持つ。各ブロックは可変長バッファ buf[]、使用量用の used、全体容量 size、そして reader 数を示す refcount を持つ。各レプリカは自分のオフセットを指し示し、refcount を基にマスターがブロックの再利用／解放を判断する。これによりブロック内容をコピーせずに複数レプリカへ同時送信でき、メモリコピーコストを削減する（＝ゼロコピーに近い挙動）。

- レプリケーションバックログと再同期  
  マスターは一定量のコマンドを保持する「repl backlog」を持ち、レプリカが途中からつながっても遡って差分を取得できる。もし要求オフセットが backlog 範囲外なら完全再同期（RDB送付）にフォールバックする。

## 実践ポイント
- TTL を使う設計では KEEPTTL 等の動作を検証し、ネットワーク遅延での振る舞いをテストする（特にハッシュフィールドTTL）。  
- レプリケーションでは決定論的に再現されない操作（時刻・浮動小数点）はマスターで最終値に書き換える方針を採ると不整合を減らせる。  
- 高スループットを狙うなら、参照カウント＋共有バッファ（replBufBlock 的設計）でコピーを減らすアーキテクチャを検討する。  
- レプリケーションバックログのサイズと再同期コストを運用方針に合わせて調整する（短すぎると頻繁にフル同期が発生）。  
- テストケース：マスターでコマンドを順に送ったあと、レプリカ側で意図的に遅延を入れてTTLや書き換えロジックの整合性を検証する。

短く言えば、Valkey/Redis が取る「コマンド書き換え」と「参照カウント型共有バッファ」は、安全性と効率のトレードオフを巧みに解いている。日本の現場でもTTLやレプリケーション設計の理解はパフォーマンスと可用性を両立する鍵です。
