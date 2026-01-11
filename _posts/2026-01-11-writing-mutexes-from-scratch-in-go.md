---
layout: post
title: "Writing mutexes from scratch in Go - Goでミューテックスを一から書いて学ぶ"
date: 2026-01-11T02:30:22.764Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://rybicki.io/blog/2026/01/01/mutexes-from-scratch-in-go.html"
source_title: "Writing mutexes from scratch in Go | functional fascinations"
source_id: 860436508
excerpt: "Goで自作ミューテックスを実装し性能差やfutex最適化まで実測で学べる入門記事"
---

# Writing mutexes from scratch in Go - Goでミューテックスを一から書いて学ぶ
Goで自作ロックを作ると、ロックの意外なコストや現場での判断基準が身につく — 実装とベンチで学ぶ同期プリミティブの本質

## 要約
Goでスピンロック→原子命令→テスト＆テスト・アンド・セット→futex（Linux）まで段階的に実装・測定し、単純なロックとOS協力型ロックの性能トレードオフを示す記事です。

## この記事を読むべき理由
ミューテックスは「使うのは簡単」でも「作るのは奥が深い」典型例です。日本のサーバー開発やクラウド運用でも、Goは普及しており、ロック設計や性能対策を理解するとデバッグやチューニングの幅が広がります。

## 詳細解説
- なぜ単純な実装がダメか  
  単純なブールフラグでのスピンロック（busy-wait）はデータレースを生みます。複数のゴルーチンが読み→書きの間に指示が競合すると、不整合が発生します。

- ハードウェア原子命令での解決  
  atomic.SwapUint32 のような原子操作は「読み書きを一塊で扱う」ため、安全にロック獲得を実現します。Unlockにもatomicを使う理由は、コンパイラ／CPUが命令を並べ替えるためにメモリ順序保証が必要だからです。

- 応答性改善：busy-waitをやめる工夫  
  ただし純粋なスピンはCPUを浪費します。runtime.Gosched() をループ内で呼ぶとゴルーチンを譲ることでユーザ空間の無駄な忙待ちを減らせます。さらに test-and-test-and-set（先にLoadで見てからSwapを試す）で原子命令の頻度を下げられます。

- ベンチの落とし穴  
  単純なベンチでスピンロックが実行時間（wall time）上速く見えても、/usr/bin/time などで見るとユーザCPU時間やシステムCPU時間が大きく膨らみ、実は非効率（スケジューラや忙待ちのコスト）なことがあります。複数コア環境では「real time」と「CPU time」を両方見ることが重要です。

- futexによるOS協力型ロック（Linux限定）  
  futexはユーザ空間で軽く試行し、待ちが長いときだけカーネルでスリープさせる仕組み（FUTEX_WAIT / FUTEX_WAKE）。Goでは golang.org/x/sys/unix 経由で syscall を使い、build tag（//go:build linux）でプラットフォーム分岐します。常に futexWake を呼ぶと無駄なので「待ちがいるか」を追跡する仕組みも必要です。

## 実践ポイント
- 本番ではまず sync.Mutex を使う（最適化はコストと複雑性を伴う）  
- 学習目的や特殊用途で実装するなら：atomic の正しい使い方、メモリ順序、race detector を活用すること  
- ベンチは wall time に加え user/sys（/usr/bin/time）や pprof でCPU使用状況を確認すること  
- Linux専用の最適化（futex）を入れる場合は build tags を使い、Dockerなどで実機相当の環境で計測すること  
- 高コンテキストスイッチや高CPU消費が見えるなら忙待ちをやめ、Gosched や futex／条件変数へ移行する

短くまとめると、ロックは「簡単そうに見えて環境依存・ハードウェア依存の最適化課題」が多い部品です。Goで自作してみると、sync.Mutexを選ぶ理由や、いつOSと協調したほうが良いかが腑に落ちます。
