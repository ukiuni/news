---
layout: post
title: "What's new in Linux kernel for PostgreSQL - PostgreSQL向けに進化するLinuxカーネルの最新動向"
date: 2026-03-03T12:01:41.405Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://erthalion.info/2026/02/03/new-linux-for-postgresql/"
source_title: "What's new in Linux kernel... for PostgreSQL &middot;      Erthalion's blog"
source_id: 47230847
excerpt: "非キャッシュ/原子IOやBPFでPostgres性能と信頼性向上の可能性、導入注意点"
---

# What's new in Linux kernel for PostgreSQL - PostgreSQL向けに進化するLinuxカーネルの最新動向
PostgreSQL運用が劇的に変わるかもしれない、カーネル側の実装アップデートを初心者にも分かりやすく解説する短めガイド

## 要約
Linuxカーネルに入ってきた近年の変更（uncached buffered IO、atomic/“untorn” writes、cachestat syscall、BPFによるカスタマイズ）は、PostgreSQLの性能・信頼性改善に直接つながる可能性がある。だが採用には互換性・実装上の注意点がある。

## この記事を読むべき理由
日本でも大規模DBやクラウド運用が増え、ストレージ特性やカーネル機能を理解すると「実運用での性能向上」「障害回避」「チューニングの精度向上」が期待できるため。

## 詳細解説
- Uncached buffered IO（RWF_DONTCACHE）  
  - pwritev2(..., RWF_DONTCACHE) フラグで「ページキャッシュを参照するが、IO後にキャッシュに残さない」動作を指示。  
  - 利点：メモリ不足でのreclaimによるパフォーマンス変動を減らせるケースあり。実測ではキャッシュが満杯の状況でキャッシュありより安定して高IOPSを出すことが示唆される。  
  - 注意：通常の buffered IO と振る舞いが異なるためアプリ側で期待する一貫性／キャッシュ効果が変わる可能性がある。

- Untorn / Atomic writes（RWF_ATOMIC）  
  - NVMe/SCSIのハードウェア的な「原子的書き込み」を利用するためのフラグ pwritev2(..., RWF_ATOMIC)。デバイスがサポートするブロック境界・最大単位を満たす必要あり。  
  - DB的意義：部分書き（torn page）問題を軽減でき、PostgreSQLのFull Page Image（FPI）などの重い保護策を緩和できる可能性がある。  
  - 現状：原子書き込みは基本的にDirect IO前提で、バッファードIOでのサポートは未確定。導入にはデバイスの能力確認とアプリ側のIOパターン調整が必要。

- Page cache state（cachestat syscall）  
  - cachestat(fd, range, …) によりページキャッシュの状態（キャッシュ済ページ数、dirty、writeback、evictedなど）を効率的に取得可能に。  
  - PostgreSQLではバッファ割当（effective_cache_size）に基づく経験則を使っているが、実行時に実際のカーネルページキャッシュ情報が取得できれば、より正確なI/O予測やプラン選択に活用可能。  
  - ただし「キャッシュが満杯ならプレフェッチを止める」など単純な方針が常に有利とは限らないため検証が必要。

- BPFでのカスタマイズ（sched_ext / cache_ext / io_uring / OOM）  
  - BPFのstruct opsを使い、スケジューラ（sched_ext）、ページキャッシュのエビクションポリシー（cache_ext）、io_uringの振る舞い、さらにはOOMキラーの決定ロジックまでカスタム実装が可能に。  
  - DB向け活用例：クエリ優先度に応じたCPU割当、OLTP優先のキャッシュ保持ポリシー、io_uringのポーリング改善やメモリ枯渇時のDB優先保護など。  
  - リスク：カーネル内の振る舞いを変えるため、安全性・検証・メンテナンス負荷が高まる。商用環境では慎重な採用計画が必須。

- PostgreSQLとの結び付き（実装上の現実）  
  - PostgreSQLは移植性を重視するため、Linux限定の新機能を採用するには議論と互換性対策が必要。  
  - 既存の保護策（FPIやWAL）との関係を慎重に評価する必要がある。

- 参考となる数式（バッファ効果の近似）  
  - Mackert & Lohman の近似式（記事で引用されるIndex fetch予測式の一部）を実行時のキャッシュ情報で置き換えれば、より現実的なI/O推定が可能：  
  $$
  PF = \begin{cases}
  \min\left(\dfrac{2TNs}{2T+Ns},\; T\right) & (T \le b)\\[6pt]
  \dfrac{2TNs}{2T+Ns} & (T > b,\; Ns \le \dfrac{2Tb}{2T-b})\\[6pt]
  b + (Ns - \dfrac{2Tb}{2T-b})\cdot \dfrac{T-b}{T} & (T > b,\; Ns > \dfrac{2Tb}{2T-b})
  \end{cases}
  $$  
  - ここで $T$=テーブルのページ数、$N$=タプル数、$s$=選択率、$b$=利用可能バッファページ数（カーネルのページキャッシュ含む）。

## 実践ポイント
- まずは検証環境で試す：QEMUのNVMeエミュレーションでRWF_ATOMICやRWF_DONTCACHEの挙動を確認する。  
- デバイス能力を確認：NVMeのatomic単位や最大サイズを調べ、アプリのIOパターンが適合するか確認。  
- cachestatを使って実データを取得し、effective_cache_sizeやPlannerのパラメータと照らして性能差を計測する。  
- BPFカスタムは限定的に試験導入し、安全性・フォールバック経路を確保してから本番へ。  
- コミュニティ貢献：PostgreSQL側の採用検討やパッチ議論に参加して、Linuxの新機能を実運用に橋渡しする。

（元記事：What's new in Linux kernel... for PostgreSQL — Erthalion, 03 Feb 2026）
