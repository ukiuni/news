---
  layout: post
  title: "I built a GPU-accelerated SQLite on Apple Silicon to test a theory about the PCIe bottleneck - PCIeボトルネックを検証するためにApple SiliconでGPU高速化SQLiteを作った"
  date: 2026-01-07T12:50:06.089Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/sadopc/unified-db"
  source_title: "GitHub - sadopc/unified-db: What if your database didn&#39;t need to copy data to the GPU? Exploring Apple Silicon&#39;s unified memory architecture for GPU-accelerated SQLite queries."
  source_id: 468913024
  excerpt: "PCIeボトルネックを回避し、MシリーズでSQLiteをゼロコピーGPU化、最大十倍高速化を実証"
  image: "https://opengraph.githubassets.com/3b73a2c73193dad87881c5629b857fdda558ae1bd1707100233cfad7e2ad2f2a/sadopc/unified-db"
---

# I built a GPU-accelerated SQLite on Apple Silicon to test a theory about the PCIe bottleneck - PCIeボトルネックを検証するためにApple SiliconでGPU高速化SQLiteを作った
M1/M2/M3で“ゼロコピー”DBが現実に — SQLiteをGPUで高速化した衝撃の実験

## 要約
Apple Siliconの統合メモリ（unified memory）を使い、CPU↔GPUのコピーを省いた「ゼロコピー」方式でSQLiteの集計/ソート/フィルタをGPU化。大規模データで数倍〜十倍近い高速化を確認した実験プロジェクト。

## この記事を読むべき理由
日本でもMacが開発マシンや解析端末として広く使われる中、外部GPUやPCIe転送に依存しない「オンマシンでの高速分析」は実運用やプロトタイピングの効率を劇的に改善する可能性があるため。

## 詳細解説
- 核心アイデア：Apple Silicon（M1/M2/M3/M4）はCPUとGPUが物理メモリを共有するため、storageModeSharedを使えばCPUとGPUで同じバッファをコピーなしで共有できる。これにより、従来のPCIe越しのデータ転送（ボトルネック）を回避してGPU計算の恩恵を得られる。
- 実装：Swiftのラッパ（MetalDatabase）＋Metalの計算カーネルで構成。主要なGPU処理は以下。
  - 平行集約（SUM, AVG, MIN, MAX, COUNT）
  - Bitonicソートによる並列ソート
  - WHERE句の並列フィルタ評価
  - storageModeSharedを使ったゼロコピー操作
- アーキテクチャレイヤー：Swift API → Metal compute shaders → Unified Memory (storageModeShared) → SQLite
- ベンチマーク例（M3 Pro、1M行）：SUM: CPU 45ms → GPU 8ms（約5.6x）、SORT: CPU 890ms → GPU 95ms（約9.4x）など。効果はデータ規模とアルゴリズムに依存。
- 要件：macOS 14+, Apple Silicon, Swift 5.9+, Xcode 15+
- 制約と注意点：
  - 小規模データではGPU起動・同期コストで逆効果になる可能性
  - 統合メモリはCPU/GPUで帯域とキャッシュ競合が起きるため、ワークロードによっては期待通りスケールしない
  - Metalカーネルの最適化（スレッドグループサイズ、メモリアクセスパターン）が性能を左右する

## 日本市場との関連
- ローカル解析が中心のスタートアップや研究開発、社内データ分析（数百万行規模）をMacで行うチームに適合。外部GPUやクラウドを使わずに高速化できるためコスト削減やデータガバナンス面でも利点がある。
- 金融・広告・ログ分析・IoT前処理など、オンデバイスで低レイテンシに集計・フィルタしたいユースケースに有効。
- Mシリーズを採用している日本の開発者コミュニティや教育現場での実験教材としても魅力的。

## 実践ポイント
- 試す手順（簡潔）：
  1. リポジトリをクローンしてビルド、テストを実行（swift test）
  2. 実データでSUM/SORT/FILTERの処理時間を比較
  3. Metalのプロファイラ（Instruments）でメモリ/スレッド挙動を観察
- 実装上のチェックリスト：
  - 小さなバッチではCPU実行を選ぶハイブリッド戦略を用意する
  - カーネルでのメモリアクセスを連続化し、分岐を減らす
  - スレッドグループサイズ・ワークセットをターゲットチップ（M1/M3等）に合わせて調整する
- すぐに使えるサンプル（Quick Start）：

```swift
// Swift
import MetalSQLite

let db = try MetalDatabase(path: "data.db")
let sum = try db.metalSum(table: "sales", column: "amount")
let sorted = try db.metalSort(table: "sales", column: "amount", ascending: true)
```

以上を踏まえ、まずは手元のMacで実際にワークロードを動かしてみることを強く推奨する。GPUが本当に効くかはデータ形状とカーネル実装次第で変わるため、計測とチューニングが重要。
