---
layout: post
title: "Understanding the Go Runtime: The Scheduler - Goランタイムを理解する：スケジューラ"
date: 2026-03-13T01:03:11.685Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://internals-for-interns.com/posts/go-runtime-scheduler/"
source_title: "The Scheduler | Internals for Interns"
source_id: 47309940
excerpt: "GMPモデルで数百万ゴルーチンを効率運用し性能改善とデバッグを実現するGoスケジューラの核心"
image: "https://internals-for-interns.com/images/go-runtime-header.webp"
---

# Understanding the Go Runtime: The Scheduler - Goランタイムを理解する：スケジューラ
Goの秘密兵器「GMPモデル」──数百万ゴルーチンを効率的に回す仕組み

## 要約
GoのスケジューラはG（goroutine）・M（OSスレッド）・P（プロセッシングコンテキスト）の三要素で、数百万の軽量ゴルーチンを少数のCPUコア上で効率よく動かす仕組みを実現している。

## この記事を読むべき理由
Goはサーバー開発やマイクロサービスで広く使われ、日本のインフラ／バックエンド開発でも高負荷・高並列処理に直面する場面が増えています。スケジューラの設計を理解すると、パフォーマンス対策やデバッグ（ゴルーチンリーク、長時間システムコールなど）のヒントが得られます。

## 詳細解説
- GMPモデルの全体像  
  - G（goroutine）: 軽量な並行単位。初期スタックは約2KBで、実行状態・保存レジスタ・実行中のMポインタ等を持つ。  
  - M（machine/OS thread）: 実際にCPUで動くスレッド。各Mは現在実行中のユーザG（curg）とランタイム用のg0を持つ。g0はスケジューリングやGC処理用でスタックが大きく固定。  
  - P（processor）: スケジューリング文脈（ローカルランキュー、runnext、mcache等）を持つ。MはPを借りて初めてGoコードを実行できる。Pの数はGOMAXPROCSで制御（デフォルトは論理コア数）。

- なぜPが重要か  
  - システムコールでMがブロックしても、Pを別のMに割り当て直せば他のゴルーチンは止まらない。これがGMPの設計上の大きな利点。

- スケジューラ状態（schedt）  
  - グローバルな実行キュー、gFree一覧、pidle/midle（アイドルPとM）やスピニング数などを管理。ローカルキューを優先することでロック競合を減らす。

- ゴルーチンのライフサイクル（要点）  
  - 生成: newproc() → ローカルgFreeやグローバルgFreeから再利用、なければ新規割当。初期は_Grunnableでrunnextに入ることが多い。  
  - 実行: pickして_Grunningに。M上でPを借りて走る。  
  - 自己駐車: チャネル受信・mutex待ち・sleep等ではゴルーチン自身がgopark()で待機状態に入り、Mは次のゴルーチンをschedule()で拾う。  
  - 再開: goready()で_Grunnableにしてrunnextやローカルキューへ。生産者-消費者でrunnextを使った高速なやり取りが可能。  
  - システムコール: entersyscall()で_Gsyscallに入りMがカーネルでブロック。長引けばsysmonがPを奪い、別のMにPを渡すことで実行継続性を保つ。

## 実践ポイント
- GOMAXPROCSは環境に応じて調整（コンテナやVMではホストの論理コア数とズレることに注意）。  
- 長時間ブロッキングするシステムコールは避ける／非同期化する（ネット接続やファイルI/O）。  
- 大量ゴルーチン生成は安価だが、再利用とリークに留意（worker poolやcontextでキャンセル）。  
- プロファイリング（runtime/pprof, goroutine dumps）でgoparkの状態やsyscallの停滞を確認。  
- 高負荷環境ではローカルキャッシュ（mcache）やランキューの性質を意識して、ホットパスでロックを避ける設計を心がける。

短くまとめると、GMPの理解はGoアプリの性能チューニングとトラブルシュートに直結します。まずはGOMAXPROCSの設定とゴルーチンのブロッキング箇所を確認することから始めましょう。
