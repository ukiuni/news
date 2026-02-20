---
layout: post
title: "ThunderKittens 2.0: Even Faster Kernels for Your GPUs - ThunderKittens 2.0：GPU向けさらに高速なカーネル"
date: 2026-02-20T19:29:42.129Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://hazyresearch.stanford.edu/blog/2026-02-19-tk-2"
source_title: "ThunderKittens 2.0: Even Faster Kernels for Your GPUs · Hazy Research"
source_id: 402084259
excerpt: "ThunderKittens2.0が不要なメモリ同期を削りBlackwellでcuBLAS超え"
image: "https://hazyresearch.stanford.edu/hazy-logo.png"
---

# ThunderKittens 2.0: Even Faster Kernels for Your GPUs - ThunderKittens 2.0：GPU向けさらに高速なカーネル
魅惑の「GPU最適化ツール」進化版：ThunderKittens 2.0で見えた“やらない最適化”の威力

## 要約
ThunderKittens 2.0は、Blackwell世代GPU向けに内部を大幅にリファクタリングし、不必要なメモリ同期やアセンブラのヒントを削ることで、MXFP8/NVFP4やBF16のGEMMでcuBLASに匹敵／上回る性能を出したリリースです。チューニングの鍵は「何をやめるか」にありました。

## この記事を読むべき理由
国内のMLインフラやGPU最適化に関わるエンジニアにとって、最新PTXの挙動やメモリ一貫性・テンソルコアのパイプライン設計といった“最後の数％を稼ぐ”知見は実用的価値が高く、コスト効率や実行速度に直結します。

## 詳細解説
- リリースの要点
  - MXFP8/NVFP4（低精度）やCLCスケジューリング、テンソルメモリ制御、PDLなど新機能。
  - 内部コードの大幅リファクタとビルド簡略化、業界からの貢献で最先端カーネルを実装。
  - ベンチは同一ランダム入力・ウォームアップ・L2除去を含む厳密な手順で比較。

- メモリ一貫性（PTXの因果順序とプロキシ）
  - PTXでは「因果（causality）」で書き込み→読み込みの可視性が保証される。だが異なるアクセス群（proxy）間は fence.proxy が必要。
  - ThunderKittensでは、TMA (cp.async.bulk.tensor)→mbarrier→tcgen05.mma の流れで既に因果順序が成立しており、明示的な fence や after_thread_sync は不要と判定。これらを削ることで数十TFLOP級の改善が得られた。

- テンソルコアとメモリのパイプライン
  - ブロックスケーリング（MXFP8/NVFP4）ではスケール値の供給がボトルネックに。設計上、Blackwell向けには1 CTA あたり 4連続 MMA（= MMAステージ）を用意する必要がある。
  - スケール数の簡単な導出例：
    - MXFP8: 1スケール/32要素 → 1ステージあたり $128\times128/32=512$ 個
    - NVFP4: 1スケール/16要素 → 1ステージあたり $128\times256/16=2048$ 個
  - tcgen05.cp.32x128.warpx4 は 512 値を一度にコピーするため MXFP8 とは相性良いが、NVFP4 では複数回の cp が必要→元設計では warp 間で大量待ちが発生し約10%の性能低下。
  - 発見：tcgen05.cp（ドキュメント表記のtypo含む）が tcgen05.mma と暗黙にパイプラインされるケースを利用し、コピーとMMAを同一スレッドにまとめることで待ちを排除、性能回復。

- テンソルメモリの二重バッファリング
  - テンソルメモリ（128×512）を二分割（各128×256）して、一方をコアで使いながら他方をエピローグが読み出すパターンで競合を避ける。実運用での設計指針。

- ベンチマークの注意点
  - L2キャッシュ・電力やウォームアップを考慮して計測すること。論理的に同じコードでも、PTX表現やアセンブラのヒント次第で生成命令が変わり性能差が出る。

## 実践ポイント
- 不要なメモリフェンスを疑え：因果関係（causality）とproxyを整理して、不要な fence を取り除くと大きく速くなる。
- PTXドキュメントを読み、暗黙のパイプライン（tcgen05.cp ↔ tcgen05.mma 等）を活用する設計に切り替える。
- スケール値やテンソルメモリの容量計算を先にやる：$128\times128/32$ のように必要量を定量化してボトルネックを可視化する。
- ベンチは「同一入力」「十分なウォームアップ」「L2除去」を必ず入れて比較する。
- ThunderKittensの例をローカルでビルドして、Blackwell系GPUでの最適化手法を試す（ビルド構造が簡素化されています）。

以上を踏まえれば、国内のML/HPC環境でも「最後の数％〜10%」を取り戻すヒントが得られます。興味があれば公式リポジトリとPTXの該当節を直接確認してみてください。
