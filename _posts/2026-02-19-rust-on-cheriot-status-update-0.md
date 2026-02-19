---
layout: post
title: "Rust on CHERIoT: Status update #0 - CHERIoT上のRust：状況報告#0"
date: 2026-02-19T05:52:17.659Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://rust.cheriot.org/2026/02/15/status-update.html"
source_title: "Status update #0 | CHERIoT Rust"
source_id: 1295582248
excerpt: "CHERIoTでRustが動作開始、実用化に向けた技術課題とすぐ試せる手順"
---

# Rust on CHERIoT: Status update #0 - CHERIoT上のRust：状況報告#0
魅せるIoT安全性へ一歩前進──CHERIoTでRustが動き始めた理由と実務で押さえるべきポイント

## 要約
CHERIoT向けにRustを動作させるプロジェクトの半年分の進捗報告。新ターゲット追加、LLVM対応、ポインタとキャパビリティの扱いの分離など、実行可能コードを出すまでの技術的変更とテスト基盤の整備が進んでいます。

## この記事を読むべき理由
日本でもIoTや組込みシステムの安全性は重要課題です。ハードウェアでメモリ安全を支援するCHERI系アーキテクチャにRustが対応する意義は大きく、産業用途（家電、車載、産業機器）での採用可能性やツールチェーンの将来に直接影響します。

## 詳細解説
- 新ターゲット導入：riscv32cheriot-unknown-cheriotrtos というターゲットをrustcに追加。コンパイラ側は最小限の変更で新しいバックエンド（CHERIoT向けLLVM）と連携可能に。
- LLVMのCHERIoTポート：memcpy/memmoveなどコピー命令で「コピーする対象がキャパビリティかどうか」「メタデータを残すか」を扱うため、LLVM側のC APIシグネチャが変わっている点を吸収。
- アドレス空間の扱い：LLVM IR上でデフォルトのアドレス空間をaddrspace(0)以外（CHERIoTはaddrspace(200)）にできるように。これにより「アドレス（address）」と「ポインタのメモリ表現（pointer）」を区別できるようになった。
- ポインタ幅 vs アドレス幅：CHERIoTはアドレスが32ビット、キャパビリティ（ポインタ表現）が64ビットという差がある。コンパイラ内部でpointer_size()ではなくpointer_offset()/index幅を使うなど、サイズの概念を分離する変更を導入。
- コアライブラリとCHERI固有機能：core/allocをCHERIoTターゲットでビルドできるようにし、CHERI特有の組み込み（intrinsics）やdiscriminant生成の調整を実施。
- 実機相当の検証：codegen-llvmテストに加え、SailベースのCHERIoTシミュレータ上での実行テストと専用ランナーでのデバッグ整備。例えば、尾関数ジャンプで使用するレジスタが上書きされるLLVM側バグを発見して修正した事例などがある。
- 追加対応：objectクレートのe_flags補正、AtomicPtrサポート（ポインタ表現が64ビットでもATOMIC幅を確保）などツールチェーン周りの互換性修正。

## 実践ポイント
- 試してみる（ワンライナー）：公式リポジトリをクローンしてビルドしてみる手順が公開されています。まずはシミュレータ環境で動かすのがおすすめ。
- 注目すべき技術点：ポインタ幅とアドレス幅の分離、addrspace指定、CHERI固有intrinsicsの扱い。組込み向けRustで低レイヤを触るなら理解必須。
- CIとテスト：codegen-llvmだけでなく実行テスト（シミュレータ）を回す習慣は、アーキテクチャ固有の不整合を早期に見つけるため有効。
- 日本での関連性：RISC-Vや組込みIoT製品を扱う企業は、ハードウェア支援のメモリ安全性×Rustの組合せを研究すると競争優位になり得ます。
- 参加・相談：開発は公開リポジトリで進行中。ビルドや実行で詰まったらIssueやプロジェクトの公開チャットで報告・相談しましょう。
