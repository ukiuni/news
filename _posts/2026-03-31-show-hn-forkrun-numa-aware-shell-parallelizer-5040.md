---
layout: post
title: "Show HN: Forkrun – NUMA-aware shell parallelizer (50×–400× faster than parallel) - Show HN: Forkrun – NUMA対応シェル並列化ツール（GNU Parallelより50×–400×高速）"
date: 2026-03-31T18:22:16.574Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/jkool702/forkrun"
source_title: "GitHub - jkool702/forkrun: NUMA-Aware Contention-Free Dynamically-Auto-Tuning Bash-Native Streaming Parallelization Engine · GitHub"
source_id: 47541746
excerpt: "NUMA最適化でシェル処理を50〜400倍高速化、ログ前処理を劇的短縮"
image: "https://opengraph.githubassets.com/577b1fdc855fa5c03380a70ab49519855c2a2aba7c6bc9614e028763cd176ba8/jkool702/forkrun"
---

# Show HN: Forkrun – NUMA-aware shell parallelizer (50×–400× faster than parallel) - Show HN: Forkrun – NUMA対応シェル並列化ツール（GNU Parallelより50×–400×高速）
驚異の“born-local”並列化でシェル処理が数十〜数百倍速くなる――現場のデータ準備が劇的に短縮される理由

## 要約
forkrunは、GNU Parallelやxargs -Pの「置き換え」を目指すシェルネイティブの並列化エンジンで、NUMAを意識したメモリ配置とロックフリー設計で50×〜400×の高速化を実現します。

## この記事を読むべき理由
日本の開発現場や研究機関で大量ログ整形や前処理を走らせるとき、従来ツールではCPU資源やメモリ配置がボトルネックになりがちです。forkrunはオンプレ多ソケットサーバやクラウドの大インスタンスでのコスト削減・処理時間短縮に直結します。

## 詳細解説
- 性能概観  
  - ベンチ: 一例で24M行/s vs GNU Parallel 58k行/s（約415×）など。平均CPU利用率は約95%（GNU Parallelは約6%）。バッチディスパッチは200,000+/秒（GNU Parallelは約500）。
- 設計の肝
  - NUMA「Born-Local」: stdinからspliceでmemfdへデータを入れ、set_mempolicy(MPOL_BIND)でページを各ソケットに事前配置。ワーカーが触る前にローカルに置くことでクロスソケットのメモリ移動をほぼゼロにする。
  - インデクサ（ソケット単位）: 各ノードにピン留めしたインデクサがAVX2/NEONでレコード境界を高速スキャンし、実行時のバックプレッシャに応じて動的にバッチ化。
// 競合回避と奪い合い
  - クレーム: ワーカーは単一のatomic_fetch_addでバッチを取得。CASループやロックがなく、競合が発生しにくい。余分はエスクロー経由でアイドルワーカーが窃取。
  - 再利用/破棄: 背景スレッドがfallocate(PUNCH_HOLE)で処理済み領域を解放しつつ、オフセット座標系を壊さない。
- 自動チューニング
  - PIDベースのコントローラが入力速度・消費速度・ワーカー飢餓を監視し、最適バッチサイズをO(log L)ステップで発見。ユーザー側で-nや-jを指定する必要がほぼない。
- 配布と安全性
  - 単一のbashスクリプト（frun.bash）にコンパイル済みC拡張が埋め込まれており、依存なしで使える（Perl/Python不要）。組み込みバイナリはGitHub Actionsでビルドされ、追跡可能な透明性を確保。
- 要件・注意点
  - Bash ≥ 4.0（5.1推奨）、Linux Kernel ≥ 3.17（memfd必要）。現状、ワーカーが各NUMAノードで最低1つ生存することを正しさの前提としている（将来的に障害対策が計画中）。

## 実践ポイント
- すぐ試す（軽量ソース方式）:
```bash
bash
source <(curl -sL https://raw.githubusercontent.com/jkool702/forkrun/main/frun.bash)
```
- 使い方例:
```bash
bash
frun my_bash_func < inputs.txt
cat file_list | frun -k sed 's/old/new/'
frun -s -I 'gzip -c >{ID}.gz' < raw_logs
```
- 運用上の提案（日本の現場向け）
  - 大規模オンプレ多ソケットサーバや高コアVMで効果絶大。ログ/CSV前処理、ETLバッチ、HPCプリプロセスに適用してI/O/CPUコストを削減可能。
  - クラスタ管理下（Slurm等）では「再開・失敗時の耐性」がロードマップ項目のため、重要ジョブで使う前に検証環境でリカバリ挙動を確認すること。
  - WSL等NUMAが効かない環境では恩恵が限定されるので、まずは対象ノードのNUMA構成を確認する。

以上を踏まえ、もし「大量行単位のシェル処理が遅くて困っている」なら、forkrunは試す価値が高いツールです。
