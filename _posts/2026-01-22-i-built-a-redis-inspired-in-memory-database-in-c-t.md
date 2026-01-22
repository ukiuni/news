---
layout: post
title: "I built a Redis-inspired in-memory database in C to understand WAL, crash recovery, and TTL — looking for feedback on design - Redis風のインメモリDBをCで自作してWAL・クラッシュ回復・TTLを学んだ話"
date: 2026-01-22T11:46:56.157Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/pie-314/RadishDB"
source_title: "GitHub - pie-314/RadishDB: Redis-inspired in-memory key–value database in C with WAL, crash recovery, TTL, AOF rewrite, REPL, and TCP server. Built to understand real database internals."
source_id: 420492144
excerpt: "C製の学習用Redis風DBでWAL・クラッシュ回復・TTL実装の設計解説"
image: "https://opengraph.githubassets.com/b2d13d05567414e7b22e8f4fd9f3cbc9de5e026fa00b5d151c953dc830517ccb/pie-314/RadishDB"
---

# I built a Redis-inspired in-memory database in C to understand WAL, crash recovery, and TTL — looking for feedback on design - Redis風のインメモリDBをCで自作してWAL・クラッシュ回復・TTLを学んだ話
RadishDBで学ぶ「データベースの中身」が見える体験 — 小さくて本格派なストレージエンジン入門

## 要約
Cで書かれた学習向けのインメモリK-Vデータベース「RadishDB」は、WAL（AOF）、クラッシュリカバリ、TTL、有効期限の掃除、AOFリライト、スナップショット（.rdbx）など、実務で重要なストレージ基盤を実装して学ぶことを目的とするプロジェクトです。

## この記事を読むべき理由
データベース内部（耐障害性・永続化・期限管理）の仕組みはプロダクト運用やコスト最適化に直結する知識で、日本のエンジニアや学生が「手で触れて理解」するのに最適な教材だからです。

## 詳細解説
- 目的と設計思想  
  - RadishDBは学習目的だがRedis／RocksDB／Postgresで使われる現実的な解法を採用。エンジン（command semantics）とプロトコルを分離し、REPL・TCPサーバ・将来のプロトコルへ共通の実行基盤を提供する設計。

- ストレージとデータ構造  
  - ハッシュテーブル（Separate chaining、自動リサイズ、load factor > 0.75）でキー／バリューを保持。キーと値はヒープ管理。

- 永続化（2層）  
  1. スナップショット（.rdbx）: バイナリで全状態を保存。フォーマットはヘッダ＋キー数＋各キー・値・期限時刻。高速ロード向け。  
  2. Append-Only File (AOF / WAL): ヘッダ（AOFX1 + base_size）と長さプレフィックス付きコマンド列。各書き込みで fsync() を行い、起動時は決定論的にリプレイ。部分書き込みは安全に無視される仕組み。

- AOFリライト（ログ圧縮）  
  - 現在のメモリ状態をシリアライズして新しいAOFを書き、古い履歴を破棄。ヘッダのベースサイズ更新によりディスク増大を制限し、ファイル肥大化を防ぐ。

- TTL / 有効期限  
  - 各キーにexpires_atを記録。読み取り時の受動的削除と、インクリメンタルなスイーパーによる能動的削除を組み合わせ、RedisライクなTTL動作を実現。

- モジュール構成（主要ファイル）  
  - engine.c / aof.c / expires.c / hashtable.c / persistence.c / repl.c / server.c など。学習用途に適した分離と可読性。

- サポートコマンド例  
  - SET/GET/DEL/TTL/COUNT/SAVE/LOAD/BENCH/INFO/HELP/EXIT。REPLとTCPサーバ（ポート8080、単一クライアント）で動作確認可能。

## 実践ポイント
- 試す手順：リポジトリをclone→make→./radishdb（REPL）または ./radishdb --server（TCP）。AOFを残して強制終了→再起動してクラッシュ回復を確認する。  
- 学習用途の着眼点：fsync頻度と起動時間、AOFリライトのタイミング、TTLスイーパーの負荷と精度、部分書き込み対策の実装を比較検証する。  
- 日本の現場での応用例：小規模キャッシュや学内講義、SREの運用演習、組み込み／エッジ環境向け軽量永続化の設計検討に有用。  
- 貢献・フィードバック：ARCHITECTURE.md／LEARNINGS.mdを読み、設計意図やトレードオフに対する提案をGitHubで投げると作者の学習プロセスに貢献できる。

短時間で「内部が見える」実装例に触れたい技術者や学生にとって、RadishDBは実践的かつ学びが大きいリポジトリです。
