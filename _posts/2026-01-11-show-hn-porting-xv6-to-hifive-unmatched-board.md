---
layout: post
title: "Show HN: Porting xv6 to HiFive Unmatched board - xv6 を SiFive HiFive Unmatched ボードへ移植"
date: 2026-01-11T15:26:49.603Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/eyengin/xv6-riscv-unmatched"
source_title: "GitHub - eyengin/xv6-riscv-unmatched: A port of xv6-riscv to the SiFive HiFive Unmatched board."
source_id: 46565833
excerpt: "xv6をHiFive Unmatchedで実機起動、SPLとSPIで動作確認済み"
image: "https://opengraph.githubassets.com/68d0502808ecc853fee90b28ab5b930d3cc5c48d3d4ce1c2ce02ec1239373a08/eyengin/xv6-riscv-unmatched"
---

# Show HN: Porting xv6 to HiFive Unmatched board - xv6 を SiFive HiFive Unmatched ボードへ移植
魅力タイトル: 実機で動く教育用OSを自分の手で — xv6 が HiFive Unmatched（FU740）で動くようになった理由と導入ガイド

## 要約
xv6-riscv を SiFive HiFive Unmatched ボード向けに移植し、U-Boot SPL を使ってカーネルを直接 M モードで起動、SPI モードの SD カードドライバを実装して実機での usertests を通過させたプロジェクトです。実機検証済みで、QEMU でも動作させられます。

## この記事を読むべき理由
日本でも RISC-V の採用が増え、組込み・教育分野で実機検証が重要になっています。xv6 は OS 教材として有名で、実機で動かすことでハードウェア依存の挙動やブートパスの理解が深まります。本記事は、その移植の肝と実際に手を動かすためのポイントを分かりやすく整理します。

## 詳細解説
- 目的と背景  
  xv6 は教育用の Unix ライクな小さな OS。移植先の HiFive Unmatched（FU740）はマルチハートの RISC-V ボードで、実機での挙動確認ができる点が魅力。通常の xv6-riscv は OpenSBI + カーネルという流れが多いが、本プロジェクトは U‑Boot の SPL（Secondary Program Loader）を利用して xv6 カーネルを直接ロードし、OpenSBI を置き換えるアプローチを採用しています。これによりハード初期化を SPL に任せ、カーネル側の変更を最小限に抑えています。

- ブートフローの特徴  
  1. U‑Boot SPL (v2023.01 を推奨) がボードの初期化を行う。  
  2. xv6 カーネルは ELF から生のバイナリに変換され、FIT イメージ（xv6-unmatched.itb）にパッケージされる。  
  3. SPL がその FIT イメージを認識してカーネルを起動。  
  この構成は OpenSBI の代替として SPL を使うことで、カーネル変更を抑えつつ実機起動を実現します。

- ハード固有の対応  
  - SD カード: VirtIO を使えない実機のため、SiFive ソース由来の SPI モード SD ドライバを移植。  
  - U‑Boot: 新しい U‑Boot だと SPL で CPU クロック初期化が失敗する問題が報告され、v2023.01 を指定してビルドするのが安定するという注意点があります。  
  - UART と MSEL: コンソールは UART（115200）で確認。ブートモードスイッチ（MSEL）を SD Boot に設定する必要あり（例: 1011）。

- 開発環境とビルドの流れ（概略）  
  主に Ubuntu 24.04 を想定。要求パッケージを入れ、リポジトリを取得して make ターゲットでビルド。U‑Boot は SPL のみ（u-boot-spl.bin）を作成して SD に書き込みます。QEMU の sifive_u ターゲットでも動作検証可能で、実機と QEMU 間ではビルドアーティファクトを切り替える必要があります。

## 実践ポイント
- 必要パッケージ（例）
```bash
# bash
sudo apt update
sudo apt install git build-essential gdb-multiarch qemu-system-misc \
gcc-riscv64-linux-gnu binutils-riscv64-linux-gnu flex bison libssl-dev \
python3-setuptools python3-dev swig device-tree-compiler u-boot-tools
```

- xv6 ソース取得とビルド
```bash
# bash
git clone https://github.com/eyengin/xv6-riscv-unmatched
cd xv6-riscv-unmatched
make unmatched   # xv6-unmatched.itb が生成される
```

- U‑Boot SPL のビルド（v2023.01 推奨）
```bash
# bash
git clone https://github.com/u-boot/u-boot.git
cd u-boot
git checkout v2023.01
make sifive_unmatched_defconfig
make CROSS_COMPILE=riscv64-linux-gnu- spl/u-boot-spl.bin
```

- SD カード準備（デバイス名を必ず確認）
  sgdisk でパーティションを作り、生成した SPL・FIT・fs.img をそれぞれのパーティションへ dd で書き込みする。書き込み先を間違えるとデータ消失するので注意。

- 実機起動手順（チェックリスト）
  - MSEL スイッチを SD Boot（1011）にセット  
  - microSD を挿入、UART 接続（115200）でログを監視  
  - 電源投入で U‑Boot SPL ログ → xv6 カーネル起動を確認  
  - QEMU で先に動作確認する場合は: make clean; make qemu

- 注意点とトラブルシュート
  - U‑Boot のバージョンによる初期化の違いに注意（v2023.01 を推奨）  
  - SD カードは SDHC（UHS）での相性や容量が影響する場合あり（テスト報告例: SanDisk Ultra 32GB）  
  - 実機での usertests 実行でハード依存の不具合を洗い出せるので、まずは小さなテストケースから動作確認を進めること

以上を踏まえれば、教育用途や実機での OS 挙動確認を目的とした xv6 の移植・検証を自分の環境で再現できます。興味がある方はまず QEMU で流れを掴み、その後 HiFive Unmatched で実機検証に挑戦してください。
