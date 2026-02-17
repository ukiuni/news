---
layout: post
title: "BarraCUDA Open-source CUDA compiler targeting AMD GPUs - AMD GPUをターゲットにしたオープンソースCUDAコンパイラ"
date: 2026-02-17T23:20:41.301Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/Zaneham/BarraCUDA"
source_title: "GitHub - Zaneham/BarraCUDA: Open-source CUDA compiler targeting AMD GPUs (and more in the future!). Compiles .cu to GFX11 machine code."
source_id: 47052941
excerpt: "CUDAソースをLLVM不要でRDNA3向けに直接コンパイルする軽量オープンソースコンパイラ"
image: "https://opengraph.githubassets.com/00561db4d59695cf9b2dfbcf6b87dc16e55d57dcb377e974a53d8e7b27348f5b/Zaneham/BarraCUDA"
---

# BarraCUDA Open-source CUDA compiler targeting AMD GPUs - AMD GPUをターゲットにしたオープンソースCUDAコンパイラ
NVIDIAのCUDAコードをそのままAMDで走らせる—“LLVMなし”で直コンパイルする奇妙な挑戦

## 要約
BarraCUDAは純粋なC99実装（約15k行）で、.cuファイルを直接RDNA3（gfx1100）向けのGFX11機械語にコンパイルして.hsacoを出力するオープンソースコンパイラ。LLVMやHIP変換を介さずに動作します。

## この記事を読むべき理由
日本でもAMD GPUはデータセンターやワークステーションで採用が進んでおり、CUDAエコシステムの独占を回避したい開発者や研究者にとって、CUDAソースを直接AMD向けに変換するツールは貴重です。ベンダーロックイン対策や教育・研究用途の可能性があります。

## 詳細解説
- コア思想：.cu（CUDA C）をそのまま解析して独自IR（BIR）に落とし、手書きの命令選択とエンコードでGFX11命令語を生成する。LLVMに依存しない“一からのコンパイラ”。
- 実装概要：プリプロセッサ → レクサ → 再帰降下パーサ → セマンティクス → BIR（SSA） → mem2reg → 命令選択 → レジスタ割当（VGPR/SGPR）→ バイナリエンコード → ELF(.hsaco)。
- 対応機能（一部）：__global__/__device__/__host、threadIdx/blockIdx等の組込み、__shared__、__syncthreads、各種アトミック、ワープ操作（__shfl系）、warp vote、ベクトル型、半精度、cooperative groups、テンプレート基本展開、フルCプリプロセッサ、エラー回復など。
- 制限事項（現状）：裸のunsigned、複合代入（+=等）、__constant__、2D共有配列宣言、テクスチャ／サーフェス、デバイス側カーネル起動（Dynamic Parallelism）、ホストコード生成や複数翻訳単位未対応等。ただし多くは「未実装」でありアーキテクチャ的障壁ではない。
- 検証と品質：生成命令はllvm-objdumpで検証済み。テストスイート（複数カーネル）あり。ビルドは単純で依存なし（C99コンパイラがあれば make でOK）。
- 将来計画：短期は欠点の修正、中期は最適化（命令スケジューリング、より良いレジスタ割当など）、長期はバックエンド追加（Tenstorrent/RISC-V、Intel Arcなど）。

ビルドと簡単な使い方例：
```bash
# ビルド（C99コンパイラが必要）
make

# AMDバイナリ生成
./barracuda --amdgpu-bin kernel.cu -o kernel.hsaco

# IRやASTをダンプしてデバッグ
./barracuda --ir kernel.cu
./barracuda --ast kernel.cu
```

## 実践ポイント
- まずは小さなカーネル（vector_add等）で試す：未対応機能にぶつかりにくい。
- AMD RDNA3環境（gfx1100）で.hsacoを実行して動作確認。生成物はELF形式でGPUが実行可能。
- ベンチ目的なら最適化不足に注意。研究／移植性検証や教育用途に向く。
- コントリビュート余地が大きい：パーサ修正、最適化パス追加、別バックエンド実装は歓迎される領域。
- 日本の企業・研究機関での採用検討時は、ホスト側コード生成や実運用での未対応点（複数TU、テクスチャなど）をチェックしてから評価を進める。

興味があればリポジトリ（README）を確認して簡単なカーネルで動かしてみてください。
