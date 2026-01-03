---
  layout: post
  title: "Writing a SIMD-optimized Parquet library in pure C: lessons from implementing Thrift parsing, bit-packing, and runtime CPU dispatch - SIMD最適化された純C実装のParquetライブラリ：Thriftパーサ、ビットパッキング、実行時CPUディスパッチの実践知見"
  date: 2026-01-03T21:06:33.309Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/Vitruves/carquet"
  source_title: "GitHub - Vitruves/carquet: A high-performance, pure C library for reading and writing Apache Parquet files"
  source_id: 473166521
  excerpt: "組み込み向けに200KBで高速Parquet処理、SIMD最適化と実行時CPU切替で性能革新"
  image: "https://opengraph.githubassets.com/7c7084b87e73018bfbd72813edfea821c47531a0a7d264815082706446554542/Vitruves/carquet"
---

# Writing a SIMD-optimized Parquet library in pure C: lessons from implementing Thrift parsing, bit-packing, and runtime CPU dispatch - SIMD最適化された純C実装のParquetライブラリ：Thriftパーサ、ビットパッキング、実行時CPUディスパッチの実践知見
クリックせずにはいられないタイトル: 「50MBのArrowを捨てて200KBのParquetを選ぶ理由 — 組み込み×高速処理の最前線」

## 要約
Carquetは純C（C11）で書かれた高性能Parquet読み書きライブラリで、SIMD最適化、実行時CPUディスパッチ、Thriftパーサや各種ビットパッキングを実装し、組み込みや制約環境での利用を最優先にしている。

## この記事を読むべき理由
日本の組み込み・エッジ開発、レガシーCコードベース、あるいはバイナリサイズや依存を極力抑えたいプロダクトでは、既存のArrow（C++）では過剰。Carquetは「小さく速く」Parquetを扱える選択肢を提示するため、実務での採用判断や性能改善のヒントが得られる。

## 詳細解説
- 設計方針：完全な純C実装（外部依存はzstdとzlibのみ。Snappy/LZ4は内部実装）により、C言語環境へ直接組み込み可能。バイナリサイズは約200KB（Arrowは数十MB）。
- Parquet対応範囲：全ての物理型（INT32/INT64/FLOAT/DOUBLE/BYTE_ARRAY 等）、主要エンコーディング（PLAIN、RLE、DICTIONARY、DELTA_BINARY_PACKED、BYTE_STREAM_SPLIT など）、複数圧縮（ZSTD/SNAPPY/GZIP/LZ4）と基本的なネスト表現・定義レベルをサポート。ただし、深く複雑なネストや暗号化は未対応。
- パフォーマンス技術：
  - SIMD最適化（SSE4.2 / AVX2 / AVX-512 / NEON / SVE）を各コードパスに実装し、実行時にCPU機能を検出して最適実装へ切替えるランタイムディスパッチを採用。フォールバックはスカラー実装。
  - ThriftパーシングをCで実装し、ヘッダ解析・メタデータ読取を効率化。
  - ビットパッキング／デルタ符号化やバイトストリーム分割などのデコード経路をSIMD化して読み取り性能を向上。
  - ARM向けにCRC32ハードウェア加速を活用、mmap/ゼロコピー読み取りやOpenMPによる列並列読みを提供。
- 互換性：PyArrowと互換性があり、ツールチェーン混在時のデータ交換が容易。

## 日本市場との関連
- 組み込み機器（IoT、車載、産業機器）やオンプレの制約あるサーバで有効。日本企業の多いリアルタイム／省メモリな用途に親和性が高い。
- ARMベースのIoTゲートウェイやRaspberry Pi等でNEON最適化を有効にすれば、パフォーマンスと省電力の両立が期待できる。
- レガシーCで動く既存ソフトにParquet入出力を追加する際、FFIを介さず直接統合できるのは大きな利点。

## 実践ポイント
- ビルドの基本（例）:
```bash
# ReleaseビルドでNEONを有効にする例（ARM向け）
cmake .. -DCMAKE_BUILD_TYPE=Release -DCARQUET_ENABLE_NEON=ON -DCARQUET_BUILD_SHARED=ON
make -j$(nproc)
sudo make install
```
- 運用Tips:
  - 小メモリ環境なら reader options で use_mmap=true とバッチ読み（batch_reader）を利用してゼロコピーで処理。
  - 必要な列だけ投影（column projection）＋列統計によるRowGroupフィルタ（predicate pushdown）でI/Oを大幅削減。
  - ARMデバイスでは CRC32 ハードウェアを活かすとページ検査が高速。ビルド時にNEON/SVEフラグを確認する。
- 採用判断:
  - バイナリサイズと純Cが重要 → Carquetを検討。
  - フル機能のネストやマルチスレッドZSTD等が必須 → Arrowを推奨。

短時間で試せること：既存の小さなParquetファイルでCarquetをビルドして読み書きし、Arrowと比較してバイナリサイズ・読み書き遅延・メモリ消費を計測すると、導入可否の判断が容易になる。
