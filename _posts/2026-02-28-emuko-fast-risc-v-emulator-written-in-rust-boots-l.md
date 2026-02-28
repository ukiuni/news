---
layout: post
title: "Emuko: Fast RISC-V emulator written in Rust, boots Linux - Emuko：Rustで書かれた高速RISC‑Vエミュレータ（Linux起動）"
date: 2026-02-28T00:10:35.222Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/wkoszek/emuko"
source_title: "GitHub - wkoszek/emuko: Fast RISC-V emulator written in Rust. Boots Linux."
source_id: 47187121
excerpt: "Rust製JIT RISC‑VエミュレータemukoでLinux即起動、スナップショットとHTTP"
image: "https://opengraph.githubassets.com/e1cdd4f3201b481ac49a545866d38c1ba113ca15835f3446946d12a765b7ee46/wkoszek/emuko"
---

# Emuko: Fast RISC-V emulator written in Rust, boots Linux - Emuko：Rustで書かれた高速RISC‑Vエミュレータ（Linux起動）
手軽にLinuxを起動できる軽量RISC‑V体験 — Rust製JITエミュレータ「emuko」を試してみよう

## 要約
Rustで実装された軽量なRV64エミュレータで、JITで高速に動作しLinux（BusyBox）を起動可能。スナップショット、HTTPデーモン、差分チェッカーなど開発向け機能が充実しています。

## この記事を読むべき理由
日本の組込み／IoT開発者や研究者がRISC‑V環境を手早くローカルで試せる選択肢。特にARM64（Apple Silicon）やx86_64上で高速に動かせるため、実機が手元にない場面での開発効率が向上します。

## 詳細解説
- ISA・機能
  - RV64IMAFDC（64ビット、整数/乗算/原子/浮動小数点/倍精度/圧縮命令）をサポート。M/S/Uの特権モードとSv39仮想メモリを備える。
- 実行方式
  - JIT（動的翻訳）をARM64/x86_64向けに提供。ホストに合わせたadaptive backendで性能を引き出す。インタプリタとJITの差分チェック機能でJITの正当性を検証できる。
- 開発向け機能
  - 完全なLinuxブート（BusyBoxユーザランド）、対話型シェル。
  - スナップショット／リストア（手動・自動）、デーモンモード（HTTP API）、WebSocketベースのUARTコンソール、UART 16550/CLINT/PLIC/SBI 1.0など周辺器機の実装。
  - 依存をほぼ一つ（zstd）の純Rust実装で、導入・監査が容易。
- 他ツールとの位置づけ
  - QEMUは豊富なボード/エコシステム、SpikeはISA準拠のシミュレータ、Renodeはマルチノードや複雑なデバイスモデルに強い。emukoは「軽量で高速」「スナップショット」「HTTP/WebSocketで操作可能」といった開発効率機能が特徴。

## 実践ポイント
- 試す手順（ローカル環境でまず動かす）
```bash
# ビルド
cargo build --release
# ダウンロード（Debian netboot kernel/initrd）
emuko dow
# デーモン起動＆コンソール接続
emuko start
# 基本コマンド例
# Ctrl+] でコンソールをデタッチ
emuko snap        # スナップショット
emuko restore <name>  # スナップ復元
# デーモンAPI: http://127.0.0.1:7788/v1/api/
# WebSocket UART: ws://127.0.0.1:7788/v1/ws/uart
```
- 日本での活用例
  - 量産前のファームウェア検証、大学の授業やハッカソンでのRISC‑V入門、Apple Silicon上での高速検証環境として有用。
- 注意点
  - 現状はまだ小規模プロジェクト（スター数等）で発展中。大規模ボードサポートや成熟したツール連携が必要ならQEMU等も併用を検討。

以上がemukoの要点。まずはローカルでビルドしてLinuxを起動し、スナップショットやHTTP APIを触ってみることをおすすめします。
