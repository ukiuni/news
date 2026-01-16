---
layout: post
title: "Read_once(), Write_once(), but Not for Rust - READ_ONCE()/WRITE_ONCE()、しかし Rust では採用されない"
date: 2026-01-16T16:46:54.927Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lwn.net/SubscriberLink/1053142/8ec93e58d5d3cc06/"
source_title: "READ_ONCE(), WRITE_ONCE(), but not for Rust [LWN.net]"
source_id: 46647059
excerpt: "RustはREAD_ONCE/WRITE_ONCEを採用せず、Atomicで同期の意図と安全性を明確化する道を選んだ"
---

# Read_once(), Write_once(), but Not for Rust - READ_ONCE()/WRITE_ONCE()、しかし Rust では採用されない
Rustが「おなじみマクロ」をスルーした理由 — 安全性と意図の明確化を選んだ設計論争

## 要約
Linuxカーネルで長年使われてきたREAD_ONCE()/WRITE_ONCE()をRust側に移植する提案が出たが、Rustコミュニティは「ボンドエイド的なマクロ」よりもAtomic型で意図を明示する方針を支持して提案は見送られた。

## この記事を読むべき理由
カーネルやドライバ開発で並行アクセスの扱いは致命的なバグの温床。Rustでカーネルを書く日本のエンジニアやOS系エンジニアは、CとRustで「同じデータを扱うが異なるAPI」が出現する現実を知り、適切な同期設計と移植判断ができる必要がある。

## 詳細解説
- READ_ONCE()/WRITE_ONCE()の役割  
  - コンパイラ最適化による読み書きの省略や重複を防ぎ、単一の読み/書きを強制する。コンパイラレベルでの原子性（readが途中のビット混在を返さない）を保証する一方、強い順序付けはしない（smp_load_acquire等とは異なる）。
- 提案されたRust実装案  
  - 提案者はRustマクロでREAD_ONCE()/WRITE_ONCE()を呼び出し、最終的にstdのread_volatile()/write_volatile()を使う実装を提示した。これにより既存のvolatileベースの箇所を置き換えられる可能性があった。
- 反対意見と理由  
  - Rust側の反対は主に「意図の不明瞭さ」：READ_ONCE()/WRITE_ONCE()は用途が混在（単純にデータ競合を避けたいのか、原子的な更新が必要なのか）が多く、APIとして曖昧になる。代わりにAtomic型（Atomic::from_ptr().load(Relaxed) など）で必要な保証（atomicity・順序など）を明示する方が良い、という設計原則に基づく。
  - Rustのドキュメントはvolatileアクセスを並行同期に用いるのは安全でないと明記しており（non-atomic扱い）、read/write_volatileだけで同期を担保するのは問題があるとされる。
- 波及する実務的インパクト  
  - RustとCで並行制御APIが異なると、同じデータ構造を両言語から扱う場面で設計や検査が複雑化する。逆に、この議論がきっかけでC側の古いコード（暗黙的に「普通の書き込み＝原子」と仮定している箇所）をWRITE_ONCE()/atomicに直すきっかけにもなっている。
- アーキテクチャ依存の注意点  
  - あるアーキテクチャでは本来のハードウエア原子性がないため、カーネルはソフトウェアで64ビット原子をロックで実装している場合があり、単なるREAD_ONCE()での代用は不適切となるケースがある。

## 実践ポイント
- Rustでカーネル/ドライバを書くときは、volatileベースの置換に安易に走らず、Atomic APIで「必要な保証」を明示する設計を優先する。  
- Cコードを保守する立場なら、暗黙の「単純書き込みが安全」仮定を洗い出し、必要ならWRITE_ONCE()/atomicに置換する。KCSANや静的解析を活用して候補を検出する。  
- ターゲットアーキテクチャの原子サポートとコンパイラ（LLVM/ツールチェイン）の実装差に注意し、実機での生成コードと性能を確認する。  
- 互換性を保つため、跨言語で扱う共有データについては「どの言語でどの保証を提供するか」を明文化してコードレビュー基準に盛り込む。

この議論は単なるマクロの採否に留まらず、「設計の透明性」と「言語ごとの並行プログラミングモデルの違い」を浮き彫りにした点で、今後のカーネル開発に重要な示唆を与えています。
