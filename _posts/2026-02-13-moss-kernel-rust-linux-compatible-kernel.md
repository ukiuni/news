---
layout: post
title: "moss-kernel: Rust Linux-compatible kernel - Rustで書かれたLinux互換カーネル"
date: 2026-02-13T15:41:56.915Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/hexagonal-sun/moss-kernel"
source_title: "GitHub - hexagonal-sun/moss-kernel: Rust Linux-compatible kernel"
source_id: 1735165626
excerpt: "Rust製AArch64対応のLinux互換カーネル、非同期設計で実用的な互換性を実現"
image: "https://opengraph.githubassets.com/a183e2b33652564611b0657599a4b1642da1589941241f2f33823b1230e9d7fe/hexagonal-sun/moss-kernel"
---

# moss-kernel: Rust Linux-compatible kernel - Rustで書かれたLinux互換カーネル
Rustで作る未来のOSコア――非同期設計とLinuxバイナリ互換を両立する注目プロジェクト

## 要約
mossはRustとAarch64アセンブリで書かれた、Linuxユーザ空間バイナリと互換性のある実験的カーネルで、Rustのasync/awaitを核にした非同期カーネル設計を実装しています。

## この記事を読むべき理由
非同期プログラミングをカーネル設計に持ち込む試みは、デッドロック低減やモダンな安全性をOSレベルで実現する可能性があり、ARM（AArch64）中心の日本の組込み／クラウド環境に直接関係します。Rustに興味あるエンジニア、OS実装を学びたい学生・研究者、組込み開発者にとって必読です。

## 詳細解説
- コア設計  
  - 完全なAArch64サポートと、将来のx86_64/RISC-V移植を見据えたHAL（ハードウェア抽象層）。  
  - MMU有効化、ページテーブル管理、Copy-on-Write、ユーザ空間との安全なコピー、ページフォルト処理、カーネルのスタックオーバーフロー検出など、実用レベルのメモリ管理を実装。  
- 非同期（async）コア  
  - 全ての非自明なシステムコールをasync関数で実装し、.awaitでスリープ可能。スピンロックをスリープポイント越しに保持できないことをコンパイラで強制し、典型的なデッドロッククラスを排除。未来の待ち処理を割り込みで中断するinterruptable()も提供。  
- プロセス/スケジューリング  
  - 単一CPU/マルチCPU対応（EEVDFスケジューラ）、IPIによるタスク移動、fork/execve/cloneなどを含む約105のLinux互換システムコールを実装。Arch Linux aarch64の動的リンクユーザ空間（bash、BusyBox、coreutils、strace 等）が動作。ptraceでstraceが動く点は互換性の高さを示す。  
- VFSとドライバ  
  - 非同期抽象の仮想ファイルシステム、ramdisk、FAT32（読み取り）、ext2/3/4（読み取り + 部分書き込み）、tmpfs、procfsなどを提供。  
- 開発体制とテスト基盤  
  - libkernelによりアーキテクチャ分離し、ホスト（x86）上でロジックをテスト可能。強い型付け（VA/PA/UA）、per-CPUキャッシュを備えたスラブアロケータ、230+のテスト群、usertestでユーザ空間のsyscall挙動検証が可能。  
- ビルドと実行環境  
  - QEMUでのAArch64エミュレーション、aarch64-none-elfツールチェーンなどが必要。標準的なビルドスクリプトとイメージ作成スクリプトを備える。  
- ロードマップと制約  
  - 進行中の課題はTCP/IPスタック、完全な読み書き可能ファイルシステム、systemd対応拡充。現時点での非目標はaarch64以外のバイナリ互換性や商用向けのハードニング。実験的プロジェクトとして公開（MITライセンス）。

## 実践ポイント
- まずはローカルで試す（Debian系の例）:
```bash
# 必要パッケージ
apt install qemu-system-aarch64 dosfstools mtools

# ビルド／実行（リポジトリルートで）
./scripts/build-deps.sh
./scripts/create-image.sh
cargo run --release
```
- ホスト上でロジックテスト:
```bash
cargo test -p libkernel --target x86_64-unknown-linux-gnu
```
- 日本の活用観点: ARMベースの組込み機器やクラウド（AArch64インスタンス）での安全なカーネル実験、OS教育用教材、Rustでのデバイスドライバ開発・ポーティングの実践場として有用。  
- 貢献の入り口: ドライバ追加、x86/RISC‑Vポート、システムコール拡張、ネットワーク実装など。Issue/PRでコントリビュート可能。

mossは「Rustの安全性」と「Linux互換性」を組み合わせた実験的な挑戦で、OS設計や組込み／クラウドでのARM活用を考える開発者にとって学びと実践の余地が大きいプロジェクトです。
