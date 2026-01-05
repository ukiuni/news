---
  layout: post
  title: "VS Code Extension for RV - RV（RISC-V）向け VS Code 拡張"
  date: 2026-01-05T11:28:19.113Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://marketplace.visualstudio.com/items?itemName=ranaumarnadeem.riscv-toolchain"
  source_title: "RISC-V Toolchain - Visual Studio Marketplace"
  source_id: 470694631
  excerpt: "WindowsでもDockerで即ビルド、VS CodeからRISC‑V開発を完結。"
  image: "https://ranaumarnadeem.gallerycdn.vsassets.io/extensions/ranaumarnadeem/riscv-toolchain/1.0.1/1767529016853/Microsoft.VisualStudio.Services.Icons.Default"
---

# VS Code Extension for RV - RV（RISC-V）向け VS Code 拡張
魅力的タイトル: Windowsでも即ビルド。VS CodeからDockerベースのRISC-Vツールチェーンを使い倒す方法

## 要約
VS Code拡張「RISC‑V Toolchain」を使えば、Docker上のGNUツールチェーンでWindows／macOS／Linuxから直接RISC‑Vのビルド・逆アセンブル・バイナリ変換が可能。面倒なローカル環境構築を回避し、組込み開発やFPGA検証のワークフローを素早く回せる。

## この記事を読むべき理由
日本の開発現場（組込み機器、FPGA、教育・研究室、IoTスタートアップ）はRISC‑V採用が進んでおり、Linux環境に依存しない手軽なビルド環境は導入障壁を大きく下げる。特にWindows中心の開発者やCI環境で、ツールチェーンをDocker化して一貫したビルドを確保したい人に有益。

## 詳細解説
- 仕組み
  - VS Code拡張がDockerイメージ（既定: ranaumarnadeem/riscv-toolchain）を実行し、riscv64-unknown-elf-gcc等のGNUツールでコンパイル／リンク／objcopyを行う。ローカルにツールチェーンをインストールする必要はないが、Docker Desktopの稼働が前提。

- 主な機能
  - サイドバーでアーキテクチャ（RV32I/IM/IMAC/… ／ RV64I/IM/…）や最適化レベル（O0,O1,O2,O3,Os,Oz）を選んでワンクリックビルド。
  - Bare‑Metalモード：最小のcrt0とカスタムリンカスクリプトでOS無しターゲット向けのスタンドアロン実行ファイルを生成（ブートローダやファームウェア向け）。
  - 逆アセンブル表示：シンタックスハイライト付きで生成されたアセンブリを表示。grepライクなフィルタで関数名・命令・レジスタで絞り込み可能（例: main, addi, a0, main\|loop）。
  - ELF→生バイナリ（.bin）変換：フラッシュ書き込みやFPGA初期化用の平坦バイナリを生成。
  - エラー表示：GCCの警告／エラーをVS Codeの問題パネルとエディタに連携。
  - カスタムリンクスクリプト（.ld）やcrt0.Sをプロジェクトに置けば自動で利用可能。

- 自動化・CI向けの利用
  - MakefileやBashスクリプトからDockerコマンドでコンパイルできるため、CIやビルドサーバに組み込みやすい。例）Makefileやスクリプトでカレントディレクトリをボリュームマウントしてコンパイル。

- 設定・コマンド
  - 設定例: riscv-toolchain.dockerImage, riscv-toolchain.defaultArch, riscv-toolchain.defaultOptimization, riscv-toolchain.bareMetal
  - サイドバーの3ボタン: Build（.elf生成）、Dump（逆アセンブル）、Binary（.bin変換）
  - トラブルシューティング: Docker未検出、権限問題、イメージ未取得など。

## 実践ポイント
- まずは環境準備
  - Docker Desktopをインストールして起動。
  - イメージを事前にpull: 
```bash
docker pull ranaumarnadeem/riscv-toolchain
```
- VS Codeでの基本ワークフロー
  1. C/C++ファイルを開く。  
  2. サイドバーのRISC‑Vパネルでアーキテクチャと最適化を選択。  
  3. Buildボタンで.elfを作成。Dumpでアセンブリ確認、Binaryでフラッシュ向け.binを生成。

- カスタムメモリマップやブート処理が必要な場合
  - 自分のリンカスクリプト（project.ld）とcrt0.Sをプロジェクトに置き、Bare‑Metalを有効化してビルドする。

- CI／スクリプト統合の例
```makefile
CC = docker run --rm -v $(PWD):/work ranaumarnadeem/riscv-toolchain riscv64-unknown-elf-gcc
CFLAGS = -march=rv32imac -mabi=ilp32 -O2

all: program.elf

program.elf: main.c
	$(CC) $(CFLAGS) -o /work/$@ /work/$<
```

```bash
#!/bin/bash
DOCKER_IMAGE="ranaumarnadeem/riscv-toolchain"
docker run --rm -v "$(pwd):/work" $DOCKER_IMAGE \
  riscv64-unknown-elf-gcc -march=rv32imac -mabi=ilp32 -O2 \
  -o /work/output.elf /work/main.c
```

- 日本国内での活用案
  - ハードウェアベンダーの評価ボードやFPGA検証、大学の組込み演習でWindows端末から手軽に環境をそろえられる。CIでイメージを固定すれば再現性の高いビルドが可能。

短時間でRISC‑V開発を始めたい、または既存プロジェクトをDocker化して環境差異を無くしたいエンジニアには即効性の高い拡張。まずはDockerイメージをpullして、VS Codeから一度ビルドしてみることをおすすめする。
