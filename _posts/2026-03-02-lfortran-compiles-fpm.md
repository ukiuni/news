---
layout: post
title: "LFortran compiles fpm - LFortranがfpmをコンパイル可能に"
date: 2026-03-02T22:13:04.726Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lfortran.org/blog/2026/02/lfortran-compiles-fpm/"
source_title: "LFortran compiles fpm -"
source_id: 47188014
excerpt: "LFortranがfpmをビルド実行可能に—Fortran資産の移植と高速化が現実に"
image: "https://lfortran.org/images/lfortran_logo.svg"
---

# LFortran compiles fpm - LFortranがfpmをコンパイル可能に
Fortranの“現代化”が加速：LFortranが公式パッケージマネージャ fpm をビルド＆実行できるようになり、実務的な互換性と速度改善が見えてきた

## 要約
LFortranがFortran Package Manager（fpm）を正しくビルド・実行できるようになり、複雑な言語機能や外部依存をクリアしてベータ目前の精度に到達しています（プロジェクト進捗9/10）。

## この記事を読むべき理由
日本の研究機関・製造業・HPC現場には古くて巨大なFortran資産が多く、LFortranの成熟はモダン化・移植・高速化の現実的な選択肢を提供します。特にパッケージ管理・ビルド互換性が向上すれば、メンテ性と導入コストが下がります。

## 詳細解説
- なぜfpmが重要か：fpmはFortranのパッケージマネージャで、依存解決やビルド手順を含む“システム的”なプロジェクト。コンパイルだけでなくコマンド引数、環境変数、ファイルI/O、モジュール依存解析など複合的な機能を試す良いベンチマークです。
- 実装された言語機能：クラス、継承、仮想関数、allocatableコンポーネント、コンストラクタ、クラス配列、select type、associate、自動LHS再割当、文字列と文字列配列など、ほぼ全モダンFortran機能に対応。これらの実装で多数のバグが潰されました。
- 大改修点：クラス・仮想関数・継承処理をClangのC++処理に倣って再設計（Fortran固有の拡張あり）。ASR（Abstract Semantic Representation）を中心に変換→最適化→LLVM生成のパイプラインを整備。
- CIと品質保証：fpmのテスト群をCIで毎コミット実行。フレークな不具合が出ないことを確認した上で公開。
- 対応依存ライブラリ：M_CLI2（CLI解析）、toml-f（TOML）、fortran-regex、fortran-shlex、Jonquil（JSON）をサポート。
- 性能とボトルネック：Apple M4での比較例 — gfortranでの fpm ビルドが約42s、LFortranだと約16.6s（単コア）。プロファイルでは「LLVM IR → オブジェクト生成」が総時間の約75%を占めており、ここを独自バックエンドで改善すれば10倍程度の高速化が期待できます。
- 現状と今後：coarraysとparametrized derived types（PDT）は未実装で、ベータは中規模コードで約90%の成功率を目標。現状はアルファだが、バグは小さく修正が進みやすい段階。

## 実践ポイント
- 試す（推奨、Conda環境例）:
```bash
git clone https://github.com/fortran-lang/fpm
git checkout d0f89957541bdcc354da8e11422f5efcf9fedd0e
conda create -n fpm lfortran=0.60.0 fpm gfortran
conda activate fpm
fpm --compiler=lfortran test --flag --cpp --flag --realloc-lhs-arrays --flag --use-loop-variable-after-loop
```
- トラブルシューティング: LFortranはデフォルトで境界チェック有効。未初期化や形状不一致はランタイムエラーで検出され、潜在的なセグフォを防げます。
- パフォーマンス分析: ビルドに --verbose と --time-report を付けて重いファイル（例: lfortran -c app/main.f90 ... --time-report）を特定する。
- コントリビュート: バグ報告・PR、Zulip/Fortran Discourseでの議論参加で開発を加速可能。
- 日本での活用案: 既存のFortran資産のモダン化パイロット（数千行未満）から導入し、LFortranの実行互換性と高速化を検証するのが現実的。

以上。LFortranの進展はFortran資産を抱える日本の現場にとって注目すべき出来事です。
