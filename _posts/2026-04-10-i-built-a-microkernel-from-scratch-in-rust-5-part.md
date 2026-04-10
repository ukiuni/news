---
layout: post
title: "I built a microkernel from scratch in Rust (5-part series: boot, IPC, preemption, virtual memory) - Rustでゼロからマイクロカーネルを作った（5部構成：ブート、IPC、プリエンプション、仮想メモリ）"
date: 2026-04-10T04:50:29.233Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.desigeek.com/post/2026/02/building-microkernel-part0-why-build-an-os/"
source_title: "Building a microkernel in Rust (Part 0): Why build an OS from scratch? | Amit Bahree's (useless?) insight!"
source_id: 366845202
excerpt: "RustでARM64向けマイクロカーネルをQEMUでブート〜IPC〜仮想メモリまで学べる"
---

# I built a microkernel from scratch in Rust (5-part series: boot, IPC, preemption, virtual memory) - Rustでゼロからマイクロカーネルを作った（5部構成：ブート、IPC、プリエンプション、仮想メモリ）
あなたのマシンの「下」を自分で作る──Rustで学ぶゼロからのOS開発入門

## 要約
Amit Bahree氏のシリーズは、AArch64（ARM64）向けにRustで最小限のマイクロカーネルをゼロから構築し、ブートからIPC、スケジューリング、仮想メモリまで段階的に解説する教育プロジェクトです。QEMUのvirtマシンで誰でも手元のPC上で試せます。

## この記事を読むべき理由
日本でもARM環境（Raspberry Pi、Apple Silicon、クラウドのGraviton）が身近になった今、OSの基礎を理解することは組み込みからクラウドまで幅広く役立ちます。実機不要で始められ、低レイヤの動作原理を実践的に学べます。

## 詳細解説
- 対象と環境：AArch64向けにQEMUの「virt」マシンを使うため、固定のメモリマップ（PL011 UART、GIC割り込み、ARMタイマー）上で安定して動作確認できる。実機固有の煩雑さを取り除いて学習に集中できる。  
- 何を作るか：最小限のマイクロカーネル（rustOS）。メッセージパッシング型のIPC、まずは協調的スケジューラを実装し、その後タイマ割り込みでプリエンプションを導入。最後に4層ページテーブルとMMUで仮想メモリを扱う。  
- アーキテクチャ的分離：コードはプラットフォーム非依存のkernelクレートと、ハードウェア固有のhal・プラットフォームクレートに分離。kernelはLoggerトレイトなどを通じてハード依存実装にアクセスする設計。これはLinuxのarch/ とkernel/ の分離と同じ考え方。  
- なぜRustか：型システムで多くのバグを防げる一方、OSでは依然としてunsafe領域が必要。Cやアセンブリだけでは見落としやすいクラスのバグをコンパイル時に検出しやすい点が利点。  
- 学習方針：ただコードを貼るのではなく、レジスタ設定やTCR_EL1のビットフィールドなど「なぜその値か」を逐一説明する教育重視のシリーズ。実戦的だが学習目的であり、プロダクション用の安全性や完全性は保証しない。

## 実践ポイント
- リポジトリ（bahree/rust-microkernel）をクローンして、まずはQEMU上でビルド＆起動してみる。Dockerイメージも用意されているのでローカル環境構築を省略可能。  
- 最初の到達点：シリアル（PL011）に文字を出すブートまで追うことで、CPU起動→初期化→出力の流れを体感する。  
- 次に触るべき箇所：IPCルーター実装でメッセージの流れ、スケジューラ実装で文脈保存（コンテキストスイッチ）の仕組み、ページテーブルの生成とMMU有効化のコード。  
- 学び方：各パートを2〜4時間目安で追う。コードを読んで動かす→小さく改変して挙動の違いを観察する（例：タイマ周期を変える、メッセージサイズを変える）。  
- 注意点：学習プロジェクトのため安全性や完全性は限定的。unsafeコードやハードウェア直接アクセスの影響を理解して実験すること。

以上を順に追えば、「電源投入→コード実行」までの低レイヤ処理を自分で辿れるようになります。興味があればリポジトリとQEMUでまず一度動かしてみてください。
