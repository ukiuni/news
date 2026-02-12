---
layout: post
title: "How to run your userland code inside the kernel: Writing a faster `top` - ユーザーランドのコードをカーネル内で動かす方法：より高速な `top` の作り方"
date: 2026-02-12T13:22:37.760Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://over-yonder.tech/#articles/rstat"
source_title: "over|yonder"
source_id: 443517640
excerpt: "eBPFでユーザーコードをカーネル内集約し、topを大幅高速化する方法"
---

# How to run your userland code inside the kernel: Writing a faster `top` - ユーザーランドのコードをカーネル内で動かす方法：より高速な `top` の作り方
topを超速で動かす――ユーザーコードを「安全に」カーネル側で走らせる発想で観測を劇的に軽くする方法

## 要約
ユーザーランドで頻繁に発生するシステムコールや /proc パースをカーネル側で集約・前処理することで、ツール（例：top）のレスポンスとスケーラビリティを大幅に改善できる、というアイデアと実践手法を紹介する記事です。

## この記事を読むべき理由
従来の監視ツールは大量のコンテキストスイッチやファイル読み出しで負荷が高く、クラウド環境や大規模マシンでボトルネックになりやすい。日本のSRE／開発者が少ないオーバーヘッドでリアルタイムに状態を把握するための実践的知識が得られます。

## 詳細解説
- なぜ遅いか：top などは各更新で多数の syscalls と /proc ファイルアクセスを行い、ユーザー↔カーネル往復が多い。多プロセス・多CPU環境ではこれが顕著に効く。
- 解決アプローチ：カーネル内で必要なデータを集約・差分計算し、ユーザー側へは既に集計された小さなデータを渡す。これにより syscall 回数とコンテキストスイッチを削減する。
- 実現手段（安全にカーネルでコード実行する代表例）：
  - eBPF：ユーザーが定義した小さなプログラムをカーネルにロードし、tracepoint／kprobe／sched hooks 等にアタッチしてイベントを処理。BPF マップで集計し、ring buffer や perf イベントでユーザーに送る。検証器(verifier)により安全性が担保されるためプロダクションで使いやすい。
  - prototyping：bpftrace で短いスクリプトを作って挙動確認。安定化したら libbpf/CO-RE に移行してビルド・配布。
- top向けの具体的処理例：
  - CPU 使用率差分：sched_switch や task stats から per-CPU 累積値を集約して delta を計算。
  - I/O / メモリ統計：tracepoints や task_io_accounting を使いプロセスごとに集計。
  - 出力効率化：ユーザー側は定期的に ring buffer を読み取るだけで UI を更新。
- 注意点：
  - カーネルバージョン依存、BPF verifier の制約（スタック／ループ／メモリ割当）、権限（CAP_SYS_ADMIN 等）がある。
  - 計測コード自体がカーネル負荷を生まないよう設計（軽い処理・per-CPU 集計・バッチング）。

## 実践ポイント
- まず bpftrace で狙いの指標をプロトタイプ化して効果を確認する。
- libbpf / CO-RE を使ってカーネル互換性を担保した実装に移行する（ビルド時に BTF を活用）。
- データ搬送は ring buffer/perf buffer を使い、ユーザー側は最小限の syscalls で描画する設計にする。
- 実運用前にカーネル負荷と verifier ログを確認し、必要なら集計頻度やサンプリングに落とす。
- 日本国内のクラウド／オンプレ環境での互換性とセキュリティポリシーを確認する（カーネルモジュールや CAP 権限の扱い）。

元記事は over|yonder の Kieran Hannigan による実装・考察がベースです。興味があればまず bpftrace の簡単なスクリプトから試してみてください。
